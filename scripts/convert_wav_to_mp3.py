import os
from pydub import AudioSegment

WAV_DIR = "Music_WAV"
MP3_DIR = "Music_MP3"
MP3_BITRATE = "320k"

def convert_wav_to_mp3(src, dst):
    try:
        audio = AudioSegment.from_wav(src)
        audio.export(dst, format="mp3", bitrate=MP3_BITRATE)
        print(f"✅ {os.path.basename(src)} → {os.path.basename(dst)}")
    except Exception as e:
        print(f"❌ Error converting {src}: {e}")

def main():
    if not os.path.exists(WAV_DIR):
        print(f"⚠️ Directory does not exist: {WAV_DIR}")
        return
    os.makedirs(MP3_DIR, exist_ok=True)

    wavs = [f for f in os.listdir(WAV_DIR) if f.lower().endswith(".wav")]
    if not wavs:
        print("ℹ️ No WAV files found in Music_WAV/.")
        return

    for f in wavs:
        src = os.path.join(WAV_DIR, f)
        base, _ = os.path.splitext(f)
        dst = os.path.join(MP3_DIR, base + ".mp3")
        convert_wav_to_mp3(src, dst)

    print("🎵 Conversion completed. Copy the MP3s to Music_List/ if you want to tag them.")

if __name__ == "__main__":
    main()
