# Jupyter kernels & virtual environments

This repo is one VS Code workspace holding ~50 project folders, several of which
have their own `uv`-managed `.venv`. That layout breaks the usual kernel
discovery, so the setup below is deliberate. Read this before "fixing" it.

## The constraint

VS Code's Python extension only auto-discovers a `.venv` that sits in a
**workspace-folder root**. Here the workspace root is the repo, and the venvs are
one level down (`52-Packt-.../.venv`), so they never appear under
*Select Another Kernel… → Python Environments…*.

Two settings look like they should fix this. Neither does:

| Setting | Why it does not work |
| --- | --- |
| `jupyter.venvFolders` | Not a real setting. The Jupyter extension contributes no such key, so it is silently ignored. |
| `python.venvPath` | Means "a folder whose **immediate children** are venvs" (e.g. `~/.venvs`). It does **not** scan a tree, and it does **not** expand `${workspaceFolder}`. |

`python.venvPath` is therefore set to `~/.venvs` in user settings — its correct
use — and nothing in this repo relies on it.

## The setup

Each project venv is registered as a **global Jupyter kernelspec** in
`~/Library/Jupyter/kernels`. Global kernelspecs are visible to every notebook in
every folder and every workspace, and to JupyterLab / `nbconvert` / `papermill`
as well — not just VS Code.

```
packt-tf-images   -> 52-Packt-.../.venv        Python 3.12.13, TF 2.19.1 + Metal GPU
tf-images         -> 51.TutGator.../.venv      Python 3.13.14
python3           -> /opt/anaconda3/bin/python Python 3.13.5   (global fallback)
```

`uvkernel` (at `~/.local/bin/uvkernel`) manages these:

```bash
uvkernel                    # register ./.venv as a global kernel
uvkernel --pin              # write that kernel into every .ipynb of the project
uvkernel --all <repo-root>  # do both for every <root>/*/.venv
uvkernel --list             # what is registered
uvkernel --prune            # drop kernels whose python no longer exists
```

**For a new project:** `uv venv && uv sync && uvkernel && uvkernel --pin`.

## How auto-selection actually works

There is no VS Code or Jupyter setting for "use the venv next to this notebook".
The only mechanism is the notebook's own `metadata.kernelspec.name`:

1. Notebook names a kernel that exists → VS Code selects it silently on open.
   This is what `uvkernel --pin` writes.
2. Notebook names `python3` (the ~475 notebooks elsewhere in this repo) → falls
   back to the global `python3` kernelspec, i.e. Anaconda base.

Caveat: **VS Code writes its own selection back into this metadata on save.** If
a notebook is open in the editor while you run `--pin`, the editor's copy wins.
Close the notebook first, or just pick the kernel once in the UI — VS Code
persists it to the same field and auto-selection works from then on.

## Notes

- `~/.local/share/jupyter/kernels/python3` also defines `python3`. The canonical
  user dir on macOS is `~/Library/Jupyter/kernels` (`jupyter --paths`), so the
  spec is mirrored there; both point at Anaconda base.
- `ipykernel` 7.x is in use in `52-Packt-...`; it warns about unencrypted TCP
  transport on kernel start. Harmless for local work.
- Prerelease interpreters (3.14/3.15) are hidden from the picker via
  `jupyter.kernels.excludePythonEnvironments` in user settings — most ML wheels
  do not exist for them.
