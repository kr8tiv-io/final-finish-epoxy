<?php
declare(strict_types=1);

const TO_ADDRESS = 'kr8tiv@kr8tiv.io';
const MAX_FILES = 3;
const MAX_EACH = 12 * 1024 * 1024;
const MAX_TOTAL = 20 * 1024 * 1024;

function clean(string $value, int $limit): string
{
    $value = trim(str_replace(["\r", "\n", "\0"], ' ', $value));
    $value = strip_tags($value);
    if (strlen($value) > $limit) {
        $value = substr($value, 0, $limit);
    }
    return $value;
}

function header_name(string $value): string
{
    $value = str_replace(['<', '>', '"', '\\'], '', $value);
    return $value === '' ? 'Client' : $value;
}

function too_fast(): bool
{
    $ip = (string)($_SERVER['REMOTE_ADDR'] ?? 'unknown');
    $dir = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'ff-updates';
    if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) {
        return false;
    }
    $path = $dir . DIRECTORY_SEPARATOR . hash('sha256', $ip);
    $now = time();
    $hits = [];
    $raw = is_file($path) ? (string)@file_get_contents($path) : '';
    if ($raw !== '') {
        foreach (explode(',', $raw) as $stamp) {
            $stamp = (int)$stamp;
            if ($stamp > $now - 3600) {
                $hits[] = (string)$stamp;
            }
        }
    }
    if (count($hits) >= 6) {
        return true;
    }
    $hits[] = (string)$now;
    @file_put_contents($path, implode(',', $hits), LOCK_EX);
    return false;
}

function page(string $title, string $body, bool $ok): void
{
    $status = $ok ? '200 OK' : '400 Bad Request';
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Robots-Tag: noindex, nofollow');
    http_response_code($ok ? 200 : 400);
    $class = $ok ? 'ok' : 'error';
    echo '<!DOCTYPE html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>'
        . htmlspecialchars($title, ENT_QUOTES, 'UTF-8')
        . '</title><link rel="stylesheet" href="../kr8tiv-report.css"></head><body><main class="wrap" style="padding:4rem 0"><p class="kicker">KR8TIV · Final Finish Epoxy</p><h1>'
        . htmlspecialchars($title, ENT_QUOTES, 'UTF-8')
        . '</h1><p class="' . $class . '">'
        . $body
        . '</p><p><a href="./">Back to the form</a> · <a href="../report/">Report</a></p></main></body></html>';
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ./', true, 303);
    exit;
}

if (!empty($_POST['company_website'])) {
    page('Received.', 'The form was accepted.', true);
}

if (too_fast()) {
    page('Wait before another request.', 'Six requests in an hour is the limit from one connection. Write to kr8tiv@kr8tiv.io if this one is urgent. Nothing was emailed.', false);
}

$name = clean((string)($_POST['your_name'] ?? ''), 120);
$email = clean((string)($_POST['email'] ?? ''), 160);
$phone = clean((string)($_POST['phone'] ?? ''), 40);
$pageUrl = clean((string)($_POST['page_url'] ?? ''), 400);
$note = clean((string)($_POST['note'] ?? ''), 4000);
$terms = (string)($_POST['terms'] ?? '');

if ($name === '' || $email === '' || $pageUrl === '' || $terms !== 'yes' || filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
    page('The form needs a name, a real email, the page, and the terms box.', 'Fill those in, then send it again. Nothing was emailed.', false);
}

$current = $_POST['current_words'] ?? [];
$replacement = $_POST['replacement_words'] ?? [];
if (!is_array($current) || !is_array($replacement)) {
    page('The wording fields did not arrive.', 'Send the form again from the page.', false);
}

$pairs = [];
$count = max(count($current), count($replacement));
for ($i = 0; $i < $count; $i++) {
    $from = clean((string)($current[$i] ?? ''), 4000);
    $to = clean((string)($replacement[$i] ?? ''), 4000);
    if ($from === '' && $to === '') {
        continue;
    }
    if ($from === '' || $to === '') {
        page('Each change needs both sides.', 'Write the words on the site, and the words that should replace them.', false);
    }
    $pairs[] = [$from, $to];
}
if ($pairs === []) {
    page('A change is required.', 'Paste the words to replace, and the words that should replace them.', false);
}

$allowed = [
    'image/jpeg' => 'jpg',
    'image/png' => 'png',
    'image/webp' => 'webp',
    'image/gif' => 'gif',
    'video/mp4' => 'mp4',
    'video/webm' => 'webm',
    'video/quicktime' => 'mov',
    'application/pdf' => 'pdf',
];

$files = [];
$total = 0;
$upload = $_FILES['files'] ?? null;
if (is_array($upload) && isset($upload['name']) && is_array($upload['name'])) {
    $incoming = 0;
    foreach ($upload['error'] as $error) {
        if ($error !== UPLOAD_ERR_NO_FILE) {
            $incoming++;
        }
    }
    if ($incoming > MAX_FILES) {
        page('Three files is the limit.', 'Remove the extra files, or put a link in the note.', false);
    }
    foreach ($upload['error'] as $index => $error) {
        if ($error === UPLOAD_ERR_NO_FILE) {
            continue;
        }
        if ($error !== UPLOAD_ERR_OK) {
            page('A file did not upload.', 'Try a smaller file. The limit is 12 MB each.', false);
        }
        $size = (int)$upload['size'][$index];
        $total += $size;
        if ($size > MAX_EACH || $total > MAX_TOTAL) {
            page('That file is too large for email.', 'Keep each file under 12 MB, and the set under 20 MB. Put a link in the note for anything larger.', false);
        }
        $tmp = (string)$upload['tmp_name'][$index];
        if (!is_uploaded_file($tmp)) {
            page('A file did not upload.', 'Send the form again from the page.', false);
        }
        $mime = mime_content_type($tmp) ?: '';
        if (!isset($allowed[$mime])) {
            page('That file type is not accepted.', 'Use JPG, PNG, WEBP, GIF, MP4, WEBM, MOV, or PDF.', false);
        }
        $files[] = [
            'tmp' => $tmp,
            'name' => 'final-finish-' . ($index + 1) . '.' . $allowed[$mime],
            'mime' => $mime,
        ];
    }
}

$lines = [
    'Project: Final Finish Epoxy',
    'Name: ' . $name,
    'Email: ' . $email,
    'Phone: ' . ($phone !== '' ? $phone : '(none)'),
    'Page: ' . $pageUrl,
    'Terms accepted: section 13, two small tweaks.',
    '',
    'Changes:',
];
foreach ($pairs as $index => $pair) {
    $lines[] = 'Change ' . ($index + 1);
    $lines[] = 'On the site now: ' . $pair[0];
    $lines[] = 'Replace with: ' . $pair[1];
    $lines[] = '';
}
$lines[] = 'Note: ' . ($note !== '' ? $note : '(none)');
$bodyText = implode("\n", $lines);

$subject = 'Final Finish Epoxy update request';
$from = 'no-reply@lightgrey-wasp-945457.hostingersite.com';
$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

if ($files === []) {
    $headers = [
        'From: KR8TIV <' . $from . '>',
        'Reply-To: ' . header_name($name) . ' <' . $email . '>',
        'Content-Type: text/plain; charset=UTF-8',
        'MIME-Version: 1.0',
    ];
    $sent = mail(TO_ADDRESS, $encodedSubject, $bodyText, implode("\r\n", $headers), '-f ' . $from);
} else {
    $boundary = 'ff_' . bin2hex(random_bytes(8));
    $headers = [
        'From: KR8TIV <' . $from . '>',
        'Reply-To: ' . header_name($name) . ' <' . $email . '>',
        'MIME-Version: 1.0',
        'Content-Type: multipart/mixed; boundary="' . $boundary . '"',
    ];
    $message = "--{$boundary}\r\n";
    $message .= "Content-Type: text/plain; charset=UTF-8\r\n\r\n";
    $message .= $bodyText . "\r\n";
    foreach ($files as $file) {
        $data = chunk_split(base64_encode((string)file_get_contents($file['tmp'])));
        $message .= "--{$boundary}\r\n";
        $message .= 'Content-Type: ' . $file['mime'] . '; name="' . $file['name'] . "\"\r\n";
        $message .= "Content-Transfer-Encoding: base64\r\n";
        $message .= 'Content-Disposition: attachment; filename="' . $file['name'] . "\"\r\n\r\n";
        $message .= $data . "\r\n";
    }
    $message .= "--{$boundary}--";
    $sent = mail(TO_ADDRESS, $encodedSubject, $message, implode("\r\n", $headers), '-f ' . $from);
}

if (!$sent) {
    page('The server did not accept the email.', 'Write to kr8tiv@kr8tiv.io with the same wording. Nothing was stored on the site.', false);
}

page('Sent.', 'The request is on its way to kr8tiv@kr8tiv.io. If you do not hear back, send the same note directly to that address.', true);
