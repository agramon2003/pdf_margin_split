import fitz
import os

# Default variables
default_path = "d:/Python/"
source_file = "source.pdf"
destination_file = "destination.pdf"
margin = 3  # in cm
margin_pixels = margin * 28.3465

# To rename each PDF generated with applied margins
renamed_pdfs = "_PDFsam_"

# Verify if the source file exists in the default path
full_source_path = os.path.join(default_path, source_file)
if not os.path.exists(full_source_path):
    print(f"{source_file} file not found in {default_path}")
    exit()

# Create the full path of the destination file
full_destination_path = os.path.join(default_path, destination_file)

# Open the source PDF file
pdf = fitz.open(full_source_path)

# Create an empty destination PDF file
new_pdf = fitz.open()

# Loop through all the pages of the PDF
for page in pdf:
    # Get the current dimensions of the page
    dimensions = page.mediabox

    # Calculate the new dimensions with the desired margins (3 cm)
    new_width = dimensions[2] - dimensions[0] + margin_pixels * 2
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
    new_destination_file = os.path.join(default_path, f"{i+1}{renamed_pdfs}{destination_file}")
    # Save the new PDF
    new_pdf.save(new_destination_file)

print(f"Created {total_pages} PDF files with applied {margin} cm margins")
