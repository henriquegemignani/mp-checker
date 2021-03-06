import typing
from pathlib import Path
from typing import Iterator, Optional

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QCheckBox, QApplication, QFileDialog, QMainWindow, QWidget, QComboBox, QTextEdit, \
    QLineEdit

from randovania import get_data_path
from randovania.layout.layout_description import LayoutDescription
from randovania.layout.preset_migration import VersionedPreset


def map_set_checked(iterable: Iterator[QCheckBox], new_status: bool):
    for checkbox in iterable:
        checkbox.setChecked(new_status)


def lock_application(value: bool):
    QApplication.instance().main_window.setEnabled(value)


def _prompt_user_for_file(window: QMainWindow,
                          caption: str,
                          filter: str,
                          dir: Optional[str] = None,
                          new_file: bool = False) -> Optional[Path]:
    """
    Helper function for all `prompt_user_for_*` functions.
    :param window:
    :param caption:
    :param filter:
    :param new_file: If false, prompt for an existing file.
    :return: A string if the user selected a file, None otherwise
    """
    if new_file:
        method = QFileDialog.getSaveFileName
    else:
        method = QFileDialog.getOpenFileName
    open_result = method(window, caption=caption, dir=dir, filter=filter)
    if not open_result or open_result == ("", ""):
        return None
    return Path(open_result[0])


def prompt_user_for_vanilla_input_file(window: QMainWindow, extensions: typing.List[str],
                                       existing_file: Optional[Path] = None) -> Optional[Path]:
    """
    Shows an QFileDialog asking the user for a vanilla game file
    :param window:
    :param extensions:
    :param existing_file: An existing file to pre-fill with.
    :return: A string if the user selected a file, None otherwise
    """
    return _prompt_user_for_file(
        window,
        caption="Select the vanilla game {}.".format("/".join(extensions)),
        dir=str(existing_file) if existing_file is not None else None,
        filter=";".join(f"*.{ext}" for ext in extensions),
    )


def prompt_user_for_output_file(window: QMainWindow,
                                default_name: str,
                                extensions: typing.List[str]) -> Optional[Path]:
    """
    Shows an QFileDialog asking the user where to place the output file
    :param window:
    :param default_name: Name of a file that will be offered by default in the UI.
    :param extensions:
    :return: A string if the user selected a file, None otherwise
    """
    return _prompt_user_for_file(
        window,
        caption="Where to place the Randomized game file.",
        dir=default_name,
        filter=";".join(f"*.{ext}" for ext in extensions),
        new_file=True,
    )


def prompt_user_for_output_game_log(window: QMainWindow, default_name: str) -> Optional[Path]:
    """
    Shows an QFileDialog asking the user for a Randovania seed log
    :param window:
    :param default_name:
    :return: A string if the user selected a file, None otherwise
    """
    return _prompt_user_for_file(window, caption="Select a Randovania seed log.",
                                 dir=default_name,
                                 filter="Randovania Game, *.{}".format(LayoutDescription.file_extension()),
                                 new_file=True)


def prompt_user_for_input_game_log(window: QMainWindow) -> Optional[Path]:
    """
    Shows an QFileDialog asking the user for a Randovania seed log
    :param window:
    :return: A string if the user selected a file, None otherwise
    """
    return _prompt_user_for_file(window, caption="Select a Randovania seed log.",
                                 filter="Randovania Game, *.{}".format(LayoutDescription.file_extension()),
                                 new_file=False)


def prompt_user_for_database_file(window: QMainWindow) -> Optional[Path]:
    """
    Shows an QFileDialog asking the user for a Randovania database file
    :param window:
    :return: A string if the user selected a file, None otherwise
    """
    return _prompt_user_for_file(window, caption="Select a Randovania database file.", filter="*.json")


def prompt_user_for_preset_file(window: QMainWindow, new_file: bool) -> Optional[Path]:
    """
    Shows an QFileDialog asking the user for a Randovania preset file
    :param window:
    :param new_file: If it should be an existing file (False) or not.
    :return: A path if the user selected a file, None otherwise
    """
    return _prompt_user_for_file(window, caption="Select a Randovania Preset file.",
                                 filter=f"Randovania Preset, *.{VersionedPreset.file_extension()};;"
                                        f"All Files (*.*)",
                                 new_file=new_file)


def set_default_window_icon(window: QWidget):
    """
    Sets the window icon for the given widget to the default icon
    :param window:
    :return:
    """
    window.setWindowIcon(QIcon(str(get_data_path().joinpath("icons", "sky_temple_key_NqN_icon.ico"))))


def set_combo_with_value(combo: QComboBox, value):
    """
    Searches all items of the given combo for the given value and changes the current index to that one.
    :param combo:
    :param value:
    :return:
    """
    combo.setCurrentIndex(combo.findData(value))


def set_error_border_stylesheet(edit: QTextEdit, has_error: bool):
    edit.has_error = has_error
    if has_error:
        edit.setStyleSheet(":enabled { border: 1px solid red; }"
                           ":disabled { border: 1px solid red; background: #CCC }")
    else:
        edit.setStyleSheet("")


def set_edit_if_different(edit: QLineEdit, new_text: str):
    """
    Sets the text of the given QLineEdit only if it differs from the current value.
    Prevents snapping the user's cursor to the end unnecessarily.
    :param edit:
    :param new_text:
    :return:
    """
    if edit.text() != new_text:
        edit.setText(new_text)


def get_network_client():
    from randovania.gui.lib.qt_network_client import QtNetworkClient
    return typing.cast(QtNetworkClient, QApplication.instance().network_client)


def get_game_connection():
    from randovania.game_connection.game_connection import GameConnection
    return typing.cast(GameConnection, QApplication.instance().game_connection)


def show_install_visual_cpp_redist():
    from PySide2 import QtWidgets

    download_url = 'https://aka.ms/vs/16/release/vc_redist.x64.exe'
    support_url = 'https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads'

    QtWidgets.QMessageBox.critical(
        None,
        "Unable to load Dolphin backend",
        "Please install the latest "
        f"<a href='{download_url}'>Microsoft Visual C++ Redistributable</a>.<br /><br />"
        f"For more details, see <a href='{support_url}'>Microsoft's webpage</a>.")


def set_clipboard(text: str):
    from PySide2 import QtWidgets
    QtWidgets.QApplication.clipboard().setText(text)
