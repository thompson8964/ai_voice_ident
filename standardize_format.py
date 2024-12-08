import os
from pydub import AudioSegment
os.environ["PATH"] += os.pathsep + r"E:\ffmpeg"
AudioSegment.converter = r'E:\ffmpeg\ffmpeg.exe'
AudioSegment.ffprobe = r'E:\ffmpeg\ffprobe.exe'


from tqdm import tqdm
import argparse

# AudioSegment.converter = which("ffmpeg")
#AudioSegment.ffprobe = which("ffprobe")

def convert_to_wav_44100_16bit(input_folder, output_folder):
    """
    Converts all audio files in the input_folder to 44,100 Hz, 16-bit WAV format.

    Parameters:
    - input_folder: Path to the folder containing input audio files.
    - output_folder: Path to the folder to save converted files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in tqdm(os.listdir(input_folder)):
        if file_name.lower().endswith(('.mp3', '.wav', '.flac', '.ogg', '.aac')):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.wav')

            try:
                # Load the audio file
                audio = AudioSegment.from_file(input_path)
                # Resample to 44.1 kHz and set to 16-bit
                audio = audio.set_frame_rate(44100).set_sample_width(2)
                # Export as WAV
                audio.export(output_path, format="wav")
                print(f"Converted: {file_name} -> {output_path}")
            except Exception as e:
                print(f"Failed to convert {input_path}: {e}")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input_path", "-i", required=True, help="input path")
    arg_parser.add_argument("--output_path", "-o", required=True, help="output path")
    args = arg_parser.parse_args()

    # extra_audio_features_multiple("real_mpeg", False, "audio_real_test.csv", "audio_real_train.csv")
    convert_to_wav_44100_16bit(
        input_folder=args.input_path,
        output_folder=args.output_path,
    )
