"""Notebooks in frischen Kerneln vollständig ausführen und Ausgaben speichern."""
import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", default=["BadenWuerttemberg.ipynb"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    for name in args.notebooks:
        path = root / name
        notebook = nbformat.read(path, as_version=4)
        print(f"Ausführen: {path.name}", flush=True)
        def progress(cell, cell_index, **kwargs):
            if cell.cell_type == "code":
                print(f"  Zelle {cell_index + 1}/{len(notebook.cells)}", flush=True)
        NotebookClient(notebook, timeout=900, kernel_name="python3", on_cell_start=progress,
                       resources={"metadata": {"path": str(root)}}).execute()
        # Keine lokalen Dateipfade oder Laufzeitmetadaten in die Veröffentlichung übernehmen.
        for cell in notebook.cells:
            cell.metadata.pop("execution", None)
        nbformat.write(notebook, path)
        print(f"Fertig: {path.name}", flush=True)


if __name__ == "__main__":
    main()
