"""
Strava API integration package.

This package provides a comprehensive interface for interacting with the Strava API,
including activity management, authentication, and data models.
"""

# Re-export main classes and functions for convenient imports
# from .models import StravaConfig, StravaPost
from .client import StravaAPIClient

__all__ = [
    # "StravaConfig",
    # "StravaPost", 
    "StravaAPIClient",
]

__version__ = "0.1.0"
