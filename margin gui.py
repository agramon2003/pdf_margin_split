import fitz
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Default variables
DEFAULT_PATH = Path("d:/Python/")
MARGIN_CM = 3
MARGIN_PIXELS = MARGIN_CM * 28.3465
RENAMED_PDFS = "_PDFsam_"

# Create the Tk instance and hide the main window
root = tk.Tk()
root.withdraw()

def main():
# Ask user for source file
    source_file = filedialog.askopenfilename(initialdir=DEFAULT_PATH, title="Select source PDF file", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if not source_file:
        print("No source file selected")
        return

    # Verify if the source file exists in the default path and has the .pdf extension
    source_file_path = Path(source_file)
    if not source_file_path.exists() or source_file_path.suffix.lower() != ".pdf":
        print(f"{source_file} file not found or not a PDF file")
        return

    # Ask user for destination file
    destination_file = filedialog.asksaveasfilename(initialdir=DEFAULT_PATH, title="Save PDF file as", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if not destination_file:
        print("No destination file selected")
        return

    # Create the full path of the destination file
    full_destination_path = Path(destination_file)

    # Open the source PDF file
    pdf = fitz.open(source_file)

    # Create an empty destination PDF file
    new_pdf = fitz.open()

    # Loop through all the pages of the PDF
    for page in pdf:
        # Get the current dimensions of the page
        dimensions = page.mediabox

        # Calculate the new dimensions with the desired margins
        new_width = dimensions[2] - dimensions[0] + MARGIN_PIXELS * 2
        new_height = dimensions[3] - dimensions[1]
        new_dimensions = (0, 0, new_width, new_height)

        # Add the page with the new dimensions to the new PDF
        new_page = new_pdf.new_page(-1, width=new_width, height=new_height)
        new_page.set_cropbox(new_dimensions)
        new_page.show_pdf_page(new_page.rect, pdf, page.number)

    # Save the new PDF file
    new_pdf.save(full_destination_path)

    # Split the destination PDF file into one PDF per page
    pdf_destination = fitz.open(full_destination_path)
    total_pages = pdf_destination.page_count

    for i, page in enumerate(pdf_destination):
        new_pdf = fitz.open()
        new_pdf.insert_pdf(pdf_destination, from_page=i, to_page=i)
        # Rename the created PDF with the page number and given name
        new_destination_file = DEFAULT_PATH / f"{i+1}{RENAMED_PDFS}{full_destination_path.name}"
        # Save the new PDF
        new_pdf.save(new_destination_file)

    messagebox.showinfo("Operation completed", f"Created {total_pages} PDF files with applied {MARGIN_CM} cm margins")

if __name__ == "__main__":
    main()
