import pytest as pytest

from commands.mc_api import McApi


def test_is_indigo():
    print()
    mc_api = McApi()
    mc_api.mc_connect()

