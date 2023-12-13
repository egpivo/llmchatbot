from typing import Any

import bentoml
import torch
from bentoml._internal.models.model import Model


class BasicTranslator(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(
        self,
        processor: Model,
        mode: Model,
    ) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = bentoml.transformers.load_model(processor)
        self.model = bentoml.transformers.load_model(mode)
        self.model.to(self.device)

    def translate(self) -> Any:
        return NotImplementedError
