import bentoml
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from llmchatbot.model.finetune import WHISPER_MODEL_NAME, WHISPER_PROCESSOR_NAME
from llmchatbot.model.finetune.trainer.basic import BasicTrainer


class Text2SpeechTrainer(BasicTrainer):
    whisper_processor = None
    whisper_model = None

    def train(self):
        self.whisper_processor = WhisperProcessor.from_pretrained(self.processor_name)
        self.whisper_model = WhisperForConditionalGeneration.from_pretrained(
            self.model_name
        )
        self.whisper_model.config.forced_decoder_ids = None

    def save(self):
        saved_whisper_processor = bentoml.transformers.save_model(
            WHISPER_PROCESSOR_NAME,
            self.whisper_processor,
        )
        self.logger.info(f"Saved: {saved_whisper_processor}")

        saved_whisper_model = bentoml.transformers.save_model(
            WHISPER_MODEL_NAME,
            self.whisper_model,
        )
        self.logger.info(f"Saved: {saved_whisper_model}")
