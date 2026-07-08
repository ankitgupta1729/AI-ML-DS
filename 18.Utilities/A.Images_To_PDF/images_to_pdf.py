import os
import tempfile
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from tqdm import tqdm

# ================= CONFIG =================

IMAGE_FOLDER = "images"
OUTPUT_PDF = "Data_Science_and_ML_Notes.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4

MARGIN_X = 2.2 * cm
MARGIN_Y = 2.5 * cm

BACKGROUND_COLOR = HexColor("#FFFFFF")
PAGE_NUMBER_COLOR = HexColor("#9CA3AF")

IMAGE_MAX_WIDTH = PAGE_WIDTH - (2 * MARGIN_X)
IMAGE_MAX_HEIGHT = PAGE_HEIGHT - (2 * MARGIN_Y)

# ==========================================


def get_sorted_images(folder):
    return sorted(
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    )


def prepare_image(image_path):
    """
    Fix orientation and save to a temp file (REQUIRED for ReportLab stability)
    """
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    img.save(temp.name, format="JPEG", quality=95, subsampling=0)

    return temp.name, img.size


def draw_page_number(c, page_num):
    c.setFillColor(PAGE_NUMBER_COLOR)
    c.setFont("Helvetica", 9)
    c.drawCentredString(PAGE_WIDTH / 2, 1.3 * cm, str(page_num))


def add_image_page(c, image_path, page_num):
    # Background
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)

    temp_img_path, (img_w, img_h) = prepare_image(image_path)

    scale = min(
        IMAGE_MAX_WIDTH / img_w,
        IMAGE_MAX_HEIGHT / img_h
    )

    new_w = img_w * scale
    new_h = img_h * scale

    x = (PAGE_WIDTH - new_w) / 2
    y = (PAGE_HEIGHT - new_h) / 2

    c.drawImage(
        temp_img_path,
        x,
        y,
        width=new_w,
        height=new_h,
        preserveAspectRatio=True
    )

    draw_page_number(c, page_num)
    c.showPage()

    os.remove(temp_img_path)


def create_pdf():
    images = get_sorted_images(IMAGE_FOLDER)

    if not images:
        print("❌ No images found")
        return

    print(f"\n📘 Creating PDF from {len(images)} images...\n")

    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    c.setTitle("Data Science & Machine Learning Notes")

    for page_num, img in enumerate(
        tqdm(images, desc="📄 Processing Pages", unit="page"),
        start=1
    ):
        add_image_page(c, img, page_num)

    c.save()
    print(f"\n✅ PDF created successfully: {OUTPUT_PDF}")


if __name__ == "__main__":
    create_pdf()