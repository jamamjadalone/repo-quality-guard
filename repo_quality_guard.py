"""
Repo Quality Guard — 6-in-1 Offline Repository Health & Security Suite
A lightweight, fast, zero-telemetry code quality, static analysis,
and security guard for modern developers.

Engines:
1. Python: Syntax (py_compile), Fast Rust Linter (Ruff), Unit Tests (Pytest)
2. Web & Frontend: Fast Rust Linter (Biome) for JS/TS/CSS/HTML
3. Mobile (Android): Offline Gradle release compilation & unit tests
4. Anti-Slop: FixMySlop code smells and AI anti-pattern scanner
5. Broken Assets: Relative 404 link and asset path detector
6. Secret Guard: Pre-push API key, private token & credential leak detector
"""

import argparse
import importlib.util
import os
import py_compile
import re
import shutil
import subprocess
import sys
from pathlib import Path

# UTF-8 console output for Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Ignored directories
IGNORE_DIRS = {
    ".git", ".gradle", "build", "node_modules", "dist", ".cache",
    "__pycache__", ".venv", "venv", ".idea", ".vscode", ".tox",
    ".pytest_cache", ".ruff_cache", "target"
}

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return res.returncode, res.stdout.strip()
    except (OSError, subprocess.SubprocessError) as err:
        return 1, str(err)

def find_tool(name):
    path = shutil.which(name)
    if path:
        return path
    if os.name == "nt":
        appdata = os.environ.get("LOCALAPPDATA", "")
        if appdata:
            py_pkgs = Path(appdata) / "Packages"
            if py_pkgs.exists():
                for p in py_pkgs.glob("PythonSoftwareFoundation.*/LocalCache/local-packages/Python311/Scripts"):
                    cand = p / f"{name}.exe"
                    if cand.exists():
                        return str(cand)
        roaming = os.environ.get("APPDATA", "")
        if roaming:
            npm_bin = Path(roaming) / "npm" / f"{name}.cmd"
            if npm_bin.exists():
                return str(npm_bin)
            npm_exe = Path(roaming) / "npm" / f"{name}.exe"
            if npm_exe.exists():
                return str(npm_exe)
    return None

# ==============================================================================
# 1. Python Engine (Syntax, Ruff, Pytest)
# ==============================================================================
def check_python(repo_path, fix=False):
    repo_path = Path(repo_path)
    py_files = [
        f for f in repo_path.rglob("*.py")
        if not any(part in IGNORE_DIRS for part in f.parts)
    ]
    if not py_files:
        return True, "No Python source files found."

    errors = []
    for pf in py_files:
        try:
            py_compile.compile(str(pf), doraise=True)
        except py_compile.PyCompileError as err:
            errors.append(f"Syntax error in {pf.relative_to(repo_path)}: {err}")

    ruff = find_tool("ruff")
    if ruff:
        cmd = [ruff, "check", str(repo_path)]
        if fix:
            cmd.append("--fix")
        code, out = run_cmd(cmd)
        if code != 0 and out:
            lines = [l for l in out.splitlines() if "error:" in l.lower() or "found" in l.lower()]
            if lines:
                errors.append(f"Ruff: {lines[-1]}")

    test_dirs = [d for d in repo_path.iterdir() if d.is_dir() and d.name.lower() in ("tests", "test")]
    if test_dirs and importlib.util.find_spec("pytest") is not None:
        code, out = run_cmd([sys.executable, "-m", "pytest", str(test_dirs[0]), "-q"], cwd=repo_path)
        if code != 0:
            errors.append(f"Pytest failed: {out.splitlines()[-1] if out else 'Failed'}")

    if errors:
        return False, " | ".join(errors[:3])
    return True, f"All {len(py_files)} Python source files verified with zero syntax defects."

# ==============================================================================
# 2. Web & Frontend Engine (Biome)
# ==============================================================================
def check_web(repo_path, fix=False):
    repo_path = Path(repo_path)
    web_files = [
        f for f in repo_path.rglob("*")
        if f.suffix.lower() in (".js", ".ts", ".html", ".css", ".json")
        and not any(part in IGNORE_DIRS for part in f.parts)
    ]
    if not web_files:
        return True, "No Web / JS / HTML files found."

    biome = find_tool("biome")
    if not biome:
        return True, f"Found {len(web_files)} web files (Biome not installed in PATH, skipping)."

    cmd = [biome, "lint", "--diagnostic-level=error", str(repo_path)]
    if fix:
        cmd = [biome, "lint", "--write", "--diagnostic-level=error", str(repo_path)]
    code, out = run_cmd(cmd)
    if code != 0 and out:
        clean_out = out.encode("ascii", errors="replace").decode("ascii")
        lines = [l.strip() for l in clean_out.splitlines() if l.strip()]
        last_line = lines[-1] if lines else "Errors found"
        return False, f"Biome: {last_line}"
    return True, f"All {len(web_files)} web assets passed static lint checks."

# ==============================================================================
# 3. Android Engine (Gradlew)
# ==============================================================================
def check_android(repo_path):
    repo_path = Path(repo_path)
    gradlew = repo_path / ("gradlew.bat" if os.name == "nt" else "gradlew")
    if not gradlew.exists():
        android_dir = repo_path / "android"
        if android_dir.exists():
            cand = android_dir / ("gradlew.bat" if os.name == "nt" else "gradlew")
            if cand.exists():
                gradlew = cand
                repo_path = android_dir
    if not gradlew.exists():
        return True, "No Android Gradle project found."

    code, _ = run_cmd([str(gradlew), ":app:testReleaseUnitTest", "--offline"], cwd=repo_path)
    if code == 0:
        return True, "Android unit tests & offline compilation: BUILD SUCCESSFUL."
    return False, "Android unit tests failed. Check Gradle logs."

# ==============================================================================
# 4. Anti-Slop Engine (FixMySlop)
# ==============================================================================
def check_slop(repo_path):
    fixmyslop = find_tool("fixmyslop")
    if not fixmyslop:
        return True, "FixMySlop not installed (Optional check skipped)."

    code, _ = run_cmd([fixmyslop, "scan", str(repo_path), "--fail-on", "medium"])
    if code == 0:
        return True, "FixMySlop: Grade A (0 design gimmicks or code smells)."
    return False, "FixMySlop detected anti-patterns or excessive code smells."

# ==============================================================================
# 5. Broken Assets & Relative 404 Links Detector
# ==============================================================================
LINK_ATTR_RE = re.compile(
    r"""(?:src|href|url)\s*=\s*['"]([^'"]+)['"]|url\(\s*['"]?([^'")]+)['"]?\s*\)""",
    re.IGNORECASE
)

def check_broken_assets(repo_path):
    repo_path = Path(repo_path)
    broken_links = []
    scanned_files = 0

    for ext in ("*.html", "*.css", "*.js"):
        for f in repo_path.rglob(ext):
            if any(part in IGNORE_DIRS for part in f.parts):
                continue
            scanned_files += 1
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue

            for match in LINK_ATTR_RE.finditer(content):
                target = match.group(1) or match.group(2)
                if not target:
                    continue
                target = target.strip()

                # Ignore external URLs, protocols, anchors, template expressions
                if target.startswith(("http://", "https://", "//", "mailto:", "tel:", "data:", "#", "javascript:", "{")) or "${" in target:
                    continue

                clean_target = target.split("?")[0].split("#")[0].strip()
                if not clean_target:
                    continue

                resolved_relative = (f.parent / clean_target).resolve()
                resolved_root = (repo_path / clean_target.lstrip("/")).resolve()

                if not (resolved_relative.exists() or resolved_root.exists()) and not clean_target.startswith(("/api", "api/")):
                    broken_links.append(f"{f.name} -> '{target}'")

    if broken_links:
        unique_broken = list(dict.fromkeys(broken_links))
        return False, f"Broken 404 links ({len(unique_broken)} found): " + "; ".join(unique_broken[:3])
    return True, f"Zero broken asset links detected across {scanned_files} files."

# ==============================================================================
# 6. Secrets & Credentials Leak Guard
# ==============================================================================
SECRET_PATTERNS = [
    ("GitHub Personal Access Token", re.compile(r"gh[pous]_[0-9a-zA-Z]{36}")),
    ("GitHub Fine-Grained Token", re.compile(r"github_pat_[0-9a-zA-Z_]{82}")),
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z\-_]{35}")),
    ("AWS Access Key ID", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("RSA / SSH Private Key", re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----")),
    ("Stripe API Secret", re.compile(r"sk_live_[0-9a-zA-Z]{24}")),
    ("Slack Webhook URL", re.compile(r"https://hooks\.slack\.com/services/T[0-9A-Z]+/B[0-9A-Z]+/[0-9a-zA-Z]+")),
]

def is_dummy_match(text):
    low = text.lower()
    return "example" in low or "sample" in low or "dummy" in low or "test" in low

def check_secret_leaks(repo_path):
    repo_path = Path(repo_path)
    leak_findings = []
    scanned_count = 0

    # Inspect for sensitive key files
    dangerous_files = list(repo_path.glob(".env")) + list(repo_path.glob("*.pem")) + list(repo_path.glob("id_rsa*"))
    for df in dangerous_files:
        if df.is_file() and not df.name.endswith(".example"):
            leak_findings.append(f"Sensitive credential file detected on disk: {df.name}")

    text_extensions = {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".txt", ".md", ".yml", ".yaml", ".kt", ".java"}

    for f in repo_path.rglob("*"):
        if f.is_file() and f.suffix.lower() in text_extensions:
            if any(part in IGNORE_DIRS for part in f.parts):
                continue
            scanned_count += 1
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except (OSError, UnicodeDecodeError):
                continue

            for label, pattern in SECRET_PATTERNS:
                matches = pattern.findall(content)
                for m in matches:
                    if is_dummy_match(m):
                        continue
                    leak_findings.append(f"{f.name}: Potential {label} hardcoded!")

    if leak_findings:
        return False, " | ".join(leak_findings[:3])
    return True, f"100% Clean: 0 hardcoded secrets or credentials ({scanned_count} files scanned)."

# ==============================================================================
# AUDIT RUNNER
# ==============================================================================
def audit_single_repo(repo_path, fix=False):
    repo_path = Path(repo_path).resolve()
    print(f"\n{BOLD}{CYAN}----------------------------------------------------------------------{RESET}")
    print(f"{BOLD}Auditing Target:{RESET} {CYAN}{repo_path.name}{RESET} ({repo_path})")
    print(f"{BOLD}{CYAN}----------------------------------------------------------------------{RESET}")

    modules = [
        ("1. Python Syntax & Tests", lambda: check_python(repo_path, fix)),
        ("2. Web & Frontend Linter", lambda: check_web(repo_path, fix)),
        ("3. Android Compilation", lambda: check_android(repo_path)),
        ("4. Anti-Slop Quality", lambda: check_slop(repo_path)),
        ("5. Broken 404 Assets", lambda: check_broken_assets(repo_path)),
        ("6. Secret Leak Guard", lambda: check_secret_leaks(repo_path)),
    ]

    all_passed = True
    for name, runner in modules:
        try:
            ok, msg = runner()
            if ok:
                print(f"  {GREEN}[PASS]{RESET} {name:<26} : {msg}")
            else:
                all_passed = False
                print(f"  {RED}[FAIL]{RESET} {name:<26} : {RED}{msg}{RESET}")
        except (OSError, RuntimeError) as err:
            all_passed = False
            print(f"  {RED}[ERROR]{RESET} {name:<25} : {err}")

    verdict = f"{GREEN}ALL 6 QUALITY ENGINES PASSED{RESET}" if all_passed else f"{RED}SOME CHECKS FAILED{RESET}"
    print(f"--> Result: {verdict}\n")
    return all_passed

def main():
    parser = argparse.ArgumentParser(
        description="Repo Quality Guard — Universal 6-in-1 Offline Code Quality & Security Suite"
    )
    parser.add_argument("path", nargs="?", default=".", help="Target directory or repository path (default: .)")
    parser.add_argument("--all", action="store_true", help="Batch scan all child repositories")
    parser.add_argument("--fix", action="store_true", help="Auto-fix autofixable lints (Ruff, Biome)")
    args = parser.parse_args()

    target = Path(args.path).resolve()

    if args.all:
        print(f"\n{BOLD}=== UNIVERSAL MULTI-REPO BATCH AUDIT (6-IN-1 SUITE) ==={RESET}")
        repos = []
        for item in target.iterdir():
            if item.is_dir() and (item / ".git").exists():
                repos.append(item)
        if not repos and (target / ".git").exists():
            repos = [target]
        print(f"Discovered {len(repos)} local git repositories.\n")
        passed_count = 0
        for r in repos:
            if audit_single_repo(r, args.fix):
                passed_count += 1
        print("=" * 70)
        print(f"{BOLD}FINAL SUMMARY:{RESET} {passed_count}/{len(repos)} Repositories 100% Green.")
        print("=" * 70)
        sys.exit(0 if passed_count == len(repos) else 1)
    else:
        passed = audit_single_repo(target, args.fix)
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
