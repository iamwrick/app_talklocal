import logging
import os
from datetime import datetime
from talklocal.handle_error import ErrorHandler

class OutputGenerator:
    '''Output generation handler'''
    def __init__(self, output_path="./output"):
        '''Constructor to initialize the output generator

        Args:
            output_path (str, optional): The directory path to store output files.
                Defaults to "./output".
        '''
        self.output_path = output_path

    def store_transcript(self, transcript_text):
        '''Stores transcript text in a file

        Args:
            transcript_text (str): The transcript text to be stored.
            is_partial (bool, optional): Whether the transcript is partial.
                Defaults to False.
        '''
        file_name = "transcript_full.txt"
        self._store_text_file(file_name, transcript_text)

    def store_translated_output(self, translated_text):
        '''Stores translated output text in a file

        Args:
            translated_text (str): The translated output text to be stored.
            is_partial (bool, optional): Whether the translation is partial.
                Defaults to False.
        '''
        file_name = "translated_output_full.txt"
        self._store_text_file(file_name, translated_text)

    def _store_text_file(self, file_name, text_content):
        '''Helper method to store text content in a file

        Args:
            file_name (str): The name of the file to be created/used.
            text_content (str): The content to be written to the file.
        '''

        try:
            file_path = os.path.join(self.output_path, file_name)
            with open(file_path, "a") as text_file:
                text_file.write(text_content)
                text_file.write("\n")  # Add line breaks for separation of entries

        except Exception as e:
            raise ErrorHandler.OutputGenerationError(f"Error storing output: {e}")