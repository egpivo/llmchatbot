import bentoml

from llmchatbot.model.finetune import (
    T5_MODEL_NAME,
    T5_PROCESSOR_NAME,
    T5_VOCODER_NAME,
    WHISPER_MODEL_NAME,
    WHISPER_PROCESSOR_NAME,
)

# Model path
VERSION = "latest"

T5_PROCESSOR_VERSION = f"{T5_PROCESSOR_NAME}:{VERSION}"
T5_MODEL_VERSION = f"{T5_MODEL_NAME}:{VERSION}"
T5_VOCODER_VERSION = f"{T5_VOCODER_NAME}:{VERSION}"

WHISPER_PROCESSOR_VERSION = f"{WHISPER_PROCESSOR_NAME}:{VERSION}"
WHISPER_MODEL_VERSION = f"{WHISPER_MODEL_NAME}:{VERSION}"

# BentoML models
T5_PROCESSOR = bentoml.models.get(T5_PROCESSOR_VERSION)
T5_MODEL = bentoml.models.get(T5_MODEL_VERSION)
T5_VOCODER = bentoml.models.get(T5_VOCODER_VERSION)

WHISPER_PROCESSOR = bentoml.models.get(WHISPER_PROCESSOR_VERSION)
WHISPER_MODEL = bentoml.models.get(WHISPER_MODEL_VERSION)
