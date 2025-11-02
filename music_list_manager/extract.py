import os, json, csv, re
from bs4 import BeautifulSoup

FIELDS = [
    "FileName","Title","Artist","Remixer","Album","Label","Genre","BPM","Key","Length",
    "ReleaseDate","ISRC","Exclusive","Hype","Price","SourceURL","SampleURL","CoverURL","Comment"
]

def _first(*values):
    for v in values:
        if v:
            return v
    return ""

def _join_names(items):
    names = []
    for it in items or []:
        if isinstance(it, dict):
            name = it.get("name") or it.get("title") or it.get("artist") or ""
            if name:
                names.append(str(name))
        elif isinstance(it, str):
            names.append(it)
    return ", ".join(names)

def _detect_tracks(obj):
    candidates = []
    if isinstance(obj, list):
        if obj and isinstance(obj[0], dict) and any(k in obj[0].keys() for k in ("title","name","track","song")):
            candidates.append(obj)
        else:
            for x in obj:
                candidates.extend(_detect_tracks(x))
    elif isinstance(obj, dict):
        for _, val in obj.items():
            if isinstance(val, list) and val and isinstance(val[0], dict) and any(k in val[0].keys() for k in ("title","name","track","song")):
                candidates.append(val)
            else:
                candidates.extend(_detect_tracks(val))
    return candidates

def parse_track(track):
    title = _first(track.get("title"), track.get("name"), track.get("track"), track.get("song"))
    artists = _first(_join_names(track.get("artists")), _join_names(track.get("artist")), track.get("artist"))
    remixers = _join_names(track.get("remixers")) if isinstance(track.get("remixers"), (list, tuple)) else (track.get("remixer") or "")
    album = _first(track.get("album"), track.get("release",{}).get("name"))
    label = _first(track.get("label",{}).get("name") if isinstance(track.get("label"), dict) else track.get("label"))
    genre = _first(track.get("genre"), track.get("genres",{}).get("name") if isinstance(track.get("genres"), dict) else None)
    if not genre and isinstance(track.get("genres"), list):
        genre = _first(*(g.get("name") for g in track.get("genres") if isinstance(g, dict)))

    bpm = _first(track.get("bpm"), track.get("tempo"))
    key = _first(track.get("key"), track.get("initial_key"), track.get("initialKey"), track.get("musical_key"))
    length = _first(track.get("length"), track.get("duration"))
    release_date = _first(track.get("release_date"), track.get("publish_date"), track.get("date"))
    isrc = track.get("isrc","")
    exclusive = "Yes" if track.get("exclusive") else "No"
    hype = "Yes" if track.get("hype") else "No"
    price = ""
    if isinstance(track.get("price"), dict):
        price = _first(track["price"].get("display"), track["price"].get("value"))
    elif isinstance(track.get("price"), (int,float,str)):
        price = str(track.get("price"))

    source_url = _first(track.get("url"), track.get("permalink"), track.get("link"))
    sample_url = _first(track.get("sample_url"), track.get("preview",{}).get("mp3") if isinstance(track.get("preview"), dict) else None)

    img = track.get("image")
    cover_url = ""
    if isinstance(img, dict):
        cover_url = _first(img.get("uri"), img.get("url"))
    elif isinstance(img, str):
        cover_url = img

    comment = _first(track.get("mix_name"), track.get("mixName"), track.get("version"))

    return {
        "FileName":"",
        "Title": title or "",
        "Artist": artists or "",
        "Remixer": remixers or "",
        "Album": album or "",
        "Label": label or "",
        "Genre": genre or "",
        "BPM": bpm or "",
        "Key": key or "",
        "Length": length or "",
        "ReleaseDate": release_date or "",
        "ISRC": isrc or "",
        "Exclusive": exclusive,
        "Hype": hype,
        "Price": price or "",
        "SourceURL": source_url or "",
        "SampleURL": sample_url or "",
        "CoverURL": cover_url or "",
        "Comment": comment or ""
    }

def main(html_input='music_list_source.html', csv_output='music_list.csv'):
    if not os.path.exists(html_input):
        print(f"❌ File not found: {html_input}")
        return

    with open(html_input, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")

    all_tracks = []
    for s in scripts:
        content = (s.string or "").strip()
        if not content:
            continue
        candidates = re.findall(r'(\{.*\}|\[.*\])', content, flags=re.DOTALL)
        for c in candidates:
            try:
                data = json.loads(c)
            except Exception:
                continue
            lists = _detect_tracks(data)
            for lst in lists:
                for item in lst:
                    if isinstance(item, dict):
                        all_tracks.append(parse_track(item))

    if not all_tracks:
        print("⚠️ No songs found automatically. Check the HTML or adjust heuristics.")
        return

    with open(csv_output, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter=';')
        w.writeheader()
        for row in all_tracks:
            w.writerow(row)

    print(f"✅ Extracted {len(all_tracks)} tracks to {csv_output}")
    print("ℹ️ Fill the 'FileName' column with the exact filename of the real file in your music folder.")
