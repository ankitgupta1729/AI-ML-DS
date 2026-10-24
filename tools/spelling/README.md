# spelling

Reviewed spelling and technical-term corrections for the course notes.

Most notes are lecture transcripts produced by speech-to-text, which mishears
technical vocabulary ("Tenzer board" for TensorBoard, "Emmis" for MNIST,
"reloop" for ReLU), and the hand-written notes contain ordinary typos
("apllication", "persistant"). Every correction here was checked against its
context before being added; nothing is applied blindly.

| File | Purpose |
| --- | --- |
| `corrections.tsv` | The reviewed corrections: scope (module numbers or `*`), text to find, replacement, and why |
| `apply.py` | Applies them to the course notes listed in `tools/notes-to-pdf/catalog.json` |

```bash
python tools/spelling/apply.py --check   # preview: files affected, rules that match nothing
python tools/spelling/apply.py           # apply
python tools/notes-to-pdf/build.py       # then rebuild the revision PDFs
```

How it stays safe:

- Only prose changes. Fenced code, inline `code`, URLs and link/image targets
  are never edited.
- Matches are whole words, case-insensitive, and longer phrases win over
  shorter ones ("Tenzer board" → TensorBoard before "Tenzer" → TensorFlow).
- A capital letter is carried over only at the start of a sentence, because
  speech-to-text often capitalises misheard words mid-sentence.
- Course-specific mishearings are scoped to their module, so a fix for one
  course never fires in another.
- Running it again is a no-op; `--check` reports any rule that no longer
  matches anything.

Scope is deliberately "clear errors only": misspellings and misheard
terms. The wording and grammar of the transcripts are left as spoken.
