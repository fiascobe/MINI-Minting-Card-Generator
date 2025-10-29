import os
try:
    from PIL import Image
except ImportError:
    print("Error: The 'Pillow' library is required for CMYK conversion.")
    print("Please install it by running: pip install Pillow")
    exit()
    
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

def create_back_pdf_layout(back_image_path, output_pdf):
    """
    Arranges a source PNG image (converted to CMYK) onto an A4 PDF
    in a maximized, mirrored, and centered grid.
    """
    # --- Configuration ---
    card_width_mm, card_height_mm = 46, 56
    spacing_mm = 0
    margin_mm = 0  
    dpi = 300

    # --- Convert all millimeter values to PDF points ---
    card_width = card_width_mm * mm
    card_height = card_height_mm * mm
    spacing = spacing_mm * mm
    margin = margin_mm * mm
    page_width, page_height = A4

    # --- Maximization Logic ---
    usable_width = page_width - (2 * margin)
    usable_height = page_height - (2 * margin)
    cards_per_row = int((usable_width + spacing) / (card_width + spacing))
    cards_per_col = int((usable_height + spacing) / (card_height + spacing))
    cards_per_page = cards_per_row * cards_per_col
    
    print(f"Calculated layout: {cards_per_row} columns x {cards_per_col} rows = {cards_per_page} total cards.")
    
    # --- Centering Logic ---
    grid_width = (cards_per_row * card_width) + ((cards_per_row - 1) * spacing)
    grid_height = (cards_per_col * card_height) + ((cards_per_col - 1) * spacing)
    center_x = page_width / 2
    center_y = page_height / 2
    grid_origin_x = center_x - (grid_width / 2)
    grid_origin_y = center_y - (grid_height / 2)

    # --- MODIFIED: Convert source image to CMYK ---
    temp_back_path = "temp_back_cmyk.jpg"
    try:
        print(f"Opening source image: {back_image_path}")
        # Open as RGBA to handle PNG transparency
        img_rgba = Image.open(back_image_path).convert("RGBA")
        
        # Create a new white CMYK background
        cmyk_image = Image.new("CMYK", img_rgba.size, (0, 0, 0, 0)) # CMYK white
        
        # Paste the RGBA image onto the CMYK background using its alpha mask
        # This correctly handles transparency and converts to CMYK
        cmyk_image.paste(img_rgba, mask=img_rgba.split()[3])
        
        # Save as a temporary CMYK JPEG
        cmyk_image.save(temp_back_path, "JPEG", dpi=(dpi, dpi), quality=95)
        print(f"Converted source image to CMYK and saved as {temp_back_path}")
        
    except Exception as e:
        print(f"Error converting '{back_image_path}' to CMYK: {e}")
        return
    # --- End CMYK Conversion ---


    # --- Create the new PDF canvas ---
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    # --- Place Images on PDF Grid (Mirrored and Centered Layout) ---
    for i in range(cards_per_page):
        row = i // cards_per_row
        col = i % cards_per_row

        # --- COORDINATE CALCULATION (Centered and Mirrored) ---
        inverted_col = (cards_per_row - 1 - col)
        x = grid_origin_x + inverted_col * (card_width + spacing)
        inverted_row = (cards_per_col - 1 - row)
        y = grid_origin_y + (inverted_row * (card_height + spacing))
        
        # --- MODIFIED: Draw the temporary CMYK image ---
        c.drawImage(temp_back_path, x, y, width=card_width, height=card_height)

    # --- Finalize PDF ---
    c.save()
    
    # --- MODIFIED: Cleanup temporary file ---
    if os.path.exists(temp_back_path):
        try:
            os.remove(temp_back_path)
            print(f"Cleaned up {temp_back_path}")
        except Exception as e:
            print(f"Warning: Could not remove temp file {temp_back_path}. {e}")
    
    print(f"Successfully generated centered, maximized CMYK back-side PDF: {output_pdf}")


if __name__ == "__main__":
    # Define the input PNG and output PDF filenames.
    back_image_file = 'back.png'
    # --- MODIFIED: Changed output name ---
    output_pdf_file = 'back_layout_mini_CMYK.pdf'

    # Check if the required 'back.png' file exists before running.
    if not os.path.exists(back_image_file):
        print(f"Error: The file '{back_image_file}' was not found in this directory.")
        print("Please ensure you have a 'back.png' file in the same folder as the script.")
    else:
        # Call the main function with the image file.
        create_back_pdf_layout(back_image_file, output_pdf_file)