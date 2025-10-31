# Mini POAP Minting Card Generator

This project contains a set of Python scripts to automatically generate a printable, double-sided A4 PDF of mini POAP (Proof of Attendance Protocol) minting cards from a simple text file of links.

## Overview

The workflow is designed to create physical cards that can be handed out, each with a unique "Scan to Mint" QR code.

1.  [cite_start]**Input:** The process starts with a `links.txt` file, where you list all your POAP minting URLs, one per line.
2.  [cite_start]**Front Card Generation:** The `Mini minting card Front script v1.py` script reads `links.txt`, and for each link:
    * [cite_start]Generates a unique QR code.
    * [cite_start]Extracts the last 6 alphanumeric characters from the URL.
    * [cite_start]Merges the `front.png` template, the QR code, the 6-character code, and a sequential number onto a new image.
    * [cite_start]It compiles all these unique card images into a maximized, centered grid on one or more A4 pages, saving it as `cards_layout.pdf`.
3.  [cite_start]**Back Card Generation:** The `Mini minting card Back script.py` script takes the `back.png` image and arranges it in an identical, maximized grid. [cite_start]Crucially, it **mirrors the layout** horizontally, so that when you print it on the back of the front page, each card back aligns perfectly with its front. [cite_start]This is saved as `back_layout_maximized.pdf`.
4.  [cite_start]**Cut Guide (Optional):** The `Mini minting card Cut script.py` is a utility script that generates a PDF with just the rectangular outlines for the cards. [cite_start]This is useful for checking printer alignment or for manual cutting.

## Features

* [cite_start]**Automated QR Generation:** Creates QR codes from a list of URLs.
* [cite_start]**Custom Templates:** Uses `front.png` and `back.png` as customizable templates.
* [cite_start]**Dynamic Text:** Automatically adds the 6-digit POAP code and a sequential counter to each card front using the provided `rubik.ttf` font.
* [cite_start]**Maximized Layout:** Calculates the maximum number of cards (46x56 mm) that can fit on an A4 page.
* [cite_start]**Mirrored Backs:** Automatically generates a mirrored layout for the card backs, simplifying double-sided (duplex) printing.
* [cite_start]**Page Numbering:** The front-side PDF (`cards_layout.pdf`) includes simple page numbers in the bottom-right corner.

## File Structure

. ├── Mini minting card Back script.py # Script to generate the mirrored back-side PDF ├── Mini minting card Cut script.py # Utility script to generate a PDF of cut lines ├── Mini minting card Front script v1.py # The main script to generate the front-side PDF ├── back.png # Image template for the card backs ├── front.png # Image template for the card fronts ├── links.txt # INPUT: Your list of minting URLs (one per line) └── rubik.ttf # Font file used for text on the card fronts


## Requirements

To use these scripts, you need Python 3 and the following libraries:

* `reportlab` [cite: 1, 3, 4]
* `Pillow` (PIL) 
* `qrcode` 

You can install them using pip:

```bash
pip install reportlab pillow qrcode
How to Use
Install Dependencies: Run pip install reportlab pillow qrcode in your terminal.

Prepare Files:

Make sure Mini minting card Front script v1.py, Mini minting card Back script.py, front.png, back.png, and rubik.ttf are all in the same directory.

Edit links.txt and paste your POAP minting URLs into it, with one URL on each line. The file is pre-populated with 20 sample links.



Generate the Card Fronts PDF: Run the main front-end script in your terminal:

Bash

python "Mini minting card Front script v1.py"
This will create two folders (QR Codes/ and Merged Images/) and the final cards_layout.pdf file.

Generate the Card Backs PDF: Run the back-end script in your terminal:

Bash

python "Mini minting card Back script.py"
This will create the back_layout_maximized.pdf file.

(Optional) Generate Cut Guide: If you want a PDF with just the cut lines for alignment testing, run:

Bash

python "Mini minting card Cut script.py"

Note: The default settings in this cut script (rect_width_mm = 40, rect_height_mm = 50) do not match the 46x56 mm card size in the main scripts. You must edit Mini minting card Cut script.py to match the 46x56 mm size and 0 mm spacing  if you want an accurate cut guide.


Generated Files

cards_layout.pdf: The final, printable A4 PDF containing all your unique card fronts.


back_layout_maximized.pdf: The final, printable A4 PDF containing the mirrored card backs.


maximized_grid_layout.pdf: (Optional) A PDF showing only the grid outlines for cutting.


QR Codes/ (folder): Contains the intermediate QR code images.


Merged Images/ (folder): Contains the intermediate card front images (template + QR + text).

Printing Instructions
Open cards_layout.pdf and print it using your printer's "Actual Size" or "100% Scale" setting.

Take the printed page(s), flip them over, and re-insert them into your printer. (The correct way to flip—on the long edge or short edge—depends on your printer's duplexing).

Open back_layout_maximized.pdf and print it on the back of the pages you just printed.

Recommendation: Print a single test page first! Use the (modified) maximized_grid_layout.pdf on the front and the back_layout_maximized.pdf on the back to ensure your alignment is correct before printing all your cards.

Customization

Card Size: To change the card size from the default 46x56 mm, you must edit the card_width_mm and card_height_mm variables at the top of both Mini minting card Front script v1.py and Mini minting card Back script.py. The values must be identical in both files.


Card Templates: You can replace front.png and back.png with your own custom designs. The front template should have a blank space for the QR code.


Text & Font: The text position, font size, and color can be adjusted inside the merge_images_inside function in Mini minting card Front script v1.py. You can also replace rubik.ttf with a different font file (but be sure to update the font_path variable in the script).