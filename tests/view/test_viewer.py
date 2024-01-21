from unittest.mock import MagicMock

import gradio as gr
import pytest

from llmchatbot.controller.chatter import Chatter
from llmchatbot.view.viewer import ChatbotViewer


@pytest.fixture
def mock_chatter():
    return MagicMock(spec=Chatter)


def test_create_view(mock_chatter):
    viewer = ChatbotViewer(chatter=mock_chatter)
    assert isinstance(viewer.block, gr.Blocks)


def test_create_layout(mock_chatter):
    layout = ChatbotViewer._create_layout()
    assert isinstance(layout, tuple)
    assert len(layout) == 5
    for component in layout:
        assert isinstance(component, gr.components.Component)


def test_get_view(mock_chatter):
    viewer = ChatbotViewer(chatter=mock_chatter)
    view = viewer.get_view()
    assert isinstance(view, gr.Blocks)
