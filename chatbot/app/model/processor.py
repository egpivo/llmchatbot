from typing import Callable, Optional

from datasets import Audio, Dataset
from transformers import Pipeline

from chatbot.app.model import PLAYBACK_SAMPLE_RATE


class AudioProcessor:
    def __init__(
        self,
        audio_processor: Pipeline,
        text_generator: Callable[[str], str],
    ) -> None:
        self.processor = audio_processor
        self.text_generator = text_generator

    def process(self, audio_path) -> Optional[str]:
        audio_dataset = Dataset.from_dict({"audio": [audio_path]}).cast_column(
            "audio", Audio(sampling_rate=PLAYBACK_SAMPLE_RATE)
        )
        sample = audio_dataset[0]["audio"]
        try:
            input_features = self.processor(
                sample["array"],
                sampling_rate=sample["sampling_rate"],
                return_tensors="pt",
            ).input_features
            return self.text_generator(input_features)
        except ValueError as e:
            raise ValueError(f"Please check the audio sample - {e}")


class TextProcessor:
    def process(self, text_message: str) -> Optional[str]:
        return text_message
