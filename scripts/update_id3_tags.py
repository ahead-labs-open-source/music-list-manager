import csv
import os
import requests
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3

CSV_PATH = "music_list.csv"
MUSIC_DIR = "Music_List"
OUTPUT_EXT = ".mp3"

def detect_mime(url, data):
    if data and len(data) >= 8 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data and len(data) >= 3 and data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    u = (url or "").lower()
    if ".png" in u: return "image/png"
    if ".jpg" in u or ".jpeg" in u: return "image/jpeg"
    return "image/jpeg"

def download_image(url):
    if not url:
        return None, None
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            mime = detect_mime(url, r.content)
            return r.content, mime
    except Exception as e:
        print(f"⚠️  Error descargando portada: {e}")
    return None, None

def find_case_insensitive(path):
    if os.path.exists(path):
        return path
    d, f = os.path.dirname(path), os.path.basename(path)
    if not os.path.isdir(d):
        return path
    fl = f.lower()
    for x in os.listdir(d):
        if x.lower() == fl:
            return os.path.join(d, x)
    return path

def convert_to_mp3(src, dst, bitrate="320k"):
    audio = AudioSegment.from_file(src)
    audio.export(dst, format="mp3", bitrate=bitrate)
    return dst

def apply_id3(mp3_path, row, cover_bytes=None, cover_mime="image/jpeg"):
    try:
        audio = MP3(mp3_path, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass

        tags = EasyID3(mp3_path)
        if row.get("Title"): tags["title"] = row["Title"]
        if row.get("Artist"): tags["artist"] = row["Artist"]
        if row.get("Album"): tags["album"] = row["Album"]
        if row.get("Genre"): tags["genre"] = row["Genre"]
        if row.get("BPM"): tags["bpm"] = str(row["BPM"])
        if row.get("ReleaseDate"): tags["date"] = row["ReleaseDate"]
        if row.get("Label"): tags["publisher"] = row["Label"]
        if row.get("Key"): tags["initialkey"] = row["Key"]
        # Comentarios enriquecidos
        extras = []
        for k in ("ISRC","Exclusive","Hype","Price","SourceURL","SampleURL","Comment"):
            if row.get(k):
                extras.append(f"{k}={row[k]}")
        if extras:
            tags["comment"] = " | ".join(extras)
        tags.save()

        if cover_bytes:
            audio.tags.add(APIC(encoding=3, mime=cover_mime, type=3, desc="Cover", data=cover_bytes))

        audio.save()
        print(f"✅ Tagged: {os.path.basename(mp3_path)}")
    except Exception as e:
        print(f"❌ Error tagging {mp3_path}: {e}")

def main():
    if not os.path.exists(CSV_PATH):
        print(f"❌ File not found: {CSV_PATH}")
        return
    os.makedirs(MUSIC_DIR, exist_ok=True)

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            fname = (row.get("FileName") or "").strip()
            if not fname:
                print("⚠️  Row without FileName. Skipped.")
                continue

            src = os.path.join(MUSIC_DIR, fname)
            src = find_case_insensitive(src)
            if not os.path.exists(src):
                print(f"⚠️  File not found: {fname}")
                continue

            base, ext = os.path.splitext(src)
            if ext.lower() != ".mp3":
                target = base + OUTPUT_EXT
                try:
                    convert_to_mp3(src, target)
                except Exception as e:
                    print(f"❌ Error converting {fname}: {e}")
                    continue
            else:
                target = src

            cover_bytes, cover_mime = download_image(row.get("CoverURL"))
            apply_id3(target, row, cover_bytes, cover_mime)

if __name__ == "__main__":
    main()
