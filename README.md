# pipeFit poster (web version)

Phone-friendly web version of the pipeFit poster: how a robot learns to see, rebuild and pick tangled tubes from a bin.

Xiaoxiao Zhang · Shiva Tutunchi · University West, Sweden · 2026

Live page: https://xiaoxiaoz.github.io/pipefit-poster/

Visitors can save the poster from the page: both pages as high-resolution images (`assets/pipefit-poster-page1.png`, `assets/pipefit-poster-page2.png`, 3840 × 2160) or as one PDF (`assets/pipefit-poster.pdf`). On iPhone the Save button opens the share sheet ("Save Image" puts the page in Photos).

This repository holds only the web page and its images. No code or data of the research project.

QR code for the page: `qr/pipefit-poster-qr-styled.png` (2000 × 2934, for print) and `qr/pipefit-poster-qr-styled.svg`: round dots, orange corner marks, a tube in the middle and a light orange caption band; error correction level H. Variant in the UR robot colours: `qr/pipefit-poster-qr-ur.png` / `.svg`. The plain version is `qr/pipefit-poster-qr.png` / `.svg`.

The tube in the middle of the QR code, large (3000 × 3000, for printed signs): `qr/pipefit-tube-logo.png` / `.svg` (transparent background) and `qr/pipefit-tube-logo-tile.png` / `.svg` (on a white rounded tile).

The 3-D view has two buttons: tubes only, and grasp candidates (`assets/bin3d_grasp.glb`: 6 candidates drawn as two-finger grippers, colour = rank). They come from pipeFit's rule-based pick hints on this reconstruction, with the hand allowed to tilt up to 30 deg about the tube axis; the poses are in `assets/grasp_candidates_s08_full.json` (robot base frame, mm).
