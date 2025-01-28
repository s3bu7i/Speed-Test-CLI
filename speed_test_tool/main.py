import speedtest
import time
import json
import csv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from datetime import datetime

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

    # Graphical representation
    console.print("\n[bold magenta]Graphical Representation[/bold magenta]")
    console.print(
        f"[cyan]Download Speed:[/cyan] {'█' * int(download / 10)} {download} Mbps")
    console.print(
        f"[cyan]Upload Speed:[/cyan] {'█' * int(upload / 10)} {upload} Mbps")
    console.print(f"[cyan]Ping:[/cyan] {'█' * int(ping / 10)} {ping} ms")


def save_results(download, upload, ping):
    result = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "download": download,
        "upload": upload,
        "ping": ping
    }
    try:
        with open("speedtest_results.json", "a") as f:
            f.write(json.dumps(result) + "\n")
    except IOError as e:
        console.print(f"[bold red]Error saving results: {e}[/bold red]")


def load_results():
    try:
        with open("speedtest_results.json", "r") as f:
            results = [json.loads(line) for line in f]
        return results
    except FileNotFoundError:
        return []
    except IOError as e:
        console.print(f"[bold red]Error loading results: {e}[/bold red]")
        return []


def show_history():
    results = load_results()
    if not results:
        console.print("[bold red]No historical data found.[/bold red]")
        return

    table = Table(title="[bold magenta]Historical Speed Test Results")
    table.add_column("Date", style="cyan", justify="left")
    table.add_column("Download Speed", style="green", justify="right")
    table.add_column("Upload Speed", style="green", justify="right")
    table.add_column("Ping", style="green", justify="right")

    for result in results:
        table.add_row(
            result["date"],
            f"{result['download']} Mbps",
            f"{result['upload']} Mbps",
            f"{result['ping']} ms"
        )

    console.print(table)


def export_to_csv():
    results = load_results()
    if not results:
        console.print("[bold red]No historical data to export.[/bold red]")
        return

    try:
        with open("speedtest_results.csv", "w", newline='') as csvfile:
            fieldnames = ["date", "download", "upload", "ping"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        console.print(
            "[bold green]Data exported to speedtest_results.csv successfully.[/bold green]")
    except IOError as e:
        console.print(f"[bold red]Error exporting results: {e}[/bold red]")


def select_server(st):
    servers = st.get_servers()
    console.print("[bold magenta]Available Servers:[/bold magenta]")
    for i, server in enumerate(servers):
        console.print(
            f"[cyan]{i + 1}. {server['name']} ({server['country']})[/cyan]")
    choice = console.input(
        "[bold yellow]Select a server by number (or press Enter to auto-select): [/bold yellow]")
    if choice.isdigit() and 0 < int(choice) <= len(servers):
        return servers[int(choice) - 1]
    return None


def run_multiple_tests(num_tests):
    download_speeds = []
    upload_speeds = []
    pings = []

    for i in range(num_tests):
        console.print(
            f"\n[bold magenta]Running Test {i + 1} of {num_tests}[/bold magenta]")
        download, upload, ping = speed_test()
        download_speeds.append(download)
        upload_speeds.append(upload)
        pings.append(ping)

    avg_download = sum(download_speeds) / num_tests
    avg_upload = sum(upload_speeds) / num_tests
    avg_ping = sum(pings) / num_tests

    console.print("\n[bold magenta]Average Results:[/bold magenta]")
    display_results(round(avg_download, 2), round(
        avg_upload, 2), round(avg_ping, 2))


def speed_test():
    st = speedtest.Speedtest()
    server = select_server(st)
    if server:
        st.get_servers([server])

    with Progress(SpinnerColumn(), TextColumn("[bold cyan]Testing download speed...")) as progress:
        download_task = progress.add_task("download", total=100)
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        progress.update(download_task, completed=100)

    with Progress(SpinnerColumn(), TextColumn("[bold cyan]Testing upload speed...")) as progress:
        upload_task = progress.add_task("upload", total=100)
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        progress.update(upload_task, completed=100)

    ping = st.results.ping
    display_results(round(download_speed, 2), round(
        upload_speed, 2), round(ping, 2))
    save_results(round(download_speed, 2), round(
        upload_speed, 2), round(ping, 2))
    return download_speed, upload_speed, ping


def main_menu():
    console.clear()
    creative_welcome()
    while True:
        console.print("\n[bold magenta]Main Menu[/bold magenta]")
        console.print("[cyan]1. Run Speed Test[/cyan]")
        console.print("[cyan]2. Run Multiple Tests[/cyan]")
        console.print("[cyan]3. View Historical Data[/cyan]")
        console.print("[cyan]4. Export Historical Data to CSV[/cyan]")
        console.print("[cyan]5. Exit[/cyan]")
        choice = console.input("[bold yellow]Select an option: [/bold yellow]")

        if choice == "1":
            animated_spinner()
            speed_test()
        elif choice == "2":
            num_tests = int(console.input(
                "[bold yellow]Enter the number of tests to run: [/bold yellow]"))
            run_multiple_tests(num_tests)
        elif choice == "3":
            show_history()
        elif choice == "4":
            export_to_csv()
        elif choice == "5":
            console.print(
                "\n[bold green]Thank you for using the Speed Test Terminal/CLI App. Stay connected!", style="bold green")
            break
        else:
            console.print(
                "[bold red]Invalid option. Please try again.[/bold red]")


if __name__ == "__main__":
    main_menu()
