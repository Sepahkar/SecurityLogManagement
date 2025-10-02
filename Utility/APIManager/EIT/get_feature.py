"""Moduel docstring"""
import requests


def v1(feature_code: int):
    assert isinstance(feature_code, int)
    url = f'http://127.0.0.1:63000/EIT/api/feature/{feature_code}/'

    #I assume that its always 200 OK
    return requests.get(url).json().get("data")

