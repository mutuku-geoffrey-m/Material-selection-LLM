"""
EMS-OS one-click launcher (Windows).

First run : installs whatever is missing (Python, Ollama, project dependencies, llama3.2:3b model),
            creates a desktop shortcut, then opens the Streamlit workbench.
Later runs: only checks that everything is still in place, starts Ollama / Streamlit if they are
            not already running, and opens the browser.

Build the .exe once with build_exe.bat (PyInstaller). Placed in the project root, the exe and the
desktop shortcut both run this same code.
"""
import hashlib, json, os, shutil, socket, subprocess, sys, threading, time, urllib.request, webbrowser
from pathlib import Path

APP_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
MODEL = os.getenv("LOCAL_MODEL", "llama3.2:3b")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

FROZEN = getattr(sys, "frozen", False)
ROOT = Path(sys.executable).resolve().parent if FROZEN else Path(__file__).resolve().parent.parent
STATE = ROOT / ".ems_setup_state.json"
LOG = ROOT / "launcher.log"
VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"


def say(msg):
    line = f"[EMS-OS] {msg}"
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")
    except OSError:
        pass


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, **kw)


def http_ok(url, timeout=2):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False


def port_open(port):
    with socket.socket() as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def load_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(d):
    STATE.write_text(json.dumps(d, indent=2), encoding="utf-8")


def download(url, dest):
    say(f"Downloading {url}")
    urllib.request.urlretrieve(url, dest)


# ---------------------------------------------------------------- Python
def find_python():
    for cmd in (["py", "-3.12"], ["py", "-3.11"], ["py", "-3.10"], ["python"]):
        try:
            out = subprocess.run(cmd + ["-c", "import sys;print('%d.%d'%sys.version_info[:2])"],
                                 capture_output=True, text=True, timeout=20, creationflags=NO_WINDOW)
            if out.returncode == 0 and out.stdout.strip() in ("3.10", "3.11", "3.12"):
                return cmd
        except Exception:
            pass
    local = Path(os.getenv("LOCALAPPDATA", "")) / "Programs" / "Python"
    for v in ("Python312", "Python311", "Python310"):
        exe = local / v / "python.exe"
        if exe.exists():
            return [str(exe)]
    return None


def ensure_python():
    py = find_python()
    if py:
        return py
    say("Python 3.10-3.12 not found. Installing Python 3.12 ...")
    if shutil.which("winget"):
        run(["winget", "install", "-e", "--id", "Python.Python.3.12", "--silent",
             "--accept-package-agreements", "--accept-source-agreements"])
    py = find_python()
    if not py:
        installer = ROOT / "python-installer.exe"
        download("https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe", installer)
        run([str(installer), "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_launcher=1"])
        installer.unlink(missing_ok=True)
        py = find_python()
    if not py:
        sys.exit("Could not install Python automatically. Install Python 3.12 from python.org and run again.")
    return py


# ---------------------------------------------------------------- venv + packages
def ensure_venv(py):
    if not VENV_PY.exists():
        say("Creating virtual environment (.venv) ...")
        run(py + ["-m", "venv", ".venv"], check=True)
    req = ROOT / "requirements.txt"
    digest = hashlib.sha256(req.read_bytes()).hexdigest()
    state = load_state()
    if state.get("requirements_sha") != digest:
        say("Installing project dependencies (first run takes a few minutes) ...")
        run([str(VENV_PY), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        run([str(VENV_PY), "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        state["requirements_sha"] = digest
        save_state(state)


# ---------------------------------------------------------------- Ollama
def find_ollama():
    exe = shutil.which("ollama")
    if exe:
        return exe
    for base in (os.getenv("LOCALAPPDATA", ""), os.getenv("ProgramFiles", "")):
        cand = Path(base) / "Programs" / "Ollama" / "ollama.exe" if base else None
        if cand and cand.exists():
            return str(cand)
        cand = Path(base) / "Ollama" / "ollama.exe" if base else None
        if cand and cand.exists():
            return str(cand)
    return None


def ensure_ollama():
    exe = find_ollama()
    if not exe:
        say("Ollama not found. Installing ...")
        if shutil.which("winget"):
            run(["winget", "install", "-e", "--id", "Ollama.Ollama", "--silent",
                 "--accept-package-agreements", "--accept-source-agreements"])
        exe = find_ollama()
        if not exe:
            installer = ROOT / "OllamaSetup.exe"
            download("https://ollama.com/download/OllamaSetup.exe", installer)
            run([str(installer), "/VERYSILENT", "/NORESTART"])
            installer.unlink(missing_ok=True)
            exe = find_ollama()
    if not exe:
        say("WARNING: Ollama could not be installed. The system will still run in deterministic mode.")
        return None
    say(f"Ollama found: {exe}")
    if http_ok(OLLAMA_URL + "/api/tags"):
        say("Ollama service is already running.")
    else:
        say("Starting Ollama service ...")
        subprocess.Popen([exe, "serve"], creationflags=NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(40):
            if http_ok(OLLAMA_URL + "/api/tags"):
                break
            time.sleep(1)
        if http_ok(OLLAMA_URL + "/api/tags"):
            say("Ollama service started and responding.")
        else:
            say("WARNING: Ollama did not respond within 40 s. LLM commentary will be skipped until it is running "
                "(rankings and costs are unaffected). Try opening the Ollama app from the Start menu.")
    return exe


def ensure_model(exe):
    try:
        with urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=5) as r:
            names = [m.get("name", "") for m in json.loads(r.read().decode()).get("models", [])]
    except Exception:
        say("WARNING: could not query Ollama for installed models.")
        return
    wanted = MODEL if ":" in MODEL else MODEL + ":latest"
    if wanted in names:
        say(f"Model {MODEL} is installed.")
    else:
        say(f"Downloading model {MODEL} (about 2 GB, first run only) ...")
        run([exe, "pull", MODEL])


def warm_model():
    """Load the model into memory so the first query does not pay the cold-start cost."""
    def _go():
        try:
            body = json.dumps({"model": MODEL, "prompt": "ok", "stream": False, "keep_alive": "30m",
                               "options": {"num_predict": 1, "num_ctx": 2048, "num_thread": 4}}).encode()
            req = urllib.request.Request(OLLAMA_URL + "/api/generate", data=body,
                                         headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=300).read()
            say(f"Model {MODEL} is loaded in memory and ready.")
        except Exception as exc:
            say(f"WARNING: model warm-up failed ({type(exc).__name__}); the first LLM request may be slow.")
    say(f"Loading {MODEL} into memory in the background ...")
    threading.Thread(target=_go, daemon=True).start()


# ---------------------------------------------------------------- shortcut
def ensure_shortcut():
    state = load_state()
    target = sys.executable if FROZEN else str(ROOT / "Start_EMS-OS.bat")
    ps = (
        "$d=[Environment]::GetFolderPath('Desktop');"
        "$s=(New-Object -ComObject WScript.Shell).CreateShortcut(\"$d\\EMS-OS.lnk\");"
        f"$s.TargetPath='{target}';$s.WorkingDirectory='{ROOT}';"
        "$s.Description='EMS-OS Material Selection Workbench';$s.Save();Write-Output \"$d\\EMS-OS.lnk\""
    )
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True,
                         creationflags=NO_WINDOW)
    if out.returncode == 0:
        state["shortcut"] = out.stdout.strip()
        save_state(state)
        say("Desktop shortcut created: EMS-OS")


def shortcut_exists():
    p = load_state().get("shortcut")
    return bool(p) and Path(p).exists()


# ---------------------------------------------------------------- main
def load_env_file():
    """Read .env (LOCAL_MODEL, OLLAMA_BASE_URL, ...) so the launcher uses the same settings as the app."""
    global MODEL, OLLAMA_URL, APP_PORT
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.split("#")[0].strip())
    MODEL = os.getenv("LOCAL_MODEL", MODEL)
    OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", OLLAMA_URL).rstrip("/")
    APP_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", str(APP_PORT)))


def main():
    os.chdir(ROOT)
    if not (ROOT / "app.py").exists():
        sys.exit(f"app.py not found in {ROOT}. Keep EMS-OS.exe in the project folder.")
    if port_open(APP_PORT):
        say("EMS-OS is already running - opening the browser.")
        webbrowser.open(f"http://localhost:{APP_PORT}")
        return

    fast = VENV_PY.exists() and load_state().get("requirements_sha") == hashlib.sha256(
        (ROOT / "requirements.txt").read_bytes()).hexdigest()
    if fast:
        say("Setup already complete - starting EMS-OS.")
    else:
        say("First-time setup. This needs an internet connection and may take 10-20 minutes.")
        ensure_venv(ensure_python())

    if not (ROOT / ".env").exists() and (ROOT / ".env.example").exists():
        shutil.copy(ROOT / ".env.example", ROOT / ".env")
    load_env_file()

    exe = ensure_ollama()
    if exe:
        ensure_model(exe)
        warm_model()
    if not shortcut_exists():
        ensure_shortcut()

    say(f"Launching the workbench at http://localhost:{APP_PORT}")
    proc = subprocess.Popen([str(VENV_PY), "-m", "streamlit", "run", "app.py",
                             "--server.port", str(APP_PORT), "--server.address", "127.0.0.1", "--server.headless", "true",
                             "--browser.gatherUsageStats", "false"], cwd=ROOT)
    for _ in range(90):
        if port_open(APP_PORT):
            break
        time.sleep(1)
    webbrowser.open(f"http://localhost:{APP_PORT}")
    say("Running. Close this window to stop EMS-OS.")
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        say(f"ERROR: {exc!r}  (see launcher.log)")
        input("Press Enter to close ...")
