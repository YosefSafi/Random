import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from nexustask.plugins.jira_sync.plugin import JiraSyncPlugin

@pytest.mark.asyncio
async def test_sync_task_success():
    plugin = JiraSyncPlugin(api_key="secret", url="https://jira.example.com")
    
    with patch("nexustask.plugins.jira_sync.plugin.httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_client_instance.post.return_value = mock_response
        MockClient.return_value.__aenter__.return_value = mock_client_instance
        
        result = await plugin.sync_task("task-123")
        assert result is True
        mock_client_instance.post.assert_called_once()

@pytest.mark.asyncio
async def test_sync_task_failure():
    plugin = JiraSyncPlugin(api_key="secret", url="https://jira.example.com")
    
    with patch("nexustask.plugins.jira_sync.plugin.httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_client_instance.post.return_value = mock_response
        MockClient.return_value.__aenter__.return_value = mock_client_instance
        
        result = await plugin.sync_task("task-123")
        assert result is False
