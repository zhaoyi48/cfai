"""
Custom integration to integrate CloudFlareAi with Home Assistant.

For more details about this integration, please refer to
https://github.com/zhaoyi48/cloudflareai
"""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import config_validation as cv

from .api import CloudflareaiApiClient
from .const import CONF_API_TOKEN
from .const import CONF_ACCOUNT_ID
from .const import DOMAIN
from .const import PLATFORMS
from .const import STARTUP_MESSAGE
from .const import CONF_MODEL
from .const import DEFAULT_MODEL

_LOGGER: logging.Logger = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATFORMS = (Platform.CONVERSATION,)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CloudflareAI from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    account_id = entry.data.get(CONF_ACCOUNT_ID)
    api_token = entry.data.get(CONF_API_TOKEN)
    model = entry.data.get(CONF_MODEL, DEFAULT_MODEL)

    session = async_get_clientsession(hass)
    client = CloudflareaiApiClient(account_id, api_token, session)

    try:
        async with asyncio.timeout(10):
            if not await client.async_test_connection(model):
                raise ConfigEntryNotReady("Failed to connect to Cloudflare AI API")
    except Exception as err:
        raise ConfigEntryNotReady(f"Error connecting to Cloudflare AI API: {err}") from err

    hass.data[DOMAIN][entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True



async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if not await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        return False
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
