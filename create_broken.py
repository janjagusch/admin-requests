import json
import subprocess
from typing import Dict, Iterator, List


def _get_full_name(info: Dict) -> str:
    return f"{info['subdir']}/{info['fn']}"


def _get_info(package, platform) -> Dict:
    cmd = ["mamba", "search", "--channel", "conda-forge", package, "--info", "--json", "--platform", platform]
    out = subprocess.run(
        cmd,
        encoding="utf8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert not out.stderr, out.stderr
    infos = json.loads(out.stdout)
    assert len(infos.keys()) == 1, f"Multiple keys found: {infos.keys()}."
    return infos[list(infos.keys())[0]]


def _write_file(obj: str, filepath: str):
    with open(filepath, mode="w") as fp:
        fp.write(obj)


def _main(searches: List[Dict], filepath: str) -> Iterator[str]:
    full_names = "\n".join([_get_full_name(info) for search in searches for info in _get_info(**search)])
    _write_file(full_names, filepath)


if __name__ == "__main__":
    searches = [
        {"package": "tabmat", "platform": "win-64"},
        {"package": "tabmat", "platform": "osx-64"},
        {"package": "tabmat", "platform": "linux-64"},
        {"package": "glum", "platform": "win-64"},
        {"package": "glum", "platform": "osx-64"},
        {"package": "glum", "platform": "linux-64"},
    ]
    _main(searches, "./broken/glum_and_tabmat.txt")
