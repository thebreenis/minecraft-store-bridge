"""Synthetic independent provider. No Microsoft APIs, currency or game assets."""
import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "catalog.json"

class Catalog:
    def __init__(self, path=FIXTURE):
        items = json.loads(Path(path).read_text(encoding="utf-8"))["items"]
        self.items = {item["id"]: item for item in items}
        if len(items) != len(self.items):
            raise ValueError("Duplicate offer IDs")
        self.owned = set()
        self.lock = threading.RLock()

    def compatibility(self, item):
        if item["comingSoon"]:
            return "S"
        minimum = item.get("minEngine")
        if minimum is None:
            return "U"
        return "C" if tuple(minimum) <= (1, 1, 5) else "I"

    def action(self, oid):
        item = self.items[oid]
        code = self.compatibility(item)
        with self.lock:
            owned = oid in self.owned
        if item["comingSoon"]:
            return {"label": "Coming Soon", "enabled": False, "owned": owned}
        free = type(item["price"]) is int and item["price"] == 0
        if not owned and free:
            return {"label": "Free", "enabled": True, "owned": False}
        if code != "C":
            return {"label": "Incompatible", "enabled": False, "owned": owned}
        # No pack payload or paid provider exists in this toy.
        return {"label": "Owned (no example download)" if owned else "Paid example disabled",
                "enabled": False, "owned": owned}

    def claim(self, oid):
        item = self.items[oid]
        if item["comingSoon"] or type(item["price"]) is not int or item["price"] != 0:
            raise ValueError("Only verified free synthetic offers are claimable")
        with self.lock:
            already = oid in self.owned
            self.owned.add(oid)
        return {"owned": True, "alreadyOwned": already, "id": oid, "provider": "synthetic"}

    def legacy_catalog(self):
        mapping = {"SkinPack":"skinpack", "WorldTemplate":"worldtemplate", "ResourcePack":"resourcepack"}
        results = []
        for item in self.items.values():
            results.append({"score": 1.0, "document": {
                "productId": item["id"], "documentId": item["id"],
                "title": item["title"], "description": item["description"],
                "contentType": "MarketplaceDurableCatalog_V1.1",
                "tags": [item["id"], mapping[item["packType"]]],
                "images": [], "contents": [], "price": item["price"],
                "custom": {"provider": "synthetic", "packType": mapping[item["packType"]]}}})
        return {"count": len(results), "results": results}

    def states(self):
        with self.lock:
            rows = [f"{oid}|{int(oid in self.owned)}|{int(type(i['price']) is int and i['price']==0)}|{self.compatibility(i)}"
                    for oid, i in self.items.items()]
        # BAL is a toy zero, not an official or real account balance.
        return "\n".join(rows + ["BAL|0", "TAG|Synthetic Example", ""])

def handler_for(catalog):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, data, text=False):
            body = data.encode() if text else json.dumps(data).encode()
            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8" if text else "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/catalog":
                self.reply(200, catalog.legacy_catalog())
            elif path == "/states":
                self.reply(200, catalog.states(), True)
            elif path.startswith("/offers/") and path[8:] in catalog.items:
                self.reply(200, catalog.items[path[8:]])
            else:
                self.reply(404, {"error": "unknown route"})

        def do_POST(self):
            # No external browser origin, no arbitrary payload or content fetch.
            if self.headers.get("Origin"):
                self.reply(403, {"error": "browser-origin mutation disabled"})
                return
            path = urlsplit(self.path).path
            if not path.startswith("/claim/"):
                self.reply(404, {"error": "unknown route"})
                return
            try:
                self.reply(200, catalog.claim(path[7:]))
            except (ValueError, KeyError):
                self.reply(400, {"error": "not a known claimable synthetic offer"})

        def log_message(self, *args):
            pass
    return Handler

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true")
    group.add_argument("--serve", action="store_true")
    args = parser.parse_args()
    catalog = Catalog()
    if args.demo:
        print(json.dumps(catalog.legacy_catalog(), indent=2))
        oid = next(iter(catalog.items))
        print(json.dumps(catalog.claim(oid)))
        print(catalog.states())
    else:
        with ThreadingHTTPServer(("127.0.0.1", 33224), handler_for(catalog)) as server:
            print("Synthetic-only provider at http://127.0.0.1:33224; Ctrl+C stops it.")
            server.serve_forever()

if __name__ == "__main__":
    main()
