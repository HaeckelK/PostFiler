from abc import ABC, abstractmethod
from typing import Dict, List, Generator, Tuple
import os
import json
from dataclasses import dataclass

from werkzeug.datastructures import FileStorage

from utils import unix_timestamp


class RootDirectoryDoesNotExist(Exception):
    pass


@dataclass
class UploadDetails:
    category: str
    correspondenceType: str
    correspondenceDate: str
    original_filename: str
    upload_timestamp: int
    storage_method: str
    storage_reference: str

    @property
    def extension(self) -> str:
        return os.path.splitext(self.original_filename)[1]

    @property
    def year(self) -> str:
        # TODO this has coupled to input box from html form
        return self.correspondenceDate.split("-")[0][-2:]

    @property
    def month(self) -> str:
        return self.correspondenceDate.split("-")[1][-2:]


class UploadInterface(ABC):
    @abstractmethod
    def save(self, file: FileStorage, filename: str) -> str:
        """"""

    def unprocessed_uploads(self) -> Generator[Tuple[str, bytes], None, None]:
        for reference in self.get_unprocessed_references():
            data = self.load_file(reference)
            yield reference, data

    @abstractmethod
    def remove_file(self, reference: str) -> None:
        """"""

    @abstractmethod
    def get_unprocessed_references(self) -> List[str]:
        """"""

    @abstractmethod
    def load_file(self, reference: str) -> bytes:
        """"""


class NullUploadInterface(UploadInterface):
    def save(self, file: FileStorage, filename: str) -> str:
        """Do nothing."""
        return "none"

    def remove_file(self, reference: str) -> None:
        """Do nothing."""
        return

    def get_unprocessed_references(self) -> List[str]:
        """"""
        return []

    def load_file(self, reference: str) -> bytes:
        """"""
        return b""


class LocalUploadInterface(UploadInterface):
    def __init__(self, save_path: str) -> None:
        self.path = save_path
        return

    def save(self, file: FileStorage, filename: str) -> str:
        """"""
        savename = os.path.join(self.path, filename)
        file.save(savename)
        return savename

    def remove_file(self, reference: str) -> None:
        return

    def get_unprocessed_references(self) -> List[str]:
        """"""
        return [os.path.join(self.path, x) for x in os.listdir(self.path)]

    def load_file(self, reference: str) -> bytes:
        """"""
        with open(reference, "rb") as f:
            data = f.read()
        return data


class UploadDetailsRecorder(ABC):
    @abstractmethod
    def save(self, details: Dict[str, str]) -> str:
        """"""

    @abstractmethod
    def get_details(self, reference: str) -> UploadDetails:
        """"""


class JSONUploadDetailsRecorder(UploadDetailsRecorder):
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

    def get_details(self, reference: str) -> UploadDetails:
        """"""
        found = False
        for basename in os.listdir(self.path):
            if basename.lower().endswith(".json") is False:
                continue
            with open(os.path.join(self.path, basename)) as f:
                data = json.load(f)
                details = UploadDetails(**data)
            if details.storage_reference == reference:
                found = True
                break
        if found is False:
            raise TypeError
        return details


class CategoryCreator(ABC):
    def create(self, name: str) -> None:
        """"""


class TextFileCategoryCreator(CategoryCreator):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        return

    def create(self, name: str) -> None:
        """"""
        with open(self.filename, "a") as f:
            f.write(name)
            f.write("\n")
        return


class CategoryLoader(ABC):
    def load(self) -> List[str]:
        """"""


class TextFileCategoryLoader(CategoryLoader):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        return

    def load(self) -> List[str]:
        """"""
        try:
            with open(self.filename, "r") as f:
                data = f.read().splitlines()
        except FileNotFoundError:
            return []
        return list(set(data))


class TypeCreator(ABC):
    def create(self, name: str) -> None:
        """"""


class TextFileTypeCreator(TypeCreator):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        return

    def create(self, name: str) -> None:
        """"""
        with open(self.filename, "a") as f:
            f.write(name)
            f.write("\n")
        return


class TypeLoader(ABC):
    def load(self) -> List[str]:
        """"""


class TextFileTypeLoader(TypeLoader):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        return

    def load(self) -> List[str]:
        """"""
        try:
            with open(self.filename, "r") as f:
                data = f.read().splitlines()
        except FileNotFoundError:
            return []
        return list(set(data))


class FileStorageInterface(ABC):
    @abstractmethod
    def add_file(self, file: bytes, details: UploadDetails) -> str:
        """"""


class LocalFileStorageInterface(FileStorageInterface):
    def __init__(self, save_path: str) -> None:
        self.path = save_path
        return

    def add_file(self, file: bytes, details: UploadDetails) -> str:
        """"""
        if os.path.exists(self.path) is False:
            raise RootDirectoryDoesNotExist
        basename = self.create_basename(details)
        filename = os.path.join(self.path, basename)
        with open(filename, "wb") as f:
            f.write(file)
        return filename

    def create_basename(self, details: UploadDetails) -> str:
        basename = (
            details.year + details.month + "_" + details.category + "_" + details.correspondenceType + details.extension
        )
        return basename
