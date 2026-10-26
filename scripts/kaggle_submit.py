"""Run a job on a free Kaggle GPU and fetch the results back into results/.

Usage:  python scripts/kaggle_submit.py --job pretrained
Needs the Kaggle CLI configured locally (token in ~/.kaggle/access_token or kaggle.json; never commit it)
and a phone-verified Kaggle account (GPU + internet in notebooks). The kernel is private.
The job clones this public repo, downloads UHCSDB (hash-verified) and the model weights at run time.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = "https://github.com/iamvisheshsrivastava/microscopy-active-learning.git"
OUT = "/kaggle/working/out"
JOBS = {
    # frozen pretrained backbones (DINOv2) on UHCSDB at 224 px
    "pretrained": [
        f"python scripts/run_real.py --encoder pretrained --backbone facebook/dinov2-small --size 224 "
        f"--device cuda --tag _real_dinov2_small --out {OUT}",
        f"python scripts/run_real.py --encoder pretrained --backbone facebook/dinov2-base --size 224 "
        f"--device cuda --tag _real_dinov2_base --out {OUT}",
    ],
    # second real source: Aachen-Heerlen steel SEM (CC0); probe image layout first
    "aachen_probe": [f"python scripts/prepare_aachen.py --probe --out {OUT}"],
    "aachen": [f"python scripts/prepare_aachen.py --crop-bottom 0 --out {OUT}"],
    # longer contrastive pretraining on GPU at 128 px
    "contrastive128": [
        f"python scripts/run_real.py --size 128 --epochs 150 --seeds 5 --device cuda "
        f"--tag _real_contrastive128_gpu --out {OUT}",
    ],
}

TEMPLATE = '''import os, subprocess
def sh(cmd):
    print("$", cmd, flush=True)
    r = subprocess.run(cmd, shell=True)
    assert r.returncode == 0, cmd
sh("git clone --depth 1 {repo} /tmp/repo")  # outside /kaggle/working so it is not returned as output
os.chdir("/tmp/repo")
sh("pip install -q --no-deps -e . && pip install -q transformers")
if {uhcsdb}:
    sh("python scripts/get_uhcsdb.py")
sh("nvidia-smi -L")
for cmd in {jobs!r}:
    sh(cmd)
'''


def kaggle(*args):
    r = subprocess.run(["kaggle", *args], capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", choices=list(JOBS), required=True)
    ap.add_argument("--out", default="results")
    ap.add_argument("--timeout-min", type=int, default=180)
    a = ap.parse_args(argv)
    user = re.search(r"username:\s*(\S+)", kaggle("config", "view")).group(1)
    slug = f"maldl-{a.job}"
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "job.py").write_text(TEMPLATE.format(
            repo=REPO, jobs=JOBS[a.job], uhcsdb=not a.job.startswith("aachen")), encoding="utf-8")
        (d / "kernel-metadata.json").write_text(json.dumps({
            "id": f"{user}/{slug}", "title": slug, "code_file": "job.py", "language": "python",
            "kernel_type": "script", "is_private": "true", "enable_gpu": "true",
            "enable_internet": "true", "dataset_sources": [], "competition_sources": [],
            "kernel_sources": []}), encoding="utf-8")
        print(kaggle("kernels", "push", "-p", str(d)))
        deadline = time.time() + 60 * a.timeout_min
        while time.time() < deadline:
            st = kaggle("kernels", "status", f"{user}/{slug}")
            print(st.splitlines()[-1] if st else "?", flush=True)
            if "COMPLETE" in st or "ERROR" in st or "CANCEL" in st:
                break
            time.sleep(30)
        # download into a temp dir and keep only small result files (never raw data or clones)
        dl = d / "download"
        dl.mkdir()
        print(kaggle("kernels", "output", f"{user}/{slug}", "-p", str(dl)))
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        for f in dl.rglob("*"):
            if f.is_file() and f.suffix in {".csv", ".png", ".md", ".log", ".npz"} \
                    and f.stat().st_size < 12e6:
                (out / f.name).write_bytes(f.read_bytes())
    print("results copied to", out)
    return 0 if "COMPLETE" in st else 1


if __name__ == "__main__":
    sys.exit(main())
