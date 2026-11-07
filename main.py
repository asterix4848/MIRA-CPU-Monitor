"""MIRA CPU Monitor v1.0 — lightweight Turkish system monitor."""

from collections import deque
import platform
import tkinter as tk
from tkinter import ttk

import psutil


class MiraMonitor:
    REFRESH_MS = 1000
    HISTORY_SIZE = 90

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MIRA CPU Monitor v1.0")
        self.root.geometry("680x510")
        self.root.minsize(560, 440)
        self.root.configure(bg="#111827")
        self.cpu_history = deque([0.0] * self.HISTORY_SIZE, maxlen=self.HISTORY_SIZE)
        self._style()
        self._build_ui()
        psutil.cpu_percent(interval=None)
        self._update()

    def _style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#111827")
        style.configure("Card.TFrame", background="#1f2937")
        style.configure("TLabel", background="#1f2937", foreground="#e5e7eb", font=("TkDefaultFont", 10))
        style.configure("Title.TLabel", background="#111827", foreground="#f9fafb", font=("TkDefaultFont", 19, "bold"))
        style.configure("Sub.TLabel", background="#111827", foreground="#9ca3af", font=("TkDefaultFont", 10))
        style.configure("Value.TLabel", background="#1f2937", foreground="#34d399", font=("TkDefaultFont", 24, "bold"))
        style.configure("TProgressbar", troughcolor="#374151", background="#10b981", bordercolor="#374151", lightcolor="#10b981", darkcolor="#10b981")

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=22)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="MIRA CPU Monitor", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text=f"Sistem izleme aracı  ·  {platform.system()} {platform.release()}", style="Sub.TLabel").pack(anchor="w", pady=(4, 18))
        cards = ttk.Frame(outer)
        cards.pack(fill="x")
        self.cpu_value = self._metric_card(cards, "İŞLEMCİ KULLANIMI", 0)
        self.ram_value = self._metric_card(cards, "BELLEK KULLANIMI", 1)
        self.cpu_bar = self._metric_bar(cards, 0)
        self.ram_bar = self._metric_bar(cards, 1)
        graph_card = ttk.Frame(outer, style="Card.TFrame", padding=14)
        graph_card.pack(fill="both", expand=True, pady=(18, 0))
        header = ttk.Frame(graph_card, style="Card.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="İşlemci geçmişi", font=("TkDefaultFont", 11, "bold")).pack(side="left")
        self.cores_label = ttk.Label(header, text="", foreground="#9ca3af")
        self.cores_label.pack(side="right")
        self.chart = tk.Canvas(graph_card, height=210, bg="#1f2937", highlightthickness=0)
        self.chart.pack(fill="both", expand=True, pady=(12, 0))
        self.status = ttk.Label(outer, text="Güncelleniyor…", style="Sub.TLabel")
        self.status.pack(anchor="w", pady=(12, 0))
        self.chart.bind("<Configure>", lambda _event: self._draw_chart())

    def _metric_card(self, parent: ttk.Frame, title: str, column: int) -> ttk.Label:
        card = ttk.Frame(parent, style="Card.TFrame", padding=16)
        card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 8 if column == 0 else 0))
        ttk.Label(card, text=title, foreground="#9ca3af", font=("TkDefaultFont", 9, "bold")).pack(anchor="w")
        value = ttk.Label(card, text="—", style="Value.TLabel")
        value.pack(anchor="w", pady=(8, 0))
        parent.columnconfigure(column, weight=1)
        return value

    def _metric_bar(self, parent: ttk.Frame, column: int) -> ttk.Progressbar:
        card = parent.grid_slaves(row=0, column=column)[0]
        bar = ttk.Progressbar(card, maximum=100, mode="determinate")
        bar.pack(fill="x", pady=(12, 0))
        return bar

    def _draw_chart(self) -> None:
        canvas = self.chart
        canvas.delete("all")
        width, height = canvas.winfo_width(), canvas.winfo_height()
        if width < 20 or height < 20:
            return
        left, right, top, bottom = 36, width - 10, 10, height - 22
        plot_h = bottom - top
        for pct in (0, 25, 50, 75, 100):
            y = bottom - plot_h * pct / 100
            canvas.create_line(left, y, right, y, fill="#374151")
            canvas.create_text(left - 8, y, text=str(pct), anchor="e", fill="#9ca3af", font=("TkDefaultFont", 8))
        points = list(self.cpu_history)
        if len(points) > 1:
            coords = []
            for i, value in enumerate(points):
                x = left + (right - left) * i / (len(points) - 1)
                y = bottom - plot_h * value / 100
                coords.extend((x, y))
            canvas.create_line(*coords, fill="#34d399", width=2, smooth=True)
        canvas.create_text(right, height - 7, text="son 90 saniye", anchor="e", fill="#9ca3af", font=("TkDefaultFont", 8))

    def _update(self) -> None:
        try:
            cpu = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            self.cpu_history.append(cpu)
            self.cpu_value.configure(text=f"{cpu:.0f}%")
            self.ram_value.configure(text=f"{memory.percent:.0f}%")
            self.cpu_bar.configure(value=cpu)
            self.ram_bar.configure(value=memory.percent)
            self.cores_label.configure(text=f"{psutil.cpu_count(logical=True) or '—'} mantıksal çekirdek")
            self.status.configure(text=f"Kullanılan bellek: {self._format_bytes(memory.used)} / {self._format_bytes(memory.total)}  ·  Yenileme: 1 sn")
            self._draw_chart()
        except (OSError, RuntimeError) as exc:
            self.status.configure(text=f"Sistem bilgisi alınamadı: {exc}")
        self.root.after(self.REFRESH_MS, self._update)

    @staticmethod
    def _format_bytes(value: int) -> str:
        amount = float(value)
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if amount < 1024 or unit == "TB":
                return f"{amount:.1f} {unit}"
            amount /= 1024
        return f"{amount:.1f} TB"


def main() -> None:
    root = tk.Tk()
    MiraMonitor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
