"""CloudflareAI entity class."""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import (
    ATTRIBUTION,
    DOMAIN,
    NAME,
    VERSION,
)


class CloudflareaiEntity(CoordinatorEntity):
    """CloudflareAI entity class."""

    _attr_has_entity_name = True

    def __init__(self, client, config_entry) -> None:
        """Initialize the entity."""
        super().__init__(client)
        self.config_entry = config_entry
        self.entity_id = f"{DOMAIN}.{config_entry.entry_id}"

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}"

    @property
    def device_info(self) -> dict:
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": "Cloudflare",
            "entry_type": DeviceEntryType.SERVICE,
        }

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
            "account_id": self.config_entry.data.get("username"),
            "model": self.config_entry.data.get("model"),
        }
