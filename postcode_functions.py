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
    if not isinstance(postcode, str):
        raise TypeError('Function expects a string.')
    elif len(postcode) not in range(5, 8):
        return False

    postcode = postcode.replace(" ", "")
    return True


def get_postcode_for_location(lat: float, long: float) -> str:
    """
    Retrieves a postcode nearest to the given coordinates of 
    latitude and longitude.
    """
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")
    url = f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"
    result = req.get(url, timeout=15)
    data = result.json()['result']
    return data[0]['postcode']


def get_postcode_completions(postcode_start: str) -> list[str]:
    """
    Returns a list of postcodes the user may have wanted to
    use, given the starting letters of a postcode.
    """
    if not isinstance(postcode_start, str):
        raise TypeError('Function expects a string.')
    url = f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"
    result = req.get(url, timeout=15)
    data = result.json()['result']
    return data


def get_postcodes_details(postcodes: list[str]) -> dict:
    """
    Returns a dict of dicts where each dict contains one of
    the postcodes within the inputted list of postcodes, followed
    by details for that given postcode.
    """
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for postcode in postcodes:
        if not isinstance(postcode, str):
            raise TypeError("Function expects a list of strings.")
    url = f"https://api.postcodes.io/postcodes"
    postcodes = {"postcodes": postcodes}
    result = req.post(url, timeout=30, json=postcodes)
    data = result.json()
    return data


if __name__ == "__main__":
    example_postcode = get_postcode_for_location(51.507, 0.127)
    print(get_postcodes_details(['SO16 7GL', 'SO17 2LJ']))
    print(get_postcode_completions("SO16 7G"))
