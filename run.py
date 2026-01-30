import os
import sys
import subprocess
import platform
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(ROOT, "venv")
PYTHON = sys.executable


def run(cmd, cwd=ROOT):
    print(f"▶ {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def ensure_venv():
    if not os.path.exists(VENV):
        print("🧪 Creating virtual environment...")
        run(f"{PYTHON} -m venv venv")


def install_requirements():
    pip = os.path.join(VENV, "Scripts", "pip") if platform.system() == "Windows" else os.path.join(VENV, "bin", "pip")
    run(f"{pip} install --upgrade pip")
    run(f"{pip} install -r requirements.txt")


def start_process(cmd, name):
    print(f"🚀 Starting {name}")
    return subprocess.Popen(cmd, shell=True)


def main():
    ensure_venv()
    install_requirements()

    python = os.path.join(VENV, "Scripts", "python") if platform.system() == "Windows" else os.path.join(VENV, "bin", "python")

    # Start backend
    backend = start_process(
        f"{python} -m uvicorn web.backend.api:app --host 0.0.0.0 --port 8000",
        "Backend API"
    )

    time.sleep(2)

    # Start algo
    algo = start_process(
        f"{python} main.py",
        "Trading Algo"
    )

    print("\n✅ SYSTEM RUNNING")
    print("📊 Dashboard: http://127.0.0.1:8000")
    print("🛑 To stop: CTRL + C")

    backend.wait()
    algo.wait()


if __name__ == "__main__":
    main()