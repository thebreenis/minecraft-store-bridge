"""Explicitly fetch the pinned full build source. Never build or run it."""
import argparse,json,subprocess
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("destination",type=Path)
    args=p.parse_args()
    if args.destination.exists():
        p.error("Destination must not exist")
    lock=json.loads((Path(__file__).resolve().parents[1]/"upstream.lock.json").read_text())
    subprocess.run(["git","clone","--no-checkout",lock["repository"],str(args.destination)],check=True)
    subprocess.run(["git","-C",str(args.destination),"checkout","--detach",lock["commit"]],check=True)
    actual=subprocess.check_output(["git","-C",str(args.destination),"rev-parse","HEAD"],text=True).strip()
    if actual!=lock["commit"]:
        raise RuntimeError("Pinned revision mismatch")
    print("Pinned source fetched; no code executed:",actual)

if __name__=="__main__": main()
