import streamlit as st
from PIL import Image
import os
from io import BytesIO

def changeface(face_image):
    # Load the color palette image (assuming it's a grid of squares)
    palette_image_path = 'Palette.png'  # Path to the palette image
    try:
        palette_image = Image.open(palette_image_path)
    except FileNotFoundError:
        st.error("Palette image not found.")
        return None
    
    # Load the new face image to be placed on each square
    new_face_image = Image.open(face_image).convert("RGBA")
    
    # Define the size of each square in the palette (assuming all squares are the same size)
    square_size = (800, 800)  # Width, height of each square (adjust based on your palette)

 # Check if the face image size is 500x500 or 400x500
    if face_width == 550 and face_height == 550:
        face_size = (550, 550)  # Face size to fit in the squares (500x500)
    elif face_width == 400 and face_height == 500:
        face_size = (400, 500)  # Face size to fit in the squares (400x500)
    else:
        st.error("Unsupported face image size. Please upload a face image with dimensions 500x500 or 400x500.")
        return None
    
    palette_width, palette_height = palette_image.size
    
    # Resize the new face image to match the face size
    new_face_image_resized = new_face_image.resize(face_size, Image.Resampling.LANCZOS)

    rows = 9
    cols = 24
    
    # Define the horizontal and vertical gaps to center the face within each square
    gap_x = (square_size[0] - face_size[0]) // 2  # Horizontal gap
    gap_y = (square_size[1] - face_size[1]) // 2  # Vertical gap
    
    # Loop through each square in the palette and replace the face
    for row in range(rows):
        for col in range(cols):
            # Calculate the top-left corner of the current square
            left = col * square_size[0] + gap_x  # Add horizontal gap
            top = row * square_size[1] + gap_y  # Add vertical gap
            
            # Ensure that the face doesn't go beyond the palette boundaries
            if left + face_size[0] <= palette_width and top + face_size[1] <= palette_height:
                # Paste the new face with transparency using the image as its own mask
                palette_image.paste(new_face_image_resized, (left, top), new_face_image_resized)
    
    # Save the updated palette image into a BytesIO object to avoid saving it to disk
    img_bytes = BytesIO()
    palette_image.save(img_bytes, format="PNG", dpi=(300, 300))  # Save in PNG format with HD quality
    img_bytes.seek(0)  # Reset the stream position to the beginning

    return img_bytes


# Streamlit UI
st.title('Palette Face Changer')

# File upload for face image
uploaded_face = st.file_uploader("Upload your face image", type=["png", "jpg", "jpeg"])

# If face is uploaded, update the grid
if uploaded_face is not None:
    # Display the uploaded face image
    st.image(uploaded_face, caption="Uploaded Face Image", use_column_width=True)
    
    # Change face and generate the new palette image
    if st.button("Generate Palette"):
        output_image_bytes = changeface(uploaded_face)
        if output_image_bytes:
            st.image(output_image_bytes, caption="Updated Palette", use_column_width=True)
            
            # Provide a link to download the generated image
            st.download_button(
                label="Download the updated palette",
                data=output_image_bytes,
                file_name="updated_palette.png",
                mime="image/png"
            )
