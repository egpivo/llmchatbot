import argparse
import logging
from argparse import ArgumentParser

from chatbot.trainer.speech2text import Speech2TextTrainer
from chatbot.trainer.text2speech import Text2SpeechTrainer

logging.basicConfig(level=logging.INFO)


def fetch_args() -> argparse.Namespace:
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        name_or_flags="--t5_pretrained_model",
        type=str,
        dest="t5_pretrained_model",
        default="microsoft/speecht5_tts",
        help="Speech-to-text pretrained model",
    )
    arg_parser.add_argument(
        name_or_flags="--t5_pretrained_vocoderl",
        type=str,
        dest="t5_pretrained_vocoderl",
        default="microsoft/speecht5_hifigan",
        help="Speech-to-text pretrained Vocoder",
    )
    arg_parser.add_argument(
        name_or_flags="--whisper_pretrained_model",
        type=str,
        dest="whisper_pretrained_model",
        default="openai/whisper-tiny",
        help="Text-to-speech pretrained model",
    )
    return arg_parser.parse_args()


def run_training_job(args: argparse.Namespace) -> None:
    logger = logging.getLogger()

    speech2text_trainer = Speech2TextTrainer(
        processor_name=args.t5_pretrained_model,
        model_name=args.t5_pretrained_model,
        vocoder_name=args.t5_pretrained_vocoderl,
        logger=logger,
    )
    speech2text_trainer.train()
    speech2text_trainer.save()

    text2speech_trainer = Text2SpeechTrainer(
        processor_name=args.whisper_pretrained_model,
        model_name=args.whisper_pretrained_model,
        logger=logger,
    )
    text2speech_trainer.train()
    text2speech_trainer.save()


if __name__ == "__main__":
    arguments = fetch_args()
    run_training_job(arguments)
