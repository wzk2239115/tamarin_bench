# Data License

Task data in `data/tasks/` is derived from the CrypFormBench dataset
(https://arxiv.org/abs/2606.25561, "CrypFormBench: Benchmarking Formal Analysis
Capability of Large Language Models for Cryptographic Schemes"), whose spthy
protocol theories are in turn sourced from the Tamarin case studies and the
formal verification literature.

The derived task packaging (task.json, goals.md, spec.md, broken theories,
ground-truth annotations produced by `scripts/validate_tasks.py`) follows the
upstream terms; cite CrypFormBench and the original protocol modelers when
redistributing. The bundled Tamarin binaries under `docker/bin/` are official
upstream releases (https://github.com/tamarin-prover/tamarin-prover, GPLv2+;
see their repository for the full license).
