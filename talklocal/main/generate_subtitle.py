'''
The SubtitleGenerator class handles generating subtitle files.

It currently supports generating WebVTT (.vtt) and SRT (.srt) formatted subtitles.

Usage:

generator = SubtitleGenerator()
generator.generate_vtt_subtitle(translated_text)

Generates a vtt subtitle file with the translated text.

The file path and name can be specified on instantiation. By default it uses
"./subtitle/realtime_subtitle.vtt".

generate_vtt_subtitle() handles:

- Opening/writing to the vtt file
- Writing header if new file
- Generating start/end timestamps
- Writing cue with original text and timestamps

It also supports partial subtitles by passing partial_flag=True.
This will append to existing cues instead of overwriting the file.

Error handling:

- SubtitlingError custom exception raised on errors
'''
import logging
from datetime import datetime
import os
import re
from talklocal.handle_error import ErrorHandler
from datetime import timedelta
from collections import deque


class CaptionSmoothing:
    def __init__(self, window_size):
        self.window_size = window_size
        self.caption_buffer = deque(maxlen=window_size)

    def add_caption(self, new_caption):
        self.caption_buffer.append(new_caption)

    def get_smoothed_caption(self):
        print(f"Caption Buffer: {self.caption_buffer}")

        if not self.caption_buffer:
            return None  # No captions available

        # Calculate the moving average
        smoothed_caption = sum(self.caption_buffer) / max(1, len(self.caption_buffer))

        return smoothed_caption

class SubtitleGenerator:
    '''Subtitle generation handler'''
    def __init__(self, subtitle_path="./subtitle/realtime_subtitle"):
        '''Constructor to initialize the generator

                Args:
                    subtitle_path (str, optional): The file path to use for subtitles.
                        Defaults to "./subtitle/realtime_subtitle.vtt"
        '''
        self.subtitle_path = subtitle_path
        self.caption_smoother = CaptionSmoothing(window_size=5)  # Adjust the window size as needed


    def generate_vtt_subtitle(self, translated_text, partial_flag=False):
        """
            Generate a WebVTT (.vtt) subtitle file entry based on translated text.

            Args:
            - translated_text (str): Translated text to be included in the subtitle.
            - partial_flag (bool, optional): Flag indicating if the translated text is partial (default: False).

            Raises:
            - ErrorHandler.SubtitlingError: If an error occurs while generating the WebVTT subtitle.

            The function calculates the start time, end time, and writes the translated text into a WebVTT (.vtt) subtitle file.
            It uses the current timestamp as the start time, calculates the end time based on the text duration,
            and appends the translated text along with appropriate timestamp format into the specified subtitle file path.

            Note:
            - The `partial_flag` parameter allows marking subtitles as partial translations.
            - WebVTT format starts with 'WEBVTT' header followed by cue timings and text, separated by a blank line.
            """
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            start_time = timestamp + ".000"  # Assuming milliseconds precision
            end_time = self.calculate_end_time(start_time, translated_text)

            file_exists = os.path.isfile(self.subtitle_path + ".vtt")
            file_empty = os.stat(self.subtitle_path + ".vtt").st_size == 0 if file_exists else True

            with open(self.subtitle_path + ".vtt", "a") as vtt_file:
                if file_empty:
                    vtt_file.write("WEBVTT\n\n")

                # Write cue start and end times along with original and translated text
                vtt_file.write(f"{start_time} --> {end_time}\n")
                vtt_file.write(f"{translated_text}\n")
                #vtt_file.write(f"{smoothed_text}\n")

        except Exception as e:
            raise ErrorHandler.SubtitlingError(f"Subtitle generation error: {e}")


    def calculate_end_time(self, start_time, text, average_words_per_minute=150):
        '''Estimates end time for subtitle based on start time and text content.

                Uses a word-based estimate using average words per minute, plus additional
                time for punctuation and average sentence duration.

                Args:
                    start_time (str): Start timestamp in HH:MM:SS.mmm format
                    text (str): Text content to calculate duration
                    average_words_per_minute (int, optional): Defaults to 150

                Returns:
                    str: Calculated end timestamp in HH:MM:SS.mmm format
        '''
        if start_time is None:
            return None

        start_dt = datetime.strptime(start_time, "%H:%M:%S.%f")
        word_count = len(re.findall(r'\w+', text))
        seconds_per_word = 60 / average_words_per_minute
        additional_seconds = word_count * seconds_per_word

        punctuation_pause_multiplier = 1.2
        punctuation_count = len(re.findall(r'[.,?!]', text))
        additional_seconds += punctuation_count * punctuation_pause_multiplier

        seconds_per_sentence = 3
        sentence_count = len(re.split(r'[.!?]', text))
        additional_seconds += sentence_count * seconds_per_sentence

        end_dt = start_dt + timedelta(seconds=additional_seconds)
        return end_dt.strftime("%H:%M:%S.%f")[:-3] + "Z"

    def get_next_cue_number(self, file_name):
        """
        Get the next cue number for a subtitle file.

        Args:
        - file_name (str): Name of the subtitle file.

        Returns:
        - int or None: Next cue number if the file exists and contains cues; otherwise, returns 1.

        The function checks if the specified subtitle file exists. If it doesn't exist or is empty,
        it returns 1 as the default cue number. Otherwise, it reads the subtitle file,
        searches for the last cue number, and returns the next sequential cue number to be used.
        """
        if not os.path.exists(file_name):
            return 1

        with open(file_name) as f:
            lines = f.readlines()

        if len(lines) == 0:
            return 1

        last_cue_number = None
        for line in reversed(lines):
            stripped_line = line.strip()
            if stripped_line and stripped_line.isdigit():
                last_cue_number = int(stripped_line)
                break

        return last_cue_number + 1 if last_cue_number is not None else None

    def generate_srt_subtitle(self, translated_text, partial_flag=False):
        """
            Generate an SRT subtitle file entry based on translated text.

            Args:
            - translated_text (str): Translated text to be included in the subtitle.
            - partial_flag (bool, optional): Flag indicating if the translated text is partial (default: False).

            Raises:
            - ErrorHandler.SubtitlingError: If an error occurs while generating the subtitle.

            The function calculates the start time, end time, and writes the translated text into an SRT subtitle file.
            It uses the current time as the start time, calculates the end time based on the text duration,
            and appends the translated text along with appropriate cue numbers and timestamp format
            into the specified subtitle file path.

            Note:
            - The `partial_flag` parameter allows marking subtitles as partial translations.
            """

        try:
            start_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            end_time = self.calculate_end_time(start_time, translated_text)
            file_exists = os.path.isfile(self.subtitle_path + ".srt")
            file_empty = os.stat(self.subtitle_path + ".srt").st_size == 0 if file_exists else True

            with open(self.subtitle_path + ".srt", "a") as srt_file:
                cue = self.get_next_cue_number(self.subtitle_path + ".srt")
                if file_empty or cue is None:
                    cue = 1  # Default cue number if the cue retrieval fails or the file is empty

                srt_file.write(f"{cue}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{translated_text}\n\n")

        except Exception as e:
            # Handling different error types using ErrorHandler.handle_error
            raise ErrorHandler.SubtitlingError(f"error generating subtitle: {e}")
