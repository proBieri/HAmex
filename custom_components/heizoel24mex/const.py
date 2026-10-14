"""Constants for the HAmex integration."""

DOMAIN = "heizoel24mex"

# API endpoints
API_LOGIN_URL = "https://www.heizoel24.de/api/account/anmelden"
API_DASHBOARD_URL = "https://www.heizoel24.de/api/customer/mex/dashboard/get"

# Configuration
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Update interval
UPDATE_INTERVAL = 3600  # 60 minutes

# Usage idle detection: report 0 L/Tag if the volume has not changed by more
# than VOLUME_CHANGE_TOLERANCE liters within USAGE_IDLE_HOURS
USAGE_IDLE_HOURS = 24
VOLUME_CHANGE_TOLERANCE = 2  # liters, absorbs sensor jitter

# Persistent storage for volume tracking
STORAGE_VERSION = 1
