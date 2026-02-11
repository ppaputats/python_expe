import os

def create_init_files(root="."):
    for folder, subfolders, files in os.walk(root):
        # Ignore dossiers système ou caches
        if "__pycache__" in folder:
            continue

        init_path = os.path.join(folder, "__init__.py")

        # Si le dossier contient des .py OU des sous-dossiers → c’est un package
        contains_python = any(f.endswith(".py") for f in files)

        if contains_python and not os.path.exists(init_path):
            print(f"Création de : {init_path}")
            with open(init_path, "w") as f:
                f.write("")  # fichier vide

if __name__ == "__main__":
    create_init_files(".")
    print("Tous les __init__.py nécessaires ont été créés.")
