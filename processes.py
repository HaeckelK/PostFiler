from typing import Dict, Any, List

from werkzeug.datastructures import FileStorage

from interfaces import FileSaver, FileDetailsRecorder, CategoryCreator, CategoryLoader
from utils import unix_timestamp


def save_file_and_record_details(
    file: FileStorage,
    filename: str,
    details: Dict[str, Any],
    file_saver: FileSaver,
    details_recorder: FileDetailsRecorder,
) -> None:
    reference = file_saver.save(file, filename)
    prepare_file_details(details, filename, storage_method=str(type(file_saver)), reference=reference)
    details_recorder.save(details)
    return


def prepare_file_details(details: Dict[str, Any], filename: str, storage_method: str, reference: str) -> Dict[str, Any]:
    details["original_filename"] = filename
    details["upload_timestamp"] = unix_timestamp()
    details["storage_method"] = storage_method
    details["storage_reference"] = reference
    return details


def create_category(name: str, creator: CategoryCreator) -> str:
    creator.create(name)
    message = f"Created category: {name}"
    return message


def load_categories(loader: CategoryLoader) -> List[str]:
    return loader.load()
