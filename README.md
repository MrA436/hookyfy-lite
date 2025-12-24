# 🚀 HookyFY Lite

**HookyFY Lite** is a lightweight Streamlit-based tool that generates **high-impact Instagram hooks, conclusions, and captions** designed to stop the scroll and fit premium, luxury-style visuals.

It focuses on **recognition, pressure, and outcome**, not generic motivation or filler content.

---

## 🧠 What HookyFY Lite Does

* Takes a single topic (e.g. *discipline*, *comfort zone*, *wasted potential*)
* Generates **exactly 3 structured outputs**, each containing:

  * Hook (section-aware and scroll-focused)
  * Conclusion (clear consequence, no abstraction)
  * Caption (plain, grounded, non-hype)
* Uses a recognition → edge → outcome structure
* Produces copy that works with **slow, dark, luxury-style reels**

All outputs are formatted and ready to use.

---

## 🧩 Core Features

* Section-aware hooks
  *(Power, Curiosity, Shock, Relatable, Motivation)*
* Built-in constraints to avoid:

  * abstract language
  * empty motivation
  * philosophical analysis
* Consistent formatting for short-form content
* Local-first development workflow

---

## 🛠️ Built With

* [Streamlit](https://streamlit.io/) for the interface
* Python 🐍 for generation and validation logic
* AI model via OpenRouter / DeepSeek-compatible API

---

## 🖥️ Run Locally

Clone the repository:

```bash
git clone https://github.com/MrA436/hookyfy-lite.git
cd hookyfy-lite
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

---

## 🔐 Environment Variables

API keys are **not** committed.

Create a `.env` file locally:

```env
OPENROUTER_API_KEY=your_key_here
```

For deployment, set secrets through the hosting platform instead of using `.env`.

---

## 📌 Status

HookyFY Lite is under active development.

The current focus is **output quality and structure**, not feature count.
Future versions will build on this foundation.

---

## ⚠️ Note

Generated content should always be reviewed before posting.
This tool is meant to assist creative work, not replace judgment.
