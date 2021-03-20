from abc import ABC, abstractmethod
from typing import Dict
import os
import json

from werkzeug.datastructures import FileStorage

from utils import unix_timestamp


class FileSaver(ABC):
    @abstractmethod
    def save(self, file: FileStorage, filename: str) -> str:
        """"""


class NullFileSaver(FileSaver):
    def save(self, file: FileStorage, filename: str) -> str:
        """Do nothing."""
        return "none"


class LocalFileSaver(FileSaver):
    def __init__(self, save_path: str) -> None:
        self.path = save_path
        return

    def save(self, file: FileStorage, filename: str) -> str:
        """"""
        savename = os.path.join(self.path, filename)
        file.save(savename)
        return savename


class FileDetailsRecorder(ABC):
    @abstractmethod
    def save(self, details: Dict[str, str]) -> str:
        """"""


class JSONFileDetailsRecorder(FileDetailsRecorder):
    def __init__(self, save_path: str) -> None:
        self.path = save_path
        return

    def save(self, details: Dict[str, str]) -> str:
        """"""
        filename = self._create_filename()
        while os.path.exists(filename):
            filename = self._create_filename()

        with open(filename, "w") as fp:
            json.dump(details, fp)
        return filename

    def _create_filename(self) -> str:
        basename = unix_timestamp()
        filename = os.path.join(self.path, f"{basename}.json")
        return filename
