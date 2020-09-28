import datetime

import pytest
from mock import MagicMock, AsyncMock

from randovania.gui.game_session_window import GameSessionWindow
from randovania.network_client.game_session import GameSessionEntry, PlayerSessionEntry, User, GameSessionAction
from randovania.network_common.session_state import GameSessionState


@pytest.mark.asyncio
async def test_on_game_session_updated(preset_manager, skip_qtbot):
    # Setup
    network_client = MagicMock()
    network_client.current_user = User(id=12, name="Player A")
    game_connection = MagicMock()
    game_connection.pretty_current_status = "Maybe Connected"

    initial_session = GameSessionEntry(
        id=1234,
        name="The Session",
        presets=[preset_manager.default_preset, preset_manager.default_preset],
        players={
            12: PlayerSessionEntry(12, "Player A", 0, False, True),
        },
        actions=[],
        seed_hash=None,
        word_hash=None,
        spoiler=None,
        state=GameSessionState.SETUP,
    )
    second_session = GameSessionEntry(
        id=1234,
        name="The Session",
        presets=[preset_manager.default_preset],
        players={
            12: PlayerSessionEntry(12, "Player A", 0, False, True),
            24: PlayerSessionEntry(24, "Player B", 0, True, False),
        },
        actions=[
            GameSessionAction("Hello", datetime.datetime(year=2020, month=1, day=5))
        ],
        seed_hash="AB12",
        word_hash="Chykka Required",
        spoiler=True,
        state=GameSessionState.IN_PROGRESS,
    )
    network_client.current_game_session = initial_session

    window = GameSessionWindow(network_client, game_connection, preset_manager, MagicMock(), MagicMock())
    window.update_multiworld_client_status = AsyncMock()

    # Run
    await window.on_game_session_updated(second_session)
    window.update_multiworld_client_status.assert_awaited_once_with()


@pytest.mark.parametrize("in_game", [False, True])
@pytest.mark.asyncio
async def test_update_multiworld_client_status(skip_qtbot, mocker, in_game):
    # Setup
    network_client = MagicMock()
    game_connection = MagicMock()
    game_connection.pretty_current_status = "Maybe Connected"
    mocker.patch("randovania.gui.game_session_window.GameSessionWindow.on_game_session_updated")

    window = GameSessionWindow(network_client, game_connection, MagicMock(), MagicMock(), MagicMock())
    window._game_session = MagicMock()
    window._game_session.state = GameSessionState.IN_PROGRESS if in_game else GameSessionState.SETUP
    window.multiworld_client.start = AsyncMock()
    window.multiworld_client.stop = AsyncMock()

    # Run
    await window.update_multiworld_client_status()

    # Assert
    if in_game:
        called, not_called = window.multiworld_client.start, window.multiworld_client.stop
    else:
        called, not_called = window.multiworld_client.stop, window.multiworld_client.start
    called.assert_awaited_once()
    not_called.assert_not_awaited()
