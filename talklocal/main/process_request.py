import asyncio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler

from . import generate_output
from .generate_output import OutputGenerator
from .translate_transcript import Translate
from .generate_subtitle import SubtitleGenerator
from .audio_handler import AudioHandler
import logging
from ..handle_error import ErrorHandler
from ..models import OutputFormat

class TranscriptDataHandler:
    '''
    The TranscriptDataHandler provides functionality to:

    - Store transcript text and metadata
    - Retrieve stored transcript data

    It allows storing streaming transcript data from speech recognition,
    keeping track of partial vs finalized transcripts.

    The stored data can then be retrieved for further processing or persistence.

    Usage:

    handler = TranscriptDataHandler()

    handler.store_transcript_data(transcript_text, is_partial)

    data = handler.get_transcript_data()

    '''
    def __init__(self):
        '''Initializes empty list to store transcript and translated data'''
        self.transcript_data = []
        self.translated_data = []

    def store_transcript_data(self, transcript_text, is_partial):
        '''Stores transcript text and whether it is a partial transcript'''
        self.transcript_data.append((transcript_text, is_partial))

    def get_transcript_data(self):
        '''Retrieves stored transcript data'''
        return self.transcript_data[:]

    def store_translated_data(self, translated_text, is_partial):
        '''Stores transcript text and whether it is a partial transcript'''
        self.translated_data.append((translated_text, is_partial))

    def get_translated_data(self):
        '''Retrieves stored transcript data'''
        return self.translated_data[:]


class TranscriptHandler(TranscriptResultStreamHandler):
    '''
    The TranscriptHandler handles transcripts generated from a speech recognition stream.

    It processes each transcript event and handles:

    - Translating the transcript text
    - Generating subtitles
    - Storing transcript data
    - Logging/errors

    It extends the TranscriptResultStreamHandler to process the raw stream events.

    Usage:

    data_handler = TranscriptDataHandler()
    handler = TranscriptHandler(output_stream, source_lang, target_lang,
                                subtitle_format, data_handler)

     speech_to_text_client.start_stream(handler)

    '''
    def __init__(
        self,
        output_stream,
        source_language,
        target_language,
        subtitle_format,
        region,
        output_format,
        data_handler,
    ):
        '''Initializes handler with translation languages, subtitle
                format, data storage and base stream handling.'''
        super().__init__(output_stream)
        self.source_language = source_language
        self.target_language = target_language
        self.subtitle_format = subtitle_format
        self.region = region
        self.output_format = output_format
        self.sequence_number = 0
        self.data_handler = data_handler  # Store data_handler

    async def handle_transcript_event(self, transcript_event):
        """
        Handles transcription events and performs translation, subtitle generation, and output storage.

        Args:
        - transcript_event (TranscriptEvent): Event object containing transcription results.

        Raises:
        - ErrorHandler.TranscriptionError: If an error occurs while handling the transcript event.

        This method processes the transcript event received from the transcription stream.
        It retrieves transcription results and iterates through alternatives to extract transcript text.
        Then it translates the transcript text, generates subtitles based on the specified format,
        and stores the transcript and translated text if requested and not marked as partial.
        The process involves using Translate, SubtitleGenerator, and OutputGenerator instances.
        Any encountered error is handled and raised as a TranscriptionError using ErrorHandler.
        """
        translate = Translate()
        generate_subtitle = SubtitleGenerator()
        generate_output = OutputGenerator()
        try:
            results = transcript_event.transcript.results

            # Determine output format for text files
            store_transcript_text = self.output_format in [OutputFormat.TRANSCRIPT_TEXT,
                                                                      OutputFormat.BOTH_TEXT]
            store_translated_text = self.output_format in [OutputFormat.TRANSLATED_TEXT,
                                                                      OutputFormat.BOTH_TEXT]
            # Check if source and target languages are the same outside the loop.
            # Amazon Transcribe and Amazon Translate has different language codes for same language
            #same_languages = self.source_language.lower() == self.target_language.lower()
            same_languages = (
                    self.source_language.lower() == self.target_language.lower()
                    or (self.source_language == 'en-US' and self.target_language == 'en')
            )

            for result in results:
                for alt in result.alternatives:
                    transcript_text = alt.transcript
                    is_partial = result.is_partial

                    # Use the transcript text directly if languages are the same or else use the translate
                    if same_languages:
                        translated_text = transcript_text
                    else:
                        translated_text = translate.translate_text(transcript_text, self.source_language,
                                                                   self.target_language, self.region)

                    # Generate subtitles based on the specified format
                    if self.subtitle_format.lower() == 'vtt':
                        generate_subtitle.generate_vtt_subtitle(translated_text, is_partial)
                    else:
                        generate_subtitle.generate_srt_subtitle(translated_text, is_partial)

                    # Store transcript and translated text if requested and not partial
                    if not is_partial:
                        if store_transcript_text:
                            generate_output.store_transcript(transcript_text)

                        if store_translated_text:
                            generate_output.store_translated_output(translated_text)

        except Exception as e:
            # Handling different error types using ErrorHandler.handle_error
            raise ErrorHandler.TranscriptionError(f"transcript event error: {e}")

async def write_chunks(stream, audio_handler):
    """
    Streams audio chunks to Amazon Transcribe service.

    Args:
    - stream: TranscribeStreamingClient stream for audio input.
    - audio_handler: Object handling the audio streaming.
    """
    async for chunk, status in audio_handler.mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe(source_language,
                           target_language,
                           subtitle_format,
                           region_name,
                           output_format,
                           audio_handler,
                           data_handler):
    """
    Initiates the basic transcription process.

    Args:
    - source_language (str): Source language code for transcription.
    - target_language (str): Target language code for translation.
    - subtitle_format (SubtitleFormat): Subtitle format configuration.
    - region_name (str): AWS region name for transcription.
    - output_format (OutputFormat): Output format configuration.
    - audio_handler (AudioHandler): Handler for audio data.
    - data_handler (TranscriptDataHandler): Handler for transcript data.

    Returns:
    - TranscriptData or None: Transcript data generated from the transcription process.

    This function initiates the basic transcription process using AWS TranscribeStreamingClient.
    It starts a transcription stream with the specified configurations, manages the streaming data,
    and handles the transcript using a TranscriptHandler instance.
    The process involves writing audio chunks to the stream and handling stream events asynchronously.
    Upon completion, it retrieves and returns the generated transcript data using the TranscriptDataHandler.
    """

    try:
        # Initialize TranscribeStreamingClient
        client = TranscribeStreamingClient(region=region_name)

        # Start stream transcription
        stream = await client.start_stream_transcription(
            language_code=source_language,
            media_sample_rate_hz=16000,
            media_encoding="pcm",
            enable_partial_results_stabilization=True,
            partial_results_stability='medium'
        )

        # Check if data_handler is a TranscriptDataHandler instance
        if not isinstance(data_handler, TranscriptDataHandler):
            raise ValueError(
                "Invalid data_handler. Expected TranscriptDataHandler instance."
            )

        # Initialize and start TranscriptHandler to manage stream events
        handler = TranscriptHandler(
            stream.output_stream,
            source_language,
            target_language,
            subtitle_format,
            region_name,
            output_format,
            data_handler,
        )

        # Asynchronously write audio chunks to stream and handle stream events
        await asyncio.gather(
            write_chunks(stream, audio_handler), handler.handle_events()
        )

        # Retrieve transcript data from data_handler and log success or warning messages
        transcript_data = data_handler.get_transcript_data()
        if transcript_data:
            logging.info("Transcript data extracted successfully.")
        else:
            logging.warning("No transcript data extracted.")

        return transcript_data

    except Exception as e:
        # Handling different error types using ErrorHandler.handle_error
        ErrorHandler.TranscriptionError(f"transcript streaming client error: {e}")
        return None

async def process_request(user_input):
    """
    Initiates the real-time transcription process.

    Args:
    - user_input (UserInput): UserInput object containing source/target languages and other configurations.

    Returns:
    - TranscriptData or None: Transcript data generated from the real-time transcription process.

    This function starts the real-time transcription process based on the provided user input.
    It initializes necessary handlers for audio and transcript data, then awaits the execution
    of the 'basic_transcribe' function to generate transcript data based on the specified configuration.
    The generated transcript data is returned upon completion of the transcription process.
    """
    print("processing real-time streaming request ......")
    source_language = user_input.source_language
    target_language = user_input.target_language
    subtitle_format = user_input.subtitle_format
    region = user_input.region
    output_format = user_input.output_format
    audio_handler = AudioHandler()
    data_handler = TranscriptDataHandler()
    transcript_data = await basic_transcribe(
             source_language, target_language, subtitle_format, region, output_format, audio_handler, data_handler)
    return transcript_data

