# Real-Time Transcription and Translation Package

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Real-Time Transcription, multilingual Translation, and Subtitling
This project aims to develop a system that can perform real-time speech transcription, translation, and 
subtitling in over 70 languages. 

The key features includes:- 
- Real-time speech-to-text transcription - As audio streams in real-time, whether from live meetings, events, calls, or videos, the system will automatically generate text transcripts using state-of-the-art speech recognition models.
- Real-time translation - The transcripts generated can further be translated into more than 100 languages in real-time while the audio continues streaming. This allows for simultaneous interpretation-like capabilities.
- Syncing subtitles generation - Using the transcribed and/or translated text, the system can concurrently generate subtitle files in industry standard formats like .VTT (Web Video Text Tracks) and .SRT (SubRip Subtitle). These can be used to display live subtitles for the incoming audio/video streams.
- Text export of transcripts & translations - The system also allows saving the generated transcripts and translations into simple text files for further use. Users can choose to export just the transcription or just the translations or both for any given audio stream.

The goal is to create a system that can ingest live audio/video streams and use speech recognition and neural machine translation to provide live transcription, translation and subtitling capabilities to make the content accessible to wider audiences in real-time. The project utilizes state-of-the-art deep learning approaches to provide robust and accurate speech-to-text, translation and syncing abilities.

## Installation

To get going, simply download the wheel file from 'dist' directory and install the package via pip:

```bash
pip install talklocal
```

## Usage

To use the package, provide the source_language and target_language to generate subtitles. The package supports automatic language detection.

Example usage:

```bash
# Import necessary modules and packages
import talklocal  # Importing the talklocal package
from talklocal import core  # Importing the core module from talklocal
import asyncio  # Importing the asyncio module for asynchronous operations
from talklocal.models import OutputFormat #Importing output format support

# Creating a UserInput object defining parameters for transcript processing
user_input = talklocal.models.UserInput(
    source_language="en-US",  # Source language for the transcription
    target_language="es-ES",  # Target language for translation
    subtitle_format="vtt",  # optional Subtitle format to generate (e.g., VTT format)
    region="us-east-1",  # optional AWS region for the transcription service
    output_format=OutputFormat.BOTH_TEXT # optional Transcript, Translated output or Both
    )

# Define an asynchronous function named main
async def main():
    # Process the user input and await the results asynchronously
    results = await core.process_request(user_input)
    print(results)  # Print the obtained results

# Entry point of the script - execute only if this file is run directly (not imported)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()  # Get the event loop
    loop.run_until_complete(main())  # Run the main asynchronous function
    loop.close()  # Close the event loop after completion

```

## Features
- Real-time transcription and translation using machine learning.
- Supports automatic language detection for source language.
- Generates subtitles in VTT and SRT formats.

## Contributing
Contributions are welcome! Feel free to open issues, submit feature requests, or contribute code via pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.


