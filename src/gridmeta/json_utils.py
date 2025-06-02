import json
import requests
from pathlib import Path
from jsonschema import validate


def fetch_schema_from_url(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def read_json(json_file_path: Path) -> dict:
    with open(json_file_path, "r", encoding="utf-8") as file_pointer:
        contents = json.load(file_pointer)
    return contents


def write_to_json_file(content: dict, out_json_file: Path):
    with open(out_json_file, "w", encoding="utf-8") as file_pointer:
        json.dump(content, file_pointer)


def validate_json_file_from_schema_file(json_file: Path, schema_file: Path):
    schema = read_json(schema_file)
    validate(instance=read_json(json_file), schema=schema)


def validate_json_file_from_schema_url(json_file: Path, schema_url: str):
    schema = fetch_schema_from_url(schema_url)
    validate(instance=read_json(json_file), schema=schema)


def validate_json_data_from_schema_file(json_data: dict, schema_file: Path):
    schema = read_json(schema_file)
    validate(instance=json_data, schema=schema)


def validate_json_data_from_schema_url(json_data: dict, schema_url: Path):
    schema = fetch_schema_from_url(schema_url)
    validate(instance=json_data, schema=schema)
