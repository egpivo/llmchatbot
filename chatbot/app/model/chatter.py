import logging
from dataclasses import astuple
from threading import Lock
from typing import Any, Callable, List, Optional, Tuple

import bentoml
from bentoml._internal.models.model import Model
from langchain.chains import ConversationChain

from chatbot.app.model import PLAYBACK_SAMPLE_RATE
from chatbot.app.model.chatter_output import ChatterOutput
from chatbot.app.model.processor import AudioProcessor, TextProcessor


def set_openai_key(api_key: str) -> None:
    import openai

    openai.api_key = api_key if api_key else ""


def generate_default_response(
    history: List[Tuple[str, str]],
    transcription: str,
    speech_generator: Callable[[str], bytes],
) -> ChatterOutput:
    response = "To use this feature, please paste your OpenAI API key."
    history.append((transcription, response))
    speech = (PLAYBACK_SAMPLE_RATE, speech_generator(response))
    return ChatterOutput(history, history, speech)


def run_conversation_chain(
    api_key: str,
    chain: ConversationChain,
    transcription: str,
    history: List[Tuple[str, str]],
    speech_generator: Callable[[str], bytes],
) -> ChatterOutput:
    set_openai_key(api_key)
    output = chain.run(input=transcription)
    speech = (PLAYBACK_SAMPLE_RATE, speech_generator(output))
    history.append((transcription, output))
    return ChatterOutput(history, history, speech)


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
        api_key: str,
        audio_path: Optional[str],
        text_message: str,
        history: Optional[Tuple[str, str]],
        chain: Optional[ConversationChain],
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

                chatter_output = (
                    generate_default_response(
                        history=history,
                        transcription=transcription,
                        speech_generator=self.speech_generator,
                    )
                    if chain is None
                    else run_conversation_chain(
                        api_key=api_key,
                        chain=chain,
                        transcription=transcription,
                        history=history,
                        speech_generator=self.speech_generator,
                    )
                )
            except Exception as e:
                self.logger.error(
                    f"[Chatter] Generation error - {type(e).__name__} - {e}"
                )
        return astuple(chatter_output)
