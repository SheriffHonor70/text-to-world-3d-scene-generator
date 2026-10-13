# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Open a private security advisory on GitHub, or email
`security@text-to-world.local` (placeholder, swap before public launch).

Do **not** file public issues for:

- Arbitrary code execution via a malicious `.glb` / `.ply` scene file
- Path traversal in the asset loader
- Unsafe deserialization in the checkpoint loader
- Dependency confusion in `pyproject.toml`

## Threat model

The tool is a local desktop app. It reads prompts, writes scene files, and
loads model checkpoints. The interesting attack surfaces are:

1. **Asset import.** We parse GLB, PLY, and Gaussian splat files. A crafted
   file must not escape the sandbox directory or trigger code execution.
2. **Checkpoint loading.** `torch.load` is called with `weights_only=True`
   everywhere. Do not relax this.
3. **Prompt injection into the LLM layout planner.** The planner output is
   treated as untrusted — it is validated against a JSON schema before any
   scene node is created.
4. **Plugin loader.** Third-party pipeline stages are loaded from
   `%APPDATA%\text-to-world\plugins\`. They run in-process. We document
   this loudly and never auto-install.

## Out of scope

- Denial of service from absurdly large prompts (we cap at 4096 tokens).
- GPU driver crashes.
- Anything that requires the attacker to already have local code execution.