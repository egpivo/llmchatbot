import os
from unittest.mock import MagicMock, patch

import pytest

from chatbot.app.view.utils import set_openai_api_key


@pytest.fixture
def mock_os_environ():
    with patch.dict("os.environ", {"OPENAI_API_KEY": ""}):
        yield


@patch("chatbot.app.view.utils.load_chainer")
def test_set_openai_api_key(mock_load_chainer):
    mock_chain = MagicMock()
    mock_load_chainer.return_value = mock_chain

    result = set_openai_api_key(api_key="test")

    assert os.environ["OPENAI_API_KEY"] == ""
    mock_load_chainer.assert_called_once_with(api_key="test", tool_names=["wikipedia"])
    assert result == mock_chain
