import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tinytag import TinyTag
import os
import datetime

# --- FARBEN (Dark Mode) ---
BG_COLOR = "#1E1E1E"  # Dunkler Hintergrund
FG_COLOR = "#FFFFFF"  # Weißer Text
ACCENT_COLOR = "#3A3A3A"  # Listen-Hintergrund
HIGHLIGHT = "#007ACC"  # Blau für Auswahl


def format_duration(seconds):
    if seconds is None:
        return "-"
    return str(datetime.timedelta(seconds=int(seconds)))


class AudioAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Analyzer (Stable)")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_COLOR)

        # --- STYLE KONFIGURATION ---
        style = ttk.Style()
        style.theme_use("clam")  # 'clam' erlaubt bessere Farbanpassungen

        # Style für die Tabelle (Treeview)
        style.configure(
            "Treeview",
            background=ACCENT_COLOR,
            foreground=FG_COLOR,
            fieldbackground=ACCENT_COLOR,
            rowheight=30,
            borderwidth=0,
        )

        style.map("Treeview", background=[("selected", HIGHLIGHT)])

        # Style für die Header
        style.configure(
            "Treeview.Heading",
            background="#2D2D2D",
            foreground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )

        style.map("Treeview.Heading", background=[("active", "#404040")])

        # --- UI AUFBAU ---

        # 1. Toolbar oben
        toolbar = tk.Frame(root, bg=BG_COLOR, pady=10, padx=10)
        toolbar.pack(fill="x")

        # Buttons (Manuell gestylt für Dark Mode)
        self.btn_add = tk.Button(
            toolbar,
            text="+ Dateien auswählen",
            command=self.add_files,
            bg=HIGHLIGHT,
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
        )
        self.btn_add.pack(side="left", padx=5)

        self.btn_clear = tk.Button(
            toolbar,
            text="Liste leeren",
            command=self.clear_list,
            bg="#C42B1C",
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
        )
        self.btn_clear.pack(side="left", padx=5)

        self.lbl_stats = tk.Label(
            toolbar, text="0 Dateien", bg=BG_COLOR, fg="#AAAAAA", font=("Segoe UI", 10)
        )
        self.lbl_stats.pack(side="right", padx=10)

        # 2. Die Tabelle (Treeview)
        columns = (
            "filename",
            "format",
            "duration",
            "bitrate",
            "samplerate",
            "channels",
        )
        self.tree = ttk.Treeview(
            root, columns=columns, show="headings", selectmode="extended"
        )

        # Spalten definieren
        self.tree.heading("filename", text="Dateiname", anchor="w")
        self.tree.heading("format", text="Format", anchor="center")
        self.tree.heading("duration", text="Dauer", anchor="center")
        self.tree.heading("bitrate", text="Bitrate", anchor="center")
        self.tree.heading("samplerate", text="Sample Rate", anchor="center")
        self.tree.heading("channels", text="Kanäle", anchor="center")

        self.tree.column("filename", width=300)
        self.tree.column("format", width=80, anchor="center")
        self.tree.column("duration", width=100, anchor="center")
        self.tree.column("bitrate", width=100, anchor="center")
        self.tree.column("samplerate", width=100, anchor="center")
        self.tree.column("channels", width=80, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Packen
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Audio Dateien auswählen",
            filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a *.wma")],
        )

        if not file_paths:
            return

        for path in file_paths:
            self.analyze_file(path)

        self.update_stats()

    def analyze_file(self, path):
        filename = os.path.basename(path)
        ext = os.path.splitext(filename)[1].upper().replace(".", "")

        try:
            tag = TinyTag.get(path)

            duration = format_duration(tag.duration)
            bitrate = f"{int(tag.bitrate)} kbit/s" if tag.bitrate else "-"
            samplerate = f"{tag.samplerate} Hz" if tag.samplerate else "-"
            channels = str(tag.channels) if tag.channels else "-"

            # In Tabelle einfügen
            self.tree.insert(
                "",
                "end",
                values=(filename, ext, duration, bitrate, samplerate, channels),
            )

        except Exception as e:
            # Fehlerzeile in Rot (simuliert durch Tag, da Treeview limitationen hat, zeigen wir es einfach an)
            self.tree.insert(
                "", "end", values=(filename, "FEHLER", "-", "-", "-", str(e))
            )

    def clear_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.update_stats()

    def update_stats(self):
        count = len(self.tree.get_children())
        self.lbl_stats.config(text=f"{count} Dateien")


if __name__ == "__main__":
    root = tk.Tk()
    # Damit es auf High-DPI Monitoren nicht unscharf aussieht:
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = AudioAnalyzerApp(root)
    root.mainloop()
