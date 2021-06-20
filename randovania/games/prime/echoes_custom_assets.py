import copy
import json
import time
from typing import NamedTuple

from retro_data_structures.asset_provider import AssetProvider
from retro_data_structures.conversion import conversions
from retro_data_structures.conversion.asset_converter import AssetConverter
from retro_data_structures.dependencies import recursive_dependencies_for
from retro_data_structures.formats import PAK, format_for
from retro_data_structures.game_check import Game

from randovania import get_data_path
from randovania.interface_common.options import Options


def prime_asset_provider() -> AssetProvider:
    internal_copies_path = Options.with_default_data_dir().internal_copies_path
    paks_path = internal_copies_path.joinpath("prime1", "vanilla", "paks")

    all_files = list(paks_path.glob("*.pak"))
    return AssetProvider(all_files, Game.PRIME)


def echoes_asset_provider() -> AssetProvider:
    internal_copies_path = Options.with_default_data_dir().internal_copies_path
    paks_path = internal_copies_path.joinpath("prime2", "vanilla", "paks")

    all_files = list(paks_path.glob("*.pak"))
    return AssetProvider(all_files, Game.ECHOES)


def create_scan_visor_assets():
    dark_visor_ancs_id = 2233160302
    scan_visor_cmdl = 2949054468

    with echoes_asset_provider() as asset_provider:
        dark_visor_ancs = asset_provider.get_asset(dark_visor_ancs_id)

        scan_visor_ancs = copy.deepcopy(dark_visor_ancs)
        scan_visor_ancs.character_set.characters[0].model_id = scan_visor_cmdl


class Asset(NamedTuple):
    ancs: int
    cmdl: int


prime1_assets = {
    "Charge Beam": Asset(0xE3CBC3F3, 0xC5472401),
    "Power Beam": Asset(0x00000000, 0x00000000),
    "Wave Beam": Asset(0x09881302, 0x009771B9),
    "Ice Beam": Asset(0x52A3B1A4, 0xDA25B1BE),
    "Plasma Beam": Asset(0x6397CC1B, 0xA792116A),
    "Missile": Asset(0xA9B8E446, 0x2D7E6590),
    "Grapple Beam": Asset(0xC5B5ED4D, 0xF86621C9),
    "Combat Visor": Asset(0x00000000, 0x00000000),
    "Scan Visor": Asset(0x00000000, 0x00000000),
    "Thermal Visor": Asset(0x9F0C908A, 0x61DAB956),
    "X-Ray Visor": Asset(0x9F0C908A, 0x61DAB956),
    "Space Jump Boots": Asset(0x999E81FE, 0xA10715DA),
    "Energy Tank": Asset(0xF37BCBC7, 0x86908399),
    "Morph Ball": Asset(0x2D0FD5C9, 0x903E8AC5),
    "Morph Ball Bomb": Asset(0xDA110E43, 0xB5544D27),
    "Boost Ball": Asset(0x2D0FD5C9, 0x903E8AC5),
    "Spider Ball": Asset(0x2D0FD5C9, 0x79D95DEC),
    "Power Bomb": Asset(0xF19131AD, 0xD532BDB8),
    "Power Bomb Expansion": Asset(0x0B5BBF9E, 0x227D7166),
    "Power Suit": Asset(0x00000000, 0x00000000),
    "Varia Suit": Asset(0xA3E787B7, 0xCD995C16),
    "Gravity Suit": Asset(0x27A97006, 0x95946E41),
    "Phazon Suit": Asset(0x00000000, 0x00000000),
    "Super Missile": Asset(0x7C04E388, 0x853A56F0),
    "Wavebuster": Asset(0x7C04E388, 0x74A39FE6),
    "Ice Spreader": Asset(0x7C04E388, 0x85BA7ACB),
    "Flamethrower": Asset(0x7C04E388, 0xC54BBF68),
    "Artifact of Truth": Asset(0xFAA9C708, 0x884E88DC),
    "Artifact of Strength": Asset(0xFAA9C708, 0xFFD05A2C),
    "Artifact of Elder": Asset(0xFAA9C708, 0x64751643),
    "Artifact of Wild": Asset(0xFAA9C708, 0x10EDFFCC),
    "Artifact of Lifegiver": Asset(0xFAA9C708, 0x8B48B3A3),
    "Artifact of Warrior": Asset(0xFAA9C708, 0xFCD66153),
    "Artifact of Chozo": Asset(0xFAA9C708, 0x67732D3C),
    "Artifact of Nature": Asset(0xFAA9C708, 0x15E7B24D),
    "Artifact of Sun": Asset(0xFAA9C708, 0x8E42FE22),
    "Artifact of World": Asset(0xFAA9C708, 0x12174A4C),
    "Artifact of Spirit": Asset(0xFAA9C708, 0x89B20623),
    "Artifact of Newborn": Asset(0xFAA9C708, 0xFE2CD4D3),
}


def convert_prime1_pickups():
    next_id = 0xFFFF0000

    def id_generator(asset_type):
        nonlocal next_id
        result = next_id
        while asset_provider.asset_id_exists(result):
            result += 1

        next_id = result + 1
        return result

    start = time.time()
    with prime_asset_provider() as asset_provider:
        print("Loading PAKs")
        converter = AssetConverter(
            target_game=Game.ECHOES,
            asset_providers={Game.PRIME: asset_provider},
            id_generator=id_generator,
            converters=conversions.converter_for,
        )
        print(f"Finished loading PAKs: {time.time() - start}")

        result = {}
        for name, (ancs, cmdl) in prime1_assets.items():
            if ancs != 0 and cmdl != 0:
                result[name] = Asset(
                    ancs=converter.convert_by_id(ancs, Game.PRIME).id,
                    cmdl=converter.convert_by_id(cmdl, Game.PRIME).id,
                )
    end = time.time()
    print(f"Time took: {end - start}")

    internal_copies_path = Options.with_default_data_dir().internal_copies_path
    echoes_paks_path = internal_copies_path.joinpath("prime2", "vanilla", "paks")

    new_pak = PAK.parse_file(
        echoes_paks_path.joinpath("Metroid2.pak"),
        target_game=Game.ECHOES,
    )
    for new_asset in converter.converted_assets.values():
        if new_asset.type.upper() == "evnt":
            continue
        new_pak.resources.append({
            "compressed": 0,
            "asset": {
                "type": new_asset.type,
                "id": new_asset.id,
            },
            "contents": {
                "value": format_for(new_asset.type).build(new_asset.resource, target_game=Game.ECHOES),
            },
        })

    print("Building new PAK")
    new_path_path = internal_copies_path.joinpath("prime2", "ModdedMetroid2.pak")
    PAK.build_file(new_pak, new_path_path, target_game=Game.ECHOES)

    randomizer_data_path = get_data_path().joinpath("ClarisPrimeRandomizer", "RandomizerData.json")
    with randomizer_data_path.open() as randomizer_data_file:
        randomizer_data = json.load(randomizer_data_file)

    print("Updating RandomizerData.json")
    start = time.time()
    with AssetProvider([new_path_path], Game.ECHOES) as echoes_provider:
        for name, assets in result.items():
            dependencies = [
                {"AssetID": dependency_id, "Type": dependency_type.upper()}
                for dependency_type, dependency_id in recursive_dependencies_for(echoes_provider,
                                                                                 [assets.ancs, assets.cmdl])
            ]
            dependencies.append({
                "AssetID": assets.ancs, "Type": "ANCS",
            })

            randomizer_data["ModelData"].append({
                "Index": len(randomizer_data["ModelData"]),
                "Name": f"ConvertedPrime1_{name}",
                "Model": assets.cmdl,
                "ScanModel": 0xFFFFFFFF,
                "AnimSet": assets.ancs,
                "Character": 0,
                "DefaultAnim": 0,
                "Rotation": [0.0, 0.0, 0.0],
                "Scale": [1.000000, 1.000000, 1.000000],
                "OrbitOffset": [0.0, 0.0, 0.0],
                "Lighting": {
                    "CastShadow": True,
                    "UnknownBool1": True,
                    "UseWorldLighting": 1,
                    "UnknownBool2": False
                },
                "Assets": dependencies
            })
    with internal_copies_path.joinpath("prime2", "ModdedRandomizerData.json").open("w") as data_file:
        json.dump(randomizer_data, data_file)

    end = time.time()
    print(f"Time took: {end - start}")


if __name__ == '__main__':
    convert_prime1_pickups()
