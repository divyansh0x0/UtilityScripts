Based on your `ImageQualityModifier` class and helper functions, here is a documentation draft in a format suitable for a Word document.

---

# Documentation for Image Quality Modifier

## Project Overview
The **Image Quality Modifier** application allows users to load, modify, and save images by adjusting their resolution and quality. Developed using Pygame, it provides an interactive graphical interface to scale images and preview size changes in real-time.

---

## Table of Contents
1. Project Overview
2. Main Class: ImageQualityModifier
3. Helper Functions
4. Components Overview
5. Usage Instructions

---

### 1. Main Class: ImageQualityModifier
The `ImageQualityModifier` class is responsible for initializing and managing the image modification application. It provides functionalities for loading images, adjusting quality, displaying real-time previews, and saving modified images.

- **Attributes:**
  - `screen`: Pygame display screen.
  - `img_quality`: Image quality factor set by the slider.
  - `imgRenderPos`: Position to render the image on the screen.
  - `img_extension`: File extension of the loaded image.
  - `drag_delta`: Tracks image dragging offset.
  - `zoom`: Image zoom factor.
  - **Buttons and UI Elements**:
    - `save_btn`: Button to save modified images.
    - `resolution_slider`: Slider to adjust image quality.
    - `toast`: Toast message component to display notifications.
    - `img_information`: Dictionary storing image metadata.

- **Methods:**
  - `__init__`: Initializes Pygame components, sets up the display, and creates UI elements.
  - `update`: Updates UI elements' positions and resizes images based on user input.
  - `save_img`: Saves the modified image to disk.
  - `render`: Renders the UI, including image, buttons, and slider.
  - `load_img(path)`: Loads an image from a specified path.
  - `reload_img(path)`: Reloads an image, usually after a resolution change.
  - `draw_text`: Draws image metadata information on the screen.
  - `handle_event(event_data)`: Handles user input and interactions.
  - `loop`: Main application loop that updates the display and processes events.

### 2. Helper Functions
Helper functions assist with tasks like file validation and formatting.

- **is_valid_img_path(im_path)**  
  Checks if the image path is valid and whether the file is an acceptable image type.

- **format_byte_count(size_bytes)**  
  Converts a byte size into a human-readable format (e.g., KB, MB).

---

### 3. Components Overview

- **Button (from `components.button`)**  
  Handles the creation of buttons, specifically the "Save" button used to save the modified image.

- **Slider (from `components.slider`)**  
  Slider component allows users to adjust the quality of the image between 1 and 100%.

- **Toast (from `components.toast`)**  
  Displays temporary messages to notify users about actions like dragging an image or saving completion.

---

### 4. Usage Instructions
1. **Run the Program**: Execute the script to open the Image Quality Modifier application.
2. **Load an Image**: Drag and drop an image file into the application window.
3. **Adjust Image Quality**: Use the slider to adjust image quality. The application shows a real-time preview.
4. **Save the Modified Image**: Click the "Save" button to save the image with the new resolution and quality settings.

--- 

Would you like any adjustments or additional sections? This can be converted to a Word document with these headings and explanations, and I can add any diagrams if needed.