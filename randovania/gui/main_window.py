import asyncio
import dataclasses
import functools
import json
from functools import partial
from typing import Optional

import markdown
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QUrl, Signal, Qt
from PySide2.QtGui import QDesktopServices
from PySide2.QtWidgets import QMainWindow, QAction, QMessageBox, QDialog, QMenu, QInputDialog
from asyncqt import asyncSlot

from randovania import VERSION
from randovania.game_description import default_database
from randovania.game_description.node import LogbookNode, LoreType
from randovania.game_description.resources.simple_resource_info import SimpleResourceInfo
from randovania.games.prime import default_data
from randovania.gui.data_editor import DataEditorWindow
from randovania.gui.dialog.login_prompt_dialog import LoginPromptDialog
from randovania.gui.dialog.permalink_dialog import PermalinkDialog
from randovania.gui.dialog.trick_details_popup import TrickDetailsPopup
from randovania.gui.game_session_window import GameSessionWindow
from randovania.gui.generate_seed_tab import GenerateSeedTab
from randovania.gui.generated.main_window_ui import Ui_MainWindow
from randovania.gui.lib import common_qt_lib, async_dialog
from randovania.gui.lib.qt_network_client import handle_network_errors, QtNetworkClient
from randovania.gui.lib.trick_lib import used_tricks, difficulties_for_trick
from randovania.gui.lib.window_manager import WindowManager
from randovania.gui.online_game_list_window import GameSessionBrowserDialog
from randovania.gui.tracker_window import TrackerWindow, InvalidLayoutForTracker
from randovania.interface_common import github_releases_data, update_checker
from randovania.interface_common.options import Options
from randovania.interface_common.preset_manager import PresetManager
from randovania.layout.layout_configuration import LayoutConfiguration
from randovania.layout.layout_description import LayoutDescription
from randovania.layout.trick_level import TrickLevelConfiguration, LayoutTrickLevel
from randovania.network_client.network_client import ConnectionState
from randovania.resolver import debug

_DISABLE_VALIDATION_WARNING = """
<html><head/><body>
<p>While it sometimes throws errors, the validation is what guarantees that your seed is completable.<br/>
Do <span style=" font-weight:600;">not</span> disable if you're uncomfortable with possibly unbeatable seeds.
</p><p align="center">Are you sure you want to disable validation?</p></body></html>
"""


class MainWindow(WindowManager, Ui_MainWindow):
    newer_version_signal = Signal(str, str)
    options_changed_signal = Signal()
    _is_preview_mode: bool = False

    menu_new_version: Optional[QAction] = None
    _current_version_url: Optional[str] = None
    _options: Options
    _data_visualizer: Optional[DataEditorWindow] = None
    _map_tracker: TrackerWindow
    _preset_manager: PresetManager
    game_session_window: Optional[GameSessionWindow] = None
    _login_window: Optional[QDialog] = None
    GameDetailsSignal = Signal(LayoutDescription)

    @property
    def _tab_widget(self):
        return self.main_tab_widget

    @property
    def preset_manager(self) -> PresetManager:
        return self._preset_manager

    @property
    def main_window(self) -> QMainWindow:
        return self

    @property
    def is_preview_mode(self) -> bool:
        return self._is_preview_mode

    def __init__(self, options: Options, preset_manager: PresetManager,
                 network_client: QtNetworkClient, preview: bool):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Randovania {}".format(VERSION))
        self._is_preview_mode = preview
        self.setAcceptDrops(True)
        common_qt_lib.set_default_window_icon(self)

        self.intro_label.setText(self.intro_label.text().format(version=VERSION))

        self._preset_manager = preset_manager
        self.network_client = network_client

        if preview:
            debug.set_level(2)

        # Signals
        self.newer_version_signal.connect(self.display_new_version)
        self.options_changed_signal.connect(self.on_options_changed)
        self.GameDetailsSignal.connect(self._open_game_details)

        self.intro_play_now_button.clicked.connect(lambda: self.welcome_tab_widget.setCurrentWidget(self.tab_play))
        self.open_faq_button.clicked.connect(self._open_faq)
        self.open_database_viewer_button.clicked.connect(self._open_data_visualizer)

        self.import_permalink_button.clicked.connect(self._import_permalink)
        self.import_game_file_button.clicked.connect(self._import_spoiler_log)
        self.browse_sessions_button.clicked.connect(self._browse_for_game_session)
        self.host_new_game_button.clicked.connect(self._host_game_session)
        self.create_new_seed_button.clicked.connect(
            lambda: self.welcome_tab_widget.setCurrentWidget(self.tab_create_seed))

        # Menu Bar
        self.menu_action_data_visualizer.triggered.connect(self._open_data_visualizer)
        self.menu_action_item_tracker.triggered.connect(self._open_item_tracker)
        self.menu_action_edit_new_database.triggered.connect(self._open_data_editor_default)
        self.menu_action_edit_existing_database.triggered.connect(self._open_data_editor_prompt)
        self.menu_action_validate_seed_after.triggered.connect(self._on_validate_seed_change)
        self.menu_action_timeout_generation_after_a_time_limit.triggered.connect(self._on_generate_time_limit_change)
        self.menu_action_open_auto_tracker.triggered.connect(self._open_auto_tracker)
        self.action_login_window.triggered.connect(self._action_login_window)

        self.generate_seed_tab = GenerateSeedTab(self, self, options)
        self.generate_seed_tab.setup_ui()

        # Needs the GenerateSeedTab
        self._create_open_map_tracker_actions()
        self._setup_difficulties_menu()

        # Setting this event only now, so all options changed trigger only once
        options.on_options_changed = self.options_changed_signal.emit
        self._options = options
        with options:
            self.on_options_changed()

        self.main_tab_widget.setCurrentIndex(0)

        # Update hints text
        self._update_hints_text()

    def closeEvent(self, event):
        self.generate_seed_tab.stop_background_process()
        super().closeEvent(event)

    # Generate Seed
    def _open_faq(self):
        self.main_tab_widget.setCurrentWidget(self.help_tab)
        self.help_tab_widget.setCurrentWidget(self.tab_faq)

    def _import_permalink(self):
        dialog = PermalinkDialog()
        result = dialog.exec_()
        if result == QDialog.Accepted:
            permalink = dialog.get_permalink_from_field()
            self.generate_seed_tab.generate_seed_from_permalink(permalink)

    def _import_spoiler_log(self):
        json_path = common_qt_lib.prompt_user_for_input_game_log(self)
        if json_path is not None:
            layout = LayoutDescription.from_file(json_path)
            self.open_game_details(layout)

    async def _game_session_active(self) -> bool:
        if self.game_session_window is None or self.game_session_window.has_closed:
            return False
        else:
            await async_dialog.message_box(
                self,
                QtWidgets.QMessageBox.Critical,
                "Game Session in progress",
                "There's already a game session window open. Please close it first.",
                QMessageBox.Ok
            )
            self.game_session_window.activateWindow()
            return True

    async def _ensure_logged_in(self) -> bool:
        network_client = self.network_client
        if network_client.connection_state == ConnectionState.Connected:
            return True

        if network_client.connection_state.is_disconnected:
            message_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.NoIcon, "Connecting",
                                                "Connecting to server...", QtWidgets.QMessageBox.Cancel,
                                                self)

            connecting = network_client.connect_to_server()
            message_box.rejected.connect(connecting.cancel)
            message_box.show()
            try:
                await connecting
            finally:
                message_box.close()

        if network_client.current_user is None:
            await async_dialog.execute_dialog(LoginPromptDialog(network_client))

        return network_client.current_user is not None

    @asyncSlot()
    @handle_network_errors
    async def _browse_for_game_session(self):
        if await self._game_session_active():
            return

        if not await self._ensure_logged_in():
            return

        network_client = self.network_client
        browser = GameSessionBrowserDialog(network_client)
        await browser.refresh()
        if await async_dialog.execute_dialog(browser) == browser.Accepted:
            self.game_session_window = GameSessionWindow(network_client,
                                                         common_qt_lib.get_game_connection(),
                                                         self.preset_manager,
                                                         self,
                                                         self._options)
            self.game_session_window.show()

    @asyncSlot()
    @handle_network_errors
    async def _action_login_window(self):
        if self._login_window is not None:
            return self._login_window.show()

        self._login_window = LoginPromptDialog(self.network_client)
        try:
            await async_dialog.execute_dialog(self._login_window)
        finally:
            self._login_window = None

    @asyncSlot()
    @handle_network_errors
    async def _host_game_session(self):
        if await self._game_session_active():
            return

        if not await self._ensure_logged_in():
            return

        dialog = QInputDialog(self)
        dialog.setModal(True)
        dialog.setWindowTitle("Enter session name")
        dialog.setLabelText("Select a name for the session:")
        if await async_dialog.execute_dialog(dialog) != dialog.Accepted:
            return

        await self.network_client.create_new_session(dialog.textValue())
        self.game_session_window = GameSessionWindow(self.network_client, common_qt_lib.get_game_connection(),
                                                     self.preset_manager, self, self._options)
        self.game_session_window.show()

    def open_game_details(self, layout: LayoutDescription):
        self.GameDetailsSignal.emit(layout)

    def _open_game_details(self, layout: LayoutDescription):
        from randovania.gui.seed_details_window import SeedDetailsWindow
        details_window = SeedDetailsWindow(self, self._options)
        details_window.update_layout_description(layout)
        details_window.show()
        self.track_window(details_window)

    # Releases info
    def request_new_data(self):
        asyncio.create_task(github_releases_data.get_releases()).add_done_callback(self._on_releases_data)

    def _on_releases_data(self, task: asyncio.Task):
        releases = task.result()
        current_version = update_checker.strict_current_version()
        last_changelog = self._options.last_changelog_displayed

        all_change_logs, new_change_logs, version_to_display = update_checker.versions_to_display_for_releases(
            current_version, last_changelog, releases)

        if version_to_display is not None:
            self.display_new_version(version_to_display)

        if all_change_logs:
            changelog_tab = QtWidgets.QWidget()
            changelog_tab.setObjectName("changelog_tab")
            changelog_tab_layout = QtWidgets.QVBoxLayout(changelog_tab)
            changelog_tab_layout.setContentsMargins(0, 0, 0, 0)
            changelog_tab_layout.setObjectName("changelog_tab_layout")
            changelog_scroll_area = QtWidgets.QScrollArea(changelog_tab)
            changelog_scroll_area.setWidgetResizable(True)
            changelog_scroll_area.setObjectName("changelog_scroll_area")
            changelog_scroll_contents = QtWidgets.QWidget()
            changelog_scroll_contents.setGeometry(QtCore.QRect(0, 0, 489, 337))
            changelog_scroll_contents.setObjectName("changelog_scroll_contents")
            changelog_scroll_layout = QtWidgets.QVBoxLayout(changelog_scroll_contents)
            changelog_scroll_layout.setObjectName("changelog_scroll_layout")
            changelog_label = QtWidgets.QLabel(changelog_scroll_contents)
            changelog_label.setObjectName("changelog_label")
            changelog_label.setText(markdown.markdown("\n".join(all_change_logs)))
            changelog_label.setWordWrap(True)
            changelog_scroll_layout.addWidget(changelog_label)
            changelog_scroll_area.setWidget(changelog_scroll_contents)
            changelog_tab_layout.addWidget(changelog_scroll_area)
            self.help_tab_widget.addTab(changelog_tab, "Change Log")

        if new_change_logs:
            QMessageBox.information(self, "What's new", markdown.markdown("\n".join(new_change_logs)))
            with self._options as options:
                options.last_changelog_displayed = current_version

    def display_new_version(self, version: update_checker.VersionDescription):
        if self.menu_new_version is None:
            self.menu_new_version = QAction("", self)
            self.menu_new_version.triggered.connect(self.open_version_link)
            self.menu_bar.addAction(self.menu_new_version)

        self.menu_new_version.setText("New version available: {}".format(version.tag_name))
        self._current_version_url = version.html_url

    def open_version_link(self):
        if self._current_version_url is None:
            raise RuntimeError("Called open_version_link, but _current_version_url is None")

        QDesktopServices.openUrl(QUrl(self._current_version_url))

    # Options
    def on_options_changed(self):
        self.menu_action_validate_seed_after.setChecked(self._options.advanced_validate_seed_after)
        self.menu_action_timeout_generation_after_a_time_limit.setChecked(
            self._options.advanced_timeout_during_generation)

        self.generate_seed_tab.on_options_changed(self._options)

    # Menu Actions
    def _open_data_visualizer(self):
        self.open_data_visualizer_at(None, None)

    def open_data_visualizer_at(self,
                                world_name: Optional[str],
                                area_name: Optional[str],
                                ):
        self._data_visualizer = DataEditorWindow(default_data.decode_default_prime2(), False)

        if world_name is not None:
            self._data_visualizer.focus_on_world(world_name)

        if area_name is not None:
            self._data_visualizer.focus_on_area(area_name)

        self._data_visualizer.show()

    def _open_data_editor_default(self):
        self._data_editor = DataEditorWindow(default_data.decode_default_prime2(), True)
        self._data_editor.show()

    def _open_data_editor_prompt(self):
        database_path = common_qt_lib.prompt_user_for_database_file(self)
        if database_path is None:
            return

        with database_path.open("r") as database_file:
            self._data_editor = DataEditorWindow(json.load(database_file), True)
            self._data_editor.show()

    def _create_open_map_tracker_actions(self):
        base_layout = self.preset_manager.default_preset.layout_configuration

        for trick_level in LayoutTrickLevel:
            if trick_level != LayoutTrickLevel.MINIMAL_LOGIC:
                action = QtWidgets.QAction(self)
                action.setText(trick_level.long_name)
                self.menu_map_tracker.addAction(action)

                configuration = dataclasses.replace(
                    base_layout,
                    trick_level_configuration=TrickLevelConfiguration(trick_level, {})
                )
                action.triggered.connect(partial(self.open_map_tracker, configuration))

    def open_map_tracker(self, configuration: LayoutConfiguration):
        try:
            self._map_tracker = TrackerWindow(self._options.tracker_files_path, configuration)
        except InvalidLayoutForTracker as e:
            QMessageBox.critical(
                self,
                "Unsupported configuration for Tracker",
                str(e)
            )
            return

        self._map_tracker.show()

    def _open_item_tracker(self):
        # Importing this at root level seems to crash linux tests :(
        from PySide2.QtWebEngineWidgets import QWebEngineView

        tracker_window = QMainWindow()
        tracker_window.setWindowTitle("Item Tracker")
        tracker_window.resize(370, 380)

        web_view = QWebEngineView(tracker_window)
        tracker_window.setCentralWidget(web_view)

        self.web_view = web_view

        def update_window_icon():
            tracker_window.setWindowIcon(web_view.icon())

        web_view.iconChanged.connect(update_window_icon)
        web_view.load(QUrl("https://spaghettitoastbook.github.io/echoes/tracker/"))

        tracker_window.show()
        self._item_tracker_window = tracker_window

    # Difficulties stuff

    def _exec_trick_details(self, popup: TrickDetailsPopup):
        self._trick_details_popup = popup
        self._trick_details_popup.setWindowModality(Qt.WindowModal)
        self._trick_details_popup.open()

    def _open_trick_details_popup(self, trick: SimpleResourceInfo, level: LayoutTrickLevel):
        self._exec_trick_details(TrickDetailsPopup(
            self,
            self,
            default_database.default_prime2_game_description(),
            trick,
            level,
        ))

    def _open_difficulty_details_popup(self, difficulty: LayoutTrickLevel):
        self._exec_trick_details(TrickDetailsPopup(
            self,
            self,
            default_database.default_prime2_game_description(),
            None,
            difficulty,
        ))

    def _setup_difficulties_menu(self):
        game = default_database.default_prime2_game_description()
        for i, trick_level in enumerate(LayoutTrickLevel):
            if trick_level not in {LayoutTrickLevel.NO_TRICKS, LayoutTrickLevel.MINIMAL_LOGIC}:
                difficulty_action = QAction(self)
                difficulty_action.setText(trick_level.long_name)
                self.menu_difficulties.addAction(difficulty_action)
                difficulty_action.triggered.connect(functools.partial(self._open_difficulty_details_popup, trick_level))

        configurable_tricks = TrickLevelConfiguration.all_possible_tricks()
        tricks_in_use = used_tricks(game.world_list)

        for trick in sorted(game.resource_database.trick, key=lambda _trick: _trick.long_name):
            if trick.index not in configurable_tricks or trick not in tricks_in_use:
                continue

            trick_menu = QMenu(self)
            trick_menu.setTitle(trick.long_name)
            self.menu_trick_details.addAction(trick_menu.menuAction())

            used_difficulties = difficulties_for_trick(game.world_list, trick)
            for i, trick_level in enumerate(LayoutTrickLevel):
                if trick_level in used_difficulties:
                    difficulty_action = QAction(self)
                    difficulty_action.setText(trick_level.long_name)
                    trick_menu.addAction(difficulty_action)
                    difficulty_action.triggered.connect(
                        functools.partial(self._open_trick_details_popup, trick, trick_level))

    # ==========

    @asyncSlot()
    async def _on_validate_seed_change(self):
        old_value = self._options.advanced_validate_seed_after
        new_value = self.menu_action_validate_seed_after.isChecked()

        if old_value and not new_value:
            box = QMessageBox(self)
            box.setWindowTitle("Disable validation?")
            box.setText(_DISABLE_VALIDATION_WARNING)
            box.setIcon(QMessageBox.Warning)
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            box.setDefaultButton(QMessageBox.No)
            user_response = await async_dialog.execute_dialog(box)
            if user_response != QMessageBox.Yes:
                self.menu_action_validate_seed_after.setChecked(True)
                return

        with self._options as options:
            options.advanced_validate_seed_after = new_value

    def _on_generate_time_limit_change(self):
        is_checked = self.menu_action_timeout_generation_after_a_time_limit.isChecked()
        with self._options as options:
            options.advanced_timeout_during_generation = is_checked

    def _open_auto_tracker(self):
        from randovania.gui.auto_tracker_window import AutoTrackerWindow
        self.auto_tracker_window = AutoTrackerWindow(common_qt_lib.get_game_connection())
        self.auto_tracker_window.show()

    def _update_hints_text(self):
        game_description = default_database.default_prime2_game_description()

        number_for_hint_type = {
            hint_type: i + 1
            for i, hint_type in enumerate(LoreType)
        }
        used_hint_types = set()

        self.hint_tree_widget.setSortingEnabled(False)

        # TODO: This ignores the Dark World names. But there's currently no logbook nodes in Dark World.
        for world in game_description.world_list.worlds:

            world_item = QtWidgets.QTreeWidgetItem(self.hint_tree_widget)
            world_item.setText(0, world.name)
            world_item.setExpanded(True)

            for area in world.areas:
                hint_types = {}

                for node in area.nodes:
                    if isinstance(node, LogbookNode):
                        if node.required_translator is not None:
                            hint_types[node.lore_type] = node.required_translator.short_name
                        else:
                            hint_types[node.lore_type] = "✓"

                if hint_types:
                    area_item = QtWidgets.QTreeWidgetItem(world_item)
                    area_item.setText(0, area.name)

                    for hint_type, text in hint_types.items():
                        area_item.setText(number_for_hint_type[hint_type], text)
                        used_hint_types.add(hint_type)

        self.hint_tree_widget.resizeColumnToContents(0)
        self.hint_tree_widget.setSortingEnabled(True)
        self.hint_tree_widget.sortByColumn(0, QtCore.Qt.AscendingOrder)

        for hint_type in used_hint_types:
            self.hint_tree_widget.headerItem().setText(number_for_hint_type[hint_type], hint_type.long_name)
