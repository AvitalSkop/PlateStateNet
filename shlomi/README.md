# shlomi/ — our independent FLUX-based pipeline

A **self-contained fork** of the Plate Status Detection pipeline, kept separate from the
shared `code/` notebooks so it never interferes with Avital's work.

## Layout
- `utils.py` — our copy of the shared module. Paths resolve under **`shlomi/data/`** (not the
  repo-level `data/`), so our generated data is fully isolated.
- `01_generate_prompts.ipynb` — generates `shlomi/data/prompts.json` (5 classes, 300 prompts/class).
- `02_generate_images.ipynb` — generates images with **FLUX.1-dev** into `shlomi/data/synthetic_clean/`.

Run the notebooks from this `shlomi/` folder (or the repo root) — they import the local `utils.py`.
Generated data (`shlomi/data/synthetic_clean/`, `_pilot/`, `synthetic_degraded/`) is gitignored.

## Why a fork
The shared `code/` folder holds the original `utils.py` + `01_generate_prompts.ipynb` plus
**Avital's** divergent notebooks (Stable Diffusion generation; ResNet18 + CLIP training:
`02_generate_images_clean`, `03_degrade_and_augment`, `04_split_dataset`, `05_train_model_clean`).
We do **not** modify anything under `code/`.
