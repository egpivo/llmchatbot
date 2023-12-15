import logging

import bentoml
from transformers import SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Processor

from chatbot.model.finetune import T5_MODEL_NAME, T5_PROCESSOR_NAME, T5_VOCODER_NAME
from chatbot.model.finetune.trainer.basic import BasicTrainer


class Speech2TextTrainer(BasicTrainer):
    t5_processor = None
    t5_model = None
    t5_vocoder = None

    def __init__(
        self,
        processor_name: str,
        model_name: str,
        vocoder_name: str,
        logger: logging.Logger,
    ):
        super().__init__(processor_name, model_name, logger)
        self.processor_name = processor_name
        self.model_name = model_name
        self.vocoder_name = vocoder_name

    def train(self):
        self.t5_processor = SpeechT5Processor.from_pretrained(self.processor_name)
        self.t5_model = SpeechT5ForTextToSpeech.from_pretrained(self.model_name)
        self.t5_vocoder = SpeechT5HifiGan.from_pretrained(self.vocoder_name)

    def save(self):
        saved_t5_processor = bentoml.transformers.save_model(
            T5_PROCESSOR_NAME, self.t5_processor
        )
        self.logger.info(f"Saved: {saved_t5_processor}")
        saved_t5_model = bentoml.transformers.save_model(
            T5_MODEL_NAME,
            self.t5_model,
            signatures={"generate_speech": {"batchable": False}},
        )
        self.logger.info(f"Saved: {saved_t5_model}")
        saved_t5_vocoder = bentoml.transformers.save_model(
            T5_VOCODER_NAME, self.t5_vocoder
        )
        self.logger.info(f"Saved: {saved_t5_vocoder}")
