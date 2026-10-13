# Contributing to text-to-world-3d-scene-generator

Thanks for wanting to push this forward. This repo ships a Windows desktop
tool that turns a text prompt into an explorable 3D scene — layout, props,
materials, lighting — and exports to GLB / USD / Gaussian splats.

## Ground rules

- Python 3.11+ is the floor. 3.12 preferred.
- One feature per PR. Keep the diff readable.
- Run `python -m pytest tests/` and `python -m ruff check src/` before opening.
- New pipeline stages go under `src/text_to_world/pipelines/`. New
  renderers go under `src/text_to_world/renderers/`.
- Model checkpoints are pulled at runtime — never commit `.safetensors`,
  `.ckpt`, or `.gguf` blobs. See `docs/model_manifest.md` (coming).

## Dev setup

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
python -m text_to_world --gui
```

## Commit style

Short subject, imperative, 72 cols. Body explains the *why* if it isn't
obvious. Reference the issue with `#NNN`.

## What we won't merge

- Telemetry that phones home without an opt-in toggle.
- Anything that uploads the user's prompt or generated scenes to a remote
  service by default. Local-first or it doesn't ship.
- Hardcoded checkpoint URLs that bypass the manifest.