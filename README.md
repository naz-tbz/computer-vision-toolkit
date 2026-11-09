# Computer Vision Toolkit

This Python computer vision project organized into two parts.

## Part 1 — Mini Photo Editor

Features: brightness, contrast, grayscale, padding, thresholding, image blending, undo, operation history, and saving.

Run from the project root:

```bash
cd part1
python main.py
```

When prompted, enter the path to an image on your computer (for example, `photo.jpg` if you place a photo in `part1`). The program uses an interactive menu and shows previews using Matplotlib. Sample images from the original archive were intentionally excluded; supply your own non-private images.

## Part 2 — Face and Smile Detector

Uses your webcam, OpenCV, and two included Haar cascade XML files. It detects faces and smiles and automatically saves cropped smiling faces to a `smiling_faces` folder.

Run from the project root:

```bash
cd part2
python face_smile_detector.py
```

Press `q` to exit. Run from inside `part2` because the original program uses relative paths for its Haar cascade files. The saved `smiling_faces` images should not be committed to GitHub.

## Installation

Python 3 and a working webcam (for Part 2) are required.

```bash
python -m pip install -r requirements.txt
```
