import asyncio
import sounddevice
from talklocal.handle_error import ErrorHandler


class AudioHandler:
    """
    Handles audio streaming for real-time transcription.

    Attributes:
    - input_queue: Asynchronous queue to store audio data.
    - loop: Asyncio event loop used to handle thread-safe queue operations.
    """

    def __init__(self):
        """
        Initializes the AudioHandler object.

        Initializes an input queue to store audio data and gets the current asyncio event loop.
        """
        self.input_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()

    def callback(self, indata, frame_count, time_info, status):
        """
        Callback function for audio input.

        Args:
        - indata: Input audio data.
        - frame_count: Number of frames in the input data.
        - time_info: Timestamp or timing information of the input.
        - status: Status of the input stream.
        """
        self.loop.call_soon_threadsafe(self.input_queue.put_nowait, (bytes(indata), status))

    async def mic_stream(self):
        """
        Generates a stream of audio data from the microphone.

        Yields:
        - Audio data in chunks along with the status of the stream.
        """
        stream = sounddevice.RawInputStream(
            channels=1,
            samplerate=16000,
            callback=self.callback,
            blocksize=1024 * 2,
            dtype="int16",
        )

        stream.start()

        try:
            while True:
                indata, status = await self.input_queue.get()
                yield indata, status
        except Exception as e:
            # Handling different error types using ErrorHandler.handle_error
            raise ErrorHandler.TranscriptionError(f"audio handler error: {e}")
        finally:
            # Perform cleanup operations in the 'finally' block
            stream.stop()
