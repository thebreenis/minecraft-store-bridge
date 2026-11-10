"""Verify archival source bytes against the publication manifest; no network."""
import hashlib,json
from pathlib import Path

def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/"evidence/reference-manifest.json").read_text())
    lock=json.loads((root/"upstream.lock.json").read_text())
    assert manifest["commit"]==lock["commit"],"Commit mismatch"
    failures=[]
    listed=set()
    for entry in manifest["files"]:
        path=(root/entry["path"]).resolve()
        if root.resolve() not in path.parents:
            raise ValueError("Invalid manifest path")
        listed.add(entry["path"])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=entry["sha256"]:
            failures.append(entry["path"])
    actual={p.relative_to(root).as_posix() for p in (root/"reference").rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    failures.extend(sorted(actual-listed))
    if failures:
        raise SystemExit("Reference mismatch: "+", ".join(failures))
    print(f"Verified {len(listed)} reference files at {lock['commit']}")

if __name__=="__main__": main()
