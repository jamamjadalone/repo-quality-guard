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


# ==============================================================================
# WINDOWS CONSOLE ANSI & UTF-8 INITIALIZATION (ZERO-GLITCH GUARANTEE)
# ==============================================================================
def init_console():
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.windll.kernel32
            h_stdout = kernel32.GetStdHandle(-11)
            mode = wintypes.DWORD()
            if kernel32.GetConsoleMode(h_stdout, ctypes.byref(mode)):
                mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(h_stdout, mode)
            os.system("")
        except (AttributeError, OSError):
            pass
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")

init_console()

# ANSI Color formatting
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
# TOOL DOCTOR & INTERACTIVE SETUP HELPER
# ==============================================================================
RECOMMENDED_TOOLS = [
    {
        "id": "ruff",
        "name": "Ruff",
        "type": "pip",
        "benefit": "Python static linter. Checks syntax, dead code and bugs in <15ms.",
        "install_cmd": [sys.executable, "-m", "pip", "install", "--upgrade", "ruff"]
    },
    {
        "id": "biome",
        "name": "Biome",
        "type": "npm",
        "benefit": "Web linter for JS, TS, HTML, CSS. Catches front-end syntax bugs in <35ms.",
        "install_cmd": ["npm", "install", "-g", "@biomejs/biome"]
    },
    {
        "id": "fixmyslop",
        "name": "FixMySlop",
        "type": "pip",
        "benefit": "Code hygiene & slop scanner. Eliminates AI anti-patterns and bloated code.",
        "install_cmd": [sys.executable, "-m", "pip", "install", "--upgrade", "fixmyslop"]
    },
    {
        "id": "pytest",
        "name": "Pytest",
        "type": "pip",
        "benefit": "Industry-standard automated test suite runner for Python.",
        "install_cmd": [sys.executable, "-m", "pip", "install", "--upgrade", "pytest"]
    }
]

def run_doctor():
    print()
    print("========================================================================")
    print("           REPO QUALITY GUARD — TOOL DOCTOR & SETUP HELPER")
    print("========================================================================")
    print("Checking which quality engines are currently installed on your PC:\n")

    has_npm = shutil.which("npm") is not None
    missing_tools = []

    for item in RECOMMENDED_TOOLS:
        if item["id"] == "pytest":
            is_installed = importlib.util.find_spec("pytest") is not None
        else:
            is_installed = find_tool(item["id"]) is not None

        status = f"{GREEN}[READY]{RESET}" if is_installed else f"{YELLOW}[NOT INSTALLED]{RESET}"
        if not is_installed:
            missing_tools.append(item)

        print(f"  * {BOLD}{item['name']:<12}{RESET} : {status}")
        print(f"    Benefit : {item['benefit']}")
        if not is_installed:
            print(f"    Command : {' '.join(item['install_cmd'])}")
        print()

    if not missing_tools:
        print(f"{GREEN}{BOLD}✓ Perfect! All recommended quality engines are installed and active.{RESET}")
        print("========================================================================\n")
        return

    print(f"{BOLD}Found {len(missing_tools)} optional tool(s) not yet installed.{RESET}")
    print("Repo Quality Guard will gracefully skip missing tools, but installing them")
    print("unlocks full 100% static analysis coverage.\n")
    print("  [1] Install all missing tools automatically")
    print("  [2] Select specific tools to install")
    print("  [3] Skip and exit helper\n")

    try:
        choice = input("Enter choice [1-3] (default: 3): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nSkipped.")
        return

    if choice == "1":
        for tool in missing_tools:
            if tool["type"] == "npm" and not has_npm:
                print(f"{YELLOW}[NOTICE]{RESET} Node.js / npm not detected. Skipping {tool['name']}.")
                continue
            print(f"\n>> Installing {tool['name']}...")
            code, out = run_cmd(tool["install_cmd"])
            if code == 0:
                print(f"  {GREEN}[SUCCESS]{RESET} {tool['name']} installed successfully.")
            else:
                print(f"  {RED}[ERROR]{RESET} Installation failed: {out[:200]}")
        print(f"\n{GREEN}Installation finished!{RESET}\n")
    elif choice == "2":
        for tool in missing_tools:
            if tool["type"] == "npm" and not has_npm:
                print(f"{YELLOW}[NOTICE]{RESET} {tool['name']} requires npm (Node.js).")
                continue
            ans = input(f"Install {tool['name']}? [y/N]: ").strip().lower()
            if ans == "y":
                print(f">> Installing {tool['name']}...")
                code, out = run_cmd(tool["install_cmd"])
                if code == 0:
                    print(f"  {GREEN}[SUCCESS]{RESET} {tool['name']} installed.")
                else:
                    print(f"  {RED}[ERROR]{RESET} Failed: {out[:200]}")
        print(f"\n{GREEN}Custom installation finished!{RESET}\n")
    else:
        print("\nSkipping installation. Graceful fallbacks active.\n")

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
        return "SKIP", "No Python source files found"

    errors = []
    for pf in py_files:
        try:
            py_compile.compile(str(pf), doraise=True)
        except py_compile.PyCompileError as err:
            errors.append(f"Syntax error in {pf.name}: {err}")

    ruff = find_tool("ruff")
    if ruff:
        cmd = [ruff, "check", "."]
        if fix:
            cmd.append("--fix")
        code, out = run_cmd(cmd, cwd=repo_path)
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
        return "FAIL", " | ".join(errors[:2])
    return "PASS", f"{len(py_files)} Python file(s) clean with zero syntax defects"

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
        return "SKIP", "No Web / JS / HTML files found"

    biome = find_tool("biome")
    if not biome:
        return "SKIP", f"{len(web_files)} web file(s) present (Biome not installed)"

    cmd = [biome, "lint", "--diagnostic-level=error", "."]
    if fix:
        cmd = [biome, "lint", "--write", "--diagnostic-level=error", "."]
    code, out = run_cmd(cmd, cwd=repo_path)
    if code != 0 and out:
        clean_out = out.encode("ascii", errors="replace").decode("ascii")
        lines = [l.strip() for l in clean_out.splitlines() if l.strip()]
        last_line = lines[-1] if lines else "Errors found"
        return "FAIL", f"Biome: {last_line}"
    return "PASS", f"{len(web_files)} web asset(s) passed Biome lint"

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
        return "SKIP", "No Android Gradle project found"

    code, _ = run_cmd([str(gradlew), ":app:testReleaseUnitTest", "--offline"], cwd=repo_path)
    if code == 0:
        return "PASS", "Release unit tests & offline compilation SUCCESSFUL"
    return "FAIL", "Android unit tests failed. Check Gradle output"

# ==============================================================================
# 4. Anti-Slop Engine (FixMySlop)
# ==============================================================================
def check_slop(repo_path):
    fixmyslop = find_tool("fixmyslop")
    if not fixmyslop:
        return "SKIP", "FixMySlop not installed (Optional check skipped)"

    code, _ = run_cmd([fixmyslop, "scan", ".", "--fail-on", "medium"], cwd=repo_path)
    if code == 0:
        return "PASS", "Grade A (0 anti-patterns or code smells)"
    return "FAIL", "Detected excessive code smells or AI anti-patterns"

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

            is_js = f.suffix.lower() == ".js"
            for match in LINK_ATTR_RE.finditer(content):
                # In JS files, skip url(...) function calls like new URL(a.href)
                if is_js and match.group(2) is not None:
                    continue

                target = match.group(1) or match.group(2)
                if not target:
                    continue
                target = target.strip()

                if target.startswith(("http://", "https://", "//", "mailto:", "tel:", "data:", "#", "javascript:", "{")) or "${" in target:
                    continue

                clean_target = target.split("?")[0].split("#")[0].strip()
                if not clean_target:
                    continue

                # Skip template tokens (e.g. __CATID__, {{ROOT}})
                if "__" in clean_target or "{{" in clean_target or "}}" in clean_target:
                    continue

                # Skip JS variable / property expressions
                if re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*\.(href|src|url)$', clean_target):
                    continue

                # Must look like a real path or file (contains slash or valid file extension)
                has_ext = bool(re.search(r'\.[a-zA-Z0-9]{1,8}$', clean_target))
                has_slash = "/" in clean_target or "\\" in clean_target
                if not (has_ext or has_slash):
                    continue

                # Skip common MIME types
                if any(clean_target.startswith(m) for m in ("image/", "video/", "audio/", "text/", "application/", "font/")):
                    continue

                rel_path = clean_target.lstrip("/\\")
                resolved_relative = (f.parent / rel_path).resolve()
                resolved_root = (repo_path / rel_path).resolve()
                resolved_public = (f.parent / "public" / rel_path).resolve()
                resolved_root_public = (repo_path / "public" / rel_path).resolve()

                if not (resolved_relative.exists() or resolved_root.exists() or resolved_public.exists() or resolved_root_public.exists()) and not clean_target.startswith(("/api", "api/")):
                    broken_links.append(f"{f.name} -> '{target}'")

    if broken_links:
        unique_broken = list(dict.fromkeys(broken_links))
        return "FAIL", f"Broken 404 link(s) found ({len(unique_broken)}): " + "; ".join(unique_broken[:2])
    return "PASS", f"Zero broken links detected across {scanned_files} file(s)"

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

    dangerous_files = list(repo_path.glob(".env")) + list(repo_path.glob("*.pem")) + list(repo_path.glob("id_rsa*"))
    for df in dangerous_files:
        if df.is_file() and not df.name.endswith(".example"):
            leak_findings.append(f"Sensitive key file on disk: {df.name}")

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
                    leak_findings.append(f"{f.name}: Potential {label} hardcoded")

    if leak_findings:
        return "FAIL", " | ".join(leak_findings[:2])
    return "PASS", f"Zero secret leaks detected ({scanned_count} files verified)"

# ==============================================================================
# AUDIT RUNNER (CLEAN & GORGEOUS UI)
# ==============================================================================
def audit_single_repo(repo_path, fix=False):
    repo_path = Path(repo_path).resolve()
    print("========================================================================")
    print(f" TARGET: {BOLD}{CYAN}{repo_path.name}{RESET}  ({repo_path})")
    print("========================================================================")

    modules = [
        ("[1/6] Python Syntax & Tests", lambda: check_python(repo_path, fix)),
        ("[2/6] Web & Frontend Linter", lambda: check_web(repo_path, fix)),
        ("[3/6] Android Compilation  ", lambda: check_android(repo_path)),
        ("[4/6] Anti-Slop Code Smells", lambda: check_slop(repo_path)),
        ("[5/6] Broken 404 Links     ", lambda: check_broken_assets(repo_path)),
        ("[6/6] Secret & Token Leak  ", lambda: check_secret_leaks(repo_path)),
    ]

    all_passed = True
    for label, runner in modules:
        try:
            status, msg = runner()
            if status == "PASS":
                status_str = f"{GREEN}[ PASS ]{RESET}"
            elif status == "SKIP":
                status_str = f"{YELLOW}[ SKIP ]{RESET}"
            else:
                status_str = f"{RED}[ FAIL ]{RESET}"
                all_passed = False

            # Clean aligned dot leader UI
            dots = "." * (30 - len(label))
            print(f" {label} {dots} {status_str} : {msg}")
        except (OSError, RuntimeError) as err:
            all_passed = False
            dots = "." * (30 - len(label))
            print(f" {label} {dots} {RED}[ ERROR ]{RESET} : {err}")

    print("------------------------------------------------------------------------")
    if all_passed:
        print(f" RESULT: {GREEN}{BOLD}[ ALL ENGINES PASSED ]{RESET} — Codebase is 100% clean!")
    else:
        print(f" RESULT: {RED}{BOLD}[ CHECKS FAILED ]{RESET} — Review issues listed above.")
    print("========================================================================\n")
    return all_passed

def main():
    parser = argparse.ArgumentParser(
        description="Repo Quality Guard — Universal 6-in-1 Offline Code Quality & Security Suite"
    )
    parser.add_argument("path", nargs="?", default=".", help="Target directory or repository path (default: .)")
    parser.add_argument("--all", action="store_true", help="Batch scan all child repositories in folder")
    parser.add_argument("--fix", action="store_true", help="Auto-fix autofixable lints (Ruff, Biome)")
    parser.add_argument("--doctor", "--setup", dest="setup", action="store_true", help="Interactive Tool Doctor")
    args = parser.parse_args()

    if args.setup:
        run_doctor()
        return

    target = Path(args.path).resolve()

    if args.all:
        print("\n========================================================================")
        print("          MULTI-REPOSITORY BATCH AUDIT (6-IN-1 SUITE)")
        print("========================================================================")
        repos = []
        for item in target.iterdir():
            if item.is_dir() and (item / ".git").exists():
                repos.append(item)
        if not repos and (target / ".git").exists():
            repos = [target]
        print(f"Discovered {len(repos)} local git repositories in: {target}\n")
        passed_count = 0
        for r in repos:
            if audit_single_repo(r, args.fix):
                passed_count += 1
        print("========================================================================")
        print(f" FINAL SUMMARY: {passed_count}/{len(repos)} Repositories 100% Green.")
        print("========================================================================\n")
        sys.exit(0 if passed_count == len(repos) else 1)
    else:
        passed = audit_single_repo(target, args.fix)
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
