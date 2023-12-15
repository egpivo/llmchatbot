from unittest.mock import MagicMock

import gradio as gr
import pytest

from chatbot.controller.chatter import Chatter
from chatbot.view.viewer import ChatbotViewer


@pytest.fixture
def mock_chatter():
    return MagicMock(spec=Chatter)


def test_create_view(mock_chatter):
    viewer = ChatbotViewer(chatter=mock_chatter)
    assert isinstance(viewer.block, gr.Blocks)
    assert isinstance(viewer.state, gr.State)
    assert isinstance(viewer.agent_state, gr.State)


def test_get_view(mock_chatter):
    viewer = ChatbotViewer(chatter=mock_chatter)
    view = viewer.get_view()
    assert isinstance(view, gr.Blocks)
