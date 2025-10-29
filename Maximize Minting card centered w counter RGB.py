import os
import re
from PIL import Image, ImageDraw, ImageFont
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

# ==============================================================================
# PART 1: QR Code Generation and Merging
# (This part is MODIFIED)
# ==============================================================================

def get_last_6_alphanum(url):
    """Extracts the last 6 alphanumeric characters from a URL."""
    alphanum = re.findall(r'[A-Za-z0-9]+', url)
    return ''.join(alphanum)[-6:]

def generate_qr(url, counter, output_dir):
    """
    Generates a QR code image for a given URL and saves it.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # --- MODIFIED: Resize the QR to 210x210 ---
    img = img.resize((210, 210), Image.LANCZOS)

    # Generate unique filename with counter and last 6 alphanum chars
    suffix = get_last_6_alphanum(url)
    filename = os.path.join(output_dir, f"QR_{counter}_{suffix}.png")
    img.save(filename)
    return filename

def merge_images_inside(image_outer_path, qr_codes_folder, output_folder, base_filename, font_size=100, counter_font_size=40):
    """
    Merges QR code images with a base design, adds a 6-character code, and a sequential counter.
    """
    image_outer = Image.open(image_outer_path)
    font_path = "rubik.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
        counter_font = ImageFont.truetype(font_path, counter_font_size)
        print(f"Loaded font from: {font_path}")
    except Exception as e:
        print(f"Failed to load font '{font_path}': {e}")
        font = ImageFont.load_default()
        counter_font = ImageFont.load_default()
        print("Falling back to default font.")

    merged_image_paths = []

    # --- START: SORTING FIX ---
    # (Unchanged)
    qr_files = [f for f in os.listdir(qr_codes_folder) if f.startswith("QR_") and f.endswith(".png")]

    def get_file_number(filename):
        match = re.search(r'QR_(\d+)_', filename)
        if match:
            return int(match.group(1))
        return 0 

    sorted_qr_files = sorted(qr_files, key=get_file_number)
    # --- END: SORTING FIX ---

    for i, filename in enumerate(sorted_qr_files, start=1):
        qr_filepath = os.path.join(qr_codes_folder, filename)
        image_inner = Image.open(qr_filepath).convert("RGB")

        match = re.search(r'QR_\d+_([A-Za-z0-9]{6})\.png', filename)
        code = match.group(1) if match else "######"

        # --- MODIFIED: Center the QR code ---
        # Calculate QR paste position for centering
        outer_width, outer_height = image_outer.size
        inner_width, inner_height = image_inner.size
        qr_x = (outer_width - inner_width) // 2
        qr_y = ((outer_height - inner_height) // 2) + 10
        paste_position = (qr_x, qr_y)
        # --- END MODIFICATION ---

        image_combined = image_outer.copy()
        image_combined.paste(image_inner, paste_position)

        draw = ImageDraw.Draw(image_combined)

        # --- Draw 6-character code ---
        text = code
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        # Center horizontally under the QR
        text_x = qr_x + (image_inner.width - text_width) // 2
        # --- MODIFIED: Position 60px down from QR bottom ---
        text_y = qr_y + image_inner.height + 50
        draw.text((text_x, text_y), text, font=font, fill="black")

        # --- MODIFIED: Add Counter based on new pixel coordinates ---
        counter_text = str(i)
        counter_color = "#ccc8e4"

        # Get counter text bounding box
        counter_bbox = draw.textbbox((0, 0), counter_text, font=counter_font)
        counter_text_width = counter_bbox[2] - counter_bbox[0]
        
        # Calculate horizontal position (centered under QR)
        counter_x = qr_x + (image_inner.width - counter_text_width) // 2
        
        # Calculate vertical position (175px from QR bottom)
        counter_y = qr_y + image_inner.height + 160

        draw.text((counter_x, counter_y), counter_text, font=counter_font, fill=counter_color)
        # --- END MODIFICATION ---

        # The rest of the function remains the same
        original_counter_match = re.search(r'QR_(\d+)_', filename)
        original_counter = original_counter_match.group(1) if original_counter_match else "X"
        
        merged_filename = f"{base_filename}_{original_counter}_{code}.png"
        output_filepath = os.path.join(output_folder, merged_filename)

        image_combined.save(output_filepath)
        print(f"Merged image {filename} saved as {output_filepath}")
        merged_image_paths.append(output_filepath)
        
    return merged_image_paths

# ==============================================================================
# PART 2: PDF Layout and Creation (Unchanged)
# ==============================================================================

def create_pdf_from_images(images, output_pdf):
    """
    Lays out merged images onto an A4 PDF using the maximized grid logic.
    """
    # --- Configuration (MODIFIED) ---
    # Set to match the maximized cut script
    card_width_mm, card_height_mm = 46, 56
    spacing_mm = 0
    margin_mm = 0  # Use 0 margin for maximization calculation
    dpi = 300

    # --- Convert to points ---
    card_width = card_width_mm * mm
    card_height = card_height_mm * mm
    spacing = spacing_mm * mm
    margin = margin_mm * mm
    page_width, page_height = A4

    # --- Maximization Logic (Copied from maximized_cut script) ---
    # Calculate the usable area of the page
    usable_width = page_width - (2 * margin)
    usable_height = page_height - (2 * margin)

    # Calculate how many rectangles + spaces can fit
    cards_per_row = int((usable_width + spacing) / (card_width + spacing))
    cards_per_col = int((usable_height + spacing) / (card_height + spacing))
    total_cards = cards_per_row * cards_per_col
    
    print(f"Calculated PDF layout: {cards_per_row} columns x {cards_per_col} rows = {total_cards} total cards.")
    
    # --- Centering Logic (Now uses calculated values) ---
    # Calculate total grid dimensions
    grid_width = (cards_per_row * card_width) + ((cards_per_row - 1) * spacing)
    grid_height = (cards_per_col * card_height) + ((cards_per_col - 1) * spacing)

    # Find page center
    center_x = page_width / 2
    center_y = page_height / 2

    # Calculate the bottom-left corner of the *entire grid*
    grid_origin_x = center_x - (grid_width / 2)
    grid_origin_y = center_y - (grid_height / 2)
    # --- End Logic ---

    c = canvas.Canvas(output_pdf, pagesize=A4)
    cards_per_page = cards_per_row * cards_per_col
    temp_files_to_clean = []

    for i, img_path in enumerate(images):
        if i % cards_per_page == 0 and i != 0:
            c.showPage()

        row = (i % cards_per_page) // cards_per_row
        col = (i % cards_per_page) % cards_per_row

        # --- Updated Position Calculation ---
        # Calculate position from the new grid origin
        x = grid_origin_x + col * (card_width + spacing)

        # Y-position is calculated from the bottom (grid_origin_y).
        # We must invert the row for bottom-up drawing.
        inverted_row = (cards_per_col - 1 - row)
        y = grid_origin_y + (inverted_row * (card_height + spacing))
        # --- End Updated Calculation ---

        img = Image.open(img_path).convert("RGBA")
        
        # Calculate the target pixel size to match the 46x56 mm card
        target_size_px = (int(card_width_mm / 25.4 * dpi), int(card_height_mm / 25.4 * dpi))
        
        # Resize the merged image (from front.png) to fit the 46x56mm slot
        img = img.resize(target_size_px, Image.LANCZOS)

        # Create a white background for any transparency
        white_bg = Image.new("RGB", img.size, (255, 255, 255))
        white_bg.paste(img, mask=img.split()[3]) # Paste using alpha mask

        temp_path = f"temp_{i}.jpg"
        white_bg.save(temp_path, dpi=(dpi, dpi), quality=95)
        temp_files_to_clean.append(temp_path)

        # Draw the image on the canvas at the calculated x, y
        c.drawImage(temp_path, x, y, width=card_width, height=card_height)
        # No crop marks are drawn

    c.save()
    for temp_file in temp_files_to_clean:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    print(f"PDF generated: {output_pdf}")

# ==============================================================================
# MAIN EXECUTION
# (This part is unchanged)
# ==============================================================================

if __name__ == "__main__":
    # --- Configuration ---
    links_file = "links.txt"
    base_image_path = 'front.png'
    qr_codes_folder = 'QR Codes'
    merged_images_folder = 'Merged Images'
    output_pdf_path = 'cards_layout.pdf'
    base_filename = 'merged_image'
    font_size = 20
    counter_font_size = 20 # Font size for the new counter

    # --- Step 1: Generate QR Codes ---
    if not os.path.exists(qr_codes_folder):
        os.makedirs(qr_codes_folder)

    counter = 1
    with open(links_file, "r") as file:
        for url in file.readlines():
            url = url.strip()
            if url: # Ensure the line is not empty
                generate_qr(url, counter, qr_codes_folder)
                counter += 1
    print(f"QR codes generated successfully in the '{qr_codes_folder}' folder!")

    # --- Step 2: Merge QR codes with the base image ---
    os.makedirs(merged_images_folder, exist_ok=True)
    merged_image_paths = merge_images_inside(
        image_outer_path=base_image_path,
        qr_codes_folder=qr_codes_folder,
        output_folder=merged_images_folder,
        base_filename=base_filename,
        font_size=font_size,
        counter_font_size=counter_font_size # Pass the new parameter
    )

    # --- Step 3: Create the final PDF layout ---
    create_pdf_from_images(merged_image_paths, output_pdf_path)

    # Optional: Cleanup intermediate folders if not needed
    # import shutil
    # shutil.rmtree(qr_codes_folder)
    # shutil.rmtree(merged_images_folder)
    # print("Cleaned up intermediate folders.")