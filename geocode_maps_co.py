"""One-time geocoding for the Dudenhofen market dataset.

Run in this folder with: python3 geocode_maps_co.py
The API key is requested with hidden input and is never written to disk.
"""
import getpass
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data.json"
DATA_JS_PATH = ROOT / "data.js"
ZIP_PATH = ROOT / "dorfflohmarkt-dudenhofen-pwa.zip"
BASE = "https://geocode.maps.co/search"


def parts(address):
    street, _, rest = address.partition(",")
    postal, _, city = rest.strip().partition(" ")
    return street.strip(), postal.strip(), city.strip() or "Dudenhofen"


def query(key, address):
    street, postal, city = parts(address)
    params = urllib.parse.urlencode({
        "street": street,
        "city": city,
        "postalcode": postal or "67373",
        "country": "Germany",
        "countrycodes": "de",
        "format": "jsonv2",
        "limit": "1",
    })
    req = urllib.request.Request(
        f"{BASE}?{params}",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise RuntimeError("API-Schlüssel ungültig oder nicht berechtigt (HTTP %d)." % exc.code)
        if exc.code == 429:
            raise RuntimeError("Rate-Limit erreicht (HTTP 429); bitte später erneut starten.")
        raise RuntimeError("Geokodierungsdienst antwortet mit HTTP %d." % exc.code)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError("Geokodierungsdienst nicht erreichbar (%s)." % type(exc).__name__)


def write_data(data):
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    DATA_PATH.write_text(payload, encoding="utf-8")
    DATA_JS_PATH.write_text("window.MARKET_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")


def main():
    if not DATA_PATH.exists():
        sys.exit("data.json wurde nicht gefunden. Skript aus dem entpackten App-Ordner starten.")
    key = getpass.getpass("Geocode.maps.co API-Schlüssel (Eingabe bleibt verborgen): ").strip()
    if not key:
        sys.exit("Kein API-Schlüssel eingegeben.")
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    places = data["places"]
    pending = [p for p in places if not p.get("coordinates")]
    if not pending:
        print("Alle Standorte haben bereits Koordinaten.")
        return
    print(f"Geokodiere {len(pending)} Standorte. Übertragen wird jeweils nur die Adresse.")
    ok, unmatched = 0, []
    for i, place in enumerate(pending):
        try:
            results = query(key, place["address"])
        except RuntimeError as exc:
            print(f"Abbruch nach {i} erfolgreichen Abfragen: {exc}")
            break
        if results:
            result = results[0]
            try:
                place["coordinates"] = [float(result["lat"]), float(result["lon"])]
                place["geocodeMatch"] = result.get("display_name", "")
                ok += 1
            except (KeyError, TypeError, ValueError):
                unmatched.append(place["id"])
        else:
            unmatched.append(place["id"])
        if (i + 1) % 10 == 0 or i + 1 == len(pending):
            write_data(data)
            print(f"Fortschritt: {i + 1}/{len(pending)}; Treffer {ok}; ohne Treffer {len(unmatched)}")
        if i + 1 < len(pending):
            time.sleep(0.25)
    write_data(data)
    if ZIP_PATH.exists():
        files = ["index.html", "app.js", "data.json", "data.js", "manifest.webmanifest", "sw.js", "icon.svg", "marker.png", "README.md", "geocode_maps_co.py"]
        with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
            for name in files:
                archive.write(ROOT / name, name)
    print(f"Fertig. Treffer: {ok}; ohne Treffer: {len(unmatched)}.")
    if unmatched:
        print("Einträge ohne Treffer (IDs): " + ", ".join(unmatched))
    print("Koordinaten stehen in data.json; geocodeMatch enthält die Anbieter-Antwort zur Prüfung.")


if __name__ == "__main__":
    main()
