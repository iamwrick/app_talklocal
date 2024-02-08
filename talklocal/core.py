import asyncio
import argparse
from talklocal.main import process_request
from talklocal.models import UserInput


async def main(user_input):
    """
    Async function to initiate the processing of a user input for transcript generation.

    Args:
    - user_input (UserInput): UserInput object containing source/target languages and other configurations.
    """
    await process_request(user_input)


if __name__ == "__main__":
    # Create argument parser to accept command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-language", type=str, required=True)
    parser.add_argument("--target-language", type=str, required=True)
    parser.add_argument("--subtitle-format", type=str, required=False)
    parser.add_argument("--aws-region", type=str, required=False)
    parser.add_argument("--output_format", type=str, required=False)

    # Parse command-line arguments
    args = parser.parse_args()

    # Create a UserInput object based on command-line arguments
    user_input = UserInput(
        source_language=args.source_language,
        target_language=args.target_language,
        subtitle_format=args.subtitle_format,
        region=args.aws_region,
        output_format=args.output_format
    )

    # Run the main function asynchronously, passing the UserInput object
    asyncio.run(main(user_input))