"""Constants for CloudFlareAi."""
# Base component constants
NAME = "CloudFlareAi"
DOMAIN = "cloudflareai"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/zhaoyi48/cloudflareai/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_ACCOUNT_ID = "username"
CONF_API_TOKEN = "password"
CONF_MODEL = "model"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_MODEL = "@cf/meta/llama-2-7b-chat-int8"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
