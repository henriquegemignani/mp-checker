import json
import os
from unittest.mock import MagicMock, ANY

import randovania
from randovania.games.patchers.randomprime_patcher import RandomprimePatcher
from randovania.interface_common.cosmetic_patches import CosmeticPatches
from randovania.interface_common.players_configuration import PlayersConfiguration
from randovania.layout.layout_description import LayoutDescription


def test_create_patch_data(test_files_dir):
    # Setup
    file = test_files_dir.joinpath("log_files", "prime1_and_2_multi.rdvgame")
    description = LayoutDescription.from_file(file)
    patcher = RandomprimePatcher()
    players_config = PlayersConfiguration(0, {0: "Prime", 1: "Echoes"})
    cosmetic_patches = CosmeticPatches()

    # Run
    data = patcher.create_patch_data(description, players_config, cosmetic_patches)
    print(data)

    # Assert
    assert data == {
        'seed': 1499122484,
        'preferences': {
            'artifactHintBehavior': None,
            'mapDefaultState': 'visible',
            'obfuscateItems': False,
            'qolCosmetic': True,
            'qolGameBreaking': True,
            'qolLogical': True,
            'qolMajorCutscenes': False,
            'qolMinorCutscenes': False,
            'quickplay': False,
            'quiet': False,
            'trilogyDiscPath': None,
        },
        'gameConfig': {
            'artifactHints': {
                'Chozo': '&push;&main-color=#FF6705B3;Artifact '
                         'of Chozo&pop; is located in '
                         "&push;&main-color=#d4cc33;Echoes&pop;'s "
                         '&push;&main-color=#FF3333;Dark '
                         'Agon Wastes - Ing Cache 1&pop;.',
                'Elder': '&push;&main-color=#FF6705B3;Artifact '
                         'of Elder&pop; is located in '
                         "&push;&main-color=#d4cc33;Echoes&pop;'s "
                         '&push;&main-color=#FF3333;Agon '
                         'Wastes - Sand Cache&pop;.',
                'Lifegiver': '&push;&main-color=#FF6705B3;Artifact of Lifegiver&pop; is located in '
                             "&push;&main-color=#d4cc33;Echoes&pop;'s "
                             '&push;&main-color=#FF3333;Temple Grounds - Storage Cavern B&pop;.',
                'Nature': '&push;&main-color=#FF6705B3;Artifact of Nature&pop; is located in '
                          "&push;&main-color=#d4cc33;Echoes&pop;'s "
                          '&push;&main-color=#FF3333;Sanctuary Fortress - Hall of Combat Mastery&pop;.',
                'Newborn': '&push;&main-color=#FF6705B3;Artifact of Newborn&pop; is located in '
                           "&push;&main-color=#d4cc33;Echoes&pop;'s "
                           '&push;&main-color=#FF3333;Great Temple - Transport A Access&pop;.',
                'Spirit': '&push;&main-color=#FF6705B3;Artifact of Spirit&pop; is located in '
                          "&push;&main-color=#d4cc33;Echoes&pop;'s "
                          '&push;&main-color=#FF3333;Temple '
                          'Grounds - Transport to Agon '
                          'Wastes&pop;.',
                'Strength': '&push;&main-color=#FF6705B3;Artifact '
                            'of Strength&pop; is located in '
                            "&push;&main-color=#d4cc33;Echoes&pop;'s "
                            '&push;&main-color=#FF3333;Agon '
                            'Wastes - Storage D&pop;.',
                'Sun': '&push;&main-color=#FF6705B3;Artifact '
                       'of Sun&pop; is located in '
                       "&push;&main-color=#d4cc33;Echoes&pop;'s "
                       '&push;&main-color=#FF3333;Agon '
                       'Wastes - Command Center&pop;.',
                'Truth': '&push;&main-color=#FF6705B3;Artifact '
                         'of Truth&pop; is located in '
                         "&push;&main-color=#d4cc33;Echoes&pop;'s "
                         '&push;&main-color=#FF3333;Agon '
                         'Wastes - Mining Station '
                         'Access&pop;.',
                'Warrior': '&push;&main-color=#FF6705B3;Artifact '
                           'of Warrior&pop; is located in '
                           "&push;&main-color=#d4cc33;Echoes&pop;'s "
                           '&push;&main-color=#FF3333;Agon '
                           'Wastes - Portal Access A&pop;.',
                'Wild': '&push;&main-color=#FF6705B3;Artifact '
                        'of Wild&pop; is located in '
                        "&push;&main-color=#d4cc33;Prime&pop;'s "
                        '&push;&main-color=#FF3333;Tallon '
                        'Overworld - Transport Tunnel '
                        'B&pop;.',
                'World': '&push;&main-color=#FF6705B3;Artifact '
                         'of World&pop; is located in '
                         "&push;&main-color=#d4cc33;Echoes&pop;'s "
                         '&push;&main-color=#FF3333;Ing Hive '
                         '- Culling Chamber&pop;.'},

            'artifactTempleLayerOverrides': {
                'Artifact of Chozo': True,
                'Artifact of Elder': True,
                'Artifact of Lifegiver': True,
                'Artifact of Nature': True,
                'Artifact of Newborn': True,
                'Artifact of Spirit': True,
                'Artifact of Strength': True,
                'Artifact of Sun': True,
                'Artifact of Truth': True,
                'Artifact of Warrior': True,
                'Artifact of Wild': True,
                'Artifact of World': True,
            },
            'autoEnabledElevators': False,
            'creditsString': None,
            'etankCapacity': 110,
            'gameBanner': {'description': 'Seed Hash: Culling Chamber Staging',
                           'gameName': 'Metroid Prime: Randomizer',
                           'gameNameFull': 'Metroid Prime: Randomizer - ALKZLIJL'},
            'heatDamagePerSec': 10.0,
            'itemMaxCapacity': {'Unknown Item 1': 65536},
            'mainMenuMessage': f'{randovania.VERSION}\nCulling Chamber Staging',
            'nonvariaHeatDamage': True,
            'staggeredSuitDamage': True,
            'startingItems': {
                'bombs': False,
                'boostBall': False,
                'charge': False,
                'energyTanks': 0,
                'flamethrower': False,
                'grapple': False,
                'gravitySuit': False,
                'ice': False,
                'iceSpreader': False,
                'missiles': 5,
                'morphBall': True,
                'phazonSuit': False,
                'plasma': False,
                'powerBeam': True,
                'powerBombs': 0,
                'scanVisor': True,
                'spaceJump': True,
                'spiderBall': False,
                'superMissile': False,
                'thermalVisor': False,
                'variaSuit': False,
                'wave': False,
                'wavebuster': False,
                'xray': False,
            },
            'startingMemo': '5 Missiles',
            'startingRoom': 'Tallon Overworld:Landing Site'},
        'levelData': {
            'Impact Crater': {'transports': {}, 'rooms': {}},
            'Phendrana Drifts': {
                'transports': {
                    'Phendrana Drifts North\x00(Phendrana Shorelines)': 'Tallon Overworld East\x00(Frigate Crash Site)',
                    'Phendrana Drifts South\x00(Quarantine Cave)': 'Magmoor Caverns West\x00(Monitor Station)'},
                'rooms': {
                    'Phendrana Shorelines': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False},
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                                'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                                'count': 37,
                                'respawn': False}]},
                    'Chozo Ice Temple': {
                        'pickups': [
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Energy Tank",
                                'hudmemoText': 'Sent Energy Tank to Echoes!',
                                'count': 38,
                                'respawn': False}]},
                    'Ice Ruins West': {
                        'pickups': [
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                'count': 39,
                                'respawn': False}]},
                    'Ice Ruins East': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False},
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                'count': 41,
                                'respawn': False}]},
                    'Chapel of the Elders': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False}]},
                    'Ruined Courtyard': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False}]},
                    'Phendrana Canyon': {
                        'pickups': [
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Energy Tank",
                                'hudmemoText': 'Sent Energy Tank to Echoes!',
                                'count': 44,
                                'respawn': False}]},
                    'Quarantine Cave': {
                        'pickups': [
                            {
                                'type': 'Energy Tank',
                                'model': 'Energy Tank',
                                'scanText': 'Your Energy Tank',
                                'hudmemoText': 'Energy Tank acquired!',
                                'count': 1,
                                'respawn': False}]},
                    'Research Lab Hydra': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False}]},
                    'Quarantine Monitor': {
                        'pickups': [
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                'count': 47,
                                'respawn': False}]},
                    'Observatory': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False}]},
                    'Transport Access': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False}]},
                    'Control Tower': {
                        'pickups': [
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                'count': 50,
                                'respawn': False}]},
                    'Research Core': {
                        'pickups': [
                            {
                                'type': 'Energy Tank',
                                'model': 'Energy Tank',
                                'scanText': 'Your Energy Tank',
                                'hudmemoText': 'Energy Tank acquired!',
                                'count': 1,
                                'respawn': False}]},
                    'Frost Cave': {
                        'pickups': [
                            {
                                'type': 'Energy Tank',
                                'model': 'Energy Tank',
                                'scanText': 'Your Energy Tank',
                                'hudmemoText': 'Energy Tank acquired!',
                                'count': 1,
                                'respawn': False}]},
                    'Research Lab Aether': {
                        'pickups': [
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                'count': 53,
                                'respawn': False},
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                                'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                                'count': 54,
                                'respawn': False}]},
                    'Gravity Chamber': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False},
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                'count': 56,
                                'respawn': False}]},
                    'Storage Cave': {
                        'pickups': [
                            {
                                'type': 'Missile',
                                'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!',
                                'count': 5,
                                'respawn': False}]},
                    'Security Cave': {
                        'pickups': [
                            {
                                'type': 'Unknown Item 1',
                                'model': 'Nothing',
                                'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                'count': 58,
                                'respawn': False}]}}},
            'Frigate Orpheon': {'transports': {}, 'rooms': {}},
            'Magmoor Caverns': {
                'transports': {
                    'Magmoor Caverns North\x00(Lava Lake)': 'Tallon Overworld West\x00(Root Cave)',
                    'Magmoor Caverns West\x00(Monitor Station)': 'Phendrana Drifts South\x00(Quarantine Cave)',
                    'Magmoor Caverns East\x00(Twin Fires)': 'Phazon Mines East\x00(Main Quarry)',
                    'Magmoor Caverns South\x00(Magmoor Workstation, Debris)': 'Chozo Ruins South\x00(Reflecting Pool, Far End)',
                    'Magmoor Caverns South\x00(Magmoor Workstation, Save Station)': 'Phazon Mines West\x00(Phazon Processing Center)'},
                'rooms': {
                    'Lava Lake': {
                        'pickups': [
                            {'type': 'Unknown Item 1', 'model': 'Nothing', 'scanText': "Echoes's Morph Ball Bomb",
                             'hudmemoText': 'Sent Morph Ball Bomb to Echoes!', 'count': 91, 'respawn': False}]},
                    'Triclops Pit': {
                        'pickups': [
                            {'type': 'Unknown Item 1', 'model': 'Nothing',
                             'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                             'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                             'count': 92, 'respawn': False}]},
                    'Storage Cavern': {
                        'pickups': [
                            {'type': 'Energy Tank', 'model': 'Energy Tank',
                             'scanText': 'Your Energy Tank',
                             'hudmemoText': 'Energy Tank acquired!',
                             'count': 1, 'respawn': False}]},
                    'Transport Tunnel A': {
                        'pickups': [{'type': 'Missile', 'model': 'Missile',
                                     'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                     'hudmemoText': 'Missile Expansion acquired!',
                                     'count': 5, 'respawn': False}]},
                    'Warrior Shrine': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                                     'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                                     'count': 95, 'respawn': False}]},
                    'Shore Tunnel': {'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                                  'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                                                  'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                                                  'count': 96, 'respawn': False}]}, 'Fiery Shores': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                     'hudmemoText': 'Sent Missile Expansion to Echoes!', 'count': 97,
                                     'respawn': False}, {'type': 'Energy Tank', 'model': 'Energy Tank',
                                                         'scanText': 'Your Energy Tank',
                                                         'hudmemoText': 'Energy Tank acquired!', 'count': 1,
                                                         'respawn': False}]}, 'Plasma Processing': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                     'hudmemoText': 'Sent Missile Expansion to Echoes!', 'count': 99,
                                     'respawn': False}]}, 'Magmoor Workstation': {'pickups': [
                        {'type': 'Missile', 'model': 'Missile',
                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                         'hudmemoText': 'Missile Expansion acquired!', 'count': 5, 'respawn': False}]}}},
            'Phazon Mines': {
                'transports': {
                    'Phazon Mines East\x00(Main Quarry)': 'Magmoor Caverns East\x00(Twin Fires)',
                    'Phazon Mines West\x00(Phazon Processing Center)': 'Magmoor Caverns South\x00(Magmoor Workstation, Save Station)'},
                'rooms': {
                    'Main Quarry': {
                        'pickups': [
                            {
                                'type': 'Missile', 'model': 'Missile',
                                'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                'hudmemoText': 'Missile Expansion acquired!', 'count': 5,
                                'respawn': False}]},
                    'Security Access A': {
                        'pickups': [
                            {'type': 'Unknown Item 1', 'model': 'Nothing',
                             'scanText': "Echoes's Energy Tank",
                             'hudmemoText': 'Sent Energy Tank to Echoes!', 'count': 75,
                             'respawn': False}]},
                    'Storage Depot B': {
                        'pickups': [
                            {'type': 'Energy Tank', 'model': 'Energy Tank',
                             'scanText': 'Your Energy Tank',
                             'hudmemoText': 'Energy Tank acquired!', 'count': 1,
                             'respawn': False}]},
                    'Storage Depot A': {
                        'pickups': [
                            {'type': 'Spider Ball', 'model': 'Spider Ball',
                             'scanText': 'Your Spider Ball',
                             'hudmemoText': 'Spider Ball acquired!', 'count': 1,
                             'respawn': False}]},
                    'Elite Research': {
                        'pickups': [
                            {'type': 'Unknown Item 1', 'model': 'Nothing',
                             'scanText': "Echoes's Sonic Boom",
                             'hudmemoText': 'Sent Sonic Boom to Echoes!',
                             'count': 78, 'respawn': False},
                            {'type': 'Nothing', 'model': 'Nothing',
                             'scanText': 'Your Nothing',
                             'hudmemoText': 'Nothing acquired!',
                             'count': 0, 'respawn': False}
                        ]},
                    'Elite Control Access': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 80, 'respawn': False}]},
                    'Ventilation Shaft': {'pickups': [
                        {'type': 'Missile', 'model': 'Missile',
                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                         'hudmemoText': 'Missile Expansion acquired!',
                         'count': 5, 'respawn': False}]},
                    'Phazon Processing Center': {'pickups': [
                        {'type': 'Power Bomb', 'model': 'Power Bomb Expansion',
                         'scanText': 'Your Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percent',
                         'hudmemoText': 'Power Bomb Expansion acquired!',
                         'count': 1, 'respawn': False}]},
                    'Processing Center Access': {'pickups': [
                        {'type': 'Missile', 'model': 'Missile',
                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                         'hudmemoText': 'Missile Expansion acquired!',
                         'count': 5, 'respawn': False}]},
                    'Elite Quarters': {
                        'pickups': [
                            {'type': 'Unknown Item 1', 'model': 'Nothing',
                             'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                             'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                             'count': 84, 'respawn': False}]},
                    'Central Dynamo': {'pickups': [
                        {'type': 'Energy Tank', 'model': 'Energy Tank',
                         'scanText': 'Your Energy Tank',
                         'hudmemoText': 'Energy Tank acquired!', 'count': 1,
                         'respawn': False}]}, 'Metroid Quarantine B': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Darkburst",
                                     'hudmemoText': 'Sent Darkburst to Echoes!',
                                     'count': 86, 'respawn': False}]},
                    'Metroid Quarantine A': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 87, 'respawn': False}]}, 'Fungal Hall B': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                                     'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                                     'count': 88, 'respawn': False}]},
                    'Phazon Mining Tunnel': {'pickups': [
                        {'type': 'Missile', 'model': 'Missile',
                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                         'hudmemoText': 'Missile Expansion acquired!',
                         'count': 5, 'respawn': False}]},
                    'Fungal Hall Access': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Energy Tank",
                         'hudmemoText': 'Sent Energy Tank to Echoes!',
                         'count': 90, 'respawn': False}]}}},
            'Tallon Overworld': {'transports': {
                'Tallon Overworld North\x00(Tallon Canyon)': 'Chozo Ruins East\x00(Reflecting Pool, Save Station)',
                'Tallon Overworld East\x00(Frigate Crash Site)': 'Phendrana Drifts North\x00(Phendrana Shorelines)',
                'Tallon Overworld West\x00(Root Cave)': 'Magmoor Caverns North\x00(Lava Lake)',
                'Tallon Overworld South\x00(Great Tree Hall, Upper)': 'Chozo Ruins West\x00(Main Plaza)',
                'Tallon Overworld South\x00(Great Tree Hall, Lower)': 'Chozo Ruins North\x00(Sun Tower)'},
                'rooms': {'Landing Site': {'pickups': [
                    {'type': 'Varia Suit', 'model': 'Varia Suit',
                     'scanText': 'Your Varia Suit',
                     'hudmemoText': 'Varia Suit acquired!', 'count': 1,
                     'respawn': False}]}, 'Alcove': {'pickups': [
                    {'type': 'X-Ray Visor', 'model': 'X-Ray Visor',
                     'scanText': 'Your X-Ray Visor',
                     'hudmemoText': 'X-Ray Visor acquired!', 'count': 1,
                     'respawn': False}]}, 'Frigate Crash Site': {'pickups': [
                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                     'scanText': "Echoes's Emerald Translator",
                     'hudmemoText': 'Sent Emerald Translator to Echoes!',
                     'count': 61, 'respawn': False}]}, 'Overgrown Cavern': {
                    'pickups': [{'type': 'Missile', 'model': 'Missile',
                                 'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                 'hudmemoText': 'Missile Expansion acquired!',
                                 'count': 5, 'respawn': False}]}, 'Root Cave': {
                    'pickups': [{'type': 'Plasma Beam', 'model': 'Plasma Beam',
                                 'scanText': 'Your Plasma Beam',
                                 'hudmemoText': 'Plasma Beam acquired!',
                                 'count': 1, 'respawn': False}]},
                    'Artifact Temple': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Violet Translator",
                         'hudmemoText': 'Sent Violet Translator to Echoes!',
                         'count': 64, 'respawn': False}]},
                    'Transport Tunnel B': {'pickups': [
                        {'type': 'Artifact of Wild',
                         'model': 'Artifact of Wild',
                         'scanText': 'Your Artifact of Wild',
                         'hudmemoText': 'Artifact of Wild acquired!',
                         'count': 1, 'respawn': False}]},
                    'Arbor Chamber': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Screw Attack",
                         'hudmemoText': 'Sent Screw Attack to Echoes!',
                         'count': 66, 'respawn': False}]},
                    'Cargo Freight Lift to Deck Gamma': {'pickups': [
                        {'type': 'Phazon Suit', 'model': 'Phazon Suit',
                         'scanText': 'Your Phazon Suit',
                         'hudmemoText': 'Phazon Suit acquired!',
                         'count': 1, 'respawn': False}]},
                    'Biohazard Containment': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                         'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                         'count': 68, 'respawn': False}]},
                    'Hydro Access Tunnel': {'pickups': [
                        {'type': 'Missile', 'model': 'Missile',
                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                         'hudmemoText': 'Missile Expansion acquired!',
                         'count': 5, 'respawn': False}]},
                    'Great Tree Chamber': {'pickups': [
                        {'type': 'Energy Tank', 'model': 'Energy Tank',
                         'scanText': 'Your Energy Tank',
                         'hudmemoText': 'Energy Tank acquired!',
                         'count': 1, 'respawn': False}]},
                    'Life Grove Tunnel': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                         'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                         'count': 71, 'respawn': False}]}, 'Life Grove': {
                        'pickups': [{'type': 'Boost Ball', 'model': 'Boost Ball',
                                     'scanText': 'Your Boost Ball',
                                     'hudmemoText': 'Boost Ball acquired!',
                                     'count': 1, 'respawn': False},
                                    {'type': 'Missile', 'model': 'Missile',
                                     'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                     'hudmemoText': 'Missile Expansion acquired!',
                                     'count': 5, 'respawn': False}]}}},
            'Chozo Ruins': {'transports': {
                'Chozo Ruins West\x00(Main Plaza)': 'Tallon Overworld South\x00(Great Tree Hall, Upper)',
                'Chozo Ruins North\x00(Sun Tower)': 'Tallon Overworld South\x00(Great Tree Hall, Lower)',
                'Chozo Ruins East\x00(Reflecting Pool, Save Station)': 'Tallon Overworld North\x00(Tallon Canyon)',
                'Chozo Ruins South\x00(Reflecting Pool, Far End)': 'Magmoor Caverns South\x00(Magmoor Workstation, Debris)'},
                'rooms': {'Main Plaza': {'pickups': [
                    {'type': 'Power Bomb', 'model': 'Power Bomb Expansion',
                     'scanText': 'Your Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percent',
                     'hudmemoText': 'Power Bomb Expansion acquired!', 'count': 1,
                     'respawn': False}, {'type': 'Missile', 'model': 'Missile',
                                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                         'hudmemoText': 'Missile Expansion acquired!',
                                         'count': 5, 'respawn': False},
                    {'type': 'Power Bomb', 'model': 'Power Bomb',
                     'scanText': 'Your Power Bomb',
                     'hudmemoText': 'Power Bomb acquired!', 'count': 4,
                     'respawn': False}, {'type': 'Missile', 'model': 'Missile',
                                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                         'hudmemoText': 'Missile Expansion acquired!',
                                         'count': 5, 'respawn': False}]},
                    'Ruined Fountain': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 5, 'respawn': False}]}, 'Ruined Shrine': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                                     'count': 6, 'respawn': False},
                                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                                     'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                                     'count': 7, 'respawn': False},
                                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                     'count': 8, 'respawn': False}]}, 'Vault': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                                     'hudmemoText': 'Sent Missile Expansion to Echoes!',
                                     'count': 9, 'respawn': False}]},
                    'Training Chamber': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Energy Tank",
                         'hudmemoText': 'Sent Energy Tank to Echoes!',
                         'count': 10, 'respawn': False}]}, 'Ruined Nursery': {
                        'pickups': [{'type': 'Missile', 'model': 'Missile',
                                     'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                     'hudmemoText': 'Missile Expansion acquired!',
                                     'count': 5, 'respawn': False}]},
                    'Training Chamber Access': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 12, 'respawn': False}]}, 'Magma Pool': {
                        'pickups': [{'type': 'Energy Tank', 'model': 'Energy Tank',
                                     'scanText': 'Your Energy Tank',
                                     'hudmemoText': 'Energy Tank acquired!',
                                     'count': 1, 'respawn': False}]},
                    'Tower of Light': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 14, 'respawn': False}]}, 'Tower Chamber': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                                     'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                                     'count': 15, 'respawn': False}]},
                    'Ruined Gallery': {'pickups': [
                        {'type': 'Missile', 'model': 'Missile',
                         'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                         'hudmemoText': 'Missile Expansion acquired!',
                         'count': 5, 'respawn': False},
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 17, 'respawn': False}]},
                    'Transport Access North': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 18, 'respawn': False}]}, 'Gathering Hall': {
                        'pickups': [{'type': 'Missile', 'model': 'Missile',
                                     'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                     'hudmemoText': 'Missile Expansion acquired!',
                                     'count': 5, 'respawn': False}]}, 'Hive Totem': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                                     'count': 20, 'respawn': False}]}, 'Sunchamber': {
                        'pickups': [{'type': 'Missile', 'model': 'Missile',
                                     'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                     'hudmemoText': 'Missile Expansion acquired!',
                                     'count': 5, 'respawn': False},
                                    {'type': 'Wavebuster', 'model': 'Wavebuster',
                                     'scanText': 'Your Wavebuster',
                                     'hudmemoText': 'Wavebuster acquired!',
                                     'count': 1, 'respawn': False}]},
                    'Watery Hall Access': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                         'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                         'count': 23, 'respawn': False}]}, 'Watery Hall': {
                        'pickups': [{'type': 'Energy Tank', 'model': 'Energy Tank',
                                     'scanText': 'Your Energy Tank',
                                     'hudmemoText': 'Energy Tank acquired!',
                                     'count': 1, 'respawn': False},
                                    {'type': 'Energy Tank', 'model': 'Energy Tank',
                                     'scanText': 'Your Energy Tank',
                                     'hudmemoText': 'Energy Tank acquired!',
                                     'count': 1, 'respawn': False}]}, 'Dynamo': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                                     'count': 26, 'respawn': False},
                                    {'type': 'Missile', 'model': 'Missile',
                                     'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                     'hudmemoText': 'Missile Expansion acquired!',
                                     'count': 5, 'respawn': False}]}, 'Burn Dome': {
                        'pickups': [{'type': 'Missile', 'model': 'Missile',
                                     'scanText': 'Your Missile Expansion. Provides 5 Missiles and 1 Item Percent',
                                     'hudmemoText': 'Missile Expansion acquired!',
                                     'count': 5, 'respawn': False},
                                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Energy Tank",
                                     'hudmemoText': 'Sent Energy Tank to Echoes!',
                                     'count': 29, 'respawn': False}]}, 'Furnace': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Light Ammo Expansion. Provides 20 Light Ammo and 1 Item Percentage",
                                     'hudmemoText': 'Sent Light Ammo Expansion to Echoes!',
                                     'count': 30, 'respawn': False},
                                    {'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Energy Tank",
                                     'hudmemoText': 'Sent Energy Tank to Echoes!',
                                     'count': 31, 'respawn': False}]},
                    'Hall of the Elders': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Missile Expansion. Provides 5 Missiles and 1 Item Percentage",
                         'hudmemoText': 'Sent Missile Expansion to Echoes!',
                         'count': 32, 'respawn': False}]}, 'Crossway': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Dark Ammo Expansion. Provides 20 Dark Ammo and 1 Item Percentage",
                                     'hudmemoText': 'Sent Dark Ammo Expansion to Echoes!',
                                     'count': 33, 'respawn': False}]},
                    'Elder Chamber': {'pickups': [
                        {'type': 'Unknown Item 1', 'model': 'Nothing',
                         'scanText': "Echoes's Energy Tank",
                         'hudmemoText': 'Sent Energy Tank to Echoes!',
                         'count': 34, 'respawn': False}]}, 'Antechamber': {
                        'pickups': [{'type': 'Unknown Item 1', 'model': 'Nothing',
                                     'scanText': "Echoes's Power Bomb Expansion. Provides 1 Power Bomb and 1 Item Percentage",
                                     'hudmemoText': 'Sent Power Bomb Expansion to Echoes!',
                                     'count': 35, 'respawn': False}]}}}}}


def test_patch_game(mocker, tmp_path):
    mock_patch_iso_raw: MagicMock = mocker.patch("py_randomprime.patch_iso_raw")
    mock_open_iso: MagicMock = mocker.patch("randovania.games.patchers.randomprime_patcher.IsoDolEditor.open_iso")
    patch_data = {"patch": "data"}
    game_files_path = MagicMock()
    progress_update = MagicMock()

    patcher = RandomprimePatcher()

    # Run
    patcher.patch_game(tmp_path.joinpath("input.iso"), tmp_path.joinpath("output.iso"),
                       patch_data, game_files_path, progress_update)

    # Assert
    expected = {
        "patch": "data",
        "inputIso": os.fspath(tmp_path.joinpath("input.iso")),
        "outputIso": os.fspath(tmp_path.joinpath("output.iso")),
    }
    mock_patch_iso_raw.assert_called_once_with(json.dumps(expected, indent=4, separators=(',', ': ')), ANY)
    mock_open_iso.assert_called_once_with(tmp_path.joinpath("output.iso"))
