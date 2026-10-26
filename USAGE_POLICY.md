# Usage Policy & Guidelines

**Last Updated:** October 2026  
**Project:** Repo Quality Guard

---

## 1. Permitted Use

Repo Quality Guard is open-source software provided under the **MIT License**.

- **Personal & Educational**: Free to use, modify, and study for learning and personal codebases.
- **Open-Source Projects**: Recommended for use in pre-commit hooks, local developer workflows, and CI validation.
- **Commercial & Enterprise**: Permitted for auditing proprietary, client, or enterprise repositories without licensing fees or royalties.

---

## 2. Zero-Telemetry & Privacy Guarantee

Repo Quality Guard was designed from the ground up to respect developer privacy and intellectual property:

1. **100% Offline Execution**: The tool never makes outbound network connections, HTTP requests, or API pings during code audits.
2. **Zero Analytics**: No telemetry, tracking identifiers, crash dumps, or repository metadata are collected or sent anywhere.
3. **Local Hardware Processing**: All regex scanning, AST parsing, and file checks occur strictly in your local device's memory.

---

## 3. Safe Execution Protocol

- By default, Repo Quality Guard runs in **read-only audit mode**. It inspects your files without altering any source code.
- Source code modifications only occur if the user explicitly passes the `--fix` flag (which delegates safe autofixes to standard formatters like Ruff or Biome).
- Users are encouraged to ensure their repository has a clean Git working tree before applying automated fixes.

---

## 4. Responsible Secret Scanning

The **Secret Leak Guard** is intended as a defensive safety net to prevent accidental commits of credentials. 

- While it detects common API patterns (GitHub tokens, AWS keys, Google API keys, private RSA keys), developers should maintain proper secret management practices (e.g., `.gitignore`, environment variables, secret managers).
- The scanner should not be relied upon as the sole enterprise security audit mechanism.

---

## 5. Disclaimer of Warranty

The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability.
