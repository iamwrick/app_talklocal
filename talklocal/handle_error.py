class ErrorHandler:
    """Utility class for handling different types of errors in a unified manner."""

    class TranscriptionError(Exception):
        """Custom exception class for Transcription errors."""

        def __init__(self, message, original_error=None):
            """
            Initialize TranscriptionError.

            Args:
            - message (str): Error message.
            - original_error (Exception, optional): Original error (if available). Defaults to None.
            """
            super().__init__(message)
            self.original_error = original_error

        def __str__(self):
            return f"TranscriptionError: {self.original_error}"

        def __repr__(self):
            return f"TranscriptionError: {self.original_error}"

    class TranslationError(Exception):
        """Custom exception class for Translation errors."""

        def __init__(self, message, original_error=None):
            """
            Initialize TranslationError.

            Args:
            - message (str): Error message.
            - original_error (Exception, optional): Original error (if available). Defaults to None.
            """
            super().__init__(message)
            self.original_error = original_error

        def __str__(self):
            return f"TranslationError: {self.original_error}"

        def __repr__(self):
            return f"TranslationError: {self.original_error}"

    class SubtitlingError(Exception):
        """Custom exception class for Subtitling errors."""

        def __init__(self, message, original_error=None):
            """
            Initialize SubtitlingError.

            Args:
            - message (str): Error message.
            - original_error (Exception, optional): Original error (if available). Defaults to None.
            """
            super().__init__(message)
            self.original_error = original_error

        def __str__(self):
            return f"SubtitlingError: {self.original_error}"

        def __repr__(self):
            return f"SubtitlingError: {self.original_error}"

    class OutputGenerationError(Exception):
        """Custom exception class for output generation errors."""

        def __init__(self, message, original_error=None):
            """
            Initialize OutputGenerationError.

            Args:
            - message (str): Error message.
            - original_error (Exception, optional): Original error (if available). Defaults to None.
            """
            super().__init__(message)
            self.original_error = original_error

        def __str__(self):
            return f"OutputGenerationError: {self.original_error}"

        def __repr__(self):
            return f"OutputGenerationError: {self.original_error}"

    @staticmethod
    def handle_error(error_type, message):
        """
        Utility function to handle different types of errors.

        Args:
        - error_type (str): Type of error.
        - message (str): Error message.

        Raises:
        - ValueError: If an invalid error type is specified.
        - TranscriptionError: If the error type is 'transcription'.
        - TranslationError: If the error type is 'translation'.
        - SubtitlingError: If the error type is 'subtitling'.
        - OutputGenerationError: If the error type is 'output'.
        """
        if error_type == 'transcription':
            raise ErrorHandler.TranscriptionError(message)
        elif error_type == 'translation':
            raise ErrorHandler.TranslationError(message)
        elif error_type == 'subtitling':
            raise ErrorHandler.SubtitlingError(message)
        elif error_type == 'output':
            raise ErrorHandler.OutputGenerationError(message)
        else:
            raise ValueError("Invalid error type specified")
