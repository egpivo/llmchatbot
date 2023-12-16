import logging
import os

from chatbot.model.finetune import SPEECH2TEXT_CANDIDATES, TEXT2SPEECH_CANDIDATES
from chatbot.model.finetune.executor import (
    execute_speech2text_training,
    execute_text2speech_training,
)


def check_and_finetune_models(model_path: str, logger: logging) -> None:
    if not os.path.isdir(model_path):
        logger.error(
            f"All models not found in {model_path}! Rerunning model fine-tuning."
        )
        execute_speech2text_training(logger=logger)
        execute_text2speech_training(logger=logger)
        return

    is_normal = True

    def check_and_train(candidate_list, model_type):
        for candidate in candidate_list:
            candidate_path = os.path.join(model_path, candidate)
            if not os.path.isdir(candidate_path):
                os.mkdir(candidate_path)
                logger.error(
                    f"Model {candidate} not found! Rerunning {model_type} fine-tuning."
                )
                return False
        return True

    is_normal &= check_and_train(SPEECH2TEXT_CANDIDATES, "speech2text")
    is_normal &= check_and_train(TEXT2SPEECH_CANDIDATES, "text2speech")

    if is_normal:
        logger.info("All models have been checked.")
