import bentoml
import numpy as np

from chatbot.runner import WHISPER_MODEL_VERSION, WHISPER_PROCESSOR_VERSION
from chatbot.runner.basic import BasicRunner

VERSION = "latest"
WHISPER_PROCESSOR = bentoml.models.get(
    WHISPER_PROCESSOR_VERSION.format(version=VERSION)
)
WHISPER_MODEL = bentoml.models.get(WHISPER_MODEL_VERSION.format(version=VERSION))


class Speech2TextRunner(BasicRunner):
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
