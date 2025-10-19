# 💰 GoldTrack Pro — Multi-Currency & Gold Tracking System

GoldTrack Pro is a **real-time currency and gold monitoring desktop application** built with **Python and Tkinter**. It allows users to track multiple currencies and gold prices (TRY based) over the last 7 days, visualize trends with interactive charts, and get real-time updates from reliable APIs.

----------

## 🌟 Features

-   **Multi-Currency Tracking:** Monitor USD, EUR, and XAU (gold) in TRY.
    
-   **Real-Time Gold Prices:** Fetches latest gold prices via online APIs and converts USD/oz → TRY → gram.
    
-   **Interactive Charts:** Visualize trends over the last 7 days with line charts and tooltips.
    
-   **Custom Styling:** Modern dark theme with responsive Tkinter GUI.
    
-   **Selectable Currencies:** Choose which currencies to compare using checkboxes.
    
-   **Dynamic Info Messages:** Success, warning, and error messages for API or user actions.
    
-   **Responsive Window:** Automatically adjusts chart size when the window is resized.
    

----------

## 📈 Screenshots

_(Add screenshots here to showcase the GUI and charts)_

----------

## 🛠 Tech Stack

-   **Python 3** – Core programming language.
    
-   **Tkinter** – GUI development for desktop applications.
    
-   **Requests** – API requests for currency and gold data.
    
-   **Matplotlib** – Charting and visualization.
    
-   **Random** – Fallback values if APIs are unavailable.
    

----------

## ⚡ Installation & Usage

1.  Clone the repository:
    

`git clone https://github.com/yourusername/GoldTrack.git cd GoldTrack` 

2.  (Optional) Create a virtual environment:
    

`python -m venv venv source venv/bin/activate # Linux/macOS venv\Scripts\activate # Windows` 

3.  Install dependencies:
    

`pip install -r requirements.txt` 

4.  Run the application:
    

`python GoldTrack.py` 

----------

## 📝 Features in Detail

-   **API Fallbacks:** If APIs are unreachable, the app generates estimated values to maintain functionality.
    
-   **Currency Conversion:** Converts USD/oz gold prices to TRY per gram.
    
-   **Interactive Plot:** Each currency line shows its latest value on the chart.
    
-   **Info Messages:** Provides feedback on successful updates or errors.
    

----------

## 🔧 Future Improvements

-   Add historical data storage for long-term analysis.
    
-   Enable export of chart data to CSV.
    
-   Integrate additional currencies and precious metals.
    

----------

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.