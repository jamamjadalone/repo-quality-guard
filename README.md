# Repo Quality Guard

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-sky.svg)](https://www.python.org/)
[![Rust-Powered Speed](https://img.shields.io/badge/Speed-%3C50ms-purple.svg)](#credits--built-with)
[![100% Offline](https://img.shields.io/badge/Architecture-100%25%20Offline-blue.svg)](#why-repo-quality-guard)

**Repo Quality Guard** is a lightweight, zero-telemetry, 6-in-1 repository health and pre-push verification tool for software developers.

It unifies syntax checking, Rust-powered static analysis, unit testing, 404 broken asset link scanning, anti-slop code smells, and pre-commit secret leak prevention into a single command that runs in **under 2 seconds** with **zero RAM overhead**.

---

## 🚀 How to Use (3 Common Real-World Scenarios)

### Scenario 1: Auditing Any Project Folder on Your Desktop / PC
You don't need to move your projects. You can audit any project folder from anywhere:

**Using the 1-Click Menu (Windows):**
1. Double-click `run_audit.bat`.
2. Choose **`[4] CUSTOM`**.
3. Paste the path to your project (for example `C:\Projects\MyProject`) and press Enter!

**Using the Command Line:**
```bash
python repo_quality_guard.py "C:\Projects\MyProject"
```

---

### Scenario 2: Drop Directly into Any Repo (Zero Setup)
Simply copy `repo_quality_guard.py` and `run_audit.bat` into any project folder.
Double-click `run_audit.bat` and press **`[1]`** to audit that repository in 2 seconds.

---

### Scenario 3: Automated GitHub CI (Run on Every Git Push)
To automatically run Repo Quality Guard on GitHub whenever you push code or open a pull request, create `.github/workflows/quality.yml` in your repository:

```yaml
name: Repo Quality Guard

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Rust Tools
        run: pip install ruff fixmyslop pytest
      - name: Run Quality Audit
        run: python repo_quality_guard.py .
```
Every push will now automatically get verified and receive a green checkmark `✔` on GitHub!

---

## The Interactive 1-Click Console

When running `run_audit.bat`, you get a clear, glitch-free menu:

```text
========================================================================
    REPO QUALITY GUARD — 1-Click Code Quality & Health Auditor
========================================================================

  What do you want to test today?

  [1] QUICK AUDIT: Test current folder (Fast & Safe, Read-Only)
  [2] AUTO-FIX:    Test & automatically fix format errors (--fix)
  [3] MULTI-REPO:  Scan all projects in this workspace at once
  [4] CUSTOM:      Enter any specific folder path on your PC
  [5] TOOL DOCTOR: Check missing tools & install them interactively
  [6] EXIT
========================================================================
```

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

## Interactive Tool Doctor & Setup Helper

Repo Quality Guard includes an interactive **Tool Doctor** (`--doctor` or `--setup` or menu option `[5]`).

It scans your system for recommended tools, explains the specific engineering benefit of each tool, and gives you a clear choice:
1. **Auto-Install Missing Tools**: Automatically installs recommended pip and npm packages.
2. **Selective Install**: Interactively asks which specific tools you wish to enable.
3. **Graceful Skip**: Continue with your existing tools without installing anything.

---

## Why Repo Quality Guard?

- **Low-Spec Friendly**: Designed to run seamlessly on machines with limited RAM (4GB–8GB) where heavy Docker containers or browser-based test runners choke system resources.
- **100% Local & Private**: Never uploads your code, metrics, or telemetry to external servers. All checks run locally on your hardware.
- **Graceful Tool Fallback**: Missing optional tools (e.g. Biome, FixMySlop, or Gradle) are gracefully skipped with informational notices instead of breaking your run.

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
