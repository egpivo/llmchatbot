import torch
from datasets import load_dataset


def load_speaker_embeddings() -> torch.Tensor:
    embeddings = load_dataset(
        "Matthijs/cmu-arctic-xvectors",
        split="validation",
    )
    speaker_tensor = torch.tensor(embeddings[7306]["xvector"])
    return speaker_tensor.unsqueeze(0)
