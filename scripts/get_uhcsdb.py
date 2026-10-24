"""Fetch the UHCSDB micrographs (Zenodo-archived mirror) into data/raw/uhcs_mirror and verify hashes.

The original NIST host (hdl.handle.net/11256/940) was unreachable when this repo was built, so this uses
https://github.com/rydia001/UHCS_micrographs_mirror (doi:10.5281/zenodo.23050463, CC BY 3.0 US).
~580 MB. Hashes are checked against the mirror's own manifest (not against NIST).
Cite: DeCost et al., Integr. Mater. Manuf. Innov. 6, 197-205 (2017), doi:10.1007/s40192-017-0097-0.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from maldl.data.uhcsdb import verify_manifest  # noqa: E402

URL = "https://github.com/rydia001/UHCS_micrographs_mirror.git"


def main(dest="data/raw/uhcs_mirror"):
    dest = Path(dest)
    if not (dest / "manifest.json").exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", URL, str(dest)], check=True)
    n, problems = verify_manifest(dest)
    print(f"verified {n} images, {len(problems)} problems")
    for p in problems[:10]:
        print(" ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:2]))
