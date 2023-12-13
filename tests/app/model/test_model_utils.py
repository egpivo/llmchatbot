from pathlib import Path

import numpy
import pytest
import torch

from chatbot.app.model.utils import load_audio_data, load_speaker_embeddings

FIXTURE_DIR = Path(__file__).parent.resolve() / "_fixture_files"


@pytest.fixture
def sample_audio_data():
    return f"{FIXTURE_DIR}/test.wav"


def test_load_speaker_embeddings():
    embeddings = load_speaker_embeddings()
    assert isinstance(embeddings, torch.Tensor)
    assert len(embeddings.shape) == 2


def test_load_audio_data(sample_audio_data):
    audio_data = load_audio_data(sample_audio_data)
    assert isinstance(audio_data, dict)
    assert "array" in audio_data and "sampling_rate" in audio_data
    assert isinstance(audio_data["array"], numpy.ndarray)
    assert audio_data["array"].shape[0] == 56320
