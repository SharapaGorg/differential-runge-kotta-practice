import os
import signal
import subprocess
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from time import sleep, time
import sys
from InquirerPy import prompt

if os.name == 'nt':
    import msvcrt
else:
    import termios
    import tty

console = Console()

logo = """
**************************************************
**************************************************
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
********************@@@@@@@@@@*****@@@@@@@@@@@****
********************@@@@@@@@@@*****@@@@@@@@@@@****
********************@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@*****@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@@@@@@@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@@@@@@@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@@@@@@@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@@@@@@@@@@@@@@@@@****
****@@@@@@@@@@@*****@@@@@@@@@@@@@@@@@@@@@@@@@@****
**************************************************
**************************************************
"""

first_run = True

def signal_handler(signum, frame):
    console.print("\n[bold red]Process interrupted by user. Returning to main menu...[/]")
    main()

def wait_for_keypress():
    console.print("\n[bold bright_red]Press any key to continue...[/]")
    if os.name == 'nt':
        msvcrt.getch()
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def process_stats(process):
    console.print(f"\n[bold blue]Process ID:[/] {process.pid}")
    console.print(f"[bold blue]Return Code:[/] {process.returncode}")
    if os.name != 'nt':
        import resource
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        console.print(f"[bold blue]User CPU time:[/] {usage.ru_utime:.2f} seconds")
        console.print(f"[bold blue]System CPU time:[/] {usage.ru_stime:.2f} seconds")

def display_progress(duration):
    with Progress(
        TextColumn("[bold #ff5555]{task.description}"),
        BarColumn(bar_width=console.size.width - 40, style="bright_red"),
        TimeRemainingColumn(),
        console=console,
        expand=True,
    ) as progress:
        task = progress.add_task("[bold #ff5555]Loading environment...", total=100)
        for _ in range(100):
            progress.update(task, advance=1)
            sleep(duration / 100)

def run_script(script_path):
    start_time = time()
    try:
        process = subprocess.Popen([sys.executable, script_path], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate()
    except KeyboardInterrupt:
        console.print("\n[bold red]Script execution interrupted by user. Returning to main menu...[/]")
        signal_handler(None, None)

    end_time = time()
    elapsed_time = end_time - start_time
    console.print(f"\n[bold green]Script execution completed in {elapsed_time:.2f} seconds.[/]")
    process_stats(process)
    wait_for_keypress()
    main()

def main():
    global first_run
    os.system("cls" if os.name == "nt" else "clear")

    text_block = (
        f"[#ff5555]{logo}\n\n[italic bold #ff5555]made by Egor Dushin DSAI-03"
    )

    panel_content = Panel(
        text_block,
        border_style="#ff5555",
        title="[bold #ff5555]Practical task",
        title_align="center",
        padding=(1, 2),
    )

    console.print(panel_content, justify="center")
    
    if first_run:
        display_progress(3)  # Initial duration
        first_run = False
    else:
        display_progress(1)  # Subsequent duration

    scripts_folder = "scripts"

    scripts = [f for f in os.listdir(scripts_folder) if f.endswith(".py")]

    if not scripts:
        console.print("[bold red]No Python scripts found in 'scripts' folder.[/]")
        return

    choices = [{"name": script, "value": script} for script in scripts]
    
    questions = [
        {
            "type": "list",
            "name": "script",
            "message": "Select a script to run",
            "choices": choices,
        }
    ]

    answer = prompt(questions, style=custom_style)  # Apply custom style
    script_to_run = answer.get("script")

    if script_to_run:
        script_path = os.path.join(scripts_folder, script_to_run)

        signal.signal(signal.SIGINT, signal_handler)

        run_script(script_path)

if __name__ == "__main__":
    custom_style = {
        "questionmark": "#E91E63 bold",
        "answer": "#2196f3 bold",
        "input": "#673AB7 bold",
        "question": "",
        "pointer": "#ff5555 bold",  # Pointer color
        "highlighted": "#ff5555 bold",  # Highlight color
        "selected": "#ff5555 bold",
        "separator": "#cc5454",
        "instruction": "",  # Top instructions
        "validator": "",  # Validation instructions
        "marker": "",  # Checkmark
        "fuzzy_prompt": "",  # Fuzzy search prompt
        "fuzzy_info": "",  # Info in fuzzy search
        "fuzzy_border": "",  # Border in fuzzy search
        "fuzzy_match": "",  # Highlight in fuzzy search
        "fuzzy_selected": "",  # Selected item in fuzzy search
        "fuzzy_marker": "",  # Marker in fuzzy search
    }
    main()