"""
Split a large PDF into smaller PDFs with fixed number of pages.

Author: Ankit
Description:
    This script splits a large PDF file into multiple smaller PDF files,
    each containing a fixed number of pages (default = 10).

Requirements:
    pip install pypdf
"""

from pathlib import Path
from pypdf import PdfReader, PdfWriter


def split_pdf(
    input_pdf: str,
    output_dir: str = "split_pdfs",
    pages_per_file: int = 10
) -> None:
    """
    Splits a PDF into multiple smaller PDFs.

    Args:
        input_pdf (str): Path to the input PDF file
        output_dir (str): Directory to store split PDFs
        pages_per_file (int): Number of pages per split file
    """

    input_path = Path(input_pdf)
    output_path = Path(output_dir)

    # Create output directory if not exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Load PDF
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    print(f"Total pages in PDF: {total_pages}")

    file_count = 1

    # Process in chunks
    for start_page in range(0, total_pages, pages_per_file):

        writer = PdfWriter()
        end_page = min(start_page + pages_per_file, total_pages)

        # Add pages to new PDF
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        # Output filename
        output_file = output_path / f"part_{file_count:04d}.pdf"

        # Write file
        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Created: {output_file}")

        file_count += 1

    print("\nPDF splitting completed successfully.")


if __name__ == "__main__":

    INPUT_PDF = "Data_Science_and_ML_Notes.pdf"   # Change to your PDF path
    OUTPUT_DIR = "output_pdfs"
    PAGES_PER_FILE = 10

    split_pdf(
        input_pdf=INPUT_PDF,
        output_dir=OUTPUT_DIR,
        pages_per_file=PAGES_PER_FILE
    )