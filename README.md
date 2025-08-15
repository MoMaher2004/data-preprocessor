# Data Preprocessor V1

## 📜 Description
Data Preprocessor V1 is a simple yet powerful **Streamlit** app that lets you clean, transform, and visualize CSV datasets — all from your browser, without writing a single line of code. Perfect for quick **data preprocessing** and **exploratory analysis** before diving into machine learning or reporting.

---

## ✨ Features
- 📂 Upload and preview CSV files.
- ✂️ Drop unwanted columns or rows with missing values.
- 🏷 Convert columns to categorical data type.
- 🔄 Replace missing values with **Mean** or **Median**.
- 🗑 Remove duplicates.
- 📊 Detect and handle outliers using IQR.
- 🧩 One-hot encode categorical columns.
- 🧾 View dataset info and stats (null counts, unique values, min/max).
- 📈 Visualize with bar plots, scatter plots, heatmaps, pair plots, box plots, and count plots.
- 💾 Download your cleaned dataset as a CSV file.

---

## 🌐 Online Usage
You can try the app instantly without installation here: [https://data-preproce55or.streamlit.app/](https://data-preproce55or.streamlit.app/)

---

## 💻 How to run locally
1. **Clone the repo**  
```bash
git clone https://github.com/MoMaher2004/data-preprocessor.git
cd data-preprocessor
```

2. **Create a virtual environment (optional but recommended)**  
```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate     # Windows
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Run the app**  
```bash
streamlit run app.py
```

---

## 🛠 How to use
- Upload your CSV file.
- Choose any preprocessing or visualization option.
- **The sections are not sequential** — you can jump up and down to different sections anytime, applying changes or visualizing results in any order you like.

