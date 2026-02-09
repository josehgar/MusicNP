import os, yt_dlp, csv, random, msvcrt
import time
from turtle import st
from click import clear
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box
from pynput import keyboard

# Global variables
download_path: str = ""
csv_path: str = ""
cookiefile_path: str = ""

# To format text
console = Console()

class MyLogger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        console.print("[bold red]There was an error[/bold red]")

# It cleans the console screen depending on the OS
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def main_menu():
    clear_screen()
    text = "Introduce an option ( 1 | 2 | 3 | 4 | 5 ): " 
    show_header()
    show_configurations()
    show_options()
    try:
        opt = int(input(text).strip())
        if not (opt > 0 and opt < 6):
            os.system('cls')
            main_menu()
        else:
            match opt:
                case 1:
                    start_download()
                case 2:
                    help_info()
                case 3:
                    settings()
                case 4:
                    credits_info()
                case 5:
                    exit_from_app()             
    except ValueError:
        os.system('cls')
        main_menu()

# Shows header. DON'T MODIFY ASCII ART. It is perfectly aligned   
def show_header():
    ascii_art = r"""                                         __  __           _      _     _____  
                                        |  \/  |         (_)    | \ | |  __ \ 
                                        | \  / |_   _ ___ _  ___|  \| | |__) |
                                        | |\/| | | | / __| |/ __|     |  ___/ 
                                        | |  | | |_| \__ \ | (__| |\  | |     
                                        |_|  |_|\__,_|___/_|\___|_| \_|_|     """
    console.print(
        Panel(
            (Text(ascii_art, style="bold cyan")),
            title="[bold white]Transform your music[/bold white]",
            border_style="cyan",
            padding=(1,0),
            box=box.DOUBLE_EDGE
        )
    )
    print()
    
def show_configurations():
    info = Text()
    info.append(f"Download path: ", style="bold yellow")
    info.append(f"{download_path or None}\n", style="bold green")
    info.append(f"CSV path: ", style="bold yellow")
    info.append(f"{csv_path or None}\n", style="bold green")
    info.append(f"Cookie path: ", style="bold yellow")
    info.append(f"{cookiefile_path or "None"}", style="bold green")
    console.print(
        Panel(
            info,
            title= "[bold yellow]Settings[/bold yellow]",
            border_style="bold yellow",
            box=box.ROUNDED
        )
    )
    print()
    
def show_options():
    options = Text()
    options.append(f"1. Start Downloading\n", style="bold hot_pink")
    options.append(f"2. Help\n", style="bold hot_pink")
    options.append(f"3. Settings\n", style="bold hot_pink")
    options.append(f"4. Credits\n", style="bold hot_pink")
    options.append(f"5. Exit", style="bold hot_pink")
    console.print(
        Panel(
            options,
            title="[bold purple]Options[/bold purple]",
            border_style="bold purple",
            box=box.ROUNDED
        )
    )
    print()

def start_download():
    global download_path, csv_path, cookiefile_path
    if download_path == "" or csv_path == "" or cookiefile_path == "":
        console.print("Failed to proceed. Check if some of the configuration fields are empty.", style="bold red")
        time.sleep(1)
        main_menu()
    else:
        clear_screen()
        with open(csv_path, mode = 'r', encoding = 'utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for index, song in enumerate(reader, start=1):
                query = f"{song['Track Name']} - {song['Artist Name(s)']}"
                search_query = f"ytsearch1:{query}"
                console.print(f"{index} [bold green]DOWNLOADING:[/bold green] {query}")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'cookiefile': cookiefile_path,
                    'quiet': False,
                    'outtmpl': f'{download_path}/{index} . %(title)s.%(ext)s',
                    'logger': MyLogger(),
                    'noplaylist': True,
                    'postprocessors': [
                        {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        },
                        {'key': 'FFmpegMetadata'},
                        {'key': 'EmbedThumbnail'},
                    ],
                    'postprocessor_args': [
                        '-metadata', f'title={song["Track Name"]}',
                        '-metadata', f'artist={song["Artist Name(s)"].replace(";", ",")}',
                        '-metadata', f'album={song.get("Album Name", "Single")}',
                    ]
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([search_query])
                    espera = round(random.uniform(3,8), 2)
                    console.print(f"Waiting {espera} seconds...", style="bold yellow")
                    time.sleep(espera)
                    index += 1
                except Exception as e:
                    console.print(f"[bold red]There was an error installing the current track. Skipping[/bold red]")

def help_info():
    clear_screen()
    helping = Text()
    helping.append("1. What is MusicNP?\n", style="bold blue")
    helping.append("""MusicNP is a tool that allows you to download songs from Spotify given a .csv file. MusicNP features a waiting technique between song downloads that avoids YouTube from spotting this program as a bot. MusicNP has an incredible downloading accuracy, with the 96% of songs downloaded correctly.\n""")
    helping.append("\n")
    helping.append("2. Where can I get the .csv file?\n", style="bold blue")
    helping.append("You can obtain your .csv file from Exportify (link is in the credits section).\n")
    helping.append("\n")
    helping.append("3. What is a cookiefile.txt?\n", style="bold blue")
    helping.append("The cookiefile.txt is used so that YouTube recognizes us as a registered user instead of an anonymous one. Without a cookiefile, YouTube will detect that this is a bot and will throw more errors than expected. You can get your cookiefile.txt by installing 'get cookies.txt LOCALLY' in the extension shop in Google. Then, get into YouTube, open the extension and click export. This is safe, the program won't gather any personal data\n")
    helping.append("\n")
    helping.append("4. Do I need to have installed any library before installing?\n", style="bold blue")
    helping.append("Yes. The needed libraries are located in the requirements.txt in this directory. You can install them manually, or you can execute 'pip install -r requirements.txt' to install them. However, you must install FFmpeg and add it to your system path manually from its page (link in credits) in order to make the program work")
    console.print(Panel(
        helping,
        title = "Help",
        border_style="bold green",
        box=box.ROUNDED
    ))
    print("Press any key to return to main menu")
    def on_press(key):
        return False
    
    with keyboard.Listener(on_press=on_press, surpress=True) as listener:
        listener.join()
    flush_input()
    main_menu()
    
def settings():
    clear_screen()
    global download_path, csv_path, cookiefile_path
    setting = Text()
    setting.append("1. Set .csv path: \n", style="bold yellow")
    setting.append("2. Set download path: \n", style="bold yellow")
    setting.append("3. Set cookiefile path: \n", style="bold yellow")
    console.print(Panel(
        setting,
        title = "Settings",
        border_style="bold yellow"
    ))
    option: str = input("Enter an option ('m' to return to main menu): ")
    match option:
        case "1":
            text1 = "Enter your .csv file ('r' to cancel operation): "
            correct = False
            while not correct:
                csv_input = input(text1)
                if os.path.splitext(csv_input)[1] == '.csv':
                    csv_path = csv_input
                    correct = True
                    console.print("CSV file registered", style="green")
                    time.sleep(0.5)
                    settings()
                elif csv_input == 'r':
                    correct = True
                    settings()
                else:
                    text1 = "Not a valid path. Try again ('r' to cancel operation)"  
        case "2":
            text2 = "Enter your download file ('r' to cancel operation): "
            correct = False
            while not correct:
                download_p = input(text2)
                if os.path.isdir(download_p):
                    download_path = download_p
                    correct = True
                    console.print("Download directory set", style="green")
                    time.sleep(0.5)
                    settings()
                elif download_p == 'r':
                    correct = True
                    settings()
                else:
                    text1 = "Not a valid path. Try again ('r' to cancel operation)"
        case "3":
            text3 = "Enter your cookiefile ('r' to cancel operation): "
            correct = False
            while not correct:
                cookie = input(text3)
                if os.path.isfile(cookie) and os.path.splitext(cookie)[1] == '.txt':
                    cookiefile_path = cookie
                    correct = True
                    console.print("Cookie file registered", style="green")
                    time.sleep(0.5)
                    settings()
                elif csv_input == 'r':
                    correct = True
                else:
                    text1 = "Not a valid path. Try again ('r' to cancel operation)"
        case "m":
            clear_screen()
            main_menu()
        case _:
            settings()
            
def credits_info():
    clear_screen()
    creditos = Text()
    creditos.append("Developed by Jose Ángel\n")
    creditos.append("Exportify page: https://exportify.net", style="bold cyan")
    creditos.append("Exportify GitHub: https://github.com/watsonbox/exportify", style="bold cyan")
    creditos.append("FFmpeg: https://www.ffmpeg.org", style="bold cyan")
    creditos.append("Cookiefile: https://chromewebstore.google.com/detail/cclelndahbckbenkjhflpdbgdldlbecc?utm_source=item-share-cb ", style="bold cyan")
    console.print(
        Panel(
            creditos,
            title="Credits",
            border_style="bold cyan",
            box=box.DOUBLE_EDGE
        )
    )
    print("Press any key to return to main menu")
    def on_press(key):
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            return True
        if hasattr(key, 'char') and key.char == '\x03':
            return True
        return False
    
    with keyboard.Listener(on_press=on_press, surpress=True) as listener:
        listener.join()
    flush_input()
    main_menu()
    
def exit_from_app():
    clear_screen()
    ascii_art = r"""
          ,.  - · - .,  '           ,-·-.          ,'´¨;                   _,.,  °    
,·'´,.-,   ,. -.,   `';,'        ';   ';\      ,'´  ,':\'          ,.·'´  ,. ,  `;\ '  
 \::\.'´  ;'\::::;:'  ,·':\'       ;   ';:\   .'   ,'´::'\'       .´   ;´:::::\`'´ \'\  
  '\:';   ;:;:·'´,.·'´\::::';      '\   ';::;'´  ,'´::::;'       /   ,'::\::::::\:::\:' 
  ,.·'   ,.·:'´:::::::'\;·´         \  '·:'  ,'´:::::;' '      ;   ;:;:-·'~^ª*';\'´   
  '·,   ,.`' ·- :;:;·'´              '·,   ,'::::::;'´        ;  ,.-·:*'´¨'`*´\::\ '  
     ;  ';:\:`*·,  '`·,  °           ,'  /::::::;'  '       ;   ;\::::::::::::'\;'   
     ;  ;:;:'-·'´  ,.·':\           ,´  ';\::::;'  '         ;  ;'_\_:;:: -·^*';\   
  ,·',  ,. -~:*'´\:::::'\‘         \`*ª'´\\::/‘            ';    ,  ,. -·:*'´:\:'\° 
   \:\`'´\:::::::::'\;:·'´           '\:::::\';  '            \`*´ ¯\:::::::::::\;' '
    '\;\:::\;: -~*´‘                 `*ª'´‘                  \:::::\;::-·^*'´     
             '                          '                       `*´¯              
    """
    print(ascii_art)
    time.sleep(1)
    
def flush_input():
    while msvcrt.kbhit():
        msvcrt.getch()