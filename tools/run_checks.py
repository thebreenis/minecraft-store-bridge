"""Run only synthetic/mocked tests; prohibit network and isolate runtime state."""
import sys, tempfile, types, unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"reference"/"runtime"))

def blocked(*args,**kwargs):
    raise AssertionError("Network operation attempted during offline tests")

def main():
    import requests
    with tempfile.TemporaryDirectory(prefix="store-bridge-tests-") as tmp:
        runtime=types.ModuleType("runtime_paths")
        runtime.STATE=Path(tmp)
        runtime.PACK=Path(tmp)
        runtime.CATALOG=Path(tmp)/"nonexistent-catalog.json"
        sys.modules["runtime_paths"]=runtime
        # The original reference imports only, with all state rooted above.
        with patch("socket.create_connection",blocked), patch("socket.socket.connect",blocked), patch.object(requests.sessions.Session,"request",blocked):
            suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"))
            result=unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__=="__main__":
    raise SystemExit(main())
