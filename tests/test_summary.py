import pytest
from unittest.mock import patch, MagicMock
from analysis.summary import get_ai_summary

@patch("analysis.summary.st")
def test_get_ai_summary_no_api_key(mock_st):
    # Simulate missing API key
    mock_st.secrets.get.return_value = None
    
    result = get_ai_summary("Some analysis text")
    assert result is None

@patch("analysis.summary.requests.post")
@patch("analysis.summary.st")
def test_get_ai_summary_groq_success(mock_st, mock_post):
    # Setup secrets
    mock_st.secrets.get.side_effect = lambda key: "groq_key" if key == "GROQ_API_KEY" else "hf_key"
    
    # Mock successful Groq response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Groq summary"}}]
    }
    mock_post.return_value = mock_response
    
    result = get_ai_summary("test")
    assert result == "Groq summary"
    # Verify it called Groq endpoint
    assert mock_post.call_args[0][0] == "https://api.groq.com/openai/v1/chat/completions"

@patch("analysis.summary.requests.post")
@patch("analysis.summary.st")
def test_get_ai_summary_groq_fails_hf_success(mock_st, mock_post):
    # Setup secrets
    mock_st.secrets.get.side_effect = lambda key: "groq_key" if key == "GROQ_API_KEY" else "hf_key"
    
    # First call (Groq) fails, second (HF) succeeds
    mock_response_fail = MagicMock()
    mock_response_fail.raise_for_status.side_effect = Exception("Groq error")
    
    mock_response_success = MagicMock()
    mock_response_success.json.return_value = {
        "choices": [{"message": {"content": "HF fallback summary"}}]
    }
    
    mock_post.side_effect = [mock_response_fail, mock_response_success]
    
    result = get_ai_summary("test")
    assert result == "HF fallback summary"
    assert mock_post.call_count == 2
    assert mock_post.call_args_list[1][0][0] == "https://router.huggingface.co/v1/chat/completions"

@patch("analysis.summary.requests.post")
@patch("analysis.summary.st")
def test_get_ai_summary_all_fail(mock_st, mock_post):
    mock_st.secrets.get.return_value = "some_key"
    mock_post.side_effect = Exception("All fail")
    
    result = get_ai_summary("test")
    assert result is None
