import os, csv

def _sanitize(name):
    bad = r'\/:*?"<>|'
    return "".join(c for c in (name or "") if c not in bad).strip()

def _build_name(artist, title, label, year):
    artist = _sanitize(artist) or "Unknown Artist"
    title = _sanitize(title) or "Unknown Title"
    label = _sanitize(label) if label else ""
    y = (year[:4] if isinstance(year, str) and len(year) >= 4 else "")
    if label and y:
        return f"{artist} - {title} [{label}] ({y}).mp3"
    if label:
        return f"{artist} - {title} [{label}].mp3"
    if y:
        return f"{artist} - {title} ({y}).mp3"
    return f"{artist} - {title}.mp3"

def main(csv_path='music_list.csv', music_dir='Music_List'):
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return
    os.makedirs(music_dir, exist_ok=True)

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            fname = (row.get("FileName") or "").strip()
            if not fname:
                print("⚠️  Row without FileName. Skipped.")
                continue

            base, _ = os.path.splitext(fname)
            src = os.path.join(music_dir, base + ".mp3")
            if not os.path.exists(src):
                # búsqueda sin distinguir mayúsculas/minúsculas
                target_lower = (base + ".mp3").lower()
                found = None
                for f in os.listdir(music_dir):
                    if f.lower() == target_lower:
                        found = os.path.join(music_dir, f)
                        break
                if not found:
                    print(f"⚠️  MP3 file not found for renaming: {fname}")
                    continue
                src = found

            new_name = _build_name(row.get("Artist"), row.get("Title"), row.get("Label"), row.get("ReleaseDate"))
            dst = os.path.join(music_dir, new_name)
            try:
                os.rename(src, dst)
                print(f"✅ {os.path.basename(src)} → {new_name}")
            except Exception as e:
                print(f"❌ Error renaming {src}: {e}")
