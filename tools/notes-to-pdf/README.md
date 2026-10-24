# notes-to-pdf

Builds the revision PDFs that sit in each module's `pdf/` folder from the
course notes (`Note.md`, `Notes.md`, …). The Markdown sources are **read only** —
the tool never writes to them.

## What it does

1. **Parses** a note into blocks: headings, bare `N.` lecture markers, prose,
   lists, code and screenshots (all the image spellings used in this repo:
   `![](…)`, `! [](…)`, `[1.png](…)`, `images/` or `Images/`).
2. **Places every screenshot next to the sentence it illustrates.** Most course
   notes were captured as *all screenshots of a lecture first, then the
   transcript*. Each screenshot has the lecturer's subtitle burned in, so the
   tool OCRs it (Tesseract, once for the full frame and once for the
   isolated white subtitle text) and finds where those exact words occur in
   the transcript. A monotone alignment (dynamic programming) keeps
   screenshots in their original order; any screenshot without a reliable
   match stays right after the previous one. Notes whose images were placed
   by hand are left exactly as written.
3. **Gives every lecture a real title.** In order of preference: a heading
   the notes already have; the slide title shared by most of the lecture's
   slides (OCR lines validated against the lecture's own vocabulary and
   rejected if they read like sentence fragments); otherwise a key-phrase
   title mined from the lecture's transcript (distinctive 1–3 word phrases,
   TF-IDF across lectures, original acronym casing kept). Figures are
   captioned with their slide titles. The text of the notes is never changed.
4. **Renders** a styled HTML document — cover, contents with page numbers,
   section openers, figures, highlighted code — and prints it with headless
   Chromium (Playwright). A second pass fills in the real page numbers.
5. **Splits** very large courses into volumes of at most ~45 MB (GitHub warns above 50 MB), so every file
   stays well under GitHub's 100 MB limit.

Screenshots are included exactly as captured — full frame, subtitles and all —
only downscaled to 1400 px wide and stored as JPEG to keep file sizes sensible;
Chromium embeds them without re-encoding. Fonts (Inter,
Source Serif 4, JetBrains Mono — SIL Open Font License, see `fonts/`) are
bundled as static TrueType files so the PDFs look the same on every machine.

## Usage

```bash
# one-time setup
sudo apt install tesseract-ocr        # macOS: brew install tesseract
pip install -r tools/notes-to-pdf/requirements.txt
(cd tools/notes-to-pdf && npm install && npx playwright install chromium)

python tools/notes-to-pdf/build.py --list      # what will be built
python tools/notes-to-pdf/build.py             # build everything
python tools/notes-to-pdf/build.py 47 55       # only modules 47 and 55
```

OCR text for every screenshot ships in `ocr-cache.json.gz`, so a fresh clone
only needs Tesseract for new screenshots. Prepared images and intermediate
HTML are cached in
`tools/notes-to-pdf/.cache/` (git-ignored), keyed by file content, so
re-builds after editing a note take seconds per course.

## Adding a course

Add an entry to [`catalog.json`](catalog.json):

```json
{"module": "62.My-New-Course", "source": "Note.md", "category": "dl",
 "file": "My-New-Course-Notes", "title": "My New Course", "short": "My Course",
 "provider": "Udemy", "subtitle": "One line about what it covers"}
```

`module` is the folder name (the tool finds it inside any category folder);
`sources` (a list of `{path, title}`) combines several notes into one PDF.

## Layout

| Path | Purpose |
| --- | --- |
| `build.py` | CLI: catalog → PDFs |
| `catalog.json` | Which notes to build, titles and categories |
| `notes_pdf/parse.py` | Markdown → typed blocks |
| `notes_pdf/ocr.py` | Tesseract OCR with a content-hash cache |
| `notes_pdf/align.py` | Screenshot ↔ transcript alignment |
| `notes_pdf/titles.py` | Lecture and figure titles (slide OCR, key phrases) |
| `notes_pdf/images.py` | Resize and compress screenshots (frames are not altered) |
| `notes_pdf/render.py`, `style.css` | HTML document and print stylesheet |
| `render_pdf.js` | Playwright/Chromium print backend |
| `fonts/` | Bundled fonts and their licences |
