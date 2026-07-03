"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def validate_postcode(postcode: str) -> bool:
    """Validates a given postcode."""
    if not isinstance(postcode, str):
        raise TypeError('Function expects a string.')
    cache = load_cache()
    if postcode in cache and 'valid' in cache[postcode]:
        return cache[postcode]['valid']
    else:
        url = f"https://api.postcodes.io/postcodes/{postcode}/validate"
        try:
            result = req.get(url, timeout=15)
            result.raise_for_status()
        except req.exceptions.HTTPError as e:
            status = e.response.status_code
            if 500 <= status < 600:
                raise req.RequestException('Unable to access API.')
        cache[postcode] = {"valid": result.json()['result']}
        save_cache(cache)
        return result.json()['result']


def get_postcode_for_location(lat: float, long: float) -> str:
    """
    Retrieves a postcode nearest to the given coordinates of 
    latitude and longitude.
    """
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")
    url = f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"
    try:
        result = req.get(url, timeout=15)
        result.raise_for_status()
    except req.exceptions.HTTPError as e:
        status = e.response.status_code
        if 500 <= status < 600:
            raise req.RequestException('Unable to access API.')
    data = result.json()['result']
    if data is None:
        raise ValueError("No relevant postcode found.")
    return data[0]['postcode']


def get_postcode_completions(postcode_start: str) -> list[str]:
    """
    Returns a list of postcodes the user may have wanted to
    use, given the starting letters of a postcode.
    """
    if not isinstance(postcode_start, str):
        raise TypeError('Function expects a string.')
    cache = load_cache()
    if postcode_start in cache and 'completions' in cache[postcode_start]:
        return cache[postcode_start]['completions']
    else:
        url = f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"
        try:
            result = req.get(url, timeout=15)
            result.raise_for_status()
        except req.exceptions.HTTPError as e:
            status = e.response.status_code
            if 500 <= status < 600:
                raise req.RequestException('Unable to access API.')
        data = result.json()['result']
        cache[postcode_start] = {"completions": data}
        save_cache(cache)
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
    try:
        result = req.post(url, timeout=15)
        result.raise_for_status()
    except req.exceptions.HTTPError as e:
        status = e.response.status_code
        if 500 <= status < 600:
            raise req.RequestException('Unable to access API.')
    data = result.json()['result']
    return data


if __name__ == "__main__":
    print(get_postcode_completions("SO16 7GL"))
