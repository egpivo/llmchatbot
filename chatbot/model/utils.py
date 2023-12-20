import torch
from datasets import Audio, Dataset, load_dataset

from chatbot.model import PLAYBACK_SAMPLE_RATE


def load_speaker_embeddings() -> torch.Tensor:
    embeddings = load_dataset(
        "Matthijs/cmu-arctic-xvectors",
        split="validation",
    )
    speaker_tensor = torch.tensor(embeddings[7306]["xvector"])
    return speaker_tensor.unsqueeze(0)


def load_audio_data(audio_path: str) -> dict:
    audio_dataset = Dataset.from_dict({"audio": [audio_path]}).cast_column(
        "audio", Audio(sampling_rate=PLAYBACK_SAMPLE_RATE)
    )
    return audio_dataset[0]["audio"]
