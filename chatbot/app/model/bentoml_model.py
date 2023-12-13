import bentoml

from chatbot.app.controller import (
    T5_MODEL_VERSION,
    T5_PROCESSOR_VERSION,
    T5_VOCODER_VERSION,
    WHISPER_MODEL_VERSION,
    WHISPER_PROCESSOR_VERSION,
)

VERSION = "latest"
WHISPER_PROCESSOR = bentoml.models.get(
    WHISPER_PROCESSOR_VERSION.format(version=VERSION)
)
WHISPER_MODEL = bentoml.models.get(WHISPER_MODEL_VERSION.format(version=VERSION))

T5_PROCESSOR = bentoml.models.get(T5_PROCESSOR_VERSION.format(version=VERSION))
T5_MODEL = bentoml.models.get(T5_MODEL_VERSION.format(version=VERSION))
T5_VOCODER = bentoml.models.get(T5_VOCODER_VERSION.format(version=VERSION))
