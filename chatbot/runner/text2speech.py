import bentoml
import numpy as np
import torch
from datasets import Dataset, load_dataset

from chatbot.runner import T5_MODEL_VERSION, T5_PROCESSOR_VERSION, T5_VOCODER_VERSION
from chatbot.runner.basic import BasicRunner

VERSION = "latest"
T5_PROCESSOR = bentoml.models.get(T5_PROCESSOR_VERSION.format(version=VERSION))
T5_MODEL = bentoml.models.get(T5_MODEL_VERSION.format(version=VERSION))
T5_VOCODER = bentoml.models.get(T5_VOCODER_VERSION.format(version=VERSION))


def load_embeddings() -> Dataset:
    return load_dataset(
        "Matthijs/cmu-arctic-xvectors",
        split="validation",
    )


class Text2SpeechRunner(BasicRunner):
    def __init__(self) -> None:
        super().__init__(T5_PROCESSOR, T5_MODEL)
        self.vocoder = bentoml.transformers.load_model(T5_VOCODER)
        self.embeddings = load_embeddings()
        self.speaker_embeddings = torch.tensor(
            self.embeddings[7306]["xvector"]
        ).unsqueeze(0)
        self.vocoder.to(self.device)

    @bentoml.Runnable.method(batchable=False)
    def translate(self, text: str) -> np.ndarray:
        inputs = self.processor(text=text, return_tensors="pt")
        speech = self.model.generate_speech(
            inputs["input_ids"].to(self.device),
            self.speaker_embeddings.to(self.device),
            vocoder=self.vocoder,
        )
        return speech.cpu().numpy()
