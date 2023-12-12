import logging


class BasicTrainer:
    def __init__(self, processor_name: str, model_name: str, logger: logging.Logger):
        self.processor_name = processor_name
        self.model_name = model_name
        self.logger = logger

    def train(self) -> None:
        return NotImplementedError

    def save(self) -> None:
        return NotImplementedError
