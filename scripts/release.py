#!/usr/bin/env python3
"""Neue Version stempeln: python3 scripts/release.py "Was ist neu"
Zaehlt VERSION hoch, setzt VERSION_NAME (JJJJ.MM.TT.N, N = laufende Nummer pro Tag) in www/index.html
und traegt Version + Notiz oben in www/changelog.json ein. Danach committen, taggen (v<VERSION>), pushen."""
import json, re, sys, datetime, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
idx, chg = root / "www/index.html", root / "www/changelog.json"
note = " ".join(sys.argv[1:]).strip()
if not note:
    sys.exit('Bitte Notiz angeben: release.py "Was ist neu"')
h = idx.read_text(encoding="utf-8")
v = int(re.search(r"var VERSION=(\d+);", h).group(1)) + 1
log = json.loads(chg.read_text(encoding="utf-8")) if chg.exists() else []
today = datetime.date.today().isoformat()
n = 1 + sum(1 for e in log if e["date"] == today)
name = today.replace("-", ".") + "." + str(n)
h = re.sub(r"var VERSION=\d+;", f"var VERSION={v};", h, count=1)
if "var VERSION_NAME=" in h:
    h = re.sub(r"var VERSION_NAME='[^']*';", f"var VERSION_NAME='{name}';", h, count=1)
else:
    h = h.replace(f"var VERSION={v};", f"var VERSION={v};\nvar VERSION_NAME='{name}';", 1)
idx.write_text(h, encoding="utf-8")
log.insert(0, {"v": v, "name": name, "date": today, "notes": note})
chg.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"v{v} ({name}): {note}")
