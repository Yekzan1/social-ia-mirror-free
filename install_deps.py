import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    "streamlit",
    "requests",
    "bcrypt",
    "numpy",
    "pillow"
]

print("Checking MindLoop IO Dependencies...")
for pkg in packages:
    try:
        __import__(pkg if pkg != "bcrypt" else "bcrypt")
        print(f"✅ {pkg} is already installed.")
    except ImportError:
        print(f"📦 Installing {pkg}...")
        install(pkg)

print("\n🚀 All dependencies are ready for Big Tech deployment.")
