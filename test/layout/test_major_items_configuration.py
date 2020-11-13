import copy
import json

import pytest

from randovania import get_data_path
from randovania.bitpacking import bitpacking
from randovania.bitpacking.bitpacking import BitPackDecoder
from randovania.game_description import default_database
from randovania.games.game import RandovaniaGame
from randovania.layout.major_items_configuration import MajorItemsConfiguration


def _create_config_for(game: RandovaniaGame, replace: dict):
    with get_data_path().joinpath("item_database", game.value, "default_state", "major-items.json").open() as open_file:
        default_data = json.load(open_file)

    default_data["progressive_suit"] = True
    default_data["progressive_grapple"] = True
    default_data["minimum_random_starting_items"] = 0
    default_data["maximum_random_starting_items"] = 0

    data = copy.deepcopy(default_data)
    for field, value in replace.items():
        for key, inner_value in value.items():
            data[field][key] = inner_value

    return (
        MajorItemsConfiguration.from_json(default_data, default_database.item_database_for_game(game)),
        MajorItemsConfiguration.from_json(data, default_database.item_database_for_game(game)),
    )


@pytest.fixture(
    params=[
        {"encoded": b'\xc0\x00\x00', "replace": {}},
        {"encoded": b'\xc1B@\x00', "replace": {
            "items_state": {
                "Spider Ball": {
                    "include_copy_in_original_location": True,
                    "num_shuffled_pickups": 1,
                    "num_included_in_starting_items": 0,
                    "included_ammo": [],
                    "allowed_as_random_starting_item": False
                }
            }
        }},
    ],
    name="prime2_data")
def _prime2_data(request):
    return (request.param["encoded"], *_create_config_for(RandovaniaGame.PRIME2, request.param["replace"]))


@pytest.fixture(
    params=[
        {"encoded": b'\xc0\x00\x00', "replace": {}},
    ],
    name="prime3_data")
def _prime3_data(request):
    return (request.param["encoded"], *_create_config_for(RandovaniaGame.PRIME3, request.param["replace"]))


def test_decode_prime2(prime2_data):
    # Setup
    data, default, expected = prime2_data

    # Run
    decoder = BitPackDecoder(data)
    result = MajorItemsConfiguration.bit_pack_unpack(decoder, {"reference": default})

    # Assert
    assert result == expected


def test_encode_prime2(prime2_data):
    # Setup
    expected, default, value = prime2_data

    # Run
    result = bitpacking.pack_value(value, {"reference": default})

    # Assert
    assert result == expected


def test_encode_prime3(prime3_data):
    # Setup
    expected, default, value = prime3_data

    # Run
    result = bitpacking.pack_value(value, {"reference": default})

    # Assert
    assert result == expected
