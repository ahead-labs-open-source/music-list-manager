# 🎵 Music List Manager

**Generic** Python package and CLI for:
- **extracting metadata** from HTML with structured data to **CSV**,
- **tagging MP3** files (ID3v2) with cover art from CSV,
- **renaming files** with a standard format,
- and **converting WAV → MP3** if needed.

Platform-independent solution.

## 🚀 Installation

```bash
pip install .
# or for development
pip install -e .
```

## 🖥️ CLI

```bash
music-list extract [--html music_list_source.html] [--csv music_list.csv]
music-list tag [--csv music_list.csv] [--dir Music_List]
music-list rename [--csv music_list.csv] [--dir Music_List]
music-list convert [--in Music_WAV] [--out Music_MP3] [--bitrate 320k]
```

## 🛠️ Standalone Scripts

If you prefer using individual scripts instead of the CLI:

```bash
python scripts/extract_music_list.py
python scripts/update_id3_tags.py
python scripts/rename_music_files.py
python scripts/convert_wav_to_mp3.py
```

## 📁 Expected CSV format (separator ';')

```
FileName;Title;Artist;Remixer;Album;Label;Genre;BPM;Key;Length;ReleaseDate;ISRC;Exclusive;Hype;Price;SourceURL;SampleURL;CoverURL;Comment
251102_001.WAV;Take It Down;Belocca;;Take It Down;Enter Audio;Techno;136;9B;5:54;2025-10-02;;;;;;;;
mixsession_final.mp3;Bad Boy Sound;Bermio & Amber Broos;;Bad Boy Sound;Arcadia Music;Techno;140;2B;5:47;2025-08-27;;;;;;;;
```

- **FileName**: exact filename of the source file (with extension) inside `--dir`.
- `CoverURL`: direct URL to the cover art (JPG/PNG).

## 🔧 Additional Requirements

- **FFmpeg** (for conversion/reading formats): macOS `brew install ffmpeg`, Ubuntu `sudo apt install ffmpeg`, Windows download from https://ffmpeg.org/ and add to PATH.
