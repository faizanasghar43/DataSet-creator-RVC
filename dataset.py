import os
import zipfile
import math
import numpy as np
import librosa
import soundfile as sf
import tkinter as tk
from tkinter import filedialog
import shutil

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get all the MP3 or WAV files in the "audios" folder
print("Instant Dataset Maker")
print("provided to you by youtube.com/@rawonions")
print("Read the README.txt file for more info!")
print()
print("Loading...")
audio_dir = os.path.join(script_dir, 'audios')
audio = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.mp3') or f.endswith('.wav')]

# Set segment length range
min_length = 6  # 6 seconds
max_length = 9  # 9 seconds

# Create a temporary directory to store the segments
temp_dir = os.path.join(script_dir, 'temp')
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

# Split the audio into segments and save them as WAV files
segments = []
try:
    for audio_file in audio:
        # Load the audio file
        audio_path = os.path.join(script_dir, audio_file)
        audio, sr = librosa.load(audio_path, sr=None)

        # Remove the silent parts from the audio
        non_silent_ranges = librosa.effects.split(audio, top_db=20)
        non_silent_audio = np.concatenate([audio[start:end] for start, end in non_silent_ranges])

        # Split the non-silent audio into segments
        segment_length = sr * max_length
        hop_length = sr * (max_length - min_length)
        for i, segment in enumerate(librosa.util.frame(non_silent_audio, frame_length=segment_length, hop_length=hop_length, axis=0)):
            # Skip the segment if it's too short
            if len(segment) < sr * min_length:
                continue

            # Save the segment as a WAV file
            segment_path = os.path.join(temp_dir, f'file_{len(segments)}.wav')
            sf.write(segment_path, segment, sr)
            segments.append(segment_path)

    # Ask the user where to save the dataset ZIP file
    root = tk.Tk()
    root.withdraw()
    zip_path = filedialog.asksaveasfilename(defaultextension='.zip', filetypes=[('ZIP files', '*.zip')])

    # Create a folder with the same name as the ZIP file
    zip_folder = os.path.splitext(zip_path)[0]
    os.mkdir(zip_folder)

    # Create a folder inside the ZIP file with the same name as the ZIP file
    zip_folder_in_zip = os.path.join(zip_folder, os.path.basename(zip_folder))
    os.mkdir(zip_folder_in_zip)

    # Add the segments to the folder inside the ZIP file
    for segment in segments:
        segment_name = os.path.basename(segment)
        segment_path = os.path.join(zip_folder_in_zip, segment_name)
        shutil.copy(segment, segment_path)

    # Create a ZIP file and add the folder to it
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for root, dirs, files in os.walk(zip_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, zip_folder))

    # Remove the folders
    shutil.rmtree(zip_folder_in_zip)
    shutil.rmtree(zip_folder)

    print(f'Dataset saved as {zip_path}')

except Exception as e:
    print(f'Error: {e}')
    # Remove the temporary directory and its contents
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
    print('Temporary directory deleted')

else:
    # Remove the temporary directory and its contents
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
    print('Temporary directory deleted')
