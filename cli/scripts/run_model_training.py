import argparse
import logging
from argparse import ArgumentParser

from dotenv import load_dotenv

from chatbot.model.finetune.executor import (
    execute_speech2text_training,
    execute_text2speech_training,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)


def fetch_args() -> argparse.Namespace:
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--t5_pretrained_model",
        type=str,
        dest="t5_pretrained_model",
        default="microsoft/speecht5_tts",
        help="Speech-to-text pretrained model",
    )
    arg_parser.add_argument(
        "--t5_pretrained_vocoder",
        type=str,
        dest="t5_pretrained_vocoder",
        default="microsoft/speecht5_hifigan",
        help="Speech-to-text pretrained Vocoder",
    )
    arg_parser.add_argument(
        "--whisper_pretrained_model",
        type=str,
        dest="whisper_pretrained_model",
        default="openai/whisper-tiny",
        help="Text-to-speech pretrained model",
    )
    return arg_parser.parse_args()


if __name__ == "__main__":
    logger = logging.getLogger()
    arguments = fetch_args()
    execute_speech2text_training(
        t5_pretrained_model=arguments.t5_pretrained_model,
        t5_pretrained_vocoder=arguments.t5_pretrained_vocoder,
        logger=logger,
    )
    execute_text2speech_training(
        whisper_pretrained_model=arguments.whisper_pretrained_model, logger=logger
    )
