"""CloudflareAI API Client."""
import logging
from typing import Dict, List

import aiohttp

LOGGER = logging.getLogger(__name__)

class CloudflareaiApiClient:
    """CloudflareAI API Client."""

    def __init__(self, account_id: str, api_token: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._account_id = account_id
        self._api_token = api_token
        self._session = session
        self._api_base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    async def async_run(self, model: str, messages: List[Dict[str, str]]) -> Dict:
        """Run the AI model with given messages."""
        try:
            url = f"{self._api_base_url}{model}"
            payload = {"messages": messages}
            
            async with self._session.post(url, headers=self._headers, json=payload) as response:
                if response.status != 200:
                    LOGGER.error("API request failed with status %s", response.status)
                    return None
                return await response.json()
                
        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error("Error running CloudflareAI model: %s", error)
            return None

    async def async_test_connection(self, model: str) -> bool:
        """Test the API connection."""
        try:
            url = f"{self._api_base_url}{model}"
            async with self._session.get(url, headers=self._headers) as response:
                return response.status == 200
        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error("Error testing CloudflareAI connection: %s", error)
            return False
