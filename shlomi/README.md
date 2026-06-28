# shlomi/ — our independent FLUX-based pipeline

A **self-contained fork** of the Plate Status Detection pipeline, kept separate from the
shared `code/` notebooks so it never interferes with Avital's work.

## Classes (3)
The trained model uses **3 classes**: `clean` / `finished` / `full`
(`clear` = {`finished`}; `do not clear` = {`clean`, `full`}). The synthetic data was
*generated* with a finer 5-class scheme and then consolidated to these 3 — see
[`data/class_taxonomy.md`](data/class_taxonomy.md) for the full mapping.

## Pipeline (run notebooks in order, from this `shlomi/` folder or the repo root)
- `utils.py` — shared single-source-of-truth module. Paths resolve under **`shlomi/data/`** (not the
  repo-level `data/`), so our generated data is fully isolated. Holds the seed, class lineage, prompt
  builder, and project paths.
- `01_generate_prompts.ipynb` — builds `shlomi/data/prompts.json` (attribute-based prompts, ~400/class)
  with **identical nuisance distributions across classes** (no shortcut cues).
- `02_generate_images.ipynb` — generates the **undegraded** image set with **FLUX.1-dev** into
  `shlomi/data/synthetic_clean/{class}/`. Mirrors `generate_images.py` (the headless script we run on
  the GPU server with `nohup`) exactly — same seeds, filenames, manifest.
- `03_degrade_and_augment.ipynb` — turns the clean images into the CCTV-degraded training set in
  `shlomi/data/synthetic_degraded/{class}/` (low-res, blur, noise, lighting, colour cast, vignetting,
  JPEG, perspective). **Class-agnostic** (never sees the label → no degradation can become a shortcut)
  and **reproducible** (deterministic per-image seeds). This is **novelty #1**.
- `04_split_dataset.ipynb` — stratified 70/15/15 train/val/test split (mix of degraded + clean) into
  `shlomi/data/splits/`.
- `05_train_model.ipynb` — transfer-learning classifier (ResNet18) + a CLIP zero-shot baseline;
  confusion matrix, macro-F1, and the binary clear / do-not-clear accuracy.

Generated data (`shlomi/data/synthetic_clean/`, `_pilot/`, `synthetic_degraded/`, `splits/`) is
gitignored; `prompts.json` is tracked.

## Why a fork
The shared `code/` folder holds the original `utils.py` + `01_generate_prompts.ipynb` plus
**Avital's** divergent notebooks (Stable Diffusion generation; ResNet18 + CLIP training). We do
**not** modify anything under `code/`. Avital owns model training; our focus is the FLUX generation
and the CCTV degradation pipeline.
