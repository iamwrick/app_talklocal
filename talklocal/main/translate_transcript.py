import boto3
from talklocal.handle_error import ErrorHandler


class Translate:
    def __init__(self, region_name="us-east-1"):
        '''Creates boto3 translate client for given region'''
        self.region_name = region_name
        self.translate_client = boto3.client("translate", region_name=region_name)

    def translate_text(self, text, source_language_code, target_language_code, region_name=None,
                       profanity_check=False, brevity_check=False):
        '''Translates text from source language to target language

                Args:
                    text: Text to translate
                    source_language_code: Source language code
                    target_language_code: Target language code
                    profanity_check: Enable profanity filtering
                    brevity_check: Enable brevity translation check

                Returns:
                    str: Translated text
        '''
        settings = {}

        if profanity_check:
            settings["Profanity"] = "MASK"

        if brevity_check:
            settings["Brevity"] = "ON"

        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code,
                Settings=settings,
            )
            return response["TranslatedText"]
        except Exception as e:
            raise ErrorHandler.TranslationError(f"Translation error: {e}")
