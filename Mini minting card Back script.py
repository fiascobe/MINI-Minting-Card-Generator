import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

def create_back_pdf_layout(back_image_path, output_pdf):
    """
    Arranges a source PNG image onto an A4 PDF in a maximized grid,
    mirrored for back-side printing and centered on the page.
    """
    # --- Configuration (MODIFIED) ---
    # Set to match the maximized cut script
    card_width_mm, card_height_mm = 46, 56
    spacing_mm = 0
    margin_mm = 0  # Use 0 margin for maximization calculation

    # --- Convert all millimeter values to PDF points ---
    card_width = card_width_mm * mm
    card_height = card_height_mm * mm
    spacing = spacing_mm * mm
    margin = margin_mm * mm
    page_width, page_height = A4

    # --- NEW: Maximization Logic (from maximized_cut script) ---
    # Calculate the usable area of the page
    usable_width = page_width - (2 * margin)
    usable_height = page_height - (2 * margin)

    # Calculate how many cards can fit
    cards_per_row = int((usable_width + spacing) / (card_width + spacing))
    cards_per_col = int((usable_height + spacing) / (card_height + spacing))
    cards_per_page = cards_per_row * cards_per_col
    
    print(f"Calculated layout: {cards_per_row} columns x {cards_per_col} rows = {cards_per_page} total cards.")
    # --- End Maximization Logic ---
    
    # --- Centering Logic (now uses calculated values) ---
    # Calculate total grid dimensions
    grid_width = (cards_per_row * card_width) + ((cards_per_row - 1) * spacing)
    grid_height = (cards_per_col * card_height) + ((cards_per_col - 1) * spacing)

    # Find page center
    center_x = page_width / 2
    center_y = page_height / 2

    # Calculate the bottom-left corner of the *entire grid*
    grid_origin_x = center_x - (grid_width / 2)
    grid_origin_y = center_y - (grid_height / 2)
    # --- End Centering Logic ---

    # --- Create the new PDF canvas ---
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    # --- Place Images on PDF Grid (Mirrored and Centered Layout) ---
    # Loop for the new dynamically calculated number of cards
    for i in range(cards_per_page):
        # Determine the row and column for the current card
        # These now use the dynamic 'cards_per_row'
        row = i // cards_per_row
        col = i % cards_per_row

        # --- COORDINATE CALCULATION (Centered and Mirrored) ---
        
        # Invert column for horizontal mirroring (col 0 becomes 3, 1 becomes 2, etc.)
        # This places the first logical card (i=0) at the top-right grid position.
        inverted_col = (cards_per_row - 1 - col)
        x = grid_origin_x + inverted_col * (card_width + spacing)

        # Invert row for bottom-up Y-axis drawing (row 0 becomes 4, 1 becomes 3, etc.)
        # This places the first logical row (row=0) at the topmost grid position.
        inverted_row = (cards_per_col - 1 - row)
        y = grid_origin_y + (inverted_row * (card_height + spacing))
        
        # Draw the source image directly onto the PDF canvas.
        # The image will be scaled to fit the card_width and card_height.
        c.drawImage(back_image_path, x, y, width=card_width, height=card_height)

    # --- Finalize PDF ---
    c.save()
    
    print(f"Successfully generated centered, maximized back-side PDF: {output_pdf}")


if __name__ == "__main__":
    # Define the input PNG and output PDF filenames.
    back_image_file = 'back.png'
    output_pdf_file = 'back_layout_maximized.pdf' # Changed output name for clarity

    # Check if the required 'back.png' file exists before running.
    if not os.path.exists(back_image_file):
        print(f"Error: The file '{back_image_file}' was not found in this directory.")
        print("Please ensure you have a 'back.png' file in the same folder as the script.")
    else:
        # Call the main function with the image file.
        create_back_pdf_layout(back_image_file, output_pdf_file)
