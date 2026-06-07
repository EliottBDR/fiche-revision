# 📚 AI Study Sheet Generator

> Transform any PDF course into a structured study sheet, quiz, or detailed exam correction in seconds.

🔗 **[fiche-revision.streamlit.app](https://fiche-revision.streamlit.app/)**
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌐 Live App

**[→ fiche-revision.streamlit.app](https://fiche-revision.streamlit.app/)**

---

## 🎬 Demo

https://github.com/user-attachments/assets/b11f1a38-d628-4908-bb8e-1e072b155d29

---

## ✨ What it does

Upload any PDF and choose a mode:

- **📖 Study Sheet** — Key definitions, formulas, reasoning methods, common mistakes, and 10 review questions (answers hidden until revealed)
- **❓ Quiz** — 15 multiple-choice questions with hidden answers and detailed explanations
- **✏️ Exam Correction** — Full step-by-step correction of an exam paper, question by question

Adapts to **1st or 2nd year engineering prep** level. Export your result as a styled **HTML file** (printable as PDF from your browser).

---

## ⚡ How to use

1. Go to **[fiche-revision.streamlit.app](https://fiche-revision.streamlit.app/)**
2. Select a mode (Study Sheet, Quiz, or Exam Correction)
3. Select your level
4. Upload your PDF
5. Click **Generate**
6. Download the result as HTML

No account required. Completely free.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI (primary) | Groq — Llama 3.3 70B |
| AI (fallback) | Cerebras — GPT-OSS 120B |
| PDF parsing | pdfplumber |
| Export | Markdown → Styled HTML |
| Deployment | Streamlit Cloud |

---

## 🚀 Run it locally

```bash
git clone https://github.com/EliottBDR/fiche-revision.git
cd fiche-revision
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
CEREBRAS_API_KEY=your_cerebras_api_key
```

Get free API keys (no credit card):
- Groq: [console.groq.com](https://console.groq.com)
- Cerebras: [cloud.cerebras.ai](https://cloud.cerebras.ai)

```bash
streamlit run app.py
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**EliottBDR** — [github.com/EliottBDR](https://github.com/EliottBDR)
