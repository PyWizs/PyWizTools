from rich.progress import Progress, TextColumn, BarColumn
from rich.console import Console
from rich.text import Text
import itertools
import marshal
import socket
import whois
import os

console = Console()

def Banner():
    console.print("""[red3]
██▓███  ▓██   ██▓  █     █░  ██▓ ▒███████▒  ▄▄▄█████▓  ▒█████    ▒█████   ██▓       ██████ 
▓██░  ██ ▒▒██  ██▒ ▓█░ █ ░█░ ▓██▒ ▒ ▒ ▒ ▄▀░  ▓  ██▒ ▓▒ ▒██▒  ██▒ ▒██▒  ██ ▒▓██▒     ▒██    ▒ 
▓██░ ██▓ ▒ ▒██ ██░ ▒█░ █ ░█  ▒██▒ ░ ▒ ▄▀▒░   ▒ ▓██░ ▒░ ▒██░  ██▒ ▒██░  ██ ▒▒██░     ░ ▓██▄ ▒
▒██▄█▓▒  ▒ ░ ▐██▓░ ░█░ █ ░█  ░██░   ▄▀▒   ░  ░ ▓██▓ ░  ▒██   ██░ ▒██   ██ ░▒██░       ▒   ██▒
▒██▒ ░   ░ ░ ██▒▓░ ░░██▒██▓  ░██░ ▒███████▒    ▒██▒ ░  ░ ████▓▒░ ░ ████▓▒ ░░██████ ▒▒██████▒▒
▒▓▒░ ░   ░  ██▒▒▒  ░ ▓░▒ ▒   ░▓   ░▒▒ ▓░▒░▒    ▒ ░░    ░ ▒░▒░▒░  ░ ▒░▒░▒░  ░ ▒░▓   ░▒ ▒▓▒ ▒ ░
░▒ ░      ▓██ ░▒░    ▒ ░ ░    ▒ ░ ░░▒ ▒ ░ ▒      ░       ░ ▒ ▒░    ░ ▒ ▒░  ░ ░ ▒   ░░ ░▒  ░ ░
░░        ▒ ▒ ░░     ░   ░    ▒ ░ ░ ░ ░ ░ ░    ░       ░ ░ ░ ▒   ░ ░ ░ ▒     ░ ░    ░  ░  ░  
        ░ ░          ░      ░     ░ ░                    ░ ░       ░ ░       ░   ░      ░  
        ░ ░                     ░                                                      

[/red3]""", justify='center')


def Clear():
    if(os.name == 'posix'): os.system('clear')
    else: os.system('cls')


def ScanPort(host: str, start_port: int = 1, end_port: int = 1024, timeout: float = 1):
    open_port = []
    with Progress(TextColumn("{task.fields[TEST]}", justify="right"), BarColumn()) as progress:
        
        task = progress.add_task("", total=None, TEST="[bold red3]Starting Testing...")

        for port in range(start_port, end_port+1):
            progress.update(task, advance=1, TEST=f"[bold red3]Testing Port {port}...")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                result = sock.connect_ex((host, port))

                if result == 0:
                    open_port.append(port)
            except: pass
            finally: sock.close()
    
    return open_port


def portScannerHandler():
    host = console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter Host (or IP) Address >[/red3] ")
    startport = int(console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter Start Port >[/red3] "))
    endport = int(console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter End Port >[/red3] "))
    timeout = float(console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter Timeout >[/red3] "))

    Clear()
    Banner()

    openPort = ScanPort(host, startport, endport, timeout)
    
    Clear()
    Banner()

    if len(openPort) == 0: text = Text.from_markup("[bold red3]No open port founds![/bold red3]")
    else:
        text = Text.from_markup("[bold red3]The open ports:[/bold red3]\n", justify='center')
        for i, port in enumerate(openPort, 0):
            if i % 5 == 0: text.append("\n")

            color = 'red3' if i % 2 == 0 else 'red'
            ports = str(port).rjust(4)
            
            text.append(Text.from_markup(f"[grey23][ [{color}] {ports} [/{color}]][/grey23] "))

    console.print(text, justify='center')
    console.print("\n[bold red]Press enter to return to the menu[/bold red]", justify='center')
    input()


def marshalEncoderHandler():
    while True:
        filePath = console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter file path > [/red3]")
        if os.path.exists(filePath):
            if '.py' in filePath: break
            else: texterror = "[bold red3]Only .py format is supported.[/bold red3]"
        else: texterror = "[bold red3]File does not exist![/bold red3]"

        Clear()
        Banner()
        console.input(f"[grey23][[red1]![/red1]][/grey23] {texterror}\n\n [bold red]Press enter to continue[/bold red]")
        Clear()
        Banner()
    
    Clear()
    Banner()
    console.print("[grey23][[red1]+[/red1]][/grey23] [bold red3]Please wait encoding File...")

    file = open(filePath,'r', encoding="utf8").read()
    compiled_file = compile(file,'','exec'); encoded_code = marshal.dumps(compiled_file)

    name = filePath.replace(".py","")
    open(f"{name}_Encoded.py","w", encoding="utf8").write(f"""
# https://github.com/PyWizs/
import marshal
exec(marshal.loads({repr(encoded_code)}))
""")
    
    Clear()
    Banner()
    console.input(f"[grey23][[red1]+[/red1]][/grey23] [bold red3]Encoded file saved as {name}_Encoded.py[/bold red3]\n\n [bold red]Press enter to continue[/bold red]")


def domainInformationHandler():
    domain = console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter domain address >[/red3] ")
    try: 
        w = whois.whois(domain)
        Clear()
        Banner()
        console.print(f"""
[red3]!!![/red3] [red]Domain Information[/red] [red3]!!![/red3]

[grey23]*[/grey23] [bold red3]Domain Name:[/bold red3] [red1]{w.domain_name}[/red1]
[grey23]*[/grey23] [bold red3]Registrar:[/bold red3] [red1]{w.registrar}[/red1]
[grey23]*[/grey23] [bold red3]Whois Server:[/bold red3] [red1]{w.whois_server}[/red1]
[grey23]*[/grey23] [bold red3]Creation Date:[/bold red3] [red1]{w.creation_date}[/red1]
[grey23]*[/grey23] [bold red3]Expiration Date:[/bold red3] [red1]{w.expiration_date}[/red1]
[grey23]*[/grey23] [bold red3]Name Servers:[/bold red3] [red1]{w.name_servers}[/red1]
[grey23]*[/grey23] [bold red3]Status:[/bold red3] [red1]{w.status}[/red1]
[grey23]*[/grey23] [bold red3]Emails:[/bold red3] [red1]{w.emails}[/red1]
[grey23]*[/grey23] [bold red3]DNSSEC:[/bold red3] [red1]{w.dnssec}[/red1]

[bold red]Press enter to return to the menu[/bold red]
""")
    except: console.print("[bold red3]Error! Please Try Again[/bold red3]")
    input()


def size(charCount, length):
    np = charCount ** length
    
    sizeByte = np * (length + len(os.linesep))
    if sizeByte < 1024: return str(sizeByte) + "Byte"

    sizeKb = round(sizeByte / 1024)
    if sizeKb < 1024: return str(sizeKb) + "Kb"
    
    sizeMb = round(sizeKb / 1024)
    if sizeMb < 1024: return str(sizeMb) + "Mb"

    sizeGb = round(sizeMb / 1024)
    if sizeGb < 1024: return str(sizeGb) + "Gb"

    sizeTb = round(sizeGb / 1024)
    if sizeTb < 1024: return str(sizeTb) + "Tb"

    sizePb = round(sizeTb / 1024)
    if sizePb < 1024: return str(sizePb) + "Pb"

    sizeEb = round(sizePb / 1024)
    if sizeEb < 1024: return str(sizeEb) + "Eb"

    return str(round(sizeEb / 1024)) + "Zb"


def createPassword(chars, length, filename):
    mode = "a" if os.path.exists(filename) else "w"

    with open(filename, mode) as f:
        for password in itertools.product(chars, repeat=length): f.write(''.join(password) + '\n')


def passwordListHandler():
    Run = False
    psl = {"length": 3, "chars": "abcdefghijklmnopqrstuvwxyz", "file": "password.txt"}
    psl["length"] = int(console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter password list length >[/red3] "))
    while True:
        Clear()
        Banner()
        console.print(f"""
[red3]Create this password list?[/red3]
[red1]!!!!![/red1] [red3]File size:[/red3] [red]{size(len(psl['chars']), psl['length'])}[/red] [red1]!!!!![/red1]

[grey23]*[/grey23] [red3]Length:[/red3] [red1]{psl['length']}[/red1] [grey23]*[/grey23]
[grey23]*[/grey23] [red3]Chars:[/red3] [red1]{psl['chars']}[/red1] [grey23]*[/grey23]
[grey23]*[/grey23] [red3]Savefile:[/red3] [red1]{psl['file']}[/red1] [grey23]*[/grey23]

[grey23]*[/grey23] [red3]Type 'create' to create the PasswordList[/red3] [grey23]*[/grey23]
[grey23]*[/grey23] [red3]Type 'length' to edit the Length[/red3] [grey23]*[/grey23]
[grey23]*[/grey23] [red3]Type 'char' to edit the Chars[/red3] [grey23]*[/grey23]
[grey23]*[/grey23] [red3]Type 'file' to edit the Saving file[/red3] [grey23]*[/grey23]
[grey23]*[/grey23] [red3]Type 'cancel' to Cancel[/red3] [grey23]*[/grey23]
""", justify='center')

        pslinp = console.input("[red3]> [/red3]").lower()

        Clear()
        Banner()

        if pslinp == 'create': break
        elif pslinp == 'length': psl["length"] = int(console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter password list length >[/red3] "))
        elif pslinp == 'char': psl["chars"] = console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter passwordlist chars >[/red3] ")
        elif pslinp == 'file': psl["file"] = console.input("[grey23][[red1]+[/red1]][/grey23] [red3]Enter password list file name to save >[/red3] ")
        elif pslinp == 'cancel': Run = True; break
    
    if not Run:
        Clear()
        Banner()
        console.print("[red3]Please wait creating password...[/red3]")
        createPassword(psl["chars"], psl["length"], psl["file"])
        Clear()
        Banner()
        console.input(f"[red3]Password list created. File saved at '{psl['file']}'.[/red3]\n\n[bold red]Press enter to return to the menu[/bold red]")

def helpHandler():
    console.print("""
[red1]-=-=-=-[red3]HELP[/red3]-=-=-=-[/red1]

[red1]Port Scanner[/red1] [grey23]:[/grey23] [red3]Scan open ports on a host or IP address.[/red3]
[red1]Marshal Encoder[/red1] [grey23]:[/grey23] [red3]Encode a Python (.py) file using marshal.[/red3]
[red1]Domain Information[/red1] [grey23]:[/grey23] [red3]Retrieve domain info (registrar, DNS, emails, etc.).[/red3]
[red1]Password List Generator[/red1] [grey23]:[/grey23] [red3]Generate password lists with custom length, chars, and file.[/red3]
[red1]Help[/red1] [grey23]:[/grey23] [red3]Show this help message.[/red3]
[red1]Disclaimer[/red1] [grey23]:[/grey23] [red3]Show legal disclaimer and usage warnings.[/red3]
[red1]Exit[/red1] [grey23]:[/grey23] [red3]Exit the program.[/red3]
""", justify='center')
    
    console.input("\n\n[bold red]Press enter to return to the menu[/bold red]")
    

def main():
    while True:
        Clear()
        Banner()
        console.print("[grey23][[red]1[/red]][/grey23] [red1]Port Scanner[/red1]")
        console.print("[grey23][[red1]2[/red1]][/grey23] [red]Marshal Encoder[/red]")
        console.print("[grey23][[red]3[/red]][/grey23] [red1]Domain Information[/red1]")
        console.print("[grey23][[red1]4[/red1]][/grey23] [red]Password List Generator[/red]")
        console.print("[grey23][[red]5[/red]][/grey23] [red1]Help[/red1]")
        console.print("[grey23][[red1]6[/red1]][/grey23] [red]Disclaimer[/red]")
        console.print("[grey23][[red]0[/red]][/grey23] [red1]Exit[/red1]")

        x = console.input("[red3]> [/red3]")

        Clear()
        Banner()
        if x == '1': portScannerHandler()
        elif x == '2': marshalEncoderHandler()
        elif x == '3': domainInformationHandler()
        elif x == '4': passwordListHandler()
        elif x == '5': helpHandler()
        elif x == '6':
            console.print("""
[red]!!!![/red][dark_red]-DISCLAIMER-[/dark_red][red]!!!![/red]
[red3]
This software is for EDUCATIONAL and RESEARCH purposes ONLY.

Any illegal use or actions that may harm others
are STRICTLY PROHIBITED.

The developer is NOT responsible for
any misuse, damage, or legal consequences.

By using this software, YOU AGREE to these terms.[/red3]
""",justify='center')
            input()
        elif x == '0':
            console.print("[bold red3]GoodBye![bold red3]", justify='center')
            os._exit(0)
if __name__ == "__main__":
    main()