import argparse
import logging
import os
import sys
from argparse import ArgumentParser

from dotenv import find_dotenv, load_dotenv

from chatbot.exit_code import ExitCode
from chatbot.model.finetune.executor import (
    execute_speech2text_training,
    execute_text2speech_training,
)
from chatbot.utils import check_and_finetune_models

dotenv_file = find_dotenv("envs/.env")
load_dotenv(dotenv_file)

logging.basicConfig(level=logging.INFO)


def fetch_args() -> argparse.Namespace:
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--is_retraining",
        action="store_true",
        dest="is_retraining",
        help="Retrain all models",
    )
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
    model_path = os.path.join(os.getenv("BENTOML_HOME"), "models")
    status = check_and_finetune_models(model_path, logger)

    if arguments.is_retraining:
        status = 0
        logger.info("Retraining speech2text models")
        status += execute_speech2text_training(
            t5_pretrained_model=arguments.t5_pretrained_model,
            t5_pretrained_vocoder=arguments.t5_pretrained_vocoder,
            logger=logger,
        )
        logger.info("Retraining text2speech models")
        status += execute_text2speech_training(
            whisper_pretrained_model=arguments.whisper_pretrained_model, logger=logger
        )

    EXIT_CODE = (
        status
        if status == ExitCode.SUCCESS.value
        else ExitCode.MODEL_TRAINING_ERROR.value
    )

    sys.exit(EXIT_CODE)
