import bentoml
import numpy as np
import torch
from datasets import load_dataset

from chatbot.runner import T5_MODEL_VERSION, T5_PROCESSOR_VERSION, T5_VOCODER_VERSION
from chatbot.runner.basic import BasicRunner

VERSION = "latest"
T5_PROCESSOR = bentoml.models.get(T5_PROCESSOR_VERSION.format(version=VERSION))
T5_MODEL = bentoml.models.get(T5_MODEL_VERSION.format(version=VERSION))
T5_VOCODER = bentoml.models.get(T5_VOCODER_VERSION.format(version=VERSION))


def load_speaker_embeddings() -> torch.Tensor:
    embeddings = load_dataset(
        "Matthijs/cmu-arctic-xvectors",
        split="validation",
    )
    speaker_tensor = torch.tensor(embeddings[7306]["xvector"])
    return speaker_tensor.unsqueeze(0)


class Text2SpeechRunner(BasicRunner):
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
