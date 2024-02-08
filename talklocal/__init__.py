# Import submodules
from talklocal import core, main, models, handle_error

# Import specific functions
from .main import process_request
from .main import translate_transcript
from .main import generate_subtitle

# Defines what gets imported with *
__all__ = [
    'process_request',
    'translate_transcript',
    'generate_subtitle',
    'models',
    'handle_error'
]

# Module level defaults
DEFAULT_REGION = "us-east-1"

# Module version and author information
__version__ = "1.0.0"
Author='Wrick Talukdar'
