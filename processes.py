from typing import Dict, Any, List

from werkzeug.datastructures import FileStorage

from interfaces import (
    UploadInterface,
    UploadDetailsRecorder,
    CategoryCreator,
    CategoryLoader,
    TypeCreator,
    TypeLoader,
    FileStorageInterface,
)
from utils import unix_timestamp


def save_file_and_record_details(
    file: FileStorage,
    filename: str,
    details: Dict[str, Any],
    file_saver: UploadInterface,
    details_recorder: UploadDetailsRecorder,
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


def create_type(name: str, creator: TypeCreator) -> str:
    creator.create(name)
    message = f"Created type: {name}"
    return message


def load_types(loader: TypeLoader) -> List[str]:
    return loader.load()


def transfer_uploads_to_storage(
    upload_interface: UploadInterface, storage_writer: FileStorageInterface, details_loader: UploadDetailsRecorder
) -> None:
    # TODO record that this has taken place
    for reference, file_data in upload_interface.unprocessed_uploads():
        details = details_loader.get_details(reference)
        storage_writer.add_file(file_data, details=details)
        upload_interface.remove_file(reference)
    return
