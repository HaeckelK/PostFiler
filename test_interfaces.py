import os

import pytest  # noqa F401

from interfaces import (
    UploadDetails,
    LocalFileStorageInterface,
    RootDirectoryDoesNotExist,
    TextFileFieldInterface,
)


@pytest.fixture
def upload_details():
    details = UploadDetails(
        category="category",
        correspondenceType="correspondenceType",
        correspondenceDate="2021-03",
        original_filename="folder1/folder2/filename.png",
        upload_timestamp=0,
        storage_method="",
        storage_reference="",
    )
    return details


def test_upload_details_properties():
    details = UploadDetails(
        category="category",
        correspondenceType="correspondenceType",
        correspondenceDate="2021-03",
        original_filename="folder1/folder2/filename.png",
        upload_timestamp=0,
        storage_method="",
        storage_reference="",
    )
    assert details.extension == ".png"
    details.correspondenceDate = "2019-01"
    assert details.month == "01"
    assert details.year == "19"


def test_local_file_storage_interface_basename(upload_details):
    storage = LocalFileStorageInterface("")
    details = upload_details
    details.correspondenceDate = "2019-01"
    assert storage.create_basename(upload_details) == "1901_category_correspondenceType.png"


def test_local_file_storage_interface_add_file_root_directory_not_exist(upload_details, tmpdir):
    storage = LocalFileStorageInterface(os.path.join(tmpdir, "DOES_NOT_EXIST"))
    with pytest.raises(RootDirectoryDoesNotExist):
        storage.add_file(file=b"", details=upload_details)


def test_local_file_storage_interface_add_file(upload_details, tmpdir):
    os.mkdir(os.path.join(tmpdir, "storage"))
    storage = LocalFileStorageInterface(os.path.join(tmpdir, "storage"))
    storage.add_file(file=b"", details=upload_details)
    # TODO doesnt check contents saved
    assert len(os.listdir(os.path.join(tmpdir, "storage"))) == 1


def test_text_file_field_loader_empty(tmpdir):
    loader = TextFileFieldInterface(os.path.join(tmpdir, "fields.txt"))
    assert loader.load() == []


def test_text_file_field_loader_non_empty(tmpdir):
    # Given empty field data
    filename = os.path.join(tmpdir, "fields.txt")
    field_interface = TextFileFieldInterface(filename)
    # When a new field has been created
    field_interface.create("new_field")
    # Then present loader.load
    assert field_interface.load() == ["new_field"]


def test_text_file_field_creator_multiple(tmpdir):
    # Given empty field data
    filename = os.path.join(tmpdir, "fields.txt")
    field_interface = TextFileFieldInterface(filename)
    # When a new field has been created twice
    field_interface.create("new_field")
    field_interface.create("new_field")
    # Then present loader.load once
    assert field_interface.load() == ["new_field"]


def test_text_file_field_delete(tmpdir):
    # Given a non empty field data
    filename = os.path.join(tmpdir, "fields.txt")
    field_interface = TextFileFieldInterface(filename)
    field_interface.create("new_field")
    # When field deleted
    field_interface.delete("new_field")
    # Then not in load
    assert field_interface.load() == []
