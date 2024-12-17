"""Namedays integration init."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .coordinator import NamedaysUpdateCoordinator
from .const import DOMAIN

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Namedays from a config entry."""
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    coordinator = NamedaysUpdateCoordinator(hass, session)

    # Lagre koordinatoren i hass.data for senere bruk
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Start datainnhentingen i koordinatoren
    await coordinator.async_config_entry_first_refresh()

    # Forward oppsett for plattformene (sensor i dette tilfellet)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
