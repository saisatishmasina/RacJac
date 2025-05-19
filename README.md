
# 🧠 RacJac: Resume Auto-Crafter & Job-Aware Customizer

**RacJac** is an intelligent resume generator that tailors your resume to a specific job description using structured YAML input and LLM-driven keyword alignment. It outputs a clean, styled, and ATS-friendly PDF — perfect for making a great first impression.

![resume_demo](docs/demo.png) <!-- Optional: Add a screenshot here -->

---

## 🚀 Features

- ✅ Input resume content using a simple YAML file
- ✅ Paste any job description — RacJac extracts keywords and customizes the resume
- ✅ Smart summary and bullet point rewriting via LLM (OpenAI / Claude / LLaMA support)
- ✅ Resume sections rendered via modular Jinja2 templates
- ✅ Styled PDF output via HTML + WeasyPrint
- ✅ Custom ordering of resume sections
- ✅ Skill extraction and categorization using LLM or fallback matcher
- ✅ Resume comparison and similarity scoring

---

## 📁 Project Structure

```
RacJac/
├── Scripts/
│   ├── Extract/         # Skill and keyword extraction
│   ├── Generator/       # Resume generation logic
│   ├── Organizer/       # Resume data structure and parsing
│   ├── Doc/             # Section rendering utilities
│   └── Templates/       # HTML + CSS templates
├── assets/              # Sample resumes and job descriptions
├── resume.yaml          # User resume input in YAML format
├── main.py              # Entry point to generate a tailored resume
└── README.md
```

---

## 🧰 Requirements

- Python 3.9+
- Install dependencies:

```bash
pip install -r requirements.txt
```

**System dependencies for WeasyPrint**:

- **Linux**:
  ```bash
  sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libcairo2
  ```

- **macOS**:
  ```bash
  brew install cairo pango gdk-pixbuf libffi
  ```

---

## 📝 Usage

### 1. Customize your YAML resume

Edit `resume.yaml` to include your details:

```yaml
contact:
  name: "John Doe"
  email: "john@example.com"
  ...
experience:
  - job_title: Software Engineer
    company: OpenAI
    ...
```

### 2. Prepare your job description

Paste or save your job description in a `.txt` file.

### 3. Run the generator

```bash
python main.py --resume resume.yaml --jd jobs/walgreens.txt
```

You’ll find the final PDF under `output/resume.pdf`.

---

## 🤖 LLM Integration

This project supports resume enhancement using LLMs like GPT-4, Claude, or LLaMA:

- Bullet point rewriting
- Summary tailoring
- Keyword extraction
- Skill categorization

💡 You can customize the prompts and models in `Scripts/Extract/` to suit your API provider or inference engine.

---

## 📦 Output

- ✅ Tailored, ATS-friendly PDF (`output/resume.pdf`)
- ✅ Clean intermediate HTML (debug/preview)
- ✅ Categorized skills and extracted keywords
- ✅ Resume match scoring (optional)

---

## 🛠️ Customization

- Edit `Templates/resume_template.html` and `style.css` to modify layout, fonts, and themes
- Modify `render_*.py` files under `Doc/Utils` to change how sections are rendered
- Adjust LLM prompts for tone, word count, or bullet style

---

## ✅ TODO / Improvements

- [ ] Add Streamlit or Gradio GUI
- [ ] Convert PDF resumes into YAML (parser)
- [ ] More diverse prompt tuning for LLM section writing
- [ ] Add support for DOCX export
- [ ] Write unit tests and CI pipelines

---

## 🙌 Contributing

Contributions are welcome! Please open issues or PRs if you'd like to help improve RacJac.

---

## 📄 License

MIT License © [Sai Satish Masina](https://github.com/saisatishmasina)

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Jinja2-Templating-orange" />
  <img src="https://img.shields.io/badge/WeasyPrint-PDF%20Rendering-green" />
  <img src="https://img.shields.io/badge/OpenAI-LLM%20Integration-ff69b4?logo=openai" />
  <img src="https://img.shields.io/badge/YAML-Structured%20Resume-brightgreen" />
  <img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4-red" />
</p>

<p align="center">
  <b>RacJac</b> — Resume Auto-Crafter & Job-Aware Customizer
</p>
