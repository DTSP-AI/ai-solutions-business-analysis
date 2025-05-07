Thought for a couple of seconds


````markdown
# AI Business Optimization Intake

> “Because when you don’t like something about the world, you change it… or at least make a fancy form so it looks like you did.”  
> — Rick Sanchez

A **Streamlit** app that collects a business’s key data points and spins up a strategic AI & automation roadmap via OpenAI’s GPT-4. Perfect for testing your consulting chops or impressing your buddy with your AI overlord’s brilliance.

---

## 🚀 Features

- **Intake Form**  
  Collects sales, marketing, retention, AI readiness, tech-stack, goals & timeline.
- **GPT-4 Analysis**  
  Generates a clean, structured “Current System Snapshot”, “Bottlenecks”, “AI Opportunities” and “Next Steps”.
- **One-click Deployment**  
  Runs locally or on Streamlit Cloud in seconds.
- **Emoji-Powered UI**  
  Because plain text in 2025? Please.

---

## 🛠️ Requirements

- **Python** 3.9 – 3.11  
- **Streamlit** ≥ 1.28  
- **LangChain** 0.0.261  
- **python-dotenv**, **requests**, **python-dateutil**, **google-generative-ai**  
- **OPENAI_API_KEY** (GPT-4 access)

See [`requirements.txt`](requirements.txt) for pinned versions.

---

## ⚙️ Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/YourUser/marketing-assistant.git
   cd marketing-assistant
````

2. **Create a virtual env** (Windows PowerShell)

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure secrets**
   Copy `.env.example` to `.env` and fill in your key:

   ```ini
   OPENAI_API_KEY=sk-YOUR_REAL_KEY_HERE
   ```

---

## ▶️ Usage

Run the app locally:

```bash
streamlit run ai_marketing_assistant.py
```

Then point your browser at [http://localhost:8501](http://localhost:8501) and start smashing that form.

---

## ☁️ Deployment (Streamlit Cloud)

1. Push your code to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and “New app”.
3. Select your repo, branch (`main`), and main file path (`ai_marketing_assistant.py`).
4. In “Secrets” add `OPENAI_API_KEY`.
5. Click **Deploy**.
   You’ll get a public URL you can share with your buddy.

---

## 🤝 Contributing

1. Fork it.
2. Create a feature branch.
3. Send a PR.

No placeholders, no pseudocode, no bullshit—just working, tested code.

---

## 📝 License

MIT © You
(Just don’t sue Rick when your buddy’s business goes under.)

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

