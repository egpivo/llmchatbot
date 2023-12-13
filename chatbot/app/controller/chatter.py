import logging
from dataclasses import astuple
from threading import Lock
from typing import Any, Callable, List, Optional, Tuple

import bentoml
from bentoml._internal.models.model import Model
from langchain.chains import ConversationChain

from chatbot.app.model import PLAYBACK_SAMPLE_RATE
from chatbot.app.model.data import ChatterOutput
from chatbot.app.model.processor import AudioProcessor, TextProcessor

DEFAULT_RESPONSE = "To use this feature, please paste your OpenAI API key."


def set_openai_key(api_key: str) -> None:
    import openai

    openai.api_key = api_key if api_key else ""


class Chatter:
    def __init__(
        self,
        speech_generator: Callable[[str], bytes],
        text_generator: Callable[[str], str],
        processor_reference: Model,
        logger: logging.Logger,
    ) -> None:
        self.lock = Lock()
        self.speech_generator = speech_generator
        self.text_generator = text_generator
        self.processor = bentoml.transformers.load_model(processor_reference)
        self.logger = logger

        self.audio_processor = AudioProcessor(self.processor, self.text_generator)
        self.text_processor = TextProcessor()

    def __call__(
        self,
        openai_api_key: str,
        audio_path: Optional[str],
        text_message: str,
        history: Optional[Tuple[str, str]],
        chainer: Optional[ConversationChain],
    ) -> Tuple[Any]:
        history = history or []
        chatter_output = ChatterOutput(history, history)
        with self.lock:
            try:
                transcription = (
                    self.audio_processor.process(audio_path)
                    if audio_path
                    else self.text_processor.process(text_message)
                )

                chatter_output = self._generate_chatter_output(
                    openai_api_key=openai_api_key,
                    chainer=chainer,
                    transcription=transcription,
                    history=history,
                )
            except Exception as e:
                self.logger.error(
                    f"[Chatter] Generation error - {type(e).__name__} - {e}"
                )
        return astuple(chatter_output)

    def _generate_chatter_output(
        self,
        openai_api_key: str,
        chainer: Optional[ConversationChain],
        transcription: str,
        history: List[Tuple[str, str]],
    ) -> ChatterOutput:
        """
        Generate ChatterOutput based on the given parameters.

        Args:
            openai_api_key (str): OpenAI API key.
            chainer (Optional[ConversationChain]): ConversationChain instance.
            transcription (str): Transcription of the input.
            history (List[Tuple[str, str]]): List of conversation history.

        Returns:
            ChatterOutput: Resulting ChatterOutput object.
        """
        if chainer:
            set_openai_key(openai_api_key)
            response = chainer.run(input=transcription)
        else:
            response = DEFAULT_RESPONSE
        new_history = (transcription, response)
        history.append(new_history)
        speech = (PLAYBACK_SAMPLE_RATE, self.speech_generator(response))
        return ChatterOutput(history, history, speech)
