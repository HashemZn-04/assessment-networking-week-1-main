"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...


def validate_postcode(postcode: str) -> bool:
    """Validates a given postcode."""
    postcode = postcode.replace(" ", "")
    if not isinstance(postcode, str):
        raise TypeError("Postcode must be a string!")
    if len(postcode) not in range(5, 8):
        raise ValueError(
            "Postcode of valid length (5-7 characters.)")
    return True


def get_postcode_for_location(lat: float, long: float) -> str:
    """
    Retrieves a postcode nearest to the given coordinates of 
    latitude and longitude.
    """
    url = f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"
    result = req.get(url, timeout=15)
    data = result.json()['result']
    return data[0]['postcode']


def get_postcode_completions(postcode_start: str) -> list[str]:
    pass


def get_postcodes_details(postcodes: list[str]) -> dict:
    pass


if __name__ == "__main__":
    example_postcode = get_postcode_for_location(51.507, 0.127)
    print(validate_postcode(example_postcode))
