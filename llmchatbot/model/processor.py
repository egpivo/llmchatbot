from typing import Callable, Optional

from transformers import Pipeline

from llmchatbot.model.utils import load_audio_data


class AudioProcessor:
    def __init__(
        self,
        audio_processor: Pipeline,
        text_generator: Callable[[str], str],
    ) -> None:
        self.processor = audio_processor
        self.text_generator = text_generator

    def process(self, audio_path: str) -> Optional[str]:
        try:
            audio_data = load_audio_data(audio_path)
            input_features = self.processor(
                audio_data["array"],
                sampling_rate=audio_data["sampling_rate"],
                return_tensors="pt",
            ).input_features
            return self.text_generator(input_features)
        except ValueError as e:
            raise ValueError(f"Please check the audio sample - {e}")


class TextProcessor:
    def process(self, text_message: str) -> Optional[str]:
        return text_message
