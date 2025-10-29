Project: Variable Data PDF Card Generator
This project is a suite of Python scripts designed to perform Variable Data Printing (VDP). It takes a list of URLs, a front card design, and a back card design, and generates print-ready, double-sided A4 PDF layouts.

Each card on the front is unique, featuring a generated QR code, a 6-character code extracted from its URL, and a sequential counter. The scripts automatically calculate a maximized, centered grid to fit as many cards as possible on an A4 page.

Features
Variable Data: Automatically generates unique QR codes and text for each card from a simple links.txt file.

Maximized Layout: Calculates and centers a grid to fit the maximum number of 46x56mm cards on an A4 page (4 columns x 5 rows = 20 cards).

Duplex Printing: Generates a horizontally-mirrored back-side PDF that aligns with the front when printed double-sided.

Color Space Options: Provides two separate workflows:

CMYK: For professional print shops. Converts all images and text to CMYK color space.

RGB: For standard home/office printers.

Utility Script: Includes a bonus script to generate a PDF of cut-lines for a different card size (40x50mm) with custom spacing.

Requirements
You will need Python 3 and the following libraries:

Pillow (PIL)

qrcode

reportlab

You can install them using pip:

Bash

pip install Pillow qrcode reportlab
Required Files
Before running the scripts, you must have the following files in the same directory:

links.txt: A plain text file containing one URL per line. Each URL will be used to create one card.

front.png: The template image for the card front. This image should have a blank area for the QR code, 6-digit code, and counter. (Based on the script, the QR code is 294x294px and is pasted near the top-left).

back.png: The template image for the card back. This single image will be repeated on the back layout.

rubik.ttf: The font file used for the 6-digit code and the counter. If you don't have this font, you can either download it or change the font_path variable in the "Front" scripts to a font you have.

How to Use (Main 46x56mm Workflow)
This workflow generates the 46x56mm cards with no spacing between them.

Prepare Assets: Create your links.txt, front.png, and back.png files.

Install Dependencies: Run pip install Pillow qrcode reportlab.

Choose Your Color Workflow:

Option A: CMYK (For Professional Printing)

Run the front-side script:

Bash

python "Maximize Minting card centered w counter CMYK.py"
Run the back-side script:

Bash

python "Maximize Back script CMYK.py"
Output: You will get two files: cards_layout_mini_CMYK.pdf (Fronts) and back_layout_mini_CMYK.pdf (Backs).

Option B: RGB (For Home/Office Printing)

Run the front-side script:

Bash

python "Maximize Minting card centered w counter RGB.py"
Run the back-side script:

Bash

python "Maximize Back script RGB.py"
Output: You will get two files: cards_layout.pdf (Fronts) and back_layout_maximized.pdf (Backs).

Print: Send the two generated PDFs to your printer. Use the double-sided printing option (e.g., "print on both sides," "flip on long edge") to print the back layout on the reverse of the front layout.

Script Descriptions
This project contains two main workflows (CMYK and RGB) and one utility script.

Main Workflow: 46x56mm Cards (Full Bleed)
These scripts work together to create the 46x56mm card layouts.

1. Maximize Minting card centered w counter CMYK.py (Front, CMYK)
Purpose: Generates the front side of the cards in CMYK color space.

Process:

Reads each URL from links.txt.

Generates a unique QR code for each URL and saves it in the QR Codes folder.

Opens front.png (as RGBA to handle transparency).

Pastes the QR code, the 6-digit code, and the sequential counter onto the front.png template.

Composites the final RGBA image onto a white CMYK background, converting it to CMYK.

Saves each unique card as a CMYK JPEG in the Merged Images folder.

Arranges all merged images into a maximized (4x5), centered grid on an A4 PDF.

Output: cards_layout_mini_CMYK.pdf

2. Maximize Back script CMYK.py (Back, CMYK)
Purpose: Generates the back side of the cards in CMYK, mirrored to match the front.

Process:

Opens back.png.

Converts the single back.png image to a temporary CMYK JPEG.

Arranges this CMYK image into a maximized (4x5), centered, and horizontally mirrored grid on an A4 PDF.

Output: back_layout_mini_CMYK.pdf

3. Maximize Minting card centered w counter RGB.py (Front, RGB)
Purpose: Generates the front side of the cards in RGB color space.

Process:

Identical to the CMYK front script, but performs all operations in RGB.

Saves merged images as PNGs.

Flattens transparent images onto a white RGB background before placing them on the PDF.

Output: cards_layout.pdf

4. Maximize Back script RGB.py (Back, RGB)
Purpose: Generates the back side of the cards in RGB, mirrored to match the front.

Process:

Identical to the CMYK back script, but places the back.png (as RGB) directly onto the PDF grid.

The grid is maximized (4x5), centered, and horizontally mirrored.

Output: back_layout_maximized.pdf

Utility Script (Separate Workflow)
5. Maximized Cut script.py (Cut-line Grid)
Purpose: This is a standalone utility to generate a PDF of empty rectangles (cut lines) for a different card size.

Note: This script is not used by the other scripts. It is a separate tool.

Process:

Uses different dimensions: 40x50mm cards, 6mm spacing, and a 10mm page margin.

Calculates the maximum number of rectangles that can fit with this spacing.

Draws a centered grid of these empty rectangles onto a PDF.

Output: maximized_grid_layout.pdf

Configuration
You can modify the scripts to change certain behaviors:

Card Size: To change the card size (e.g., from 46x56mm), you must update the card_width_mm and card_height_mm variables in both the "Front" and "Back" scripts you are using.

Counter Color (CMYK): In Maximize Minting card centered w counter CMYK.py, you can change the color of the sequential counter by modifying the magenta_level_percent variable in the if __name__ == "__main__": block.

Counter Color (RGB): In Maximize Minting card centered w counter RGB.py, you can change the counter_color = "#da2c3d" variable in the merge_images_inside function.

Font Size: The font_size and counter_font_size variables can be changed in the if __name__ == "__main__": block of the "Front" scripts.