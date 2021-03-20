from typing import Dict, List
import os

from werkzeug.datastructures import FileStorage

import processes
from interfaces import (
    JSONFileDetailsRecorder,
    LocalFileSaver,
    TextFileCategoryCreator,
    TextFileCategoryLoader,
    TextFileTypeCreator,
    TextFileTypeLoader,
)


DETAILS_PATH = os.getenv("DETAILS_PATH", "")
FILES_PATH = os.getenv("FILES_PATH", "")

assert DETAILS_PATH != ""
assert FILES_PATH != ""


def save_file_and_record_details(file: FileStorage, filename: str, details: Dict[str, str]) -> None:
    file_saver = LocalFileSaver(FILES_PATH)
    details_recorder = JSONFileDetailsRecorder(save_path=DETAILS_PATH)
    processes.save_file_and_record_details(file, filename, details, file_saver, details_recorder)
    return


def create_category(name: str) -> str:
    creator = TextFileCategoryCreator(os.path.join(DETAILS_PATH, "categories.txt"))
    message = processes.create_category(name, creator)
    return message


def load_categories() -> List[str]:
    loader = TextFileCategoryLoader(os.path.join(DETAILS_PATH, "categories.txt"))
    return processes.load_categories(loader)


def create_type(name: str) -> str:
    creator = TextFileTypeCreator(os.path.join(DETAILS_PATH, "types.txt"))
    message = processes.create_type(name, creator)
    return message


def load_types() -> List[str]:
    loader = TextFileTypeLoader(os.path.join(DETAILS_PATH, "types.txt"))
    return processes.load_types(loader)
