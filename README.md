# auto-docker-build
# Automatic Docker Build Demo with Dockmate

This repository demonstrates **automatic Dockerfile generation and Docker image building** for Python projects using **Dockmate**.  

Instead of manually writing Dockerfiles, Dockmate analyzes your project dependencies and creates a production-ready Dockerfile automatically.

---

## 🚀 Features

- Automatic Dockerfile generation for Python projects
- GPU-aware base images for PyTorch/TensorFlow projects
- Handles `requirements.txt` or `setup.py` dependencies
- Example Flask app included as a demo project

---

## 🧩 How It Works

1. Place your Python project in a folder (here: `demo_app/`)
2. Run Dockmate to generate a Dockerfile:

```bash
Dockmate init demo_app --entrypoint "python app.py"
