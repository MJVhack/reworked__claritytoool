# coding: utf-8
import os
import sys
import shutil
import time
import json
import subprocess
from typing import List, Tuple, Callable, Optional

# --- Configuration Globale ----------------------------------------------------
class AppConfig:
    """Stocke la configuration globale de l'application."""
    HOME_PATH: Optional[str] = None

# --- Couleurs cross-platform (Colorama sur Windows) --------------------------
try:
    import colorama
    colorama.init(autoreset=True)
except ImportError:
    pass # Optionnel

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    ORANGE = "\033[38;5;208m"
    DIM = "\033[2m"
    GRAY = "\033[90m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def hr(char="─", width=60, color=Colors.GRAY):
    return f"{color}{char * width}{Colors.RESET}"

def badge(text: str, color=Colors.CYAN):
    return f"{color}[{text}]{Colors.RESET}"

def soft_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print() # Nouvelle ligne après Ctrl+C
        return ""

def load_version(default="v?.?") -> str:
    """Charge la version depuis version.txt de manière fiable."""
    try:
        # __file__ est le chemin du fichier actuel (core.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Le fichier version.txt est dans le dossier parent (rework)
        version_file = os.path.join(current_dir, "..", "..", "version.txt")
        if not os.path.exists(version_file):
             # Fallback si on est dans le dossier principal du projet
             version_file = os.path.join(current_dir, "..", "version.txt")

        with open(version_file, "r", encoding="utf-8") as f:
            return f.readline().strip()
    except (FileNotFoundError, IOError):
        return default

VERSION = load_version()

def menu():
    # header visuel moderne
    print(f"""
{Colors.CYAN}{Colors.BOLD}
   ____ _            _ _          ____ _     ___ 
  / ___| | __ _ _ __(_) |_ _   _ / ___| |   |_ _|
 | |   | |/ _` | '__| | __| | | | |   | |    | |
 | |___| | (_| | |  | | |_| |_| | |___| |___ | |
  \____|_|\__,_|_|  |_|\__|\|, |\____|_____|___|
                           |___/                  
{Colors.RESET}{badge('CLI')} {badge(VERSION, Colors.ORANGE)} {badge('Modern UI', Colors.MAGENTA)} 
{hr()} 
{Colors.DIM}Astuce: tape un numéro, 's' pour rechercher, 'q' pour quitter.{Colors.RESET}
""")

# --- Helpers système ---------------------------------------------------------
def run_cmd(cmd: str, cwd: Optional[str] = None) -> int:
    """Exécute une commande shell de manière robuste dans un répertoire donné (cwd)."""
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True, cwd=cwd)
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(f"{Colors.RED}{result.stderr.strip()}{Colors.RESET}", file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"{Colors.RED}Erreur critique en exécutant la commande: {e}{Colors.RESET}", file=sys.stderr)
        return -1

def rm_rf(path: str):
    if not os.path.exists(path):
        return
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except (IOError, OSError) as e:
        print(f"{Colors.RED}Impossible de supprimer {path}: {e}{Colors.RESET}", file=sys.stderr)


def ensure_dir(path: str):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f"{Colors.RED}Impossible de créer le dossier {path}: {e}{Colors.RESET}", file=sys.stderr)
        raise # Renvoyer l'exception peut être nécessaire pour arrêter le programme

def expand_path(p: str) -> str:
    return os.path.normpath(os.path.abspath(os.path.expanduser(p)))

# --- Base classes ------------------------------------------------------------
class ClarityTool(object):
    TITLE: str = ""
    DESCRIPTION: str = ""
    INSTALL_COMMANDS: List[str] = []
    UNINSTALL_COMMANDS: List[str] = []
    RUN_COMMANDS: List[str] = []
    OPTIONS: List[Tuple[str, Callable]] = []
    PROJECT_URL: str = ""

    def __init__(self, options=None, installable: bool = True, runnable: bool = True):
        options = options or []
        self.OPTIONS = []
        if installable:
            self.OPTIONS.append(('Install', self.install))
        if runnable:
            self.OPTIONS.append(('Run', self.run))
        if isinstance(options, list):
            self.OPTIONS.extend(options)
        else:
            # Utilisons une exception plus spécifique
            raise TypeError("options must be a list of (option_name, option_fn) tuples")

    def _print_card(self):
        clear()
        menu()
        print(f"{Colors.BOLD}{self.TITLE}{Colors.RESET}  {badge('TOOL', Colors.GREEN)}")
        if self.DESCRIPTION:
            print(f"{Colors.GRAY}{self.DESCRIPTION}{Colors.RESET}")
        if self.PROJECT_URL:
            print(f"{Colors.BLUE}↪ {self.PROJECT_URL}{Colors.RESET}")
        print(hr())

    def show_info(self):
        self._print_card()

    def _print_options(self, parent=None):
        for index, option in enumerate(self.OPTIONS):
            print(f"{Colors.CYAN}[{index + 1}]{Colors.RESET} {option[0]}")
        if self.PROJECT_URL:
            print(f"{Colors.CYAN}[98]{Colors.RESET} Ouvrir la page du projet")
        print(f"{Colors.YELLOW}[99]{Colors.RESET} Retour vers {parent.TITLE if parent else 'Quitter'}")
        print(hr())

    def show_options(self, parent=None):
        while True:
            self.show_info()
            self._print_options(parent)
            option_index = soft_input(f"{badge('Select')} ").strip().lower()

            if not option_index: # L'utilisateur a pressé Ctrl+C
                return 99

            if option_index == 'q':
                sys.exit(0)

            if option_index == 's':
                print(f"{Colors.DIM}Recherche non disponible dans ce sous-menu.{Colors.RESET}")
                time.sleep(1)
                continue

            try:
                option_index = int(option_index)
                if option_index - 1 in range(len(self.OPTIONS)):
                    # Appelle la fonction de l'option (ex: self.install)
                    ret_code = self.OPTIONS[option_index - 1][1]()
                    if ret_code != 99:
                        soft_input("\n↵ ENTER pour continuer…")
                elif option_index == 98 and self.PROJECT_URL:
                    import webbrowser
                    webbrowser.open_new_tab(self.PROJECT_URL)
                elif option_index == 99:
                    return 99
            except (TypeError, ValueError):
                print(f"{Colors.RED}Entrée invalide.{Colors.RESET}")
                time.sleep(0.8)
            except Exception as e:
                print(f"{Colors.RED}Erreur inattendue: {e}{Colors.RESET}")
                soft_input("\n↵ ENTER pour continuer…")

    def before_install(self): pass
    def install(self):
        self.before_install()
        if not AppConfig.HOME_PATH:
            print(f"{Colors.RED}Le chemin d'installation (HOME_PATH) n'est pas configuré.{Colors.RESET}")
            return 1
            
        print(f"Installation des outils dans : {AppConfig.HOME_PATH}")
        for cmd in self.INSTALL_COMMANDS:
            code = run_cmd(cmd, cwd=AppConfig.HOME_PATH)
            if code != 0:
                print(f"{Colors.RED}Échec de la commande: {cmd} (code: {code}){Colors.RESET}")
                return code
        self.after_install()
        return 0
    def after_install(self): print(f"{Colors.GREEN}Installation terminée avec succès!{Colors.RESET}")

    def before_uninstall(self) -> bool: return True
    def uninstall(self):
        if self.before_uninstall():
            for cmd in self.UNINSTALL_COMMANDS:
                run_cmd(cmd, cwd=AppConfig.HOME_PATH)
            self.after_uninstall()
    def after_uninstall(self): pass

    def before_run(self): pass
    def run(self):
        self.before_run()
        if not AppConfig.HOME_PATH:
            print(f"{Colors.RED}Le chemin d'installation (HOME_PATH) n'est pas configuré.{Colors.RESET}")
            return 1

        for cmd in self.RUN_COMMANDS:
            run_cmd(cmd, cwd=AppConfig.HOME_PATH)
        self.after_run()
        return 0
    def after_run(self): pass

class ClarityToolsCollection(ClarityTool):
    TOOLS: List[object] = []

    def show_options(self, parent=None):
        page = 0
        per_page = 10

        def filtered_tools(query: Optional[str]):
            if not query:
                return self.TOOLS
            q = query.lower().strip()
            return [t for t in self.TOOLS if q in getattr(t, "TITLE", "").lower() or q in getattr(t, "DESCRIPTION", "").lower()]

        current_filter = None
        while True:
            clear()
            menu()
            title_line = f"{Colors.BOLD}{self.TITLE}{Colors.RESET}  {badge('COLLECTION', Colors.GREEN)}"
            if current_filter:
                title_line += f"  {badge('filter:'+current_filter, Colors.ORANGE)}"
            print(title_line)
            print(hr())

            tools = filtered_tools(current_filter)
            if not tools:
                print(f"{Colors.YELLOW}Aucun outil ne correspond à votre recherche.{Colors.RESET}")
            else:
                start = page * per_page
                end = min(start + per_page, len(tools))
                for idx, tool in enumerate(tools[start:end], start=1):
                    print(f"{Colors.CYAN}[{idx}]{Colors.RESET} {tool.TITLE} {Colors.DIM}- {tool.DESCRIPTION or ''}{Colors.RESET}")
                
                total_pages = max(1, (len(tools) + per_page - 1) // per_page)
                print(hr())
                print(f"{Colors.GRAY}Page {page+1}/{total_pages} | 'n' suivant • 'p' précédent • 's' recherche • 'q' quitter{Colors.RESET}")

            print(f"{Colors.YELLOW}[99]{Colors.RESET} Retour vers {parent.TITLE if parent else 'Quitter'}")
            choice = soft_input(f"{badge('Choose')} ").strip().lower()

            if not choice: # Ctrl+C
                return 99
            if choice == 'q': sys.exit(0)
            if choice == 'n':
                if tools and (page + 1) * per_page < len(tools): page += 1
                continue
            if choice == 'p':
                if page > 0: page -= 1
                continue
            if choice == 's':
                current_filter = soft_input("Rechercher: ").strip()
                page = 0
                continue

            try:
                if choice == '99':
                    return 99
                
                choice_int = int(choice)
                start = page * per_page
                index_global = start + (choice_int - 1)
                if 0 <= index_global < len(tools):
                    tools[index_global].show_options(parent=self)
                else:
                    print(f"{Colors.RED}Choix invalide.{Colors.RESET}")
                    time.sleep(0.8)
            except (TypeError, ValueError):
                print(f"{Colors.RED}Entrée invalide.{Colors.RESET}")
                time.sleep(0.8)
            except Exception as e:
                print(f"{Colors.RED}Erreur inattendue: {e}{Colors.RESET}")
                soft_input("\n↵ ENTER pour continuer…")