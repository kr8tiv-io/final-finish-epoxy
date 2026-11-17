# One-shot page wiring for job-film captions and the elevation sheet.
from pathlib import Path

root = Path(r"C:\workspace\ff-films-elevation-2026-11-16")
FB = "https://www.facebook.com/profile.php?id=61573826827114"
OLD_SOCIAL = (
    '<a href="https://www.facebook.com/profile.php?id=61573826827114" rel="me noopener" data-astro-cid-nns7i3if>Facebook</a>'
    '<a href="https://www.instagram.com/final_finish_epoxy/" rel="me noopener" data-astro-cid-nns7i3if>Instagram</a>'
)
NEW_SOCIAL = (
    '<nav class="social-links" aria-label="Final Finish social">'
    '<a class="social-link" href="https://www.instagram.com/final_finish_epoxy/" rel="me noopener noreferrer" target="_blank">'
    '<span class="social-mark" aria-hidden="true"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.6">'
    '<rect x="3.5" y="3.5" width="17" height="17" rx="4"></rect><circle cx="12" cy="12" r="3.6"></circle>'
    '<circle cx="17.2" cy="6.9" r="0.9" fill="currentColor" stroke="none"></circle></svg></span>'
    '<span>Instagram</span><span class="social-new">opens in a new tab</span></a>'
    '<a class="social-link" href="https://www.facebook.com/profile.php?id=61573826827114" rel="me noopener noreferrer" target="_blank">'
    '<span class="social-mark" aria-hidden="true"><svg viewBox="0 0 24 24" width="15" height="15">'
    '<path fill="currentColor" d="M14.6 8.2h2.2V5.2h-2.2c-2.3 0-3.8 1.5-3.8 3.9V11H8.4v2.8h2.4V21h3.2v-7.2h2.3l.4-2.8h-2.7V9.4c0-.7.3-1.2 1.2-1.2z"></path>'
    '</svg></span><span>Facebook</span><span class="social-new">opens in a new tab</span></a></nav>'
)
LINK = '<link rel="stylesheet" href="/films-elevation.css">'
PLAY = (
    "<script>(function(){var q=window.matchMedia(\"(prefers-reduced-motion: reduce)\");"
    "function still(){var d=document.documentElement.dataset;return q.matches||d.journeyTier===\"still\"||d.journeyMotion===\"still\";}"
    "function sync(){document.querySelectorAll(\"video.job-film\").forEach(function(v){if(still()){v.pause();return;}var p=v.play();if(p&&p.catch)p.catch(function(){});});}"
    "sync();q.addEventListener(\"change\",sync);})();</script>"
)


def credit(center=False):
    cls = "job-credit job-credit--center" if center else "job-credit"
    return (
        f'<p class="{cls}">From this <a class="job-credit-link" href="{FB}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="job, opens the Facebook post in a new tab">job</a></p>'
    )


def film(name, poster):
    return (
        f'<video class="job-film" muted playsinline loop preload="none" poster="{poster}">'
        f'<source media="(max-width: 680px)" src="/videos/follow-floor/480/{name}.mp4" type="video/mp4">'
        f'<source src="/videos/follow-floor/720/{name}.mp4" type="video/mp4"></video>'
    )


def insert_home(html, anchor):
    i = html.find(f'id="{anchor}"')
    if i < 0:
        raise SystemExit(f"missing anchor {anchor}")
    j = html.find('<div class="act-fog', i)
    if j < 0:
        raise SystemExit(f"missing fog after {anchor}")
    window = html[max(0, i - 800):i]
    center = "act-copy--center" in window
    if "job-credit" in html[i:j]:
        return html, "already"
    at = j - len("</div></div>")
    if html[at:j] != "</div></div>":
        raise SystemExit(f"unexpected close before fog for {anchor}: {html[at:j+20]!r}")
    return html[:at] + credit(center) + html[at:], "center" if center else "left"


def insert_interior(html, poster_src, film_name):
    src_at = html.find(poster_src)
    if src_at < 0:
        raise SystemExit(f"missing poster {poster_src}")
    img_end = html.find(">", src_at)
    if img_end < 0:
        raise SystemExit("img end")
    img_end += 1
    if "video class=\"job-film\"" not in html[img_end:img_end + 80]:
        html = html[:img_end] + film(film_name, poster_src) + html[img_end:]
    lead = html.find("interior-lead", src_at)
    if lead < 0:
        raise SystemExit(f"missing lead after {poster_src}")
    end_p = html.find("</p>", lead)
    if end_p < 0:
        raise SystemExit("missing lead close")
    end_p += 4
    if "job-credit" not in html[end_p:end_p + 80]:
        html = html[:end_p] + credit(False) + html[end_p:]
    return html


def wire_page(path: Path, interior=None, home_anchors=None):
    html = path.read_text(encoding="utf-8")
    original = html
    if OLD_SOCIAL not in html and "social-links" not in html:
        print("NO SOCIAL", path.relative_to(root))
    else:
        html = html.replace(OLD_SOCIAL, NEW_SOCIAL)
    if LINK not in html:
        if "</head>" not in html:
            raise SystemExit(f"no head {path}")
        html = html.replace("</head>", LINK + "</head>", 1)
    if home_anchors:
        for anchor in home_anchors:
            html, how = insert_home(html, anchor)
            print("home", anchor, how)
    if interior:
        html = insert_interior(html, interior[0], interior[1])
        print("interior", path.parent.name, interior[1])
    if "video class=\"job-film\"" in html and "video.job-film" not in html:
        html = html.replace("</body>", PLAY + "</body>", 1)
    if html != original:
        path.write_text(html, encoding="utf-8", newline="\n")
        print("wrote", path.relative_to(root))
    else:
        print("unchanged", path.relative_to(root))


pages = list(root.rglob("*.html"))
for page in pages:
    interior = None
    home = None
    rel = page.relative_to(root).as_posix()
    if rel == "index.html":
        home = ["reclaim-title", "finish-title", "commercial-title", "consultation-title"]
    elif rel == "resources/index.html":
        interior = ("/images/brand/epoxy-resources-stairs-poster.webp", "epoxy-resources-stairs")
    elif rel == "services/index.html":
        interior = ("/images/brand/luminous-finish-hall.webp", "luminous-finish-hall")
    elif rel == "services/residential-epoxy-flooring/index.html":
        interior = ("/images/brand/epoxy-basement-poster.jpg", "epoxy-basement")
    elif rel == "services/commercial-epoxy-flooring/index.html":
        interior = ("/images/brand/epoxy-commercial-poster.jpg", "epoxy-commercial")
    elif rel == "finishes/index.html":
        interior = ("/images/brand/epoxy-finish-poster.jpg", "epoxy-finish")
    elif rel == "warranty/index.html":
        interior = ("/images/brand/epoxy-consultation-poster.jpg", "epoxy-consultation")
    elif rel == "process/index.html":
        interior = ("/images/brand/foundation-chamber.webp", "foundation-chamber")
    elif rel == "about/index.html":
        interior = ("/images/brand/consultation-court.webp", "consultation-court")
    wire_page(page, interior=interior, home_anchors=home)

print("pages", len(pages))
