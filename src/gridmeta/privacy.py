from dataclasses import dataclass
from typing import List, Literal, Any
from itertools import groupby

import numpy as np


@dataclass
class PrivacySetting:
    path: str
    type: Literal["discrete", "continuous"]
    sensitivity: int
    epsilon: float
    is_sensitivity_in_percentage: bool


# Define privacy settings
LOW_PRIVACY_SETTINGS = [
    PrivacySetting("assets/transformers/*/kva", "discrete", 15, 10, True),
    PrivacySetting("assets/transformers/*/count", "discrete", 10, 10, True),
]

MODERATE_PRIVACY_SETTINGS = [
    PrivacySetting("assets/transformers/*/kva", "discrete", 15, 5, True),
    PrivacySetting("assets/transformers/*/count", "discrete", 10, 5, True),
]

HIGH_PRIVACY_SETTINGS = [
    PrivacySetting("assets/transformers/*/kva", "discrete", 15, 0.1, True),
    PrivacySetting("assets/transformers/*/count", "discrete", 10, 0.1, True),
]


def get_value_from_key_path(data: dict, key_path: List[str]) -> Any:
    """
    Navigate a nested dictionary using a list of keys and return the corresponding value.

    Parameters:
        data (dict): The dictionary to explore.
        key_path (List[str]): A list of keys to form the path.

    Returns:
        Any: The value corresponding to the key path, or None if the path doesn't exist.
    """
    for key in key_path:
        # If key is not found, return None
        if not isinstance(data, dict) or key not in data:
            return None
        data = data[key]

    return data


def set_value_from_key_path(data: dict, key_path: List[str], value: Any) -> Any:
    """
    Navigate a nested dictionary using a list of keys and set the corresponding value.

    Parameters:
        data (dict): The dictionary to explore.
        key_path (List[str]): A list of keys to form the path.
        value (Any): Set any value to the path if present.

    Returns:
        Any: The value corresponding to the key path, or None if the path doesn't exist.
    """
    # Iterate through the key path, except for the last key
    for key in key_path[:-1]:
        # If the key doesn't exist, create an empty dictionary at this key
        if key not in data or not isinstance(data[key], dict):
            msg = f"{key_path=} does not exist in {data=}"
            raise KeyError(msg)
        # Move deeper into the dictionary
        data = data[key]

    # Set the value at the last key in the key path
    data[key_path[-1]] = value
    return True


def add_differential_privacy(value: float, epsilon: float, sensitivity: float) -> float:
    """
    Apply Laplace noise for differential privacy.

    Parameters:
        value (int or float): The original value.
        epsilon (float): Privacy budget (smaller = more privacy).
        sensitivity (float): The maximum change in output for one data change.

    Returns:
        float: Privacy-protected value.
    """
    # Scale for Laplace noise
    scale = sensitivity / epsilon
    # Generate noise
    noise = np.random.laplace(loc=0, scale=scale)
    # Return noisy value
    return value + noise


def add_discrete_differential_privacy(value: int, epsilon: float, sensitivity: float) -> int:
    """
    Apply Discrete Laplace noise for differential privacy.

    Parameters:
        value (int): The original integer value.
        epsilon (float): Privacy budget (smaller = more privacy).
        sensitivity (int): The maximum change in output for one data change.

    Returns:
        int: Privacy-protected integer value.
    """
    # Compute probability parameter for discrete Laplace
    p = np.exp(-epsilon / sensitivity)

    # Sample from the discrete Laplace distribution
    u = np.random.uniform(-0.5, 0.5)
    sign = 1 if u > 0 else -1
    geom_sample = np.random.geometric(1 - p) - 1  # Geometric noise
    discrete_laplace_noise = sign * geom_sample

    # Return noisy integer value
    return int(value + discrete_laplace_noise)


def split_by_star(lst):
    # Group by the '*' and filter out empty groups
    return [list(group) for key, group in groupby(lst, lambda x: x == "*") if not key]


func_mapper = {
    "discrete": add_discrete_differential_privacy,
    "continuous": add_differential_privacy,
}


def get_updated_val(item: PrivacySetting, value: float | int) -> float | int:
    new_sensitivity = (
        value * item.sensitivity / 100 if item.is_sensitivity_in_percentage else item.sensitivity
    )
    return func_mapper[item.type](value, item.epsilon, new_sensitivity)


def update_data_recursively(key_paths: list[str], data: dict, item: PrivacySetting):
    value = get_value_from_key_path(data, key_paths[0])
    if len(key_paths) > 1:
        for val in value:
            update_data_recursively(key_paths[1:], val, item)
    else:
        set_value_from_key_path(data, key_paths[0], get_updated_val(item, value))


def apply_differential_privacy(data: dict, privacy_mode: Literal["low", "moderate", "high"]):
    privacy_setting: list[PrivacySetting] = {
        "low": LOW_PRIVACY_SETTINGS,
        "moderate": MODERATE_PRIVACY_SETTINGS,
        "high": HIGH_PRIVACY_SETTINGS,
    }[privacy_mode]

    for item in privacy_setting:
        key_paths = item.path.split("/")
        star_groups = split_by_star(key_paths)
        update_data_recursively(star_groups, data, item)
    return data
