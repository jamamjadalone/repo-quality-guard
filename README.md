# Repo Quality Guard

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-sky.svg)](https://www.python.org/)
[![Rust-Powered Speed](https://img.shields.io/badge/Speed-%3C50ms-purple.svg)](#credits--built-with)
[![100% Offline](https://img.shields.io/badge/Architecture-100%25%20Offline-blue.svg)](#why-repo-quality-guard)

**Repo Quality Guard** is a lightweight, zero-telemetry, 6-in-1 repository health and pre-push verification tool for software developers.

It unifies syntax checking, Rust-powered static analysis, unit testing, 404 broken asset link scanning, anti-slop code smells, and pre-commit secret leak prevention into a single command that runs in **under 2 seconds** with **zero RAM overhead**.

---

## Quick Start (1-Minute Setup)

No heavy installation required. Run directly with Python:

```bash
# 1. Audit current directory
python repo_quality_guard.py .

# 2. Audit specific project folder
python repo_quality_guard.py /path/to/project

# 3. Batch scan all repositories in a workspace
python repo_quality_guard.py --all

# 4. Auto-fix autofixable lints (Ruff & Biome)
python repo_quality_guard.py . --fix
```

### Windows 1-Click Run
Double-click `run_audit.bat` to launch the interactive audit console.

---

## The 6 Verification Engines

| Engine | Target | Description |
| :--- | :--- | :--- |
| **Python Engine** | `*.py` | Syntax validation (`py_compile`), Rust static analysis (`Ruff`), and automated test suite (`Pytest`). |
| **Web & Frontend** | `*.js`, `*.ts`, `*.html`, `*.css` | Rust-powered syntax and accessibility static checks (`Biome`). |
| **Android Engine** | `gradlew` | Offline release compilation and unit testing (`:app:testReleaseUnitTest --offline`). |
| **Anti-Slop Quality** | Codebase | Detects bloated code, unnecessary AI gimmicks, and maintenance code smells (`FixMySlop`). |
| **Broken Asset 404s** | Web / Static | Scans `<script>`, `<link>`, `<img>`, and CSS `url(...)` to ensure referenced local files actually exist. |
| **Secret Leak Guard** | All text files | Prevents accidental commits of API keys (GitHub PATs, Google API, AWS, RSA private keys, tokens). |

---

## Why Repo Quality Guard?

- **Low-Spec Friendly**: Designed to run seamlessly on machines with limited RAM (4GB–8GB) where heavy Docker containers or browser-based test runners choke system resources.
- **100% Local & Private**: Never uploads your code, metrics, or telemetry to external servers. All checks run locally on your hardware.
- **Graceful Tool Fallback**: Missing optional tools (e.g. Biome, FixMySlop, or Gradle) are gracefully skipped with informational notices instead of breaking your run.

---

## Optional Recommended Tools

For the best experience, install the blazing-fast Rust tools globally:

```bash
# Python linter (<15ms)
pip install ruff pytest

# Web linter (<35ms)
npm install -g @biomejs/biome

# Code smell & slop scanner
pip install fixmyslop
```

---

## Usage Policy & Privacy

Please refer to [USAGE_POLICY.md](USAGE_POLICY.md) for details on fair use, commercial permissions, and our strict zero-telemetry guarantee.

---

## Credits & Built With

Repo Quality Guard orchestrates and credits the following outstanding open-source projects:

- [Ruff](https://github.com/astral-sh/ruff) by **Astral** — Extremely fast Python linter and code formatter written in Rust.
- [Biome](https://github.com/biomejs/biome) by **BiomeJS** — Fast toolchain for the web written in Rust.
- [FixMySlop](https://github.com/victor/fixmyslop) — Code quality & anti-pattern static analyzer.
- [Pytest](https://github.com/pytest-dev/pytest) — Robust testing framework for Python.
- Python Standard Library (`py_compile`, `re`, `subprocess`, `pathlib`).

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
