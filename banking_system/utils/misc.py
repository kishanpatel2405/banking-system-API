# utils/misc.py

import toml


def get_project_meta(file_path: str):
    try:
        with open(file_path, "r") as f:
            data = toml.load(f)
            return data.get("tool", {}).get("poetry", {})
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading {file_path}: {e}")
