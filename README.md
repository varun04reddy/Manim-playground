# Point Finder Dashboard (Streamlit)

An interactive dashboard to **upload a chart image**, **click the exact data points**, and **export those coordinates** for downstream plotting (e.g., Matplotlib) and curve-fitting/animation.

---

## What it does

* Upload a figure image (`.png`, `.jpg`, …).
* Optionally rotate to correct camera skew.
* Click points **directly on the image**; points are numbered in the order you click.
* Edit actions: **Undo last**, **Delete nearest**, **Clear all**, **Sort left→right**.
* Export **JSON** (and CSV) with both **pixel** and **normalized** coordinates.
* Optional preview: show an overlay and polynomial fits inside the dashboard.

---

## Tech & Dependencies

* Streamlit (UI)
* streamlit-drawable-canvas (clickable canvas)
* Pillow (image I/O & rotation)
* NumPy (numeric utilities)
* Matplotlib (optional in-app preview)

---

## Quickstart

1. Create/activate a virtual environment (recommended).
2. Install dependencies:

   ```bash
   pip install -r streamlit_app/requirements.txt
   ```

   Or manually:
   ```bash
   pip install streamlit==1.28.0 streamlit-drawable-canvas==0.9.3 pillow numpy matplotlib pandas
   ```

3. Run the dashboard:

   ```bash
   streamlit run streamlit_app/streamlit_app.py
   ```

4. Open the local URL Streamlit prints (usually `http://localhost:8501`).

> **Note:** The app runs entirely client-side on your machine. No images or coordinates are sent to any server unless you choose to.

---

## Using the Dashboard

1. **Upload Image**
   Drag-and-drop the book figure/photo into the uploader.

2. **Straighten (Optional)**
   Use the **Rotate** slider to compensate for slight camera tilt.

3. **Enable Canvas & Click Points**

   * Toggle **Enable canvas**.
   * **Left-click** to add a point (in order).
   * Points are numbered by click order.
   * Use **Undo last**, **Delete nearest**, or **Clear all** as needed.
   * Toggle **Sort left→right** to reorder points by X.

4. **Review Table**
   See a live table of pixel and normalized coordinates.

5. **Download**

   * **Download JSON** for downstream work (exact schema below).
   * **Download CSV** if you prefer spreadsheets.

6. **Preview (Optional)**
   Click **Preview overlay/fits** to see your points and sample polynomial fits rendered over the image inside the dashboard.

---

## Output Files

You’ll get two files, both derived from the image currently shown (after any rotation you applied):

### JSON (`*_points.json`)

* Purpose: a stable, library-agnostic artifact to load in plotting scripts.
* Contains the image size, raw pixel coordinates, and normalized coordinates.

**Schema**

```json
{
  "image_path": "uploaded_via_streamlit",
  "width": 1464,
  "height": 1952,
  "points_px": [[x1, y1], [x2, y2], "..."],
  "points_norm": [[x1/width, y1/height], [x2/width, y2/height], "..."],
  "rotate_deg": 0.0
}
```

### CSV (`*_points.csv`)

* Purpose: quick inspection and spreadsheet workflows.

**Header**

```
px_x,px_y,norm_x,norm_y
```

---

### Usage:
1. Export points from the Streamlit dashboard to `data/`
2. Open `notebooks/plot_points.ipynb`
3. Update file paths in the notebook cells to point to your data
4. Run cells to visualize, analyze, and export for Manim

---

## Project Structure

```
Manim-playground/
├── README.md
├── streamlit_app/          # Streamlit dashboard application
│   ├── streamlit_app.py    # Main dashboard code
│   └── requirements.txt    # Dashboard dependencies
├── data/                   # Data files and images
│   ├── test_image.png      # Sample image
│   ├── sample_points.csv   # Sample CSV export
│   ├── sample_points.json  # Sample JSON export
│   └── *_points.csv/json   # Downloaded point data goes here
├── notebooks/              # Jupyter notebooks for analysis
│   └── plot_points.ipynb   # Visualization and polynomial fitting
└── venv/                   # Virtual environment (not tracked)
```

### Directory Purpose

- **`streamlit_app/`**: Contains the interactive Point Finder Dashboard for extracting coordinates from images
- **`data/`**: Store your images and exported point data (CSV/JSON) here
- **`notebooks/`**: Jupyter notebooks for plotting, analysis, and preparing data for Manim animations

---
