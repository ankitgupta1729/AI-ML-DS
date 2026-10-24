#!/usr/bin/env bash
# Move local, untracked files into the category layout introduced in Oct 2026.
#
# The modules used to sit directly in the repo root (e.g. ./47.Coursera-...).
# They now live inside category folders (e.g. ./machine-learning/47.Coursera-...).
# `git pull` moves every *tracked* file for you, but anything git ignores
# (datasets, model weights, .venv folders, .env files, local clones) stays in
# the old folder. Run this once from the repo root after pulling:
#
#     bash tools/migrate-local-layout.sh          # dry run: shows what would move
#     bash tools/migrate-local-layout.sh --apply  # actually move the files
#
# Files that already exist at the destination are never overwritten. Old
# folders are removed only once they are empty. Re-create virtual environments
# afterwards (`uv sync` / `pipenv install`): venvs store absolute paths.
set -euo pipefail

APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1
cd "$(git rev-parse --show-toplevel)"

# old-root-folder|new-category
LAYOUT='
00.Resources|resources
01.Python|foundations
03.SQL|foundations
04.Theory|foundations
13.Decorators|foundations
45.Python-for-Everybody-University-of-Michigan-Charles-Severance-PhD|foundations
02.PySpark|data-engineering
14.Databricks|data-engineering
33.AI-Nano-Degree|machine-learning
47.Coursera-Andrew-Ng-Machine-Learning|machine-learning
48.Coursera-Andrew-Ng-Advanced-Machine-Learning|machine-learning
49.Coursera-Andrew-Ng-unsupervised-learning-recommenders-reinforcement-learning|machine-learning
50.Andrew-Ng-Course-Material|machine-learning
51.Linkedin-TensorFlow-Working-with-Images|deep-learning
52.Packt-Tensorflow-Deep-Learning-Solutions-for-Images-Will-Ballard|deep-learning
53.Convolutional-Neural-Networks-with-TensorFlow-in-Python|deep-learning
54.Deep-Learning-for-Computer-Vision-with-TensorFlow-2|deep-learning
55.Udemy-PyTorch-Deep-Learning-and-Artificial-Intelligence-by-The-Lazy-Programmer|deep-learning
56.Udemy-Introduction-to-Generative-Adversarial-Networks-with-PyTorch|deep-learning
57.Convolutional-Neural-Networks-with-Pytorch|deep-learning
58.Udemy-PyTorch-Tutorial-Neural-Networks-&-Deep-Learning-in-Python|deep-learning
59.Modern-Deep-Convolutional-Neural-Networks-with-PyTorch|deep-learning
60.Natural-Language-Processing-(NLP)-in-Python|nlp
61.GetFreeCourses.Co-Udemy-Data-Science-Transformers-for-Natural-Language-Processing|nlp
05.Code|generative-ai
17.OpenCode|generative-ai
20.LlamaIndex|generative-ai
22.LLM_Fine_Tuning|generative-ai
23.LangChain|generative-ai
24.LangChain2|generative-ai
25.Claude-Code-Deep-Dive|generative-ai
26.LangGraph|generative-ai
27.Agentic-AI-Deliver-a-successful-chatbot-POC-with-LangGraph|generative-ai
28.Building-Scalable-AI-Chatbot-with-Memory-using-LangChain-and-Streamlit|generative-ai
29.Build-Your-AI-Agent-with-LangGraph|generative-ai
30.GenAI-AgenticAI-PromptEngineering-ChatGPT|generative-ai
32.Generative-AI-for-Everyone|generative-ai
40.AI-Agent-Course-Build-a-Language‑Learning-Agent-with-OpenAI-LangGraph-Ollama-MCP|generative-ai
46.Udemy-RAG-Fine_Tuning-LLM|generative-ai
31.CICD-Pipeline|mlops
34.Fundamentals-of-Google-Cloud-Udemy|mlops
35.Deploying-Machine-Learning-Models-in-Production|mlops
36.Introduction-to-Machine-Learning-in-Production-DeepLearningAI|mlops
39.mlflow|mlops
43.Machine-Learning-Engineering-for-Production-MLOps-and-Specialization|mlops
44.Machine-learning-modeling-pipelines-in-production|mlops
09.Tools|dev-tools
10.Git|dev-tools
11.Docker|dev-tools
12.Debugger|dev-tools
15.uv_demo|dev-tools
21.pipenv-course|dev-tools
37.Youtube-UV-A-Faster-All-in-One-Package-Manager-to-Replace-Pip-and-Venv|dev-tools
38.Stop-Using-Pip-This-New-Tool-is-100x-Faster-(UV-Tutorial)|dev-tools
19.Go|programming-languages
41.YouTube-Go-Programming-Full-Course-Tech-with-Tim|programming-languages
42.Learn-Go-With-This-ONE-Project-Tech-with-Tim|programming-languages
06.Interview-Preparation|career
07.Blogs|career
08.YouTube|career
16.Improvements|career
18.Utilities|projects
'

moved=0
while IFS='|' read -r old cat; do
  [[ -z "$old" || ! -d "$old" ]] && continue
  new="$cat/$old"
  if [[ "$old" == "00.Resources" ]]; then new="resources"; fi
  while IFS= read -r -d '' f; do
    rel="${f#"$old"/}"
    dest="$new/$rel"
    if [[ -e "$dest" || -L "$dest" ]]; then
      echo "skip (exists): $dest"
      continue
    fi
    echo "move: $f -> $dest"
    moved=$((moved + 1))
    if (( APPLY )); then
      mkdir -p "$(dirname "$dest")"
      mv "$f" "$dest"
    fi
  done < <(find "$old" \( -type f -o -type l \) -print0)
  if (( APPLY )); then
    find "$old" -depth -type d -empty -delete 2>/dev/null || true
  fi
done <<< "$LAYOUT"

if (( APPLY )); then
  echo "Moved $moved file(s)."
else
  echo "Dry run: $moved file(s) would move. Re-run with --apply to move them."
fi
