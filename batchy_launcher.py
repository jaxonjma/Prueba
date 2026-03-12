#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import subprocess
import threading
import time
import shutil
import zipfile
import tempfile
import webbrowser
import socket
import logging
import tkinter as tk
from tkinter import ttk

BATCHY_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BATCHY_DIR, "app")
PYTHON_DIR = os.path.join(BATCHY_DIR, "python")
FFMPEG_DIR = os.path.join(BATCHY_DIR, "ffmpeg")
CONFIG_DIR = os.path.join(BATCHY_DIR, ".batchy")
VERSION_FILE = os.path.join(CONFIG_DIR, "version.txt")
LOG_FILE = os.path.join(CONFIG_DIR, "launcher.log")
STREAMLIT_PORT = 8501 if __import__('platform').system() == 'Darwin' else 5000

os.makedirs(CONFIG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_log = logging.getLogger("launcher")

sys.path.insert(0, APP_DIR)


def get_python_exe():
    import platform as plat
    if plat.system() == "Windows":
        exe = os.path.join(PYTHON_DIR, "python.exe")
        if not os.path.exists(exe):
            for root, dirs, files in os.walk(PYTHON_DIR):
                if "python.exe" in files:
                    return os.path.join(root, "python.exe")
        return exe
    else:
        exe = os.path.join(PYTHON_DIR, "bin", "python3")
        if not os.path.exists(exe):
            for root, dirs, files in os.walk(PYTHON_DIR):
                if "python3" in files:
                    return os.path.join(root, "python3")
        return exe


def get_current_version():
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r") as f:
                v = f.read().strip()
            if v and v != "v0.0.0":
                return v
    except Exception:
        pass
    try:
        import re as _re
        app_path = os.path.join(APP_DIR, "app.py")
        if os.path.exists(app_path):
            with open(app_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(8000)
            m = _re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', content)
            if m:
                v = m.group(1)
                save_version(v)
                return v
            if content.strip().startswith("import zlib"):
                try:
                    import zlib as _z, base64 as _b
                    data_m = _re.search(
                        r'_\w+\s*=\s*\(\n((?:[ \t]+"[^"]+"\n)+)\)', content
                    )
                    if data_m:
                        chunks = _re.findall(r'"([^"]+)"', data_m.group(1))
                        xored = _z.decompress(_b.b64decode("".join(chunks)))
                        key_parts = _re.findall(
                            r'_\w+\s*=\s*"([A-Za-z0-9+/=]{15,})"', content
                        )
                        candidates = [xored]
                        for ki in range(len(key_parts) - 1):
                            try:
                                xor_key = _b.b64decode(
                                    key_parts[ki] + key_parts[ki + 1]
                                )
                                candidates.append(
                                    bytes(
                                        a ^ xor_key[j % len(xor_key)]
                                        for j, a in enumerate(xored)
                                    )
                                )
                            except Exception:
                                pass
                        for candidate in candidates:
                            try:
                                decoded = candidate.decode("utf-8", errors="ignore")[:3000]
                                m2 = _re.search(
                                    r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', decoded
                                )
                                if m2:
                                    v = m2.group(1)
                                    if v.startswith("v") and "." in v:
                                        save_version(v)
                                        return v
                            except Exception:
                                pass
                except Exception:
                    pass
    except Exception:
        pass
    return "v0.0.0"


def save_version(version):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        f.write(version)


def load_license_key():
    try:
        sys.path.insert(0, APP_DIR)
        import license_client
        key = license_client.load_license_key()
        _log.info(f"License key loaded: {'yes' if key else 'no'}")
        return key
    except Exception as e:
        _log.error(f"Failed to load license key: {e}", exc_info=True)
    return None


def get_fingerprint():
    try:
        import license_client
        fp = license_client.generate_fingerprint()
        _log.info(f"Fingerprint generated: {fp[:8] if fp else 'none'}...")
        return fp
    except Exception as e:
        _log.error(f"Failed to generate fingerprint: {e}", exc_info=True)
    return None


def check_for_update(license_key, fingerprint, current_version):
    try:
        import license_client
        _log.info(f"Checking for update (current: {current_version})")
        result = license_client.check_for_update(license_key, fingerprint, current_version)
        _log.info(f"Update check result: {result}")
        return result
    except Exception as e:
        _log.error(f"Update check failed: {e}", exc_info=True)
        return {"updateAvailable": False}


def download_update(license_key, fingerprint, dest_path):
    try:
        import license_client
        _log.info(f"Downloading update to {dest_path}")
        result = license_client.download_update(license_key, fingerprint, dest_path)
        _log.info(f"Download result: {result}")
        return result
    except Exception as e:
        _log.error(f"Download failed: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


UPDATE_SERVER_URL = "https://imperio-studio.replit.app"


def _compare_versions(latest, current):
    import re
    def parse_v(v):
        nums = re.findall(r'\d+', v or "")
        return tuple(int(n) for n in nums) if nums else (0,)
    return parse_v(latest) > parse_v(current)


def check_for_update_public(current_version):
    import urllib.request, ssl
    try:
        _log.info(f"Public update check (current: {current_version})")
        ctx = ssl.create_default_context()
        try:
            req = urllib.request.Request(f"{UPDATE_SERVER_URL}/api/update/latest")
            resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        except (ssl.SSLError, ssl.SSLCertVerificationError):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(f"{UPDATE_SERVER_URL}/api/update/latest")
            resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(resp.read().decode("utf-8"))
        latest = data.get("latestVersion", "")
        has_update = _compare_versions(latest, current_version)
        data["updateAvailable"] = has_update
        data["currentVersion"] = current_version
        _log.info(f"Public update check result: latest={latest}, update={has_update}")
        return data
    except Exception as e:
        _log.error(f"Public update check failed: {e}", exc_info=True)
        return {"updateAvailable": False}




def safe_extract_zip(zf, dest):
    for member in zf.namelist():
        member_path = os.path.normpath(os.path.join(dest, member))
        if not member_path.startswith(os.path.normpath(dest) + os.sep) and member_path != os.path.normpath(dest):
            raise Exception(f"Unsafe path in archive: {member}")
    zf.extractall(dest)


def _migrate_shortcut(desktop):
    import platform
    system = platform.system()
    try:
        if system == "Windows":
            old_lnk = os.path.join(desktop, "Batchy.lnk")
            new_lnk = os.path.join(desktop, "Imperio Studio.lnk")
            if os.path.exists(old_lnk) and not os.path.exists(new_lnk):
                os.rename(old_lnk, new_lnk)
            old_bat = os.path.join(desktop, "Batchy.bat")
            new_bat = os.path.join(desktop, "Imperio Studio.bat")
            if os.path.exists(old_bat) and not os.path.exists(new_bat):
                os.rename(old_bat, new_bat)
        elif system == "Darwin":
            old_app = os.path.join(desktop, "Batchy.app")
            new_app = os.path.join(desktop, "Imperio Studio.app")
            if os.path.isdir(old_app) and not os.path.exists(new_app):
                os.rename(old_app, new_app)
    except Exception:
        pass


def apply_update(zip_path, app_dir):
    _log.info(f"apply_update: START zip={zip_path} app_dir={app_dir}")
    backup_dir = app_dir + "_backup"
    try:
        _log.info(f"apply_update: step 1 — clearing old backup")
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        _log.info(f"apply_update: step 2 — creating backup")
        if os.path.exists(app_dir):
            shutil.copytree(app_dir, backup_dir)
        _log.info(f"apply_update: step 3 — removing old app files")
        for item in os.listdir(app_dir):
            item_path = os.path.join(app_dir, item)
            if item in ("output", "projects", "data"):
                continue
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        _log.info(f"apply_update: step 4 — extracting zip")
        with zipfile.ZipFile(zip_path, "r") as zf:
            safe_extract_zip(zf, app_dir)
        _log.info(f"apply_update: step 4 complete — zip extracted")

        _log.info(f"apply_update: step 5 — checking launcher update")
        launcher_new = os.path.join(app_dir, "batchy_launcher.py")
        launcher_current = os.path.join(BATCHY_DIR, "batchy_launcher.py")
        if os.path.exists(launcher_new):
            try:
                with open(launcher_new, "r") as f:
                    new_content = f.read()
                with open(launcher_current, "r") as f:
                    current_content = f.read()
                if new_content != current_content:
                    pending = launcher_current + ".pending"
                    shutil.copy2(launcher_new, pending)
                    _log.info(f"apply_update: launcher pending update created")
            except Exception as e:
                _log.warning(f"apply_update: launcher pending failed: {e}")

        _log.info(f"apply_update: step 6 — workspace/desktop migration")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        old_workspace = os.path.join(desktop, "Batchy")
        workspace = os.path.join(desktop, "Imperio Studio")
        if os.path.isdir(old_workspace) and not os.path.exists(workspace):
            try:
                os.rename(old_workspace, workspace)
            except Exception:
                try:
                    shutil.copytree(old_workspace, workspace)
                    shutil.rmtree(old_workspace)
                except Exception:
                    pass
        elif os.path.isdir(old_workspace) and os.path.isdir(workspace):
            try:
                for item in os.listdir(old_workspace):
                    src_item = os.path.join(old_workspace, item)
                    dst_item = os.path.join(workspace, item)
                    if not os.path.exists(dst_item):
                        if os.path.isdir(src_item):
                            shutil.copytree(src_item, dst_item)
                        else:
                            shutil.copy2(src_item, dst_item)
                shutil.rmtree(old_workspace)
            except Exception:
                pass
        try:
            _migrate_shortcut(desktop)
            os.makedirs(workspace, exist_ok=True)
            chrome_src = os.path.join(app_dir, "chrome_extension")
            chrome_dst = os.path.join(workspace, "chrome_extension")
            if os.path.isdir(chrome_src):
                if os.path.exists(chrome_dst):
                    shutil.rmtree(chrome_dst)
                shutil.copytree(chrome_src, chrome_dst)
        except Exception as e:
            _log.warning(f"Non-critical post-update step failed (desktop/chrome): {e}")

        try:
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
        except Exception:
            pass

        clear_pycache(app_dir)

        _log.info(f"apply_update: SUCCESS — update applied")
        return True

    except Exception as e:
        _log.error(f"apply_update failed: {e}", exc_info=True)
        try:
            if os.path.exists(backup_dir):
                if os.path.exists(app_dir):
                    shutil.rmtree(app_dir)
                shutil.move(backup_dir, app_dir)
        except Exception as restore_err:
            _log.error(f"Backup restore also failed: {restore_err}")
        return False


def apply_pending_launcher_update():
    pending = os.path.join(BATCHY_DIR, "batchy_launcher.py.pending")
    if os.path.exists(pending):
        try:
            target = os.path.join(BATCHY_DIR, "batchy_launcher.py")
            shutil.copy2(pending, target)
            os.remove(pending)
        except Exception:
            pass


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def kill_existing_streamlit(port):
    import platform as plat
    try:
        if plat.system() == "Darwin":
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split("\n")
                for pid in pids:
                    pid = pid.strip()
                    if pid:
                        try:
                            os.kill(int(pid), 9)
                            _log.info(f"Killed existing process on port {port}: PID {pid}")
                        except (ProcessLookupError, ValueError):
                            pass
                time.sleep(1)
        elif plat.system() == "Windows":
            result = subprocess.run(
                ["netstat", "-ano"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.strip().split()
                    if parts:
                        pid = parts[-1]
                        try:
                            subprocess.run(["taskkill", "/F", "/PID", pid],
                                           capture_output=True, timeout=5)
                            _log.info(f"Killed existing process on port {port}: PID {pid}")
                        except Exception:
                            pass
                time.sleep(1)
    except Exception as e:
        _log.error(f"Failed to kill existing processes on port {port}: {e}")


def clear_pycache(directory):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if d == "__pycache__":
                cache_path = os.path.join(root, d)
                try:
                    shutil.rmtree(cache_path)
                    _log.info(f"Cleared __pycache__: {cache_path}")
                except Exception:
                    pass


def wait_for_streamlit(port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.5)
    return False


def find_chrome():
    import platform as plat
    if plat.system() == "Windows":
        paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]
        for p in paths:
            if os.path.exists(p):
                return p
    elif plat.system() == "Darwin":
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            return chrome_path
    return None


def open_browser(url):
    chrome = find_chrome()
    if chrome:
        try:
            subprocess.Popen([chrome, url], start_new_session=True)
            return
        except Exception:
            pass
    webbrowser.open(url)


class BatchyLauncher:
    def __init__(self):
        apply_pending_launcher_update()

        self.root = tk.Tk()
        self.root.title("Imperio Studio")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        ttk.Label(self.main_frame, text="Imperio Studio", font=("", 20, "bold")).pack(pady=(10, 5))
        self.status_label = ttk.Label(self.main_frame, text="Iniciando...", font=("", 11))
        self.status_label.pack(pady=5)
        self.progress_bar = ttk.Progressbar(self.main_frame, mode="indeterminate", length=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(15)

        self.streamlit_proc = None
        threading.Thread(target=self._startup, daemon=True).start()

    def _set_status(self, text):
        self.root.after(0, lambda: self.status_label.config(text=text))

    def _startup(self):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        old_workspace = os.path.join(desktop, "Batchy")
        new_workspace = os.path.join(desktop, "Imperio Studio")
        if os.path.isdir(old_workspace) and not os.path.exists(new_workspace):
            try:
                os.rename(old_workspace, new_workspace)
            except Exception:
                try:
                    shutil.copytree(old_workspace, new_workspace)
                    shutil.rmtree(old_workspace)
                except Exception:
                    pass
        elif os.path.isdir(old_workspace) and os.path.isdir(new_workspace):
            try:
                for item in os.listdir(old_workspace):
                    src_item = os.path.join(old_workspace, item)
                    dst_item = os.path.join(new_workspace, item)
                    if not os.path.exists(dst_item):
                        if os.path.isdir(src_item):
                            shutil.copytree(src_item, dst_item)
                        else:
                            shutil.copy2(src_item, dst_item)
                shutil.rmtree(old_workspace)
            except Exception:
                pass
        _migrate_shortcut(desktop)

        license_key = load_license_key()
        fingerprint = get_fingerprint()
        current_version = get_current_version()

        _log.info(f"Startup: version={current_version}, license={'yes' if license_key else 'NO'}, fingerprint={'yes' if fingerprint else 'NO'}")

        self._set_status("Verificando actualizaciones...")
        can_download = bool(license_key and fingerprint)
        try:
            if can_download:
                upd = check_for_update(license_key, fingerprint, current_version)
            else:
                _log.info("License key not available, using public version check only")
                upd = check_for_update_public(current_version)
            if upd.get("updateAvailable"):
                latest = upd.get("latestVersion", "")
                if not can_download:
                    _log.warning(f"Update {latest} available but cannot download without license key")
                    self._set_status(f"Actualización {latest} disponible — usa Reparar Instalación")
                    time.sleep(4)
                else:
                    expected_hash = upd.get("zipHash", "")
                    _log.info(f"Update available: {latest} (hash: {expected_hash[:16] if expected_hash else 'none'})")
                    self._set_status(f"Actualizando a {latest}...")
                    with tempfile.TemporaryDirectory() as tmp:
                        zip_path = os.path.join(tmp, "update.zip")
                        result = download_update(license_key, fingerprint, zip_path)
                        if result.get("success"):
                            hash_ok = True
                            if expected_hash:
                                with open(zip_path, "rb") as fh:
                                    actual_hash = hashlib.sha256(fh.read()).hexdigest()
                                hash_ok = (actual_hash == expected_hash)
                                if not hash_ok:
                                    _log.error(f"Hash mismatch: expected={expected_hash}, actual={actual_hash}")
                            if hash_ok and apply_update(zip_path, APP_DIR):
                                save_version(latest)
                                _log.info(f"Update applied successfully: {latest}")
                                self._set_status(f"Actualizado a {latest}")

                                req_file = os.path.join(APP_DIR, "requirements_app.txt")
                                if not os.path.exists(req_file):
                                    req_file = os.path.join(APP_DIR, "requirements.txt")
                                if os.path.exists(req_file):
                                    self._set_status("Actualizando dependencias...")
                                    python_exe = get_python_exe()
                                    env = os.environ.copy()
                                    env["PATH"] = os.path.dirname(python_exe) + os.pathsep + env.get("PATH", "")
                                    env["PATH"] = FFMPEG_DIR + os.pathsep + env["PATH"]
                                    for pip_attempt in range(2):
                                        pip_result = subprocess.run(
                                            [python_exe, "-m", "pip", "install", "-r", req_file,
                                             "--no-warn-script-location", "-q"],
                                            capture_output=True, text=True, timeout=300, env=env
                                        )
                                        if pip_result.returncode == 0:
                                            _log.info("Dependencies installed successfully")
                                            break
                                        else:
                                            _log.error(f"pip install attempt {pip_attempt + 1} failed: {pip_result.stderr}")
                                            if pip_attempt == 0:
                                                time.sleep(2)
                            elif not hash_ok:
                                _log.error("Update skipped due to hash mismatch")
                                self._set_status("Error de verificación — intento fallido")
                                time.sleep(3)
                            else:
                                _log.error("apply_update returned False")
                                self._set_status("Error al instalar actualización")
                                time.sleep(3)
                        else:
                            _log.error(f"Download failed: {result.get('error', 'unknown')}")
                            self._set_status(f"Error descargando actualización")
            else:
                _log.info("No update available")
        except Exception as e:
            _log.error(f"Update process failed: {e}", exc_info=True)

        ffprobe_path = os.path.join(FFMPEG_DIR, "ffprobe")
        if not os.path.isfile(ffprobe_path) and not os.path.isfile(ffprobe_path + ".exe"):
            if __import__('platform').system() == 'Darwin':
                try:
                    _log.info("ffprobe not found, downloading...")
                    self._set_status("Descargando ffprobe...")
                    import urllib.request
                    ffprobe_url = "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip"
                    os.makedirs(FFMPEG_DIR, exist_ok=True)
                    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
                        urllib.request.urlretrieve(ffprobe_url, tmp.name)
                        with zipfile.ZipFile(tmp.name, "r") as zf:
                            zf.extractall(FFMPEG_DIR)
                    os.chmod(ffprobe_path, 0o755)
                    _log.info("ffprobe downloaded successfully")
                except Exception as e:
                    _log.error(f"Failed to download ffprobe: {e}")

        if is_port_in_use(STREAMLIT_PORT):
            _log.info(f"Port {STREAMLIT_PORT} is in use, killing existing processes")
            self._set_status("Cerrando instancia anterior...")
            kill_existing_streamlit(STREAMLIT_PORT)
            time.sleep(2)

        self._set_status("Iniciando Imperio Studio...")
        self._launch_streamlit()

    def _launch_streamlit(self):
        python_exe = get_python_exe()
        app_entry = os.path.join(APP_DIR, "app.py")
        if not os.path.exists(python_exe):
            self._set_status("Error: Python no encontrado")
            return
        if not os.path.exists(app_entry):
            self._set_status("Error: app.py no encontrado")
            return

        env = os.environ.copy()
        env["PATH"] = os.path.dirname(python_exe) + os.pathsep + env.get("PATH", "")
        env["PATH"] = FFMPEG_DIR + os.pathsep + env["PATH"]

        streamlit_config = os.path.join(APP_DIR, ".streamlit", "config.toml")
        os.makedirs(os.path.dirname(streamlit_config), exist_ok=True)
        if not os.path.exists(streamlit_config):
            with open(streamlit_config, "w") as f:
                f.write(f"[server]\nheadless = true\nport = {STREAMLIT_PORT}\naddress = \"127.0.0.1\"\nenableXsrfProtection = false\nenableCORS = false\n\n[client]\ntoolbarMode = \"minimal\"\n\n[theme]\nbase = \"dark\"\n")

        self.streamlit_proc = subprocess.Popen(
            [python_exe, "-m", "streamlit", "run", app_entry,
             "--server.port", str(STREAMLIT_PORT),
             "--server.headless", "true",
             "--server.address", "127.0.0.1",
             "--server.enableXsrfProtection", "false",
             "--server.enableCORS", "false"],
            cwd=APP_DIR,
            env=env,
            start_new_session=True,
        )

        self._set_status("Esperando que Imperio Studio inicie...")

        if wait_for_streamlit(STREAMLIT_PORT, timeout=45):
            url = f"http://127.0.0.1:{STREAMLIT_PORT}"
            self._set_status("Abriendo navegador...")
            time.sleep(1)
            open_browser(url)
            self.root.after(500, self._minimize_or_hide)
        else:
            self._set_status("Error: Imperio Studio no pudo iniciar")

        threading.Thread(target=self._watch_process, daemon=True).start()

    def _minimize_or_hide(self):
        self.root.withdraw()

    def _watch_process(self):
        if self.streamlit_proc:
            self.streamlit_proc.wait()
        self.root.after(0, self.root.quit)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_close(self):
        if self.streamlit_proc and self.streamlit_proc.poll() is None:
            self.streamlit_proc.terminate()
            try:
                self.streamlit_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_proc.kill()
        self.root.quit()


if __name__ == "__main__":
    launcher = BatchyLauncher()
    launcher.run()
