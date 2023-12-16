import logging

from chatbot.model.finetune.trainer.speech2text import Speech2TextTrainer
from chatbot.model.finetune.trainer.text2speech import Text2SpeechTrainer


def execute_speech2text_training(
    t5_pretrained_model: str = "microsoft/speecht5_tts",
    t5_pretrained_vocoder: str = "microsoft/speecht5_hifigan",
    logger: logging.Logger = logging.getLogger(),
) -> None:
    speech2text_trainer = Speech2TextTrainer(
        processor_name=t5_pretrained_model,
        model_name=t5_pretrained_model,
        vocoder_name=t5_pretrained_vocoder,
        logger=logger,
    )
    speech2text_trainer.train()
    speech2text_trainer.save()


def execute_text2speech_training(
    whisper_pretrained_model: str = "openai/whisper-tiny",
    logger: logging.Logger = logging.getLogger(),
) -> None:
    text2speech_trainer = Text2SpeechTrainer(
        processor_name=whisper_pretrained_model,
        model_name=whisper_pretrained_model,
        logger=logger,
    )
    text2speech_trainer.train()
    text2speech_trainer.save()
