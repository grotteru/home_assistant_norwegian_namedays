"""Config flow for Namedays integration."""
from homeassistant import config_entries
from .const import DOMAIN


class NamedaysConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Namedays."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Opprett konfigurasjonsoppføringen
            return self.async_create_entry(title="Norwegian Namedays", data={})

        return self.async_show_form(step_id="user")