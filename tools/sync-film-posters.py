"""Posters from a real frame, then refresh follow-floor manifest entries."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(r"C:\workspace\ff-films-elevation-2026-11-16")
ff = Path(r"C:\Users\lucid\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin")
ffmpeg = str(ff / "ffmpeg.exe")
ffprobe = str(ff / "ffprobe.exe")
raw = root / "videos" / "follow-floor" / "raw-elevation"

POSTERS = {
    "epoxy-basement": ["images/brand/epoxy-basement-poster.jpg"],
    "epoxy-finish": ["images/brand/epoxy-finish-poster.jpg"],
    "epoxy-commercial": ["images/brand/epoxy-commercial-poster.jpg"],
    "epoxy-consultation": ["images/brand/epoxy-consultation-poster.jpg"],
    "luminous-finish-hall": [
        "images/brand/luminous-finish-hall.jpg",
        "images/brand/luminous-finish-hall.webp",
    ],
    "foundation-chamber": [
        "images/brand/foundation-chamber.jpg",
        "images/brand/foundation-chamber.webp",
    ],
    "consultation-court": [
        "images/brand/consultation-court.jpg",
        "images/brand/consultation-court.webp",
    ],
}


def dims(path: Path):
    out = subprocess.check_output(
        [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
        text=True,
    ).strip()
    w, h = out.split("x")
    return int(w), int(h)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path: Path):
    out = subprocess.check_output(
        [ffprobe, "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height,r_frame_rate", "-of", "json", str(path)],
        text=True,
    )
    data = json.loads(out)
    video = next(s for s in data["streams"] if s.get("codec_name") == "h264" or s.get("width"))
    return {
        "width": int(video["width"]),
        "height": int(video["height"]),
        "r_frame_rate": video.get("r_frame_rate", "24/1"),
        "duration": float(data["format"]["duration"]),
        "codec_name": video.get("codec_name", "h264"),
    }


for name, outputs in POSTERS.items():
    src = root / "videos" / "follow-floor" / "720" / f"{name}.mp4"
    frame = root / "_filmcheck" / f"{name}-poster-src.png"
    frame.parent.mkdir(exist_ok=True)
    subprocess.check_call([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-ss", "1.2", "-i", str(src), "-frames:v", "1", "-update", "1", str(frame)])
    for rel in outputs:
        dest = root / rel
        w, h = dims(dest)
        if dest.suffix.lower() == ".webp":
            subprocess.check_call([
                ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(frame),
                "-vf", f"scale={w}:{h}:flags=lanczos", "-c:v", "libwebp", "-quality", "82", str(dest),
            ])
        else:
            subprocess.check_call([
                ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(frame),
                "-vf", f"scale={w}:{h}:flags=lanczos", "-q:v", "3", str(dest),
            ])
        print(rel, dest.stat().st_size, w, h)

manifest_path = root / "videos" / "follow-floor" / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
replace = {
    "basement", "finish", "commercial", "consultation", "luminous-finish-hall",
    "foundation-chamber", "consultation-court", "resources-stairs",
}
kept = [a for a in manifest["assets"] if a["film"] not in replace]
new_assets = []
films = [
    ("basement", "epoxy-basement", 27, 27, 29),
    ("finish", "epoxy-finish", 27, 27, 29),
    ("commercial", "epoxy-commercial", 27, 27, 29),
    ("consultation", "epoxy-consultation", 27, 27, 29),
    ("luminous-finish-hall", "luminous-finish-hall", 27, 27, 29),
    ("foundation-chamber", "foundation-chamber", 27, 27, 29),
    ("consultation-court", "consultation-court", 27, 27, 29),
    ("resources-stairs", "epoxy-resources-stairs", None, None, None),
]
for film, filename, crf1080, crf720, crf480 in films:
    source = raw / f"{filename}-imagine.mp4"
    source_hash = sha256(source) if source.exists() else None
    for height, folder, crf in ((1080, "1080", crf1080), (720, "720", crf720), (480, "480", crf480)):
        path = root / "videos" / "follow-floor" / folder / f"{filename}.mp4"
        if not path.exists():
            print("missing", path)
            continue
        meta = probe(path)
        entry = {
            "film": film,
            "height": height,
            "crf": crf if crf is not None else 27,
            "src": f"/videos/follow-floor/{folder}/{filename}.mp4",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "codec_name": meta["codec_name"],
            "width": meta["width"],
            "r_frame_rate": meta["r_frame_rate"],
            "duration": round(meta["duration"], 6),
        }
        if source_hash:
            entry["sourceSha256"] = source_hash
        elif film == "resources-stairs":
            entry["note"] = "Midnight Aggregate floor and treads. Not re-encoded in this pass."
        new_assets.append(entry)
        print(film, height, entry["bytes"])

manifest["assets"] = kept + new_assets
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("manifest assets", len(manifest["assets"]))
