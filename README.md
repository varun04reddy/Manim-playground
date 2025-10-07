# Point Finder Dashboard (Streamlit)

An interactive dashboard to **upload a chart image**, **click the exact data points**, and **export those coordinates** for downstream plotting (e.g., Matplotlib) and curve-fitting/animation.

---

## ✨ What it does

* Upload a figure image (`.png`, `.jpg`, …).
* Optionally rotate to correct camera skew.
* Click points **directly on the image**; points are numbered in the order you click.
* Edit actions: **Undo last**, **Delete nearest**, **Clear all**, **Sort left→right**.
* Export **JSON** (and CSV) with both **pixel** and **normalized** coordinates.
* Optional preview: show an overlay and polynomial fits inside the dashboard.

---

## 🧰 Tech & Dependencies

* Streamlit (UI)
* streamlit-drawable-canvas (clickable canvas)
* Pillow (image I/O & rotation)
* NumPy (numeric utilities)
* Matplotlib (optional in-app preview)

---

## 🚀 Quickstart

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

## 🖼️ Using the Dashboard

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

## 🗂️ Output Files

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

## 📐 Coordinate System

* Coordinates are in **image pixel space**.
* X grows to the **right**, Y grows **downward** (top-left is 0,0).
* Normalized coordinates are simply `(x/width, y/height)` and let you reuse points across scaled copies of the image.

---

## 🧭 User Controls

* **Left click:** add point
* **Undo last:** remove the most recent point
* **Delete nearest:** removes the point closest to your cursor
* **Clear all:** removes all points
* **Sort left→right:** reorders by X (useful for fitting/plotting)
* **Rotate slider:** fixes small photo tilt
* **Point radius:** visual size only (does not change data)

---

## 🔌 Integrating with Plotting/Analytics

Typical workflow to plot or animate:

1. Load the **JSON** in your plotting script/tool.
2. Sort the points by `px_x` (if not already sorted).
3. Plot the points over the **same rotated image** (or record and reapply the `rotate_deg` noted in JSON).
4. Fit polynomials of desired degrees using the `points_px` array as control points.
5. Render/animate your overlay curve(s) over the image.

> The dashboard is plotting-library-agnostic. Use Matplotlib, Plotly, or any other tool you prefer—just read the JSON and go.

---

## 📊 Analysis Notebook

The included Jupyter notebook (`notebooks/plot_points.ipynb`) provides comprehensive analysis tools:

### Features:
- **Load Data**: Import CSV or JSON exports from the dashboard
- **Pixel Space Plotting**: Visualize points in original image coordinates
- **Coordinate Transformation**: Convert to mathematical XY plane (origin at bottom-left)
- **Extended Range Plots**: See polynomial behavior with 30% whitespace padding to identify overfitting
- **Side-by-Side Comparison**: Compare polynomial degrees 2-6 in a grid view
- **Normalized Coordinates**: Transform to unit square [0,1]×[0,1] for Manim
- **Export for Animation**: Save transformed coordinates and polynomial coefficients as JSON

### Usage:
1. Export points from the Streamlit dashboard to `data/`
2. Open `notebooks/plot_points.ipynb`
3. Update file paths in the notebook cells to point to your data
4. Run cells to visualize, analyze, and export for Manim

---

## ✅ Acceptance Criteria

* Users can upload an image and click at least 5 points reliably.
* Edit actions (undo, delete nearest, clear, sort) work as described.
* **JSON/CSV** export matches the schema and includes normalized values.
* Re-loading the same image with the same `rotate_deg` reproduces the overlay alignment.
* Optional in-dashboard preview correctly displays points and example fits.

---

## 🧩 Nice-to-Haves (Post-MVP)

* Zoom/pan while clicking.
* Cropping tool (pre-click).
* Import/append from existing JSON.
* Adjustable marker/label styling.
* Keyboard entry for precise pixel coordinates.

---

## 📝 Project Structure

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

## 🔒 Privacy & Data

* Images and coordinates remain local to your machine.
* No network calls are required for the MVP.

---

## 🆘 Troubleshooting

* **Points don’t line up after export:**
  Ensure the same rotation (`rotate_deg`) is applied when overlaying.
* **Image looks skewed:**
  Nudge the **Rotate** slider by ±0.5–2.0 degrees.
* **Can’t click points:**
  Confirm **Enable canvas** is toggled on.

---

## 📄 License

MIT — free to use, modify, and distribute. Attribution appreciated.
