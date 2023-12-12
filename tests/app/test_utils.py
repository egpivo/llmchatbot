import os
from unittest.mock import MagicMock, patch

import pytest

from chatbot.app.utils import set_openai_api_key


@pytest.fixture
def mock_os_environ():
    with patch.dict("os.environ", {"OPENAI_API_KEY": ""}):
        yield


@patch("chatbot.app.utils.load_chain")
def test_set_openai_api_key(mock_load_chain):
    mock_chain = MagicMock()
    mock_load_chain.return_value = mock_chain

    result = set_openai_api_key(api_key="test")

    assert os.environ["OPENAI_API_KEY"] == ""
    mock_load_chain.assert_called_once_with(api_key="test", tool_names=["wikipedia"])
    assert result == mock_chain
