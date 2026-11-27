# pipeFit poster (web version)

Phone-friendly web version of the pipeFit poster: how a robot learns to see, rebuild and pick tangled tubes from a bin.

Xiaoxiao Zhang · Shiva Tutunchi · University West, Sweden · 2026

Live page: https://xiaoxiaoz.github.io/pipefit-poster/

Visitors can save the poster from the page: both pages as high-resolution images (`assets/pipefit-poster-page1.png`, `assets/pipefit-poster-page2.png`, 3840 × 2160) or as one PDF (`assets/pipefit-poster.pdf`). On iPhone the Save button opens the share sheet ("Save Image" puts the page in Photos).

This repository holds only the web page and its images. No code or data of the research project.

QR code for the page: `qr/pipefit-poster-qr-styled.png` (2000 × 2934, for print) and `qr/pipefit-poster-qr-styled.svg`: round dots, orange corner marks, a tube in the middle and a light orange caption band; error correction level H. Variant in the UR robot colours: `qr/pipefit-poster-qr-ur.png` / `.svg`. The plain version is `qr/pipefit-poster-qr.png` / `.svg`.

The tube in the middle of the QR code, large (3000 × 3000, for printed signs): `qr/pipefit-tube-logo.png` / `.svg` (transparent background) and `qr/pipefit-tube-logo-tile.png` / `.svg` (on a white rounded tile).

The 3-D view has two buttons: tubes only, and grasp candidates (`assets/bin3d_grasp.glb`: 6 candidates drawn as two-finger grippers, colour = rank). They come from pipeFit's rule-based pick hints on this reconstruction, with the hand allowed to tilt up to 30 deg about the tube axis; the poses are in `assets/grasp_candidates_s08_full.json` (robot base frame, mm).

The theory section ("From a few visible pieces to the whole tube") embeds `theory/index.html`, an interactive demo in a plane with made-up data: candidates from sliding a piece along the recipe, the check against the other pieces, Levenberg–Marquardt refinement, and the joint refinement of two crossing tubes. In the poster page it runs in a frame (`theory/?embed=1`: light theme, the frame follows the demo's height); `theory/` on its own is the full page.

`wara/index.html` is a copy of the page for the WARA Robotics Challenge Event (title "WARA Robotics Challenge Event Team HVäst"; same content, paths one level up): https://xiaoxiaoz.github.io/pipefit-poster/wara/. Only the WARA page has the team section (team leader and the students' photo grid) and a photo in the theory contact; the main page has neither. Edit `index.html`, then run `python tools/build_wara.py` to rebuild the WARA page. Students are added with `python tools/make_team.py "<Name> <email>.png" ...` (list in `assets/team/team.json`); it rewrites both pages.
