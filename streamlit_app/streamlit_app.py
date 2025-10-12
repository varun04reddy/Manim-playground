import streamlit as st
import numpy as np
from PIL import Image
import io
import json
import pandas as pd
from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Point Finder Dashboard", layout="wide")

st.title("🎯 Point Finder Dashboard")
st.markdown("Upload an image, click data points, and export coordinates for plotting and animation.")

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points = []
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'rotation_angle' not in st.session_state:
    st.session_state.rotation_angle = 0.0
if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = 0

# Sidebar controls
st.sidebar.header("⚙️ Controls")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Image",
    type=['png', 'jpg', 'jpeg', 'bmp'],
    help="Upload a chart or figure image"
)

if uploaded_file is not None:
    # Load and store image
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image
    st.session_state.image_name = uploaded_file.name

if st.session_state.uploaded_image is not None:
    image = st.session_state.uploaded_image

    # Rotation slider
    st.sidebar.subheader("🔄 Straighten Image")
    rotation_angle = st.sidebar.slider(
        "Rotate (degrees)",
        min_value=-10.0,
        max_value=10.0,
        value=st.session_state.rotation_angle,
        step=0.1,
        help="Adjust to correct camera tilt"
    )
    st.session_state.rotation_angle = rotation_angle

    # Apply rotation
    if rotation_angle != 0:
        rotated_image = image.rotate(rotation_angle, expand=True, fillcolor='white')
    else:
        rotated_image = image

    # Get image dimensions
    img_width, img_height = rotated_image.size

    # Canvas settings
    st.sidebar.subheader("🖱️ Canvas Settings")
    enable_canvas = st.sidebar.checkbox("Enable canvas", value=True, help="Toggle to add points")
    point_radius = st.sidebar.slider("Point radius", 3, 15, 5, help="Visual size of points")

    # Point management
    st.sidebar.subheader("✏️ Edit Points")
    col1, col2 = st.sidebar.columns(2)

    if col1.button("↩️ Undo last"):
        if st.session_state.points:
            st.session_state.points.pop()
            st.session_state.canvas_key += 1
            st.rerun()

    if col2.button("🗑️ Clear all"):
        st.session_state.points = []
        st.session_state.canvas_key += 1
        st.rerun()

    sort_points = st.sidebar.checkbox("Sort left→right", value=False, help="Sort points by X coordinate")

    # Main canvas area
    st.subheader("📍 Click Points on Image")

    # Create canvas for point selection
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=point_radius * 2,
        stroke_color="#FF0000",
        background_image=rotated_image,
        update_streamlit=True,
        height=img_height,
        width=img_width,
        drawing_mode="point" if enable_canvas else "transform",
        point_display_radius=point_radius,
        key=f"canvas_{st.session_state.canvas_key}",
    )

    # Process canvas data
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data.get("objects", [])

        # Extract points from canvas
        new_points = []
        for obj in objects:
            if obj.get("type") == "circle":
                # Canvas gives top-left corner, add radius to get center
                radius = obj.get("radius", point_radius)
                x = obj.get("left", 0) + radius
                y = obj.get("top", 0) + radius
                new_points.append([x, y])

        # Update points if changed
        if len(new_points) != len(st.session_state.points):
            st.session_state.points = new_points

    # Sort points if requested
    display_points = st.session_state.points.copy()
    if sort_points and display_points:
        display_points.sort(key=lambda p: p[0])

    # Display point count
    st.info(f"📊 Points collected: **{len(display_points)}**")

    # Show table of coordinates
    if display_points:
        st.subheader("📋 Coordinates Table")

        # Calculate normalized coordinates
        points_data = []
        for i, (px_x, px_y) in enumerate(display_points):
            norm_x = px_x / img_width
            norm_y = px_y / img_height
            points_data.append({
                "Point": i + 1,
                "px_x": round(px_x, 2),
                "px_y": round(px_y, 2),
                "norm_x": round(norm_x, 4),
                "norm_y": round(norm_y, 4)
            })

        df = pd.DataFrame(points_data)
        st.dataframe(df, use_container_width=True)

        # Export section
        st.subheader("💾 Download Data")

        col1, col2, col3 = st.columns(3)

        # Prepare JSON export
        export_data = {
            "image_path": st.session_state.image_name,
            "width": img_width,
            "height": img_height,
            "points_px": [[round(x, 2), round(y, 2)] for x, y in display_points],
            "points_norm": [[round(x/img_width, 4), round(y/img_height, 4)] for x, y in display_points],
            "rotate_deg": rotation_angle
        }

        json_str = json.dumps(export_data, indent=2)

        with col1:
            st.download_button(
                label="📄 Download JSON",
                data=json_str,
                file_name=f"{st.session_state.image_name.rsplit('.', 1)[0]}_points.json",
                mime="application/json"
            )

        # Prepare CSV export
        csv_data = []
        for x, y in display_points:
            csv_data.append({
                "px_x": round(x, 2),
                "px_y": round(y, 2),
                "norm_x": round(x/img_width, 4),
                "norm_y": round(y/img_height, 4)
            })

        csv_df = pd.DataFrame(csv_data)
        csv_str = csv_df.to_csv(index=False)

        with col2:
            st.download_button(
                label="📊 Download CSV",
                data=csv_str,
                file_name=f"{st.session_state.image_name.rsplit('.', 1)[0]}_points.csv",
                mime="text/csv"
            )

        # Preview option
        with col3:
            show_preview = st.button("🔍 Preview overlay/fits")

        if show_preview and len(display_points) >= 2:
            st.subheader("🎨 Preview with Polynomial Fits")

            fig, ax = plt.subplots(figsize=(12, 8))
            ax.imshow(rotated_image)

            # Plot points
            points_array = np.array(display_points)
            ax.scatter(points_array[:, 0], points_array[:, 1],
                      c='red', s=100, marker='o', edgecolors='white', linewidths=2,
                      label='Clicked Points', zorder=5)

            # Add point numbers
            for i, (x, y) in enumerate(display_points):
                ax.text(x, y - 15, str(i+1),
                       fontsize=10, color='white', weight='bold',
                       ha='center', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

            # Fit polynomials if we have enough points
            if len(display_points) >= 3:
                x_coords = points_array[:, 0]
                y_coords = points_array[:, 1]

                # Sort by x for fitting
                sort_idx = np.argsort(x_coords)
                x_sorted = x_coords[sort_idx]
                y_sorted = y_coords[sort_idx]

                # Fit different degree polynomials
                degrees = [2, 3, 4] if len(display_points) >= 5 else [2, 3]
                colors = ['cyan', 'yellow', 'lime']

                x_smooth = np.linspace(x_sorted.min(), x_sorted.max(), 200)

                for degree, color in zip(degrees, colors):
                    if len(display_points) > degree:
                        coeffs = np.polyfit(x_sorted, y_sorted, degree)
                        poly = np.poly1d(coeffs)
                        y_smooth = poly(x_smooth)
                        ax.plot(x_smooth, y_smooth, color=color, linewidth=2,
                               alpha=0.7, label=f'Degree {degree}')

            ax.set_xlim(0, img_width)
            ax.set_ylim(img_height, 0)  # Invert Y axis
            ax.legend(loc='upper right')
            ax.set_title('Point Overlay with Polynomial Fits')
            ax.axis('off')

            st.pyplot(fig)
            plt.close()

    else:
        st.info("👆 Click on the image to add points. Enable canvas in the sidebar if needed.")

else:
    st.info("👈 Upload an image using the sidebar to get started!")
    st.markdown("""
    ### 📚 How to use:
    1. **Upload** a chart or figure image
    2. **Straighten** the image if needed using the rotation slider
    3. **Enable canvas** and click to add points
    4. **Edit** points using undo, clear, or sort options
    5. **Download** JSON/CSV with coordinates
    6. **Preview** to see your points with polynomial fits
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 About")
st.sidebar.markdown("Point Finder Dashboard v1.0")
st.sidebar.markdown("Extract data points from images for plotting and animation.")
