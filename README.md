<div align="center">

# 🧠 AI · ML · DS

**A living knowledge base for Artificial Intelligence, Machine Learning, Data Science, and the engineering craft around them.**

Course notes, revision PDFs, notebooks, hands-on projects, production-grade pipelines, agentic AI experiments, and the tooling that ties it all together.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=for-the-badge&logo=jupyter&logoColor=white">
  <img alt="PySpark" src="https://img.shields.io/badge/Apache%20Spark-PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white">
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white">
  <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
  <img alt="LangChain" src="https://img.shields.io/badge/LangChain-LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img alt="Go" src="https://img.shields.io/badge/Go-Programming-00ADD8?style=for-the-badge&logo=go&logoColor=white">
</p>

<p>
  <a href="https://github.com/ankitgupta1729/AI-ML-DS/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/ankitgupta1729/AI-ML-DS?style=flat-square&color=f5c518"></a>
  <a href="https://github.com/ankitgupta1729/AI-ML-DS/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/ankitgupta1729/AI-ML-DS?style=flat-square&color=blue"></a>
  <a href="https://github.com/ankitgupta1729/AI-ML-DS"><img alt="Repo size" src="https://img.shields.io/github/repo-size/ankitgupta1729/AI-ML-DS?style=flat-square&color=success"></a>
  <a href="#-revision-pdfs"><img alt="Revision PDFs" src="https://img.shields.io/badge/revision%20PDFs-48%20courses-purple?style=flat-square"></a>
</p>

</div>

---

## 📖 About

This repository is a **single, curated home for everything I learn and build across the AI/ML/Data stack** — from the mathematical foundations of machine learning to shipping LLM-powered agents in production.

It is organised into **domain folders**, each holding self-contained, numbered modules. Every module stands on its own: pick a topic, open it, and start reading or running code.

**Who it's for**

| You are… | Start here |
| --- | --- |
| 🎓 Learning ML/DS from scratch | [`foundations/`](foundations), [`machine-learning/`](machine-learning) |
| 📚 Revising a course | [Revision PDFs](#-revision-pdfs) — one polished PDF per course |
| 🤖 Building with LLMs & agents | [`generative-ai/`](generative-ai) |
| 🏗️ Taking models to production | [`mlops/`](mlops) |
| 🖼️ Working on deep learning & vision | [`deep-learning/`](deep-learning), [`nlp/`](nlp) |
| 💼 Preparing for interviews | [`career/`](career) |
| 🛠️ Looking for handy scripts | [`projects/18.Utilities`](projects/18.Utilities), [`tools/`](tools) |

---

## 🗂️ Repository Layout

```
AI-ML-DS/
├── foundations/            Python, SQL, theory notes
├── data-engineering/       PySpark, Databricks
├── machine-learning/       Andrew Ng ML Specialization, AI Nanodegree
├── deep-learning/          TensorFlow & PyTorch courses, CNNs, GANs, computer vision
├── nlp/                    NLP and transformers
├── generative-ai/          LLMs, RAG, LangChain, LangGraph, agents, Claude Code
├── mlops/                  ML in production, MLflow, CI/CD, Google Cloud
├── dev-tools/              Git, Docker, debugging, uv, pipenv, everyday tools
├── programming-languages/  Go
├── career/                 Interview prep, blogs, talks, retrospectives
├── projects/               Standalone utilities and side projects
├── resources/              Reference books and links
├── docs/                   Repository-level guides (Jupyter kernels, GPU setup)
├── tools/                  Repository tooling (revision-PDF builder, layout migration)
├── pyproject.toml · uv.lock · requirements.txt · Pipfile
└── README.md · CONTRIBUTING.md · AGENTS.md
```

Every course module follows the same shape:

```
<category>/<NN>.<Course-Name>/
├── Note.md        course notes (the source of truth)
├── images/        screenshots referenced from the notes
├── pdf/           generated revision PDF(s)
└── …              notebooks, code, data
```

<details open>
<summary><b>🐍 Foundations</b> — <code>foundations/</code></summary>

| Module | What's inside |
| --- | --- |
| [`01.Python`](foundations/01.Python) | Core Python, data structures, notebooks and practice exercises |
| [`03.SQL`](foundations/03.SQL) | Query fundamentals through advanced analytical SQL |
| [`04.Theory`](foundations/04.Theory) | ML, GenAI and Data Engineering theory notes |
| [`13.Decorators`](foundations/13.Decorators) | A deep dive into Python decorators |
| [`45.Python-for-Everybody-…`](foundations/45.Python-for-Everybody-University-of-Michigan-Charles-Severance-PhD) | Coursework — Python for Everybody (Univ. of Michigan) |

</details>

<details open>
<summary><b>🗄️ Data Engineering</b> — <code>data-engineering/</code></summary>

| Module | What's inside |
| --- | --- |
| [`02.PySpark`](data-engineering/02.PySpark) | Distributed data processing with Apache Spark |
| [`14.Databricks`](data-engineering/14.Databricks) | Lakehouse fundamentals and Databricks workflows |

</details>

<details open>
<summary><b>🎓 Machine Learning</b> — <code>machine-learning/</code></summary>

Full lecture notes with figures for all three courses of the DeepLearning.AI / Stanford specialization.

| Module | What's inside |
| --- | --- |
| [`47.Coursera-Andrew-Ng-Machine-Learning`](machine-learning/47.Coursera-Andrew-Ng-Machine-Learning) | Course 1 — Supervised ML: regression, classification, gradient descent |
| [`48.Coursera-Andrew-Ng-Advanced-Machine-Learning`](machine-learning/48.Coursera-Andrew-Ng-Advanced-Machine-Learning) | Course 2 — Neural networks, decision trees, practical ML system design |
| [`49.Coursera-Andrew-Ng-unsupervised-…`](machine-learning/49.Coursera-Andrew-Ng-unsupervised-learning-recommenders-reinforcement-learning) | Course 3 — Clustering, anomaly detection, recommenders, reinforcement learning |
| [`50.Andrew-Ng-Course-Material`](machine-learning/50.Andrew-Ng-Course-Material) | 17 community repos of labs, solutions and notes for the Andrew Ng courses (third-party, kept for study) |
| [`33.AI-Nano-Degree`](machine-learning/33.AI-Nano-Degree) | Nanodegree notes — search, heuristics, classical AI |

</details>

<details open>
<summary><b>🖼️ Deep Learning</b> — <code>deep-learning/</code></summary>

Convolutional architectures, transfer learning, GANs, and the TensorBoard workflow for inspecting what a network actually learned.

| Module | What's inside |
| --- | --- |
| [`51.Linkedin-TensorFlow-Working-with-Images`](deep-learning/51.Linkedin-TensorFlow-Working-with-Images) | Image pipelines in TensorFlow — loading, augmentation, CIFAR-10 training with checkpointing |
| [`52.Packt-Tensorflow-Deep-Learning-Solutions-…`](deep-learning/52.Packt-Tensorflow-Deep-Learning-Solutions-for-Images-Will-Ballard) | Packt course (Will Ballard) — practical deep-learning recipes for image problems |
| [`53.Convolutional-Neural-Networks-with-TensorFlow-in-Python`](deep-learning/53.Convolutional-Neural-Networks-with-TensorFlow-in-Python) | CNNs end to end — convolutions, pooling, regularisation, HParams tuning, TensorBoard logs |
| [`54.Deep-Learning-for-Computer-Vision-with-TensorFlow-2`](deep-learning/54.Deep-Learning-for-Computer-Vision-with-TensorFlow-2) | CNN architectures, transfer learning, object detection and YOLO |
| [`55.Udemy-PyTorch-Deep-Learning-and-…`](deep-learning/55.Udemy-PyTorch-Deep-Learning-and-Artificial-Intelligence-by-The-Lazy-Programmer) | PyTorch end to end — ANNs, CNNs, RNNs, recommenders, GANs, deep RL |
| [`56.Udemy-Introduction-to-GANs-with-PyTorch`](deep-learning/56.Udemy-Introduction-to-Generative-Adversarial-Networks-with-PyTorch) | Generative adversarial networks, pix2pix, vid2vid |
| [`57.Convolutional-Neural-Networks-with-Pytorch`](deep-learning/57.Convolutional-Neural-Networks-with-Pytorch) | Deep-learning fundamentals and CNNs in PyTorch |
| [`58.Udemy-PyTorch-Tutorial-…`](deep-learning/58.Udemy-PyTorch-Tutorial-Neural-Networks-&-Deep-Learning-in-Python) | The Python data stack, tensors, ANNs, CNNs and transfer learning |
| [`59.Modern-Deep-Convolutional-Neural-Networks-with-PyTorch`](deep-learning/59.Modern-Deep-Convolutional-Neural-Networks-with-PyTorch) | Modern CNN architectures, detection and segmentation |

> [!TIP]
> Modules 51 and 53 ship their TensorBoard run logs. Point TensorBoard at them to replay the
> training curves without retraining anything:
>
> ```bash
> tensorboard --logdir deep-learning/53.Convolutional-Neural-Networks-with-TensorFlow-in-Python/logs
> ```

</details>

<details open>
<summary><b>🗣️ Natural Language Processing</b> — <code>nlp/</code></summary>

| Module | What's inside |
| --- | --- |
| [`60.Natural-Language-Processing-(NLP)-in-Python`](nlp/60.Natural-Language-Processing-(NLP)-in-Python) | Text preprocessing, vectorisation, classic and neural NLP |
| [`61.…-Transformers-for-Natural-Language-Processing`](nlp/61.GetFreeCourses.Co-Udemy-Data-Science-Transformers-for-Natural-Language-Processing) | Attention, BERT, GPT and Hugging Face pipelines |

</details>

<details open>
<summary><b>🤖 Generative AI, LLMs & Agents</b> — <code>generative-ai/</code></summary>

| Module | What's inside |
| --- | --- |
| [`05.Code`](generative-ai/05.Code) | Reference implementations for GenAI and AI agents |
| [`20.LlamaIndex`](generative-ai/20.LlamaIndex) | RAG pipelines and data indexing with LlamaIndex |
| [`22.LLM_Fine_Tuning`](generative-ai/22.LLM_Fine_Tuning) | Fine-tuning large language models |
| [`23.LangChain`](generative-ai/23.LangChain) · [`24.LangChain2`](generative-ai/24.LangChain2) | Chains, tools, retrieval and LangChain projects |
| [`25.Claude-Code-Deep-Dive`](generative-ai/25.Claude-Code-Deep-Dive) | Working effectively with agentic coding tools |
| [`26.LangGraph`](generative-ai/26.LangGraph) | Stateful, graph-based agent orchestration |
| [`27.Agentic-AI-…-LangGraph`](generative-ai/27.Agentic-AI-Deliver-a-successful-chatbot-POC-with-LangGraph) | Chatbot POC built end-to-end with LangGraph |
| [`28.Building-Scalable-AI-Chatbot-…`](generative-ai/28.Building-Scalable-AI-Chatbot-with-Memory-using-LangChain-and-Streamlit) | Chatbot with memory, served via Streamlit |
| [`29.Build-Your-AI-Agent-with-LangGraph`](generative-ai/29.Build-Your-AI-Agent-with-LangGraph) | Building an agent from first principles |
| [`30.GenAI-AgenticAI-PromptEngineering-ChatGPT`](generative-ai/30.GenAI-AgenticAI-PromptEngineering-ChatGPT) | Prompt engineering and agentic patterns |
| [`32.Generative-AI-for-Everyone`](generative-ai/32.Generative-AI-for-Everyone) | Course notes on the GenAI landscape |
| [`40.AI-Agent-Course-…-MCP`](generative-ai/40.AI-Agent-Course-Build-a-Language‑Learning-Agent-with-OpenAI-LangGraph-Ollama-MCP) | Language-learning agent: OpenAI + LangGraph + Ollama + MCP |
| [`46.Udemy-RAG-Fine_Tuning-LLM`](generative-ai/46.Udemy-RAG-Fine_Tuning-LLM) | RAG versus fine-tuning |
| [`17.OpenCode`](generative-ai/17.OpenCode) | Open-source coding agent experiments |

</details>

<details open>
<summary><b>🏭 MLOps & Cloud</b> — <code>mlops/</code></summary>

| Module | What's inside |
| --- | --- |
| [`36.Introduction-to-ML-in-Production`](mlops/36.Introduction-to-Machine-Learning-in-Production-DeepLearningAI) | MLOps Course 1 — the ML lifecycle, data-centric AI |
| [`43.Machine-Learning-Engineering-for-Production-…`](mlops/43.Machine-Learning-Engineering-for-Production-MLOps-and-Specialization) | MLOps Course 2 — the ML data lifecycle in production |
| [`44.Machine-learning-modeling-pipelines-in-production`](mlops/44.Machine-learning-modeling-pipelines-in-production) | MLOps Course 3 — modeling pipelines, TFX, distributed training |
| [`35.Deploying-Machine-Learning-Models-in-Production`](mlops/35.Deploying-Machine-Learning-Models-in-Production) | MLOps Course 4 — serving, scaling and monitoring models |
| [`39.mlflow`](mlops/39.mlflow) | Experiment tracking and model registry |
| [`31.CICD-Pipeline`](mlops/31.CICD-Pipeline) | Continuous integration & delivery for ML |
| [`34.Fundamentals-of-Google-Cloud-Udemy`](mlops/34.Fundamentals-of-Google-Cloud-Udemy) | Cloud fundamentals for data workloads |

</details>

<details open>
<summary><b>🧰 Developer Tools & Languages</b> — <code>dev-tools/</code>, <code>programming-languages/</code></summary>

| Module | What's inside |
| --- | --- |
| [`09.Tools`](dev-tools/09.Tools) | DBeaver, Excel and other day-to-day tools |
| [`10.Git`](dev-tools/10.Git) | Git workflows and recipes |
| [`11.Docker`](dev-tools/11.Docker) | Containerising data & ML applications |
| [`12.Debugger`](dev-tools/12.Debugger) | Debugging Python effectively |
| [`15.uv_demo`](dev-tools/15.uv_demo) · [`37`](dev-tools/37.Youtube-UV-A-Faster-All-in-One-Package-Manager-to-Replace-Pip-and-Venv) · [`38`](dev-tools/38.Stop-Using-Pip-This-New-Tool-is-100x-Faster-\(UV-Tutorial\)) | `uv` — the fast Python package manager |
| [`21.pipenv-course`](dev-tools/21.pipenv-course) | Environment management with Pipenv |
| [`19.Go`](programming-languages/19.Go) · [`41`](programming-languages/41.YouTube-Go-Programming-Full-Course-Tech-with-Tim) · [`42`](programming-languages/42.Learn-Go-With-This-ONE-Project-Tech-with-Tim) | Go programming — course + project work |

</details>

<details open>
<summary><b>📚 Career, Projects & Resources</b></summary>

| Module | What's inside |
| --- | --- |
| [`career/06.Interview-Preparation`](career/06.Interview-Preparation) | DS/ML interview questions and answers |
| [`career/07.Blogs`](career/07.Blogs) | Blog drafts and write-ups |
| [`career/08.YouTube`](career/08.YouTube) | Notes and code from video tutorials |
| [`career/16.Improvements`](career/16.Improvements) | Retrospectives and feedback notes |
| [`projects/18.Utilities`](projects/18.Utilities) | Standalone scripts — images→PDF, PDF splitter, mailer, chatbots, website |
| [`resources/`](resources) | Curated PDFs, books and reference links |
| [`docs/`](docs) | [Jupyter kernels & venvs](docs/JUPYTER-KERNELS.md), [GPU setup guide](docs/guides/GPU-Setup-Guide-macOS-Linux-Windows.pdf) |

</details>

---

## 📚 Revision PDFs

Every course's notes are also published as a **designed, print-ready PDF** for revision — cover page,
clickable table of contents with page numbers, PDF bookmarks, section openers, and every lecture
screenshot placed **right next to the sentence it illustrates**.

> [!NOTE]
> **How the screenshots are placed.** In the Markdown notes, each lecture's screenshots were
> captured first and its transcript follows. Each screenshot carries the lecturer's burned-in
> subtitle, so the PDF builder reads it with OCR, finds those exact words in the transcript and
> inserts the screenshot, unaltered, at that point (keeping the original order). Lecture titles and
> figure captions come from the slide titles (or key phrases of the lecture when a slide has none).
> The Markdown files themselves are never modified — see
> [`tools/notes-to-pdf`](tools/notes-to-pdf) for the details and to rebuild.

<!-- pdf-index:start -->
<!-- pdf-index:end -->

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12** (pinned in `.python-version` / `pyproject.toml`; the legacy `Pipfile` targets 3.11)
- **Git**
- Optional, per module: [Docker](https://docs.docker.com/get-docker/), [Go](https://go.dev/dl/), [uv](https://docs.astral.sh/uv/), a Java runtime for PySpark

### Clone the repository

```bash
git clone https://github.com/ankitgupta1729/AI-ML-DS.git
cd AI-ML-DS
```

> [!IMPORTANT]
> **Updating an existing clone from before the category layout?** `git pull` moves every tracked
> file, but git-ignored files (datasets, model weights, `.venv`, `.env`) stay behind in the old
> root-level folders. Move them across once with:
>
> ```bash
> bash tools/migrate-local-layout.sh          # dry run
> bash tools/migrate-local-layout.sh --apply  # move the files
> ```
>
> Then recreate module virtual environments (`uv sync`), since venvs store absolute paths.

### Set up the base environment

<table>
<tr><th>Using <code>uv</code> (recommended)</th><th>Using <code>pip</code></th><th>Using <code>pipenv</code></th></tr>
<tr valign="top">
<td>

```bash
brew install uv
uv sync
```

</td>
<td>

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

</td>
<td>

```bash
pip install pipenv
pipenv install
pipenv shell
```

</td>
</tr>
</table>

All base dependencies are pinned in [`pyproject.toml`](pyproject.toml) and locked in `uv.lock` (mirrored in `requirements.txt` for the `pip`/`pipenv` paths).

#### Optional: auto-activate the environment with `direnv`

Install [direnv](https://direnv.net/), hook it into your shell (`eval "$(direnv hook zsh)"`), then create a local `.envrc` in the repo root:

```bash
echo 'source .venv/bin/activate' > .envrc
direnv allow .
```

From then on, every `cd` into the repo (or a subfolder) activates the environment automatically.

### Launch the notebooks

```bash
jupyter lab      # or: jupyter notebook
```

> [!TIP]
> Several modules ship their **own** `Pipfile`, `requirements.txt`, or `pyproject.toml` (e.g. `generative-ai/20.LlamaIndex`, `generative-ai/23.LangChain`, `dev-tools/15.uv_demo`). Prefer the module-local environment when working inside one. For registering those environments as Jupyter kernels, see [`docs/JUPYTER-KERNELS.md`](docs/JUPYTER-KERNELS.md).

### Configure secrets

Modules that call external APIs read credentials from a local `.env` file — never commit it (`.env` is git-ignored).

```bash
cat > .env <<'EOF'
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
EOF
```

---

## 🧭 Conventions

- **Domain folders, numbered modules** — the number reflects the order a module was added, not difficulty.
- **Self-contained modules** — each folder holds its own notes, notebooks, data and (where needed) environment files.
- **Notes are the source of truth** — `pdf/` folders are generated from them; rebuild instead of editing PDFs.
- **Notebooks first** — exploration and teaching happen in `.ipynb`; reusable logic graduates into `.py`.
- **Editor settings** — [`.editorconfig`](.editorconfig) keeps whitespace consistent across editors.

---

## 🤝 Contributing

Issues, corrections and suggestions are genuinely welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for where new material goes and how to rebuild the revision PDFs, and [`AGENTS.md`](AGENTS.md) for the guide used by coding agents.

---

## 🙏 Acknowledgements

Material here draws on excellent work from **DeepLearning.AI**, **Coursera**, **Stanford Online**, **University of Michigan**, **Udemy**, **LinkedIn Learning**, **Packt**, **Databricks**, **Tech With Tim**, and the open-source communities behind LangChain, LlamaIndex, MLflow, Apache Spark, TensorFlow, PyTorch and Go. Full credit to the original authors — these notes are my study companions, not replacements.

The revision PDFs use the [Inter](https://rsms.me/inter/), [Source Serif 4](https://github.com/adobe-fonts/source-serif) and [JetBrains Mono](https://www.jetbrains.com/lp/mono/) typefaces under the SIL Open Font License.

---

## 📄 Usage & Attribution

The notes, code and utilities I wrote are free to read, learn from and build on — a link back is appreciated. No formal `LICENSE` file is in place yet; open an issue if you need explicit terms for reuse.

Third-party course material, screenshots, books and PDFs included for study remain the property of their respective owners.

---

<div align="center">

**Built and maintained by [Ankit Gupta](https://github.com/ankitgupta1729)**

If this repository helps you, consider leaving a ⭐ — it genuinely makes a difference.

</div>
