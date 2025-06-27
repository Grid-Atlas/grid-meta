import tomli
import subprocess
import requests
from packaging import version
from pathlib import Path


def parse_dependencies(pyproject_path):
    with open(pyproject_path, "rb") as f:
        data = tomli.load(f)

    deps = set(data["project"].get("dependencies", []))

    for group in data["project"].get("optional-dependencies", {}).values():
        deps.update(group)

    # Filter out extras like 'package[foo]' and environment markers
    cleaned_deps = []
    for dep in deps:
        pkg = dep.split(";", 1)[0].strip().split("[", 1)[0].split(" ", 1)[0]
        if pkg:
            cleaned_deps.append(pkg)

    return sorted(set(cleaned_deps))


def get_latest_version(package):
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        resp = requests.get(url, timeout=5)
        if resp.ok:
            versions = list(resp.json()["releases"].keys())
            versions = [v for v in versions if not version.parse(v).is_prerelease]
            return max(versions, key=version.parse)
    except Exception:
        pass
    return None


def get_specified_version(package):
    result = subprocess.run(["pip", "show", package], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("Version:"):
            return line.split(":", 1)[1].strip()
    return None


def main():
    pyproject_path = Path("pyproject.toml")
    deps = parse_dependencies(pyproject_path)

    updates = []
    for dep in deps:
        dep = dep.split("~", 1)[0].strip()  # Remove any version specifiers like ~ or ==
        current = get_specified_version(dep)
        latest = get_latest_version(dep)
        if current and latest:
            if version.parse(latest).major > version.parse(current).major:
                updates.append(f"- **{dep}**: {current} → {latest}")

    output_file = Path("major_updates.txt")
    if updates:
        with output_file.open("w") as f:
            f.write("### 🚨 New Major Versions Detected\n\n")
            f.write("The following dependencies have newer **major versions** available:\n\n")
            f.writelines(line + "\n" for line in updates)
    elif output_file.exists():
        output_file.unlink()


if __name__ == "__main__":
    main()
