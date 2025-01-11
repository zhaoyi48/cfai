"""Adds config flow for CloudFlareAi."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CloudflareaiApiClient
from .const import (
    CONF_ACCOUNT_ID,
    CONF_API_TOKEN,
    CONF_MODEL,
    DEFAULT_MODEL,
    DOMAIN,
    PLATFORMS,
)


class CloudflareaiFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for cloudflareai."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_ACCOUNT_ID],
                user_input[CONF_API_TOKEN],
                user_input.get(CONF_MODEL, DEFAULT_MODEL)
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_ACCOUNT_ID],
                    data=user_input
                )
            self._errors["base"] = "auth"

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CloudflareaiOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        if user_input is None:
            user_input = {}
            
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ACCOUNT_ID, default=user_input.get(CONF_ACCOUNT_ID, "")): str,
                    vol.Required(CONF_API_TOKEN, default=user_input.get(CONF_API_TOKEN, "")): str,
                    vol.Optional(CONF_MODEL, default=user_input.get(CONF_MODEL, DEFAULT_MODEL)): str,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, account_id: str, api_token: str, model: str) -> bool:
        """Test if credentials are valid."""
        try:
            session = async_get_clientsession(self.hass)
            client = CloudflareaiApiClient(account_id, api_token, session)
            return await client.async_test_connection(model)
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class CloudflareaiOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for cloudflareai."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_MODEL,
                        default=self.config_entry.options.get(CONF_MODEL, DEFAULT_MODEL)
                    ): str,
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_ACCOUNT_ID), data=self.options
        )
