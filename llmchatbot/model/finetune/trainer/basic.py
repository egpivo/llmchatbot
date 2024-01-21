import logging
from abc import ABC, abstractmethod


class BasicTrainer(ABC):
    def __init__(self, processor_name: str, model_name: str, logger: logging.Logger):
        self.processor_name = processor_name
        self.model_name = model_name
        self.logger = logger

    @abstractmethod
    def train(self):
        return NotImplementedError(
            "train method must be implemented in derived classes"
        )

    @abstractmethod
    def save(self):
        return NotImplementedError("save method must be implemented in derived classes")
