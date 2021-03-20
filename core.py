from typing import Dict
import os

from werkzeug.datastructures import FileStorage

import processes
from interfaces import JSONFileDetailsRecorder, LocalFileSaver


DETAILS_PATH = os.getenv("DETAILS_PATH", "")
FILES_PATH = os.getenv("FILES_PATH", "")

assert DETAILS_PATH != ""
assert FILES_PATH != ""

def save_file_and_record_details(file: FileStorage, filename: str, details: Dict[str, str]) -> None:
    file_saver = LocalFileSaver(FILES_PATH)
    details_recorder = JSONFileDetailsRecorder(save_path=DETAILS_PATH)
    processes.save_file_and_record_details(file, filename, details, file_saver, details_recorder)
    return
