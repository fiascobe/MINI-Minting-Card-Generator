import os
import re
from PIL import Image, ImageDraw, ImageFont
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

# ==============================================================================
# PART 1: QR Code Generation and Merging
# (This part is unchanged)
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

    # Resize the QR
    img = img.resize((294, 294), Image.LANCZOS)

    # Generate unique filename with counter and last 6 alphanum chars
    suffix = get_last_6_alphanum(url)
    filename = os.path.join(output_dir, f"QR_{counter}_{suffix}.png")
    img.save(filename)
    return filename

# --- MODIFIED: Added magenta_level parameter ---
def merge_images_inside(image_outer_path, qr_codes_folder, output_folder, base_filename, font_size=100, counter_font_size=40, magenta_level=80):
    """
    Merges QR code images with a base design, adds a 6-character code, and a sequential counter.
    Outputs images in CMYK color space.
    """
    # --- MODIFIED: Open base image as RGBA to handle potential transparency ---
    try:
        image_outer = Image.open(image_outer_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to open base image: {e}")
        return []
        
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

        paste_position = (10, 10)
        qr_x, qr_y = paste_position

        # Work with a copy of the base image (which is RGBA)
        image_combined_rgba = image_outer.copy()
        image_combined_rgba.paste(image_inner, paste_position) # Paste RGB QR onto RGBA base

        # --- MODIFIED: Convert to CMYK by compositing onto a white CMYK background ---
        # Create a new white CMYK image
        cmyk_image = Image.new("CMYK", image_combined_rgba.size, (0, 0, 0, 0)) # CMYK white
        
        # Paste the RGBA image (base + QR) onto the CMYK background
        # This handles transparency and converts colors to CMYK
        cmyk_image.paste(image_combined_rgba, mask=image_combined_rgba.split()[3])

        # All drawing will now be done on the CMYK image
        draw = ImageDraw.Draw(cmyk_image)

        # --- Draw 6-character code (in CMYK) ---
        text = code
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = qr_x + (image_inner.width - text_width) // 2
        text_y = qr_y + image_inner.height + 45
        # --- MODIFIED: Use CMYK black ---
        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0, 100))

        # --- Add Counter (in CMYK) ---
        counter_text = str(i)
        
        # --- MODIFIED: Define counter color in CMYK using the magenta_level parameter ---
        # CMYK tuple: (Cyan, Magenta, Yellow, Black)
        # We vary Magenta based on the parameter, keeping C, Y, K constant
        counter_color_cmyk = (0, int(magenta_level), 72, 14) 
        
        dpi = 300
        y_offset_mm = 5
        
        y_offset_px = y_offset_mm * (dpi / 25.4)
        
        img_width, img_height = cmyk_image.size

        counter_bbox = draw.textbbox((0, 0), counter_text, font=counter_font)
        counter_text_width = counter_bbox[2] - counter_bbox[0]
        counter_text_height = counter_bbox[3] - counter_bbox[1]

        counter_x = (img_width - counter_text_width) / 2
        counter_y = img_height - y_offset_px - counter_text_height

        # --- MODIFIED: Fill with CMYK color ---
        draw.text((counter_x, counter_y), counter_text, font=counter_font, fill=counter_color_cmyk)

        # The rest of the function remains the same
        original_counter_match = re.search(r'QR_(\d+)_', filename)
        original_counter = original_counter_match.group(1) if original_counter_match else "X"
        
        # --- MODIFIED: Save as JPEG for CMYK support ---
        merged_filename = f"{base_filename}_{original_counter}_{code}.jpg"
        output_filepath = os.path.join(output_folder, merged_filename)

        cmyk_image.save(output_filepath, "JPEG", dpi=(dpi, dpi), quality=95)
        print(f"Merged CMYK image {filename} saved as {output_filepath}")
        merged_image_paths.append(output_filepath)
        
    return merged_image_paths

# ==============================================================================
# PART 2: PDF Layout and Creation (MODIFIED)
# ==============================================================================

def create_pdf_from_images(images, output_pdf):
    """
    Lays out merged CMYK images onto an A4 PDF.
    """
    # --- Configuration (MODIFIED) ---
    card_width_mm, card_height_mm = 46, 56
    spacing_mm = 0
    margin_mm = 0  
    dpi = 300

    # --- Convert to points ---
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
    total_cards = cards_per_row * cards_per_col
    
    print(f"Calculated PDF layout: {cards_per_row} columns x {cards_per_col} rows = {total_cards} total cards.")
    
    # --- Centering Logic ---
    grid_width = (cards_per_row * card_width) + ((cards_per_row - 1) * spacing)
    grid_height = (cards_per_col * card_height) + ((cards_per_col - 1) * spacing)
    center_x = page_width / 2
    center_y = page_height / 2
    grid_origin_x = center_x - (grid_width / 2)
    grid_origin_y = center_y - (grid_height / 2)

    c = canvas.Canvas(output_pdf, pagesize=A4)
    cards_per_page = cards_per_row * cards_per_col
    temp_files_to_clean = []

    for i, img_path in enumerate(images):
        if i % cards_per_page == 0 and i != 0:
            c.showPage()

        row = (i % cards_per_page) // cards_per_row
        col = (i % cards_per_page) % cards_per_row

        x = grid_origin_x + col * (card_width + spacing)
        inverted_row = (cards_per_col - 1 - row)
        y = grid_origin_y + (inverted_row * (card_height + spacing))
        
        # --- MODIFIED: Simplified image handling ---
        # The images are already opaque CMYK JPEGs.
        # We just need to open, resize, and save to a temp file for drawing.
        
        try:
            # Open the merged CMYK JPEG
            img = Image.open(img_path)
            
            # Calculate the target pixel size to match the 46x56 mm card
            target_size_px = (int(card_width_mm / 25.4 * dpi), int(card_height_mm / 25.4 * dpi))
            
            # Resize the merged image
            img_resized = img.resize(target_size_px, Image.LANCZOS)

            temp_path = f"temp_{i}.jpg"
            # Save the *resized* CMYK image
            img_resized.save(temp_path, "JPEG", dpi=(dpi, dpi), quality=95)
            temp_files_to_clean.append(temp_path)

            # Draw the CMYK image on the canvas
            c.drawImage(temp_path, x, y, width=card_width, height=card_height)
        
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")
            # Optionally draw a red error box
            c.saveState()
            c.setStrokeColorRGB(1,0,0)
            c.rect(x, y, card_width, card_height, fill=0)
            c.restoreState()


    c.save()
    for temp_file in temp_files_to_clean:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    print(f"CMYK PDF generated: {output_pdf}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    # --- Configuration ---
    links_file = "links.txt"
    base_image_path = 'front.png'
    qr_codes_folder = 'QR Codes'
    merged_images_folder = 'Merged Images'
    output_pdf_path = 'cards_layout_mini_CMYK.pdf' # Changed PDF name
    base_filename = 'merged_image'
    font_size = 20
    counter_font_size = 20 

    # --- MODIFIED: Magenta level control (0-100) ---
    # This value (percent) will be used for the 'M' in the (C,M,Y,K) color
    # The original RGB red (#da2c3d) is approx (0, 80, 72, 14) in CMYK
    magenta_level_percent = 80  # <-- CHANGE THIS VALUE (e.g., 60 for less magenta)

    # --- Step 1: Generate QR Codes ---
    if not os.path.exists(qr_codes_folder):
        os.makedirs(qr_codes_folder)

    counter = 1
    try:
        with open(links_file, "r") as file:
            for url in file.readlines():
                url = url.strip()
                if url: # Ensure the line is not empty
                    generate_qr(url, counter, qr_codes_folder)
                    counter += 1
        print(f"QR codes generated successfully in the '{qr_codes_folder}' folder!")
    except FileNotFoundError:
        print(f"Error: '{links_file}' not found.")
        exit()

    # --- Step 2: Merge QR codes with the base image ---
    os.makedirs(merged_images_folder, exist_ok=True)
    merged_image_paths = merge_images_inside(
        image_outer_path=base_image_path,
        qr_codes_folder=qr_codes_folder,
        output_folder=merged_images_folder,
        base_filename=base_filename,
        font_size=font_size,
        counter_font_size=counter_font_size,
        magenta_level=magenta_level_percent # --- MODIFIED: Pass magenta level
    )

    # --- Step 3: Create the final PDF layout ---
    if merged_image_paths:
        create_pdf_from_images(merged_image_paths, output_pdf_path)
    else:
        print("No merged images were created. PDF generation skipped.")

    # Optional: Cleanup intermediate folders if not needed
    # import shutil
    # shutil.rmtree(qr_codes_folder)
    # shutil.rmtree(merged_images_folder)
    # print("Cleaned up intermediate folders.")