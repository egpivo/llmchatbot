import logging

import bentoml
import gradio as gr
import numpy as np
from fastapi import FastAPI

from chatbot.app.model.chatter import Chatter
from chatbot.app.view import create_view
from chatbot.runner.speech2text import (
    WHISPER_MODEL,
    WHISPER_PROCESSOR,
    Speech2TextRunner,
)
from chatbot.runner.text2speech import (
    T5_MODEL,
    T5_PROCESSOR,
    T5_VOCODER,
    Text2SpeechRunner,
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

speech2text_runner = bentoml.Runner(
    runnable_class=Speech2TextRunner,
    name="speech2text",
    models=[WHISPER_PROCESSOR, WHISPER_MODEL],
)
text2speech_runner = bentoml.Runner(
    runnable_class=Text2SpeechRunner,
    name="text2speech",
    models=[T5_PROCESSOR, T5_MODEL, T5_VOCODER],
)

svc = bentoml.Service(
    name="chatbot",
    runners=[
        text2speech_runner,
        speech2text_runner,
    ],
)


@svc.api(input=bentoml.io.NumpyNdarray(), output=bentoml.io.Text())
def generate_text(speech: np.ndarray) -> str:
    text = speech2text_runner.translate.run(speech)
    return text


@svc.api(input=bentoml.io.Text(), output=bentoml.io.NumpyNdarray())
def generate_speech(text: str) -> np.ndarray:
    return text2speech_runner.translate.run(text)


chat = Chatter(generate_speech, generate_text, WHISPER_PROCESSOR, LOGGER)
app = FastAPI()
app = gr.mount_gradio_app(app, create_view(chat), path="/chatbot")
svc.mount_asgi_app(app, "/")
