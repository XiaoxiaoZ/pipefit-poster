"""Team section and theory contact for the poster pages (2026-11-27).

Where things go (user, 2026-11-27):
- the main pipeFit page (index.html) has NO team section and NO photos; its theory section ends with a text-only
  contact ("Want to know more?": name, title, email, staff page);
- the WARA copy (wara/index.html, built from index.html by tools/build_wara.py) has the team section after the header
  (team leader card, then the students' photo grid: point at / tap a photo to see the name and email) and the contact
  with a photo.

Each student photo file is named "<Full Name> <email>.<ext>" (as the user provides them). The script crops a 4:5
head-and-shoulders tile around the face, resizes it to 480x600 and saves it as WebP without metadata under
assets/team/<slug>.webp. assets/team/team.json keeps the leaders, the students (order of first addition) and the contact.

    python tools/make_team.py "C:/Users/me/Downloads/Jane Doe jane@x.se.png" ...   # add or replace students
    python tools/make_team.py --remove "Jane Doe"                                  # take a student out
    python tools/make_team.py                                                      # only rewrite both pages
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEAM = REPO / "assets" / "team"
LIST = TEAM / "team.json"
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def parse(path: Path):
    stem = path.stem if path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp") else path.name
    m = EMAIL.search(stem)
    if not m:
        sys.exit(f"no email in the file name: {path.name}")
    name = " ".join((stem[:m.start()] + " " + stem[m.end():]).split())
    if not name:
        sys.exit(f"no name in the file name: {path.name}")
    return name, m.group(0)


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "member"


def crop(src: Path, dst: Path) -> str:
    import cv2
    import numpy as np
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    W, H = im.size
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    faces = []
    for xml in ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml"):
        c = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, xml))
        for sf, mn in ((1.1, 6), (1.05, 4), (1.05, 3)):
            faces = [r for r in c.detectMultiScale(g, scaleFactor=sf, minNeighbors=mn, minSize=(W // 8, W // 8)) if r[2] >= 0.3 * W]
            if faces:
                break
        if faces:
            break
    if faces:
        x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
        cx, cy = x + w / 2, y + h / 2 + 0.12 * h
        ch = min(H, 2.9 * h)
        cw = ch * 4 / 5
        if cw > W:
            cw = W
            ch = cw * 5 / 4
        how = "face"
    else:
        cw = W
        ch = min(H, cw * 5 / 4)
        cx, cy = W / 2, min(H - ch / 2, max(ch / 2, 0.55 * H))
        how = "no face found (e.g. glasses): default crop, please look at the tile"
    left = int(round(min(max(cx - cw / 2, 0), W - cw)))
    top = int(round(min(max(cy - ch / 2, 0), H - ch)))
    tile = im.crop((left, top, left + int(cw), top + int(ch))).resize((480, 600), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tile.save(dst, "WEBP", quality=82, method=6)          # nothing but pixels: no exif, no icc
    return how


def img_src(img: str) -> str:
    """a local file under assets/team/, or a full https URL (e.g. the person's university staff page photo)"""
    return img if img.startswith("https://") else f"assets/team/{img}"


def person_card(p: dict, cls: str = "pcard", photo: bool = True) -> str:
    """one highlighted person: (photo,) badge, name, title, email and staff page"""
    e = html.escape
    page = f' &middot; <a href="{e(p["page"])}" target="_blank" rel="noopener">Staff page</a>' if p.get("page") else ""
    badge = f'<div class="pbadge">{e(p["role"])}</div>' if p.get("role") else ""
    title = f'<div class="ptitle">{e(p["title"])}</div>' if p.get("title") else ""
    pic = (f'<img class="pphoto" src="{img_src(p["img"])}" width="648" height="648" alt="{e(p["name"])}" '
           f'loading="lazy" referrerpolicy="no-referrer">') if photo and p.get("img") else ""
    return (f'<div class="{cls}">{pic}<div class="pbody">{badge}<div class="pname">{e(p["name"])}</div>{title}'
            f'<div class="pmail"><a href="mailto:{e(p["email"])}">{e(p["email"])}</a>{page}</div></div></div>')


def section(team: dict) -> str:
    """the WARA page's team section: team leader card(s), then the students' photo grid"""
    people = team["students"]
    leaders = "\n".join(person_card(p, "pcard lead") for p in team.get("leaders", []))
    lead = f'<div class="label accent">Team leader</div>\n{leaders}\n' if leaders else ""
    tiles = "\n".join(
        f'<button type="button" class="tm" data-name="{html.escape(p["name"])}" data-email="{html.escape(p["email"])}" '
        f'aria-label="{html.escape(p["name"])}, {html.escape(p["email"])}"><img src="{img_src(p["img"])}" '
        f'width="480" height="600" alt="{html.escape(p["name"])}" loading="lazy"><span class="tmname">{html.escape(p["name"])}</span></button>'
        for p in people)
    return f"""<!-- team:start (generated by tools/make_team.py) -->
<section id="team">
{lead}<div class="label accent"{' style="margin-top:22px"' if lead else ''}>Our students</div>
<div class="teamgrid" id="teamgrid">
{tiles}
</div>
<p class="tmcap" id="tmcap" aria-live="polite"><span class="hint">Point at or tap a photo to see who it is.</span></p>
</section>
<!-- team:end -->"""


CSS = """/* team:css */
.teamgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:10px}
.tm{position:relative;display:block;padding:0;border:0;background:var(--img);border-radius:14px;overflow:hidden;cursor:pointer;aspect-ratio:4/5;transition:transform .18s ease,opacity .18s ease,filter .18s ease,box-shadow .18s ease}
.tm img{width:100%;height:100%;object-fit:cover;display:block}
.tm .tmname{position:absolute;left:0;right:0;bottom:0;padding:6px 8px;background:rgba(26,28,32,.78);color:#fff;font-size:12.5px;font-weight:600;line-height:1.25;text-align:left;opacity:0;transition:opacity .18s ease}
.teamgrid:hover .tm:not(:hover),.teamgrid.has-active .tm:not(.active){opacity:.45;filter:grayscale(.6)}
.tm:hover,.tm:focus-visible,.tm.active{transform:scale(1.06);box-shadow:0 0 0 3px var(--accent),0 10px 24px rgba(26,28,32,.22);z-index:2;outline:none}
.tm:hover .tmname,.tm:focus-visible .tmname,.tm.active .tmname{opacity:1}
.tmcap{margin:12px 0 0;min-height:1.6em;font-size:16px;color:var(--ink2)}
.tmcap b{color:var(--ink)} .tmcap .hint{color:var(--ink3);font-size:14px}
@media (prefers-reduced-motion:reduce){.tm{transition:none}}
.pcard{display:flex;align-items:center;gap:16px;padding:14px;border-radius:16px;background:#fff;border:1px solid #E4E6EA}
.pcard.lead{border:2px solid var(--accent);box-shadow:0 6px 20px rgba(168,72,26,.14)}
.pphoto{flex:none;width:112px;height:112px;border-radius:14px;object-fit:cover;background:var(--img)}
.pcard.lead .pphoto{width:132px;height:132px}
.pbody{min-width:0}
.pbadge{display:inline-block;padding:3px 10px;border-radius:999px;background:var(--accent);color:#fff;font-size:12.5px;font-weight:700;letter-spacing:.3px;margin-bottom:6px}
.pname{font-family:'Space Grotesk',Inter,sans-serif;font-size:21px;font-weight:700;color:var(--ink);line-height:1.2}
.ptitle{font-size:14.5px;color:var(--ink2);margin-top:2px}
.pmail{font-size:15px;margin-top:6px;overflow-wrap:anywhere}
.contactbox{margin-top:26px;padding-top:18px;border-top:1px solid #E4E6EA}
@media (max-width:420px){.pphoto,.pcard.lead .pphoto{width:92px;height:92px}.pname{font-size:18px}.pcard{gap:12px;padding:12px}}
/* team:css-end */"""

JS = """<!-- team:js -->
<script>
(function () {
  var grid = document.getElementById('teamgrid'), cap = document.getElementById('tmcap');
  if (!grid || !cap) return;
  var hint = cap.innerHTML, tiles = grid.querySelectorAll('.tm');
  function show(t) {
    var n = t.getAttribute('data-name'), e = t.getAttribute('data-email'), b = document.createElement('b'), a = document.createElement('a');
    b.textContent = n; a.href = 'mailto:' + e; a.textContent = e;
    cap.innerHTML = ''; cap.appendChild(b); cap.appendChild(document.createTextNode(' \\u00b7 ')); cap.appendChild(a);
  }
  function current() { return grid.querySelector('.tm.active'); }
  for (var i = 0; i < tiles.length; i++) {
    tiles[i].addEventListener('mouseenter', function (ev) { show(ev.currentTarget); });
    tiles[i].addEventListener('focus', function (ev) { show(ev.currentTarget); });
    tiles[i].addEventListener('click', function (ev) {
      var t = ev.currentTarget, on = !t.classList.contains('active');
      for (var k = 0; k < tiles.length; k++) tiles[k].classList.remove('active');
      if (on) { t.classList.add('active'); show(t); } else if (!t.matches(':hover')) { cap.innerHTML = hint; }
      grid.classList.toggle('has-active', on);
    });
  }
  grid.addEventListener('mouseleave', function () { var a = current(); if (a) show(a); else cap.innerHTML = hint; });
})();
</script>
<!-- team:js-end -->
</body>"""


def contact_box(c: dict, photo: bool) -> str:
    return f"""<!-- contact:start (generated by tools/make_team.py) -->
<div class="contactbox">
<div class="label accent">Want to know more?</div>
<p class="muted" style="margin:0 0 10px">For more details about the theory or the method, contact {html.escape(c["name"].split()[0])}.</p>
{person_card(c, photo=photo)}
</div>
<!-- contact:end -->"""


def load_team() -> dict:
    raw = json.loads(LIST.read_text(encoding="utf-8")) if LIST.exists() else {}
    team = {"students": raw} if isinstance(raw, list) else raw
    team.setdefault("leaders", [])
    team.setdefault("students", [])
    return team


def put_contact(t: str, c: dict, photo: bool) -> str:
    box = contact_box(c, photo)
    if "<!-- contact:start" in t:
        return re.sub(r"<!-- contact:start.*?<!-- contact:end -->", lambda m: box, t, flags=re.S)
    s = t.index('<section id="theory">')
    e = t.index("</section>", s)
    return t[:e] + box + "\n" + t[e:]


def main_page(t: str, team: dict) -> str:
    """index.html: no team section, no team script, no photos; the card styles stay (the text-only contact uses them)"""
    t = re.sub(r"\n\n<!-- team:start.*?<!-- team:end -->", "", t, flags=re.S)
    t = re.sub(r"<!-- team:js -->.*?<!-- team:js-end -->\n", "", t, flags=re.S)
    if "/* team:css */" in t:
        t = re.sub(r"/\* team:css \*/.*?/\* team:css-end \*/", lambda m: CSS, t, flags=re.S)
    else:
        assert t.count("footer{margin-top:40px;") == 1
        t = t.replace("footer{margin-top:40px;", CSS + "\nfooter{margin-top:40px;")
    if team.get("contact"):
        t = put_contact(t, team["contact"], photo=False)
    assert "<!-- team:start" not in t and "<!-- team:js -->" not in t and 'class="pphoto"' not in t
    return t


def wara_extras(t: str, team: dict) -> str:
    """called by tools/build_wara.py on the copy of index.html, before the paths are moved one level up"""
    i = t.index("</header>") + len("</header>")
    t = t[:i] + "\n\n" + section(team) + t[i:]
    assert t.count("</body>") == 1
    t = t.replace("</body>", JS)
    if team.get("contact"):
        t = put_contact(t, team["contact"], photo=True)
    return t


def main(argv):
    team = load_team()
    people = team["students"]
    if argv[:1] == ["--remove"]:
        drop = set(argv[1:])
        people[:] = [p for p in people if p["name"] not in drop]
        argv = []
    for f in argv:
        src = Path(f)
        name, email = parse(src)
        img = slug(name) + ".webp"
        how = crop(src, TEAM / img)
        entry = {"name": name, "email": email, "img": img}
        old = next((k for k, p in enumerate(people) if p["name"] == name), None)
        if old is None:
            people.append(entry)
        else:
            people[old] = entry
        print(f"{name} <{email}> -> assets/team/{img} ({how})")
    LIST.parent.mkdir(parents=True, exist_ok=True)
    LIST.write_text(json.dumps(team, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    p = REPO / "index.html"
    p.write_text(main_page(p.read_text(encoding="utf-8"), team), encoding="utf-8", newline="\n")
    print(f"index.html: no team section, text-only contact: {bool(team.get('contact'))}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_wara
    build_wara.build()


if __name__ == "__main__":
    main(sys.argv[1:])
