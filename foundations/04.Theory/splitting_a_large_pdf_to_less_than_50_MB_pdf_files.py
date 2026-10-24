import os
from pypdf import PdfReader, PdfWriter

INPUT_FILE = "Data_Science_and_ML_Notes.pdf"
OUTPUT_DIR = "split_pdfs"
MAX_SIZE_MB = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def write_pdf(pages, output_path):
    writer = PdfWriter()
    for p in pages:
        writer.add_page(p)

    with open(output_path, "wb") as f:
        writer.write(f)


def split_pdf(input_file, max_size_mb):
    reader = PdfReader(input_file)

    part_num = 1
    temp_file = os.path.join(OUTPUT_DIR, "temp.pdf")

    current_pages = []
    start_page = 0

    for i, page in enumerate(reader.pages):
        current_pages.append(page)

        # Write temp file to check size
        write_pdf(current_pages, temp_file)
        size_mb = get_size_mb(temp_file)

        if size_mb > max_size_mb:
            # Remove last page (overflow page)
            overflow_page = current_pages.pop()

            # Save current chunk
            output_file = os.path.join(
                OUTPUT_DIR,
                f"part_{part_num:04d}_pages_{start_page+1}-{i}.pdf"
            )
            write_pdf(current_pages, output_file)
            print(f"Saved: {output_file}")

            part_num += 1

            # Start new chunk with overflow page
            current_pages = [overflow_page]
            start_page = i

    # Save remaining pages
    if current_pages:
        output_file = os.path.join(
            OUTPUT_DIR,
            f"part_{part_num:04d}_pages_{start_page+1}-{len(reader.pages)}.pdf"
        )
        write_pdf(current_pages, output_file)
        print(f"Saved: {output_file}")

    # Cleanup temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)


if __name__ == "__main__":
    split_pdf(INPUT_FILE, MAX_SIZE_MB)