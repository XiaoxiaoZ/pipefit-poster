"""Build wara/index.html from index.html (2026-11-27).

The WARA page is the main page with another title ("WARA Robotics Challenge Event Team HVäst"), plus the team section
(team leader + students' photo grid) and the theory contact with a photo (tools/make_team.py, assets/team/team.json),
with every local path moved one level up. Run it after every change to index.html:

    python tools/build_wara.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TITLE = "WARA Robotics Challenge Event Team HVäst"


def sub1(t, old, new):
    assert t.count(old) == 1, (t.count(old), old[:80])
    return t.replace(old, new)


def build():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import make_team
    w = (REPO / "index.html").read_text(encoding="utf-8")
    w = make_team.wara_extras(w, make_team.load_team())
    w = sub1(w, "<title>pipeFit: how a robot learns to see tangled tubes</title>", "<title>" + TITLE + "</title>")
    w = sub1(w, '<meta property="og:title" content="pipeFit: how a robot learns to see tangled tubes">',
             '<meta property="og:title" content="' + TITLE + '">')
    w = sub1(w, "<h1>How a robot learns to see <span>tangled tubes</span></h1>",
             "<h1>WARA Robotics Challenge Event <span>Team HVäst</span></h1>")
    n0 = w.count("assets/")
    for a, b in [('src="assets/', 'src="../assets/'), ('href="assets/', 'href="../assets/'),
                 ('poster="assets/', 'poster="../assets/'), ('content="assets/', 'content="../assets/'),
                 ("'assets/", "'../assets/"), ('src="theory/', 'src="../theory/'), ('href="theory/', 'href="../theory/')]:
        w = w.replace(a, b)
    assert w.count("../assets/") == n0
    assert w.count("theory/") == w.count("../theory/") == 2
    (REPO / "wara" / "index.html").write_text(w, encoding="utf-8", newline="\n")
    print("wara/index.html rebuilt")


if __name__ == "__main__":
    build()
