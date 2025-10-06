from pathlib import Path
import re

def searc_express(myDir: str, pattern: str, extension: str = None):

    path_base = Path(myDir)
    regex = re.compile(pattern)

    for file in path_base.rglob("*"):
        if file.is_file():
            if extension and not file.suffix == extension:
                continue
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                print(f"[!] Impossible to read {file}: {e}")
                continue

                # Vérifie si le pattern apparaît dans le contenu
            if regex.search(content):
                print(f"✅ Expression found in : {file}")

dir_root = "/home/honorom/Documents/eclipse-workspace/skrypy-pyqt6/"

searc_express(dir_root, r"\bexec_()\b", extension=".py")
