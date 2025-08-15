# coding: utf-8
# Main dev: alextoutcourt72
# New dev: MJVhack
import os
import sys
import argparse
from platform import system
from time import sleep
from typing import List
import pkgutil
import importlib
import inspect

# imports robustes
from clarity.core import (
    Colors, ClarityToolsCollection, ClarityTool, hr, menu, 
    expand_path, ensure_dir, clear, AppConfig
)
def build_tools() -> List:
    """Charge dynamiquement tous les outils depuis le package clarity.tools."""
    tools = []
    # Chemin vers le package des outils
    import clarity.tools
    package = clarity.tools
    package_path = package.__path__
    package_name = package.__name__

    # Parcourt tous les modules dans le package des outils
    for _, module_name, _ in pkgutil.walk_packages(package_path, package_name + '.'):
        try:
            # Importe le module dynamiquement
            module = importlib.import_module(module_name)
            
            # Inspecte le module à la recherche de classes d'outils
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Vérifie si la classe est une sous-classe de ClarityTool(sCollection) 
                # et si elle vient bien de notre module (pas une classe importée)
                if (issubclass(obj, ClarityTool) or issubclass(obj, ClarityToolsCollection)) and obj.__module__ == module_name:
                    # Ignore les classes de base elles-mêmes
                    if obj not in [ClarityTool, ClarityToolsCollection]:
                        # Instancie l'outil et l'ajoute à la liste
                        tools.append(obj())
                        print(f"{Colors.GREEN}[+] Outil chargé: {obj.TITLE}{Colors.RESET}")

        except ImportError as e:
            print(f"{Colors.YELLOW}[!] Module d'outil ignoré (erreur d'import): {module_name}. {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[X] Erreur critique en chargeant {module_name}: {e}{Colors.RESET}")
            
    # Trie les outils par leur titre pour un affichage cohérent
    tools.sort(key=lambda x: x.TITLE)
    return tools

all_tools = build_tools()

class AllTools(ClarityToolsCollection):
    TITLE = "All tools"
    TOOLS = all_tools
    def show_info(self):
        clear()
        menu()

# -------- Gestion du chemin d’installation -----------------------------------
def platform_pathfile() -> str:
    plat = system()
    if plat == 'Windows':
        return expand_path(r"~\claritytoolpath.txt")
    elif plat in ('Linux', 'Darwin'):
        return expand_path("~/.claritytoolpath")
    else:
        print("Your Platform is not supported")
        sys.exit(0)

def default_home() -> str:
    return expand_path("~/.clarity-tool") if system() != 'Windows' else expand_path(r"~\Clarity-Tool")

def load_home(set_to: str | None = None, reset=False) -> str:
    env = os.environ.get("CLARITY_HOME")
    pathfile = platform_pathfile()

    if reset and os.path.exists(pathfile):
        try: os.remove(pathfile)
        except OSError: pass

    if set_to:
        home = expand_path(set_to)
        with open(pathfile, "w", encoding="utf-8") as f:
            f.write(home)
        return home

    if env:
        return expand_path(env)

    if os.path.exists(pathfile):
        try:
            with open(pathfile, "r", encoding="utf-8") as f:
                return expand_path(f.readline().strip())
        except Exception:
            pass

    home = default_home()
    with open(pathfile, "w", encoding="utf-8") as f:
        f.write(home)
    return home

# -------- CLI ----------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Clarity Tool – modern CLI/UX")
    p.add_argument("--list", action="store_true", help="Lister tous les outils disponibles")
    p.add_argument("--run", type=str, help="Nom EXACT d’un outil à ouvrir")
    p.add_argument("--action", type=str, help="Nom EXACT d’une action de l’outil (ex: Update)")
    p.add_argument("--set-path", type=str, help="Définir le répertoire d’installation")
    p.add_argument("--reset-path", action="store_true", help="Réinitialiser le répertoire d’installation")
    return p.parse_args()

def find_tool_by_title(title: str):
    for t in all_tools:
        if t.TITLE == title:
            return t
    return None

def main():
    args = parse_args()

    # ---- Gestion du chemin d'installation ----
    try:
        home = load_home(set_to=args.set_path, reset=args.reset_path)
        ensure_dir(home) # S'assure que le dossier existe, avec gestion d'erreur
        AppConfig.HOME_PATH = home # Stocke le chemin dans la config globale
        print(f"{Colors.DIM}Répertoire de travail des outils : {home}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Erreur critique avec le répertoire d'installation: {e}{Colors.RESET}")
        sys.exit(1)

    # ---- Chargement et exécution ----
    # Le reste du code fonctionne sans changer de répertoire de travail.

    # Mode liste
    if args.list:
        print(hr())
        print(f"{Colors.BOLD}Outils disponibles:{Colors.RESET}")
        for t in all_tools:
            print(f" - {t.TITLE}")
        print(hr())
        sys.exit(0)

    # Mode run non interactif
    if args.run:
        tool = find_tool_by_title(args.run)
        if not tool:
            print(f"{Colors.RED}Outil introuvable: {args.run}{Colors.RESET}")
            sys.exit(2)
        if args.action:
            # chercher une option qui matche
            for label, fn in getattr(tool, "OPTIONS", []):
                if label == args.action:
                    ret = fn()
                    sys.exit(0 if ret in (None, 0) else ret)
            print(f"{Colors.RED}Action introuvable sur {tool.TITLE}: {args.action}{Colors.RESET}")
            sys.exit(3)
        else:
            # ouvre le menu de l’outil
            tool.show_options(parent=AllTools())
            sys.exit(0)

    # Mode interactif
    AllTools().show_options()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.GRAY}Fermeture demandée. À bientôt!{Colors.RESET}")
        sleep(0.5)
