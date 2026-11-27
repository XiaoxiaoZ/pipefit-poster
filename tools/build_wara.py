"""Build wara/index.html from index.html (2026-11-27).

The WARA page is the main page with another title ("WARA Robotics Challenge Event Team HVäst"), plus the team section
(team leader + students' photo grid) and the theory contact with a photo (tools/make_team.py, assets/team/team.json),
with every local path moved one level up. Run it after every change to index.html:

    python tools/build_wara.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TITLE = "WARA Robotics Challenge Event Team HVäst"
POSTER_LINK = """<section id="poster">
<div class="label">The poster</div>
<p class="muted" style="margin:0">The pipeFit poster, with both pages to save to your phone, is on the
<a href="../#poster">pipeFit digital poster</a> page.</p>
</section>"""


def sub1(t, old, new):
    assert t.count(old) == 1, (t.count(old), old[:80])
    return t.replace(old, new)


def build():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import make_team
    w = (REPO / "index.html").read_text(encoding="utf-8")
    # user 2026-11-27: the WARA page drops the thank-you line for the two students; their photos are in its team section
    w = sub1(w, '<p class="authors" style="margin-top:6px;font-size:0.9em;opacity:0.85">Thanks to <b>David Coronado Ecos</b> '
                'and <b>Vivek Dani Issac</b> for contributing features and tests.</p>\n', "")
    w = sub1(w, "<br>Thanks to David Coronado Ecos and Vivek Dani Issac for contributing features and tests.", "")   # footer
    # user 2026-11-27: no 'Save the poster' / 'Why not just use CAD or keypoints?' buttons in the header, and the poster
    # section becomes a link to the pipeFit digital poster page
    w, n = re.subn(r'<a class="btn primary getposter" href="#poster">.*?</a>\n', "", w, flags=re.S)
    assert n == 1
    w = sub1(w, '<a class="btn ghost getcompare" href="#compare">Why not just use CAD or keypoints? &darr;</a>\n', "")
    w, n = re.subn(r'<section id="poster">.*?</section>', lambda m: POSTER_LINK, w, flags=re.S)
    assert n == 1
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
