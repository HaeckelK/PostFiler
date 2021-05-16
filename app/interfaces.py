from abc import ABC, abstractmethod
from typing import Dict, List, Generator, Tuple
import os
import shutil
import json
from dataclasses import dataclass
import re

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


class LocalFile:
    def __init__(self, save_path: str) -> None:
        self.path = save_path
        return

    def check_root_exists(self) -> None:
        if os.path.exists(self.path) is False:
            raise RootDirectoryDoesNotExist


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
        self.unprocessed_path = os.path.join(save_path, "unprocessed")
        self.processed_path = os.path.join(save_path, "processed")
        for directory in (self.processed_path, self.unprocessed_path):
            if not os.path.exists(directory):
                os.mkdir(directory)
        return

    def save(self, file: FileStorage, filename: str) -> str:
        """"""
        savename = os.path.join(self.unprocessed_path, str(unix_timestamp()) + filename)
        file.save(savename)
        return savename

    def remove_file(self, reference: str) -> None:
        """Move file into a processed folder."""
        basename = os.path.basename(reference)
        newname = os.path.join(self.processed_path, basename)
        shutil.move(reference, newname)
        return

    def get_unprocessed_references(self) -> List[str]:
        """"""
        return [os.path.join(self.unprocessed_path, x) for x in os.listdir(self.unprocessed_path)]

    def load_file(self, reference: str) -> bytes:
        """"""
        with open(reference, "rb") as f:
            data = f.read()
        return data


# TODO rename from Recorder - it is read and write
class UploadDetailsRecorder(ABC):
    @abstractmethod
    def save(self, details: Dict[str, str]) -> str:
        """"""

    @abstractmethod
    def get_details(self, reference: str) -> UploadDetails:
        """"""

    # TODO make this a generator
    @abstractmethod
    def get_details_all(self) -> List[UploadDetails]:
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
            # TODO this TypeError must be caught and logged, otherwise missing details will mean the file can
            # never be processed, and the system will never get past this point.
            raise TypeError
        return details

    def get_details_all(self) -> List[UploadDetails]:
        """"""
        output = []
        for basename in os.listdir(self.path):
            if basename.lower().endswith(".json") is False:
                continue
            with open(os.path.join(self.path, basename)) as f:
                data = json.load(f)
                details = UploadDetails(**data)
            output.append(details)
        return output


class FieldInterface(ABC):
    @abstractmethod
    def create(self, name: str) -> None:
        """"""

    @abstractmethod
    def load(self) -> List[str]:
        """"""

    @abstractmethod
    def delete(self, name: str) -> None:
        """"""


class TextFileFieldInterface(FieldInterface):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        return

    def create(self, name: str) -> None:
        """"""
        with open(self.filename, "a") as f:
            f.write(name)
            f.write("\n")
        return

    def load(self) -> List[str]:
        """"""
        try:
            with open(self.filename, "r") as f:
                data = f.read().splitlines()
        except FileNotFoundError:
            return []
        data = [x for x in data if x != ""]
        return list(set(data))

    def delete(self, name: str) -> None:
        with open(self.filename, "r") as f:
            data = f.read()
        regex = r"^" + name + "$"
        subst = ""
        result = re.sub(regex, subst, data, 0, re.MULTILINE)
        with open(self.filename, "w") as f:
            f.write(result)
        return


class FileStorageInterface(ABC):
    @abstractmethod
    def add_file(self, file: bytes, details: UploadDetails) -> str:
        """"""


class LocalFileStorageInterface(FileStorageInterface, LocalFile):
    def add_file(self, file: bytes, details: UploadDetails) -> str:
        """"""
        self.check_root_exists()
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
