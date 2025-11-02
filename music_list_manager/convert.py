import os
from pydub import AudioSegment

def _convert_wav_to_mp3(src, dst, bitrate='320k'):
    audio = AudioSegment.from_wav(src)
    audio.export(dst, format="mp3", bitrate=bitrate)
    print(f"✅ {os.path.basename(src)} → {os.path.basename(dst)}")

def main(in_dir='Music_WAV', out_dir='Music_MP3', bitrate='320k'):
    if not os.path.exists(in_dir):
        print(f"⚠️ Directory does not exist: {in_dir}")
        return
    os.makedirs(out_dir, exist_ok=True)

    wavs = [f for f in os.listdir(in_dir) if f.lower().endswith('.wav')]
    if not wavs:
        print("ℹ️ No WAV files found in input directory.")
        return

    for f in wavs:
        src = os.path.join(in_dir, f)
        base, _ = os.path.splitext(f)
        dst = os.path.join(out_dir, base + ".mp3")
        try:
            _convert_wav_to_mp3(src, dst, bitrate)
        except Exception as e:
            print(f"❌ Error converting {src}: {e}")

    print("🎵 Conversion completed.")
