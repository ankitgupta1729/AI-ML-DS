import re
import sys
from pathlib import Path


def is_heading(line):
    return (
        line.isupper()
        or (line.istitle() and len(line.split()) <= 10)
        or re.match(r'^[A-Z][A-Za-z0-9\s\-:]{3,}$', line)
    )


def is_list_item(line):
    return re.match(r'^(\d+[\).\s]|[-*•]\s+)', line)


def is_code_block(line):
    return (
        line.startswith("    ")
        or line.startswith("\t")
        or re.match(r'^(>>>|\$|#include|def |class )', line)
    )


def is_quote(line):
    return line.startswith('"') or line.startswith("'")


def is_table_row(line):
    return ',' in line or '\t' in line


def clean_text(line):
    return line.rstrip()


def convert_text_to_markdown(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    md = []
    toc = []
    in_code = False
    code_buffer = []

    for line in lines:
        line = clean_text(line)

        if not line:
            md.append("")
            continue

        # Code block handling
        if is_code_block(line):
            in_code = True
            code_buffer.append(line.lstrip())
            continue
        elif in_code:
            md.append("```")
            md.extend(code_buffer)
            md.append("```")
            md.append("")
            code_buffer = []
            in_code = False

        # Headings
        if is_heading(line):
            level = 2 if len(line.split()) > 3 else 1
            heading = f"{'#' * level} {line}"
            md.append("")
            md.append(heading)
            md.append("")
            toc.append(f"- [{line}](#{line.lower().replace(' ', '-')})")
            continue

        # Lists
        if is_list_item(line):
            md.append(line)
            continue

        # Quotes
        if is_quote(line):
            md.append(f"> {line}")
            continue

        # Tables (simple CSV / tab based)
        if is_table_row(line):
            cells = re.split(r'[,\t]+', line)
            if len(cells) > 2:
                md.append("| " + " | ".join(cells) + " |")
                md.append("|" + "|".join([" --- "]*len(cells)) + "|")
                continue

        # Normal paragraph
        md.append(line)

    # Insert TOC
    if toc:
        md.insert(0, "\n".join([
            "# 📘 Document Overview",
            "",
            "## 📑 Table of Contents",
            "",
            *toc,
            "",
            "---",
            ""
        ]))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))

    print(f"✅ Markdown file created: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python text_to_markdown.py input.txt output.md")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print("❌ Input file does not exist")
        sys.exit(1)

    convert_text_to_markdown(input_file, output_file)