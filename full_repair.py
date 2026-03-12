#!/usr/bin/env python3
"""Imperio Studio - Full Repair Script v1.18.10"""
import gzip, base64, os, sys, platform, shutil, subprocess, zipfile, time, hashlib, urllib.request, ssl, tempfile

LAUNCHER_DATA = (
    "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"
    "ROR3dowrhbwca35+EoVuDv4XI0i7DK9tAAA="
)

ZIP_URL = "https://raw.githubusercontent.com/jaxonjma/Prueba/master/batchy.zip"
EXPECTED_HASH = "921d90c435868c589fd6b9e828ae1e060301b66e80737bcc007fb2c04eb4953e"
VERSION = "v1.18.10"

def get_dirs():
    system = platform.system()
    if system == "Windows":
        base = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
        batchy_dir = os.path.join(base, "Batchy")
    elif system == "Darwin":
        batchy_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Batchy")
    else:
        batchy_dir = os.path.join(os.path.expanduser("~"), ".batchy")
    return batchy_dir, os.path.join(batchy_dir, "app"), os.path.join(batchy_dir, "python")

def kill_streamlit():
    print("  Stopping any running app...")
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
    else:
        for port in [8501, 8502]:
            try:
                result = subprocess.run(["lsof", "-ti", ":" + str(port)], capture_output=True, text=True)
                for pid in (result.stdout.strip().split() if result.stdout.strip() else []):
                    try:
                        subprocess.run(["kill", "-9", pid], capture_output=True)
                        print("    Killed PID " + pid + " on port " + str(port))
                    except Exception:
                        pass
            except Exception:
                pass
    time.sleep(1)

def download_zip(url, dest_path):
    print("  Downloading v1.18.10 app files (~920KB)...")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    def progress(count, block, total):
        if total > 0:
            pct = min(100, count * block * 100 // total)
            print("\r    " + str(pct) + "%", end="", flush=True)
    urllib.request.urlretrieve(url, dest_path, reporthook=progress)
    print()

def install_zip(zip_path, app_dir):
    print("  Installing files...")
    backup = app_dir + ".bak"
    if os.path.exists(backup):
        shutil.rmtree(backup)
    if os.path.exists(app_dir):
        shutil.copytree(app_dir, backup)
        shutil.rmtree(app_dir)
    os.makedirs(app_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(app_dir)
    print("    Extracted " + str(len(os.listdir(app_dir))) + " files")

def find_python(python_dir):
    system = platform.system()
    if system == "Windows":
        candidates = [os.path.join(python_dir, "python.exe"), "python", "python3"]
    else:
        candidates = [os.path.join(python_dir, "bin", "python3"), os.path.join(python_dir, "bin", "python"), "python3", "python"]
    for c in candidates:
        try:
            r = subprocess.run([c, "--version"], capture_output=True, timeout=5)
            if r.returncode == 0:
                return c
        except Exception:
            pass
    return sys.executable

print("Imperio Studio - Full Repair (v1.18.10)")
print("=" * 44)
BATCHY_DIR, APP_DIR, PYTHON_DIR = get_dirs()
print("  Platform : " + platform.system())
print("  Batchy   : " + BATCHY_DIR)

if not os.path.exists(BATCHY_DIR):
    print("ERROR: Imperio Studio not found at " + BATCHY_DIR)
    sys.exit(1)

kill_streamlit()

with tempfile.TemporaryDirectory() as tmp:
    zip_path = os.path.join(tmp, "batchy.zip")
    try:
        download_zip(ZIP_URL, zip_path)
    except Exception as e:
        print("  Download failed: " + str(e))
        sys.exit(1)
    
    with open(zip_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()
    if actual_hash != EXPECTED_HASH:
        print("  WARNING: Hash mismatch — proceeding anyway")
    else:
        print("  Hash OK")
    
    install_zip(zip_path, APP_DIR)

# Save launcher
launcher_path = os.path.join(BATCHY_DIR, "batchy_launcher.py")
launcher_bytes = gzip.decompress(base64.b64decode("".join(LAUNCHER_DATA.split())))
with open(launcher_path, "wb") as f:
    f.write(launcher_bytes)
print("  Launcher updated: " + launcher_path)

# Save version
version_path = os.path.join(BATCHY_DIR, "version.txt")
with open(version_path, "w") as f:
    f.write(VERSION)
print("  Version saved: " + VERSION)

# Launch app
PYTHON_EXE = find_python(PYTHON_DIR)
print()
print("Launching Imperio Studio v1.18.10...")
if platform.system() == "Darwin":
    script_content = "#!/bin/bash\ncd \"$(dirname \"$0\"))\"\n\"" + PYTHON_EXE + "\" \"" + launcher_path + "\"\n"
    sh_path = os.path.join(BATCHY_DIR, "_launch.sh")
    with open(sh_path, "w") as f:
        f.write(script_content)
    os.chmod(sh_path, 0o755)
    subprocess.Popen(["open", "-a", "Terminal", sh_path])
    print("A new Terminal window will open with the app.")
    print("(You can close this window)")
elif platform.system() == "Windows":
    subprocess.Popen([PYTHON_EXE, launcher_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("App launched in a new window.")
else:
    subprocess.Popen([PYTHON_EXE, launcher_path])
    print("App launched.")
