
import os
import subprocess
from tqdm import tqdm

# Define the directory containing M4A files
input_directory = 'real'  # Change this to your directory
output_directory = 'real_mpeg'  # Change this to your output directory

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through all M4A files in the input directory
for filename in tqdm(os.listdir(input_directory)):
    if filename.endswith('.mp3'):
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(output_directory, filename)#.replace('.m4a', '.mpeg'))
        if os.path.exists(output_file):
            continue

        # Command to convert M4A to MPEG using ffmpeg
        command = [r'C:\Users\Thomas Song\PycharmProjects\audioBackend\ffmpeg_win\ffmpeg.exe', '-i', input_file, output_file]

        try:
            subprocess.run(command, check=True)
            print(f'Converted: {input_file} to {output_file}')
        except subprocess.CalledProcessError as e:
            print(f'Error converting {input_file}: {e}')