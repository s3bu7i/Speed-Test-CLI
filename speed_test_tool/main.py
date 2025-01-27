import speedtest
import time
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from random import choice
from math import sin, pi

# Initialize the console
console = Console()

def animated_spinner():
    console.print("\n", style="bold cyan")
    with Progress(SpinnerColumn(), TextColumn("[bold cyan]Analyzing your connection..."), transient=True) as progress:
        task = progress.add_task("spinner")
        for _ in range(20):
            time.sleep(0.1)
            progress.advance(task)

def creative_welcome():
    console.clear()
    banner = Text(
        """
      _______..______    _______  _______  _______     .___________. _______     _______.___________.     ______  __       __  
     /       ||   _  \  |   ____||   ____||       \    |           ||   ____|   /       |           |    /      ||  |     |  | 
    |   (----`|  |_)  | |  |__   |  |__   |  .--.  |   `---|  |----`|  |__     |   (----`---|  |----`   |  ,----'|  |     |  | 
     \   \    |   ___/  |   __|  |   __|  |  |  |  |       |  |     |   __|     \   \       |  |        |  |     |  |     |  | 
 .----)   |   |  |      |  |____ |  |____ |  '--'  |       |  |     |  |____.----)   |      |  |        |  `----.|  `----.|  | 
 |_______/    | _|      |_______||_______||_______/        |__|     |_______|_______/       |__|         \______||_______||__| 
                                                                                                                               
        Speed Test Terminal App                   
        """,
        style="bold magenta",
    )
    console.print(banner)
    console.print("""[cyan]
Welcome to my Speed Test Terminal/CLI App.
Wait some seconds baby ...
    """, style="bold cyan")
    time.sleep(2)

def display_results(download, upload, ping):
    table = Table(title="[bold magenta]Speed Test Results")
    table.add_column("Metric", style="cyan", justify="left")
    table.add_column("Value", style="green", justify="right")

    table.add_row("Ping", f"{ping} ms")
    table.add_row("Download Speed", f"{download} Mbps")
    table.add_row("Upload Speed", f"{upload} Mbps")

    console.print(table)

def speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()

    with Progress(SpinnerColumn(), TextColumn("[bold cyan]Testing download speed...")) as progress:
        download_task = progress.add_task("download", total=100)
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        progress.update(download_task, completed=100)

    with Progress(SpinnerColumn(), TextColumn("[bold cyan]Testing upload speed...")) as progress:
        upload_task = progress.add_task("upload", total=100)
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        progress.update(upload_task, completed=100)

    ping = st.results.ping
    display_results(round(download_speed, 2), round(upload_speed, 2), round(ping, 2))

def main():
    creative_welcome()
    animated_spinner()
    speed_test()
    console.print("\n[bold green]Thank you for using the Speed Test Terminal/CLI App. Stay connected!", style="bold green")

if __name__ == "__main__":
    main()
