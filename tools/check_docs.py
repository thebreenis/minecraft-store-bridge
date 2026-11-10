"""Check local Markdown targets and source line anchors."""
import re
from pathlib import Path
from urllib.parse import unquote

def main():
    root=Path(__file__).resolve().parents[1]
    errors=[]
    for doc in root.rglob("*.md"):
        if ".git" in doc.parts:continue
        for link in re.findall(r"\]\(([^)]+)\)",doc.read_text(encoding="utf-8-sig")):
            if "://" in link or link.startswith("#"):continue
            target,_,anchor=unquote(link).partition("#")
            path=(doc.parent/target).resolve()
            if not path.exists():errors.append(f"{doc.relative_to(root)}: missing {link}")
            elif re.fullmatch(r"L\d+",anchor) and path.is_file():
                if int(anchor[1:])>len(path.read_text(encoding="utf-8-sig").splitlines()):
                    errors.append(f"{doc.relative_to(root)}: invalid line {link}")
    if errors:raise SystemExit("\n".join(errors))
    print("Local Markdown links and source line anchors passed")

if __name__=="__main__":main()
