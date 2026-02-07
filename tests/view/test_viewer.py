"""Viewer tests require gradio (and thus FastAPI) to be importable.

When the lockfile pulls an old FastAPI built for Pydantic v1 alongside Pydantic v2
(e.g. due to bentoml 1.0.18 pinning starlette <0.26), gradio cannot be imported.
Skip this module in that case so the rest of the test suite can run.
"""
from unittest.mock import MagicMock

import pytest

try:
    import gradio as gr
    from llmchatbot.controller.chatter import Chatter
    from llmchatbot.view.viewer import ChatbotViewer
except (ImportError, Exception):
    pytest.skip(
        "gradio/viewer not importable (FastAPI–Pydantic v2 mismatch in this env)",
        allow_module_level=True,
    )


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
