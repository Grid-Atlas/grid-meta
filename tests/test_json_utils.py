import requests
from pathlib import Path
import jsonschema
import json

import pytest

from gridmeta.json_utils import (
    fetch_schema_from_url,
    read_json,
    write_to_json_file,
    validate_json_file_from_schema_file,
    validate_json_file_from_schema_url,
    validate_json_data_from_schema_file,
    validate_json_data_from_schema_url,
)


def test_fetch_valid_schema(mocker):
    test_url = "https://example.com/schema.json"
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"type": "object"}
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    result = fetch_schema_from_url(test_url)

    mock_get.assert_called_once_with(test_url)
    mock_response.raise_for_status.assert_called_once()
    assert result == {"type": "object"}


def test_fetch_invalid_url(mocker):
    invalid_url = "invalid://url"
    mock_get = mocker.patch("requests.get", side_effect=requests.exceptions.InvalidURL)

    with pytest.raises(requests.exceptions.InvalidURL):
        fetch_schema_from_url(invalid_url)

    mock_get.assert_called_once_with(invalid_url)


def test_read_valid_json_file():
    test_file = Path("test_data.json")
    test_data = {"key": "value", "number": 42}
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    result = read_json(test_file)
    assert result == test_data
    test_file.unlink()


def test_write_valid_dict_to_json():
    test_dict = {"key1": "value1", "key2": {"nested": "value2"}}
    output_file = Path("test_output.json")

    write_to_json_file(test_dict, output_file)

    assert output_file.exists()
    with open(output_file, "r", encoding="utf-8") as fp:
        written_content = json.load(fp)
    assert written_content == test_dict
    output_file.unlink()


def test_valid_json_matches_schema(mocker):
    mock_json_file = Path("test.json")
    mock_schema_file = Path("schema.json")
    mock_json = {"name": "test", "value": 123}
    mock_schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "value": {"type": "number"}},
    }

    mock_read_json = mocker.patch("gridmeta.json_utils.read_json")
    mock_read_json.side_effect = [mock_schema, mock_json]

    validate_json_file_from_schema_file(mock_json_file, mock_schema_file)

    mock_read_json.assert_has_calls([mocker.call(mock_schema_file), mocker.call(mock_json_file)])


def test_empty_json_file(mocker):
    mock_json_file = Path("empty.json")
    mock_schema_file = Path("schema.json")
    mock_schema = {
        "type": "object",
        "properties": {"unit": {"type": "string"}},
        "required": ["unit"],
    }

    mock_read_json = mocker.patch("gridmeta.json_utils.read_json")
    mock_read_json.side_effect = [mock_schema, {}]

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate_json_file_from_schema_file(mock_json_file, mock_schema_file)

    mock_read_json.assert_has_calls([mocker.call(mock_schema_file), mocker.call(mock_json_file)])


def test_valid_json_validates_against_schema(mocker):
    mock_schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    mock_json = {"name": "test"}
    schema_url = "http://example.com/schema.json"
    json_file = Path("test.json")

    mock_fetch = mocker.patch("gridmeta.json_utils.fetch_schema_from_url")
    mock_fetch.return_value = mock_schema

    mock_read = mocker.patch("gridmeta.json_utils.read_json")
    mock_read.return_value = mock_json

    validate_json_file_from_schema_url(json_file, schema_url)

    mock_fetch.assert_called_once_with(schema_url)
    mock_read.assert_called_once_with(json_file)


def test_invalid_schema_url_raises_http_error(mocker):
    schema_url = "http://invalid-url.com/schema.json"
    json_file = Path("test.json")

    mock_fetch = mocker.patch("gridmeta.json_utils.fetch_schema_from_url")
    mock_fetch.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(requests.exceptions.HTTPError):
        validate_json_file_from_schema_url(json_file, schema_url)


def test_validate_json_data_with_valid_schema(mocker):
    mock_schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    }
    mock_json_data = {"name": "John", "age": 30}
    schema_file = Path("schema.json")
    mock_read_json = mocker.patch("gridmeta.json_utils.read_json", return_value=mock_schema)

    validate_json_data_from_schema_file(mock_json_data, schema_file)
    mock_read_json.assert_called_once_with(schema_file)


def test_validate_json_data_with_nonexistent_schema_file(mocker):
    mock_json_data = {"name": "John"}
    nonexistent_schema_file = Path("nonexistent.json")
    mocker.patch("gridmeta.json_utils.read_json", side_effect=FileNotFoundError)

    with pytest.raises(FileNotFoundError):
        validate_json_data_from_schema_file(mock_json_data, nonexistent_schema_file)


def test_valid_json_data_validates_against_schema(mocker):
    mock_schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    }
    mock_json_data = {"name": "John", "age": 30}
    schema_url = "http://example.com/schema.json"

    mock_fetch = mocker.patch("gridmeta.json_utils.fetch_schema_from_url")
    mock_fetch.return_value = mock_schema

    validate_json_data_from_schema_url(mock_json_data, schema_url)
    mock_fetch.assert_called_once_with(schema_url)


def test_invalid_schema_url_raises_http_error_2(mocker):
    json_data = {"name": "John"}
    invalid_url = "http://invalid-url.com/schema.json"

    mock_fetch = mocker.patch("gridmeta.json_utils.fetch_schema_from_url")
    mock_fetch.side_effect = requests.exceptions.HTTPError("404 Client Error")

    # Act & Assert
    with pytest.raises(requests.exceptions.HTTPError):
        validate_json_data_from_schema_url(json_data, invalid_url)

    mock_fetch.assert_called_once_with(invalid_url)
