import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

def create_max_grid_pdf(output_pdf):
    """
    Generates a PDF with a maximized, centered grid of 40x50mm rectangles.
    """
    # --- Configuration ---
    # We use 40x50mm as it yields more rectangles (20) than 50x40mm (18)
    rect_width_mm, rect_height_mm = 40, 50
    spacing_mm = 6
    margin_mm = 10  # A safe margin for printing

    # --- Convert all millimeter values to PDF points ---
    rect_width = rect_width_mm * mm
    rect_height = rect_height_mm * mm
    spacing = spacing_mm * mm
    margin = margin_mm * mm
    page_width, page_height = A4

    # --- NEW: Maximization Logic ---
    # Calculate the usable area of the page
    usable_width = page_width - (2 * margin)
    usable_height = page_height - (2 * margin)

    # Calculate how many rectangles + spaces can fit
    # Formula: floor( (usable_dimension + spacing) / (rect_dimension + spacing) )
    rects_per_row = int((usable_width + spacing) / (rect_width + spacing))
    rects_per_col = int((usable_height + spacing) / (rect_height + spacing))
    total_rects = rects_per_row * rects_per_col
    
    print(f"Calculated layout: {rects_per_row} columns x {rects_per_col} rows = {total_rects} total rectangles.")

    # --- Centering Logic (now uses calculated values) ---
    # Calculate total grid dimensions
    grid_width = (rects_per_row * rect_width) + ((rects_per_row - 1) * spacing)
    grid_height = (rects_per_col * rect_height) + ((rects_per_col - 1) * spacing)

    # Find page center
    center_x = page_width / 2
    center_y = page_height / 2

    # Calculate the bottom-left corner of the *entire grid*
    grid_origin_x = center_x - (grid_width / 2)
    grid_origin_y = center_y - (grid_height / 2)
    # --- End Centering Logic ---

    # --- PDF Creation ---
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Set stroke color to black
    c.setStrokeColorRGB(0, 0, 0)
    # Set fill color to none (transparent)
    c.setFillColorRGB(1, 1, 1, alpha=0) 

    # --- Draw Rectangles on PDF Grid ---
    for i in range(total_rects):
        # Determine the row and column for the current card
        row = i // rects_per_row
        col = i % rects_per_row

        # Calculate the bottom-left corner of the rectangle
        # We invert the row for bottom-up drawing
        inverted_row = (rects_per_col - 1 - row)
        rect_base_x = grid_origin_x + col * (rect_width + spacing)
        rect_base_y = grid_origin_y + inverted_row * (rect_height + spacing)

        # Draw the rectangle (outline only)
        # Note: No bleed offset is needed here
        c.rect(rect_base_x, rect_base_y, rect_width, rect_height, stroke=1, fill=0)

    # --- Finalize PDF ---
    c.save()
    print(f"Successfully generated grid PDF: {output_pdf}")


if __name__ == "__main__":
    output_pdf_file = 'maximized_grid_layout.pdf'
    
    # Call the main function to create the PDF
    create_max_grid_pdf(output_pdf_file)
