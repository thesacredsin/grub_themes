#!/usr/bin/env python3
"""
GRUB Theme Installer - TUI Version
A modern terminal UI for installing GRUB themes
"""

import os
import subprocess
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, SelectionList, Log
from textual.widgets.selection_list import Selection
from textual.screen import Screen
from textual import on

THEME_DIR = '/boot/grub/themes'
THEMES = [
    'Nobara', 'Custom', 'Cyberpunk', 'Cyberpunk_2077', 
    'Shodan', 'fallout', 'CyberRe', 'CyberSynchro', 
    'CyberEXS', 'CRT', 'BIOS', 'retro'
]


class InstallScreen(Screen):
    """Screen shown during installation process"""
    
    def __init__(self, theme_name: str):
        super().__init__()
        self.theme_name = theme_name
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static(f"[bold cyan]Installing {self.theme_name} Theme[/bold cyan]", id="install-title"),
            Log(id="install-log", auto_scroll=True),
            Horizontal(
                Button("Close", variant="primary", id="close-btn"),
                id="button-container"
            ),
            id="install-container"
        )
        yield Footer()
    
    def on_mount(self) -> None:
        """Run installation when screen mounts"""
        log = self.query_one("#install-log", Log)
        self.run_installation(log)
    
    def run_installation(self, log: Log) -> None:
        """Execute the installation steps"""
        try:
            # Check root
            if os.geteuid() != 0:
                log.write_line("[bold red]ERROR: This script must be run as root![/bold red]")
                log.write_line("[yellow]Try: sudo python3 grub_theme_tui.py[/yellow]")
                return
            
            # Backup
            log.write_line("[cyan]→ Backing up GRUB config...[/cyan]")
            subprocess.run(['cp', '-an', '/etc/default/grub', '/etc/default/grub.bak'], 
                         check=True, capture_output=True)
            log.write_line("[green]✓ Backup created[/green]")
            
            # Install theme
            theme_path = f"{THEME_DIR}/{self.theme_name}"
            if not os.path.exists(theme_path):
                log.write_line(f"[cyan]→ Creating theme directory: {theme_path}[/cyan]")
                os.makedirs(theme_path, exist_ok=True)
                
                log.write_line(f"[cyan]→ Copying theme files...[/cyan]")
                subprocess.run(['cp', '-a', f'./themes/{self.theme_name}/', theme_path], 
                             check=True, capture_output=True)
                
                log.write_line("[cyan]→ Setting Plymouth watermark...[/cyan]")
                subprocess.run(['cp', '-a', './themes/watermark.png', 
                              '/usr/share/plymouth/themes/spinner/'], 
                             check=True, capture_output=True)
                log.write_line("[green]✓ Theme files installed[/green]")
            else:
                log.write_line("[yellow]! Theme already exists, skipping copy[/yellow]")
            
            # Configure GRUB
            log.write_line("[cyan]→ Configuring GRUB...[/cyan]")
            
            # Read current config
            with open('/etc/default/grub', 'r') as f:
                lines = f.readlines()
            
            # Remove old settings
            lines = [l for l in lines if not any(x in l for x in 
                    ['GRUB_TIMEOUT_STYLE=', 'GRUB_TIMEOUT=', 'GRUB_THEME=', 'GRUB_GFXMODE=', 'GRUB_TERMINAL_OUTPUT='])]
            
            # Add new settings
            lines.append('GRUB_TIMEOUT_STYLE="menu"\n')
            lines.append('GRUB_TIMEOUT="10"\n')
            lines.append(f'GRUB_THEME="{THEME_DIR}/{self.theme_name}/theme.txt"\n')
            lines.append('GRUB_GFXMODE="auto"\n')
            lines.append('GRUB_TERMINAL_OUTPUT="gfxterm"\n')
            
            # Write back
            with open('/etc/default/grub', 'w') as f:
                f.writelines(lines)
            
            log.write_line("[green]✓ GRUB configuration updated[/green]")
            
            # Update GRUB
            log.write_line("[cyan]→ Updating GRUB (this may take a moment)...[/cyan]")
            
            if os.path.exists('/usr/sbin/update-grub'):
                result = subprocess.run(['update-grub'], capture_output=True, text=True)
            elif os.path.exists('/usr/sbin/grub-mkconfig'):
                result = subprocess.run(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'], 
                                      capture_output=True, text=True)
            elif os.path.exists('/usr/sbin/grub2-mkconfig'):
                result = subprocess.run(['grub2-mkconfig', '-o', '/boot/grub2/grub.cfg'], 
                                      capture_output=True, text=True)
            else:
                log.write_line("[red]ERROR: Could not find GRUB update command[/red]")
                return
            
            if result.returncode == 0:
                log.write_line("[green]✓ GRUB updated successfully[/green]")
                log.write_line("")
                log.write_line("[bold green]🎉 Installation Complete![/bold green]")
                log.write_line(f"[cyan]Theme '{self.theme_name}' has been installed.[/cyan]")
            else:
                log.write_line(f"[red]ERROR: {result.stderr}[/red]")
                
        except subprocess.CalledProcessError as e:
            log.write_line(f"[red]ERROR: {e}[/red]")
        except Exception as e:
            log.write_line(f"[red]ERROR: {e}[/red]")
    
    @on(Button.Pressed, "#close-btn")
    def close_install(self) -> None:
        self.app.pop_screen()


class GRUBThemeApp(App):
    """Main application for GRUB theme selection"""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    #main-container {
        width: 80;
        height: auto;
        background: $surface;
        border: solid $primary;
        padding: 1 2;
    }
    
    #title {
        width: 100%;
        text-align: center;
        padding: 1;
        color: $accent;
    }
    
    #subtitle {
        width: 100%;
        text-align: center;
        padding-bottom: 1;
        color: $text-muted;
    }
    
    SelectionList {
        height: 16;
        margin: 1 0;
        border: solid $primary;
    }
    
    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0;
    }
    
    Button {
        margin: 0 1;
    }
    
    #install-container {
        width: 90;
        height: 30;
        background: $surface;
        border: solid $primary;
        padding: 1 2;
    }
    
    #install-title {
        width: 100%;
        text-align: center;
        padding: 1;
    }
    
    #install-log {
        height: 20;
        margin: 1 0;
        border: solid $primary;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("⚙️  GRUB Theme Installer", id="title"),
            Static("Select a theme to install on your system", id="subtitle"),
            SelectionList[str](
                *[Selection(theme, theme, False) for theme in THEMES],
                id="theme-list"
            ),
            Horizontal(
                Button("Install Selected", variant="success", id="install-btn"),
                Button("Quit", variant="error", id="quit-btn"),
                id="button-container"
            ),
            id="main-container"
        )
        yield Footer()
    
    @on(Button.Pressed, "#install-btn")
    def install_theme(self) -> None:
        selection_list = self.query_one("#theme-list", SelectionList)
        selected = selection_list.selected
        
        if not selected:
            self.notify("Please select a theme first!", severity="warning")
            return
        
        theme_name = selected[0]
        self.push_screen(InstallScreen(theme_name))
    
    @on(Button.Pressed, "#quit-btn")
    def quit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = GRUBThemeApp()
    app.run()
