"""Regenerate source hashes/index from an explicitly supplied pinned checkout."""
import argparse,ast,hashlib,json,re,subprocess
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream",type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    lock=json.loads((root/"upstream.lock.json").read_text())
    mapping={"runtime":"Source/Runtime","native":"Source/Native","installer":"Source/Backend/Transfer"}
    entries=[]
    lines=["# Source map","",f"Generated from pinned commit {lock['commit']}. See the manifest for byte hashes.","",
           "The constants below are exact-build anchors, not portable offsets. Links point into the archived source.",""]
    for path in sorted((root/"reference").rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts: continue
        relative=path.relative_to(root)
        group=relative.parts[1]
        upstream=mapping[group]+"/"+path.name
        blob=subprocess.check_output(["git","-C",str(args.upstream),"show",lock["commit"]+":"+upstream])
        data=path.read_bytes()
        if blob!=data:raise ValueError("Snapshot differs from pinned Git blob: "+str(relative))
        entries.append({"path":relative.as_posix(),"upstreamPath":upstream,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)})
        text=data.decode("utf-8-sig")
        lines+=["## "+relative.as_posix(),""]
        if path.suffix==".py":
            tree=ast.parse(text)
            for node in tree.body:
                if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                    lines.append(f"- [{node.name}](../{relative.as_posix()}#L{node.lineno})")
                    if isinstance(node,ast.ClassDef):
                        for child in node.body:
                            if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)):
                                lines.append(f"  - [{node.name}.{child.name}](../{relative.as_posix()}#L{child.lineno})")
        elif path.suffix in (".cpp",".h"):
            for number,line in enumerate(text.splitlines(),1):
                if re.search(r"constexpr.*k\w+.*=",line):
                    lines.append(f"- [Line {number}](../{relative.as_posix()}#L{number}): `{line.strip()}`")
            if path.name in ("coin_checkout.h","store_ui.h","presence_filter.cpp"):
                for number,line in enumerate(text.splitlines(),1):
                    if re.match(r"^(?:bool|void|DWORD|std::string|StoreUiState).*\([^;]*\)\s*\{",line):
                        lines.append(f"- [Line {number}](../{relative.as_posix()}#L{number}): `{line.strip()}`")
        else:
            lines.append(f"[Read source](../{relative.as_posix()})")
        lines.append("")
    (root/"evidence/reference-manifest.json").write_text(json.dumps({"repository":lock["repository"],"commit":lock["commit"],"files":entries},indent=2)+"\n",encoding="utf-8")
    (root/"docs/15-source-map.md").write_text("\n".join(lines),encoding="utf-8")
    print("Generated and Git-blob-verified",len(entries),"source entries")

if __name__=="__main__":main()
