from typing import Any

import bentoml
import numpy as np
import torch
from bentoml._internal.models.model import Model

from llmchatbot.model.finetune.model_loader import (
    T5_MODEL,
    T5_PROCESSOR,
    T5_VOCODER,
    WHISPER_MODEL,
    WHISPER_PROCESSOR,
)
from llmchatbot.model.utils import load_speaker_embeddings


class BasicTranslator(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(
        self,
        processor: Model,
        mode: Model,
    ) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = bentoml.transformers.load_model(processor)
        self.model = bentoml.transformers.load_model(mode)
        self.model.to(self.device)

    def translate(self) -> Any:
        return NotImplementedError


class Speech2TextTranslator(BasicTranslator):
    def __init__(
        self,
    ) -> None:
        super().__init__(WHISPER_PROCESSOR, WHISPER_MODEL)

    @bentoml.Runnable.method(batchable=False)
    def translate(self, audio_data: np.ndarray) -> str:
        if audio_data is not None:
            predicted_ids = self.model.generate(audio_data)
            transcriptions = self.processor.batch_decode(
                predicted_ids, skip_special_tokens=True
            )
            transcription = transcriptions[0]
            return transcription


class Text2SpeechTranslator(BasicTranslator):
    def __init__(self) -> None:
        super().__init__(T5_PROCESSOR, T5_MODEL)
        self.vocoder = bentoml.transformers.load_model(T5_VOCODER)
        self.speaker_embeddings = load_speaker_embeddings()

        self.speaker_embeddings.to(self.device)
        self.vocoder.to(self.device)

    @bentoml.Runnable.method(batchable=False)
    def translate(self, text: str) -> np.ndarray:
        inputs = self.processor(text=text, return_tensors="pt").to(self.device)
        speech = self.model.generate_speech(
            inputs["input_ids"],
            self.speaker_embeddings,
            vocoder=self.vocoder,
        )
        return speech.cpu().numpy()
