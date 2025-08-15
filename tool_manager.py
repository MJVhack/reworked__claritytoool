# coding=utf-8
import os
import sys
import shutil
from time import sleep
from platform import system
from clarity.core import ClarityTool, ClarityToolsCollection, Colors, expand_path, rm_rf, ensure_dir

class UpdateTool(ClarityTool):
    TITLE = "Update Clarity-Tool"
    DESCRIPTION = "Mettre à jour Clarity-Tool depuis GitHub (git requis)"

    def __init__(self):
        super().__init__([('Update', self.update)], installable=False, runnable=False)

    def update(self):
        print(f"{Colors.CYAN}Mise à jour de Clarity-Tool…{Colors.RESET}\n")
        sleep(0.5)
        # clone dans un dossier temporaire puis swap si OK
        tmp_dir = expand_path("./_clarity_update_tmp")
        rm_rf(tmp_dir)
        code = os.system("git --version >nul 2>&1" if os.name == 'nt' else "git --version >/dev/null 2>&1")
        if code != 0:
            print(f"{Colors.RED}Git n'est pas installé ou indisponible dans le PATH.{Colors.RESET}")
            return
        code = os.system(f"git clone https://github.com/alextoutcourt72/clarity-tool.git \"{tmp_dir}\"")
        if code != 0:
            print(f"{Colors.RED}Échec du clone. Vérifie ta connexion ou l'URL.{Colors.RESET}")
            return
        # Move over or instruct user; ici on propose juste
        print(f"{Colors.GREEN}Mise à jour téléchargée dans {tmp_dir}.{Colors.RESET}")
        print(f"{Colors.GRAY}Copie les fichiers voulus depuis ce dossier vers ton installation si nécessaire.{Colors.RESET}")
        return 0

class UninstallTool(ClarityTool):
    TITLE = "Uninstall Clarity-Tool"
    DESCRIPTION = "Désinstaller Clarity-Tool de ce système"

    def __init__(self):
        super().__init__([('Uninstall', self.uninstall)], installable=False, runnable=False)

    def uninstall(self):
        print(f"{Colors.YELLOW}Désinstallation de Clarity-Tool.{Colors.RESET}")
        path = expand_path("~/.clarity-tool") if system() != "Windows" else expand_path(r"~\Clarity-Tool")
        custom = input(f"Chemin d'installation détecté ({path}). Appuie sur Entrée pour confirmer ou saisis un autre chemin: ").strip()
        if custom:
            path = expand_path(custom)

        confirm = input(f"Supprimer définitivement '{path}' ? (y/N) ").strip().lower()
        if confirm != "y":
            print("Désinstallation annulée.")
            return

        try:
            rm_rf(path)
            print(f"{Colors.GREEN}Clarity-Tool supprimé: {path}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Échec de suppression: {e}{Colors.RESET}")
            return 1
        return 0

class ToolManager(ClarityToolsCollection):
    TITLE = "Uninstall or Update | Clarity-Tool"
    TOOLS = [UninstallTool(), UpdateTool()]

if __name__ == "__main__":
    ToolManager().show_options()
