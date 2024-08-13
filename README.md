# DataSet-creator-RVC
The first step in creating an RVC dataset is to gather the audio data you want to clone. This could be recordings of human voices or any other source you intend to replicate. Ensure that your audio files are collected and organized in a folder, such as an "audios" directory.

## Features

- **Supports MP3 and WAV files**: Automatically detects and processes audio files in the `audios` folder.
- **Silent Removal**: Automatically removes silent sections from the audio before processing.
- **Configurable Segment Length**: Splits audio into segments ranging from 6 to 9 seconds.
- **ZIP Packaging**: Packages all generated audio segments into a ZIP file for easy sharing or storage.
- **User-Friendly Save Prompt**: Allows users to select where to save the final ZIP file via a graphical interface.

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

```bash
pip install numpy librosa soundfile tkinter
