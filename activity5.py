import streamlit as st
import cv2
import numpy as np
from datetime import datetime

st.title("🎥 Snapshots")

# Sliders for filter thresholds
brightness = st.slider("Brightness", 0, 100, 50)
contrast = st.slider("Contrast", 0, 100, 50)
apply_gray = st.checkbox("Grayscale Filter")
apply_canny = st.checkbox("Canny Edge Detection")
apply_blur = st.checkbox("Gaussian Blur")
apply_sepia = st.checkbox("Sepia Filter")

# Button for snapshot
snapshot_button = st.button("📸 Take Snapshot")

# Start video capture
cap = cv2.VideoCapture(0)

frame_placeholder = st.empty()

def apply_sepia_filter(frame):
    """Applies a sepia filter to the frame."""
    frame_sepia = np.array(frame, dtype=np.float64)
    frame_sepia = cv2.transform(frame_sepia, np.array([[0.393, 0.769, 0.189],
                                                       [0.349, 0.686, 0.168],
                                                       [0.272, 0.534, 0.131]]))
    frame_sepia = np.clip(frame_sepia, 0, 255)
    return np.uint8(frame_sepia)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Apply brightness and contrast adjustments
    brightness_val = brightness - 50
    contrast_val = contrast - 50
    frame = cv2.convertScaleAbs(frame, alpha=1 + contrast_val / 50, beta=brightness_val)

    # Apply grayscale filter if selected
    if apply_gray:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    # Apply Canny edge detection if selected
    if apply_canny:
        edges = cv2.Canny(frame, 100, 200)
        frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Apply Gaussian blur if selected
    if apply_blur:
        frame = cv2.GaussianBlur(frame, (15, 15), 0)

    # Apply Sepia filter if selected
    if apply_sepia:
        frame = apply_sepia_filter(frame)

    # Convert BGR to RGB for Streamlit
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame_rgb, channels="RGB")

    # Take snapshot if requested
    if snapshot_button:
        filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(filename, frame)
        st.success(f"Snapshot saved as {filename}")
        snapshot_button = False  # Reset snapshot button

    # Allow continuous viewing of video
    if snapshot_button is False:
        break

cap.release()
