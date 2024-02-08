'''
This module defines enums and a model for specifying languages and formats for subtitle translation.

The SourceLanguage and TargetLanguage enums define allowed language codes.

The SubtitleFormat enum defines allowed subtitle file formats.

The UserInput class models the user input for source/target languages and subtitle
format. It provides a from_input_data() factory method to instantiate from a dict.

Overall this provides:

- Validation of input languages and formats
- Simple access to input values from UserInput instance
- Allows easy extension of supported languages
'''


from enum import Enum


class SourceLanguage(str, Enum):
    # Source language codes
    English = "en-US"
    #other codes


class TargetLanguage(str, Enum):
    # Target language codes
    Afrikaans = "af"
    Albanian = "sq"
    Amharic = "am"
    Arabic = "ar"
    Armenian = "hy"
    Azerbaijani = "az"
    Bengali = "bn"
    Bosnian = "bs"
    Bulgarian = "bg"
    Catalan = "ca"
    Chinese_Simplified = "zh"
    Chinese_Traditional = "zh-TW"
    Croatian = "hr"
    Czech = "cs"
    Danish = "da"
    Dari = "fa-AF"
    Dutch = "nl"
    Estonian = "et"
    Farsi_Persian = "fa"
    Filipino_Tagalog = "tl"
    Finnish = "fi"
    French = "fr"
    French_Canada = "fr-CA"
    Georgian = "ka"
    German = "de"
    Greek = "el"
    Gujarati = "gu"
    Haitian_Creole = "ht"
    Hausa = "ha"
    Hebrew = "he"
    Hindi = "hi"
    Hungarian = "hu"
    Icelandic = "is"
    Indonesian = "id"
    Irish = "ga"
    Italian = "it"
    Japanese = "ja"
    Kannada = "kn"
    Kazakh = "kk"
    Korean = "ko"
    Latvian = "lv"
    Lithuanian = "lt"
    Macedonian = "mk"
    Malay = "ms"
    Malayalam = "ml"
    Maltese = "mt"
    Marathi = "mr"
    Mongolian = "mn"
    Norwegian_Bokmål = "no"
    Pashto = "ps"
    Polish = "pl"
    Portuguese_Brazil = "pt"
    Portuguese_Portugal = "pt-PT"
    Punjabi = "pa"
    Romanian = "ro"
    Russian = "ru"
    Serbian = "sr"
    Sinhala = "si"
    Slovak = "sk"
    Slovenian = "sl"
    Somali = "so"
    Spanish = "es"
    Spanish_Mexico = "es-MX"
    Swahili = "sw"
    Swedish = "sv"
    Tamil = "ta"
    Telugu = "te"
    Thai = "th"
    Turkish = "tr"
    Ukrainian = "uk"
    Urdu = "ur"
    Uzbek = "uz"
    Vietnamese = "vi"
    Welsh = "cy"


class SubtitleFormat(str, Enum):
    # Subtitle formats
    SRT = "srt"
    VTT = "vtt"

class OutputFormat(str, Enum):
    # Output formats
    TRANSCRIPT_TEXT = "transcript_text"
    TRANSLATED_TEXT = "translated_text"
    BOTH_TEXT = "both_text"
    NONE = "none"  # No output in text files

class UserInput:
    """
        Model for handling source/target languages and subtitle format configuration.

        Attributes:
        - source_language (str): Source language code.
        - target_language (str): Target language code.
        - subtitle_format (SubtitleFormat): Subtitle format object.
        - region (str): AWS region (default: 'us-east-1').
        - output_format (OutputFormat): Output format configuration (default: 'none').
        """
    # Model for source/target languages and subtitle format
    def __init__(self, source_language, target_language, subtitle_format, region='us-east-1', output_format='none'):
        """
        Initialize UserInput model.

        Args:
        - source_language (str): Source language code.
        - target_language (str): Target language code.
        - subtitle_format (SubtitleFormat): Subtitle format object.
        - region (str, optional): AWS region (default: 'us-east-1').
        - output_format (str, optional): Output format configuration (default: 'none').
        """
        # Attributes
        self.source_language = source_language
        self.target_language = target_language
        self.subtitle_format = subtitle_format
        self.region = region
        self.output_format = output_format


    @classmethod
    def from_input_data(cls, input_data):
        """
        Instantiate UserInput from a dictionary.

        Args:
        - input_data (dict): Dictionary containing input data.

        Returns:
        - UserInput: Instance of UserInput created from the input data.
        """
        # Instantiate from a dictionary
        source_language = cls.get_source_language_enum(input_data["source_language"]).value # Lookup value
        target_language = cls.get_target_language_enum(input_data["target_language"]).value # Lookup value
        subtitle_format = SubtitleFormat(input_data["subtitle_format"]) # Get from dict
        region = input_data.get("region", "us-east-1")  # Get region from input data or use default
        output_format = OutputFormat(input_data.get("output_format", OutputFormat.NONE))  # Default to NONE if not provided
        return cls(source_language, target_language, subtitle_format, region, output_format)

    @staticmethod
    def get_source_language_enum(language_code):
        """
        Get the source language enum based on the language code.

        Args:
        - language_code (str): Language code.

        Returns:
        - Enum: Source language enum.
        """
        return UserInput.get_language_enum(SourceLanguage, language_code)

    @staticmethod
    def get_target_language_enum(language_code):
        """
        Get the target language enum based on the language code.

        Args:
        - language_code (str): Language code.

        Returns:
        - Enum: Target language enum.
        """
        return UserInput.get_language_enum(TargetLanguage, language_code)

    @staticmethod
    def get_language_enum(enum_class, language_code):
        """
        Helper method to lookup a language enum by code.

        Args:
        - enum_class (Enum): Enum class to search.
        - language_code (str): Language code.

        Returns:
        - Enum: Language enum or None if not found.
        """
        # Helper method to lookup a language enum by code
        for language_enum in enum_class:
            if language_code in language_enum.value:
                return language_enum
        return None