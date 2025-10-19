import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter

class DataFetcher:
    """Handles fetching currency and gold data."""

    @staticmethod
    def fetch_currency(symbol: str):
        """Fetch USD/EUR to TRY data for the last 7 days."""
        end_date = datetime.now().date()
        dates = [(end_date - timedelta(days=i)).isoformat() for i in range(7)][::-1]
        values = []

        for d in dates:
            try:
                url = f"https://api.frankfurter.app/{d}?from={symbol}&to=TRY"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                val = response.json().get("rates", {}).get("TRY")
                if val is None:
                    raise ValueError("No data received")
            except (requests.RequestException, ValueError):
                val = None
            values.append(val)
        return dates, values

    @staticmethod
    def fetch_gold():
        """Fetch gold price in TRY (last 7 days approximation)."""
        end_date = datetime.now().date()
        dates = [(end_date - timedelta(days=i)).isoformat() for i in range(7)][::-1]

        try:
            r_gold = requests.get("https://api.metals.live/v1/spot/gold", timeout=5)
            r_gold.raise_for_status()
            last_oz_usd = r_gold.json()[-1][1]
        except requests.RequestException:
            last_oz_usd = None

        try:
            r_usd = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=5)
            r_usd.raise_for_status()
            usd_try = r_usd.json()["rates"]["TRY"]
        except requests.RequestException:
            usd_try = None

        values = []
        for _ in dates:
            if last_oz_usd is None or usd_try is None:
                values.append(None)
            else:
                values.append(round((last_oz_usd * usd_try) / 31.1035, 2))
        return dates, values


class GoldTrackApp:
    """Main application class for GUI and plotting."""

    def __init__(self, root):
        self.root = root
        self.root.title("💰 GoldTrack Pro — Multi-Currency & Gold Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0e0e0e")
        self.setup_styles()
        self.setup_gui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#0e0e0e", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", background="#1f1f1f", foreground="white", padding=10, relief="flat", font=("Segoe UI", 11, "bold"))
        style.map("TButton", background=[("active", "#198754"), ("!active", "#1f1f1f")], foreground=[("active", "white")])
        style.configure("TLabelframe", background="#0e0e0e", foreground="white")
        style.configure("TLabelframe.Label", font=("Segoe UI", 12, "bold"), foreground="gold")
        style.configure("TCheckbutton", background="#0e0e0e", foreground="white", font=("Segoe UI", 11), padding=5)
        style.map("TCheckbutton", background=[("active", "#2a2a2a"), ("selected", "#198754")], foreground=[("active", "white"), ("selected", "white")])

    def setup_gui(self):
        ttk.Label(self.root, text="📊 Daily Currency & Gold Tracker (TRY Based)", font=("Segoe UI", 20, "bold"), foreground="gold", background="#0e0e0e").pack(pady=15)

        self.frame_select = ttk.Labelframe(self.root, text="Select Values to Compare")
        self.frame_select.pack(pady=10, padx=20, fill="x")

        self.currencies = {"USD": tk.BooleanVar(value=True), "EUR": tk.BooleanVar(value=False), "XAU": tk.BooleanVar(value=False)}
        for col, (cur, var) in enumerate(self.currencies.items()):
            ttk.Checkbutton(self.frame_select, text=cur, variable=var, style="TCheckbutton").grid(row=0, column=col, padx=15, pady=5)

        ttk.Button(self.root, text="📈 Fetch & Compare Data", command=self.update_chart).pack(pady=10)

        self.figure, self.ax = plt.subplots(figsize=(9, 4))
        self.figure.patch.set_facecolor("#0e0e0e")
        self.ax.set_facecolor("#141414")
        self.ax.tick_params(colors="white")
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.info_label = ttk.Label(self.root, text="💡 Select currency(ies) and fetch data.", font=("Segoe UI", 11))
        self.info_label.pack(pady=8)
        self.root.bind("<Configure>", self.on_resize)

    def update_chart(self):
        selected = [k for k, v in self.currencies.items() if v.get()]
        if not selected:
            self.show_info("⚠️ Select at least one currency.", "warning")
            return

        self.ax.clear()
        self.ax.set_facecolor("#141414")
        self.ax.tick_params(colors="white")
        colors = {"USD": "lime", "EUR": "cyan", "XAU": "gold"}
        any_data = False

        for symbol in selected:
            if symbol == "XAU":
                dates, values = DataFetcher.fetch_gold()
            else:
                dates, values = DataFetcher.fetch_currency(symbol)

            if all(v is None for v in values):
                self.show_info(f"❌ No data available for {symbol}.", "error")
                continue

            any_data = True
            self.ax.plot(dates, values, marker="o", linewidth=2, color=colors[symbol], label=symbol)
            self.ax.text(dates[-1], values[-1] if values[-1] is not None else 0, f"{values[-1]:.2f}" if values[-1] else "N/A", color=colors[symbol], fontsize=9)

        if not any_data:
            self.show_info("❌ No data could be retrieved.", "error")
            return

        self.ax.legend(facecolor="#141414", labelcolor="white")
        self.ax.set_title("Last 7 Days Currency / Gold Changes (TRY)", color="white", fontsize=14)
        self.ax.set_ylabel("₺ Value", color="white")
        self.ax.set_xlabel("Date", color="white")
        self.ax.grid(color="#303030", linestyle="--", alpha=0.5)
        self.ax.tick_params(axis='x', rotation=45)
        self.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"₺{x:,.2f}"))

        self.canvas.draw()
        self.show_info(f"✅ {', '.join(selected)} data successfully updated!", "success")

    def show_info(self, message, msg_type="info"):
        colors = {"info": "white", "success": "#198754", "warning": "#FFC107", "error": "#DC3545"}
        self.info_label.config(text=message, foreground=colors.get(msg_type, "white"))

    def on_resize(self, event):
        self.canvas.get_tk_widget().config(width=event.width - 40, height=event.height - 250)


if __name__ == "__main__":
    root = tk.Tk()
    app = GoldTrackApp(root)
    root.mainloop()
