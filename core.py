from typing import Dict, List
import os

from werkzeug.datastructures import FileStorage

import processes
from interfaces import (
    JSONUploadDetailsRecorder,
    LocalUploadInterface,
    FieldInterface,
    TextFileFieldInterface,
    LocalFileStorageInterface,
)


DATA_PATH = os.getenv("DETAILS_PATH", "")
FILES_PATH = os.getenv("FILES_PATH", "")
STORAGE_PATH = os.getenv("STORAGE_PATH", "")


assert DATA_PATH != ""
assert FILES_PATH != ""
assert STORAGE_PATH != ""

DETAILS_PATH = os.path.join(DATA_PATH, "file_details")
CONFIG_PATH = os.path.join(DATA_PATH, "config")


def save_file_and_record_details(file: FileStorage, filename: str, details: Dict[str, str]) -> None:
    file_saver = LocalUploadInterface(FILES_PATH)
    details_recorder = JSONUploadDetailsRecorder(save_path=DETAILS_PATH)
    processes.save_file_and_record_details(file, filename, details, file_saver, details_recorder)
    return


def get_category_interface() -> FieldInterface:
    return TextFileFieldInterface(os.path.join(CONFIG_PATH, "categories.txt"))


def get_type_interface() -> FieldInterface:
    return TextFileFieldInterface(os.path.join(CONFIG_PATH, "types.txt"))


def create_category(name: str) -> str:
    creator = TextFileFieldInterface(os.path.join(CONFIG_PATH, "categories.txt"))
    message = processes.create_field(name, creator)
    return message


def load_categories() -> List[str]:
    loader = TextFileFieldInterface(os.path.join(CONFIG_PATH, "categories.txt"))
    return processes.load_fields(loader)


def create_type(name: str) -> str:
    creator = TextFileFieldInterface(os.path.join(CONFIG_PATH, "types.txt"))
    message = processes.create_field(name, creator)
    return message


def load_types() -> List[str]:
    loader = TextFileFieldInterface(os.path.join(CONFIG_PATH, "types.txt"))
    return processes.load_fields(loader)


def transfer_uploads_to_storage() -> None:
    upload_interface = LocalUploadInterface(FILES_PATH)
    storage_writer = LocalFileStorageInterface(STORAGE_PATH)
    details_loader = JSONUploadDetailsRecorder(save_path=DETAILS_PATH)
    processes.transfer_uploads_to_storage(upload_interface, storage_writer, details_loader)
    return


def initial_setup():
    for directory in (DETAILS_PATH, CONFIG_PATH):
        if not os.path.exists(directory):
            os.mkdir(directory)
    return
