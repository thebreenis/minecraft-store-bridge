"""Conservative publication audit. Not a substitute for reviewing staged files."""
import re,subprocess
from pathlib import Path

def main():
    root=Path(__file__).resolve().parents[1]
    files=subprocess.check_output(["git","-C",str(root),"ls-files","--cached","--others","--exclude-standard"],text=True).splitlines()
    findings=[]
    forbidden={".appx",".msix",".tipa",".ipa",".exe",".dll",".pfx",".p12",".pem",".key",".png",".jpg",".etl",".dmp"}
    patterns=[
        ("populated Xbox credential",re.compile(r"XBL3\.0 x=\d+;[A-Za-z0-9+/=_-]{30,}")),
        ("JWT-shaped material",re.compile(r"eyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}")),
        ("private key",re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----")),
        ("absolute user profile path",re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+[\\/]")),
    ]
    for name in sorted(set(files)):
        path=root/name
        if not path.is_file():continue
        if path.suffix.lower() in forbidden:findings.append(name+": forbidden artifact extension")
        if path.stat().st_size>2*1024*1024:findings.append(name+": large file needs review")
        try:text=path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            findings.append(name+": binary content needs review");continue
        for label,pattern in patterns:
            if pattern.search(text):findings.append(name+": "+label)
    if findings:raise SystemExit("\n".join(findings))
    print("Publication audit passed for",len(set(files)),"files; review staged diff before publishing.")

if __name__=="__main__":main()
