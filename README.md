# 🧠 Goal Decomposer Agent

A terminal-based AI agent that breaks down high-level goals into actionable steps using **Groq** or **OpenAI**, and then **evaluates** the generated plan using **Judgeval**'s `FaithfulnessScorer`.

---

## 📦 Features

- ✅ Goal decomposition using **Groq (LLaMA 3.3 70B)** or **OpenAI GPT-4.1**
- ✅ Terminal prompt + automatic JSON step formatting
- ✅ Evaluates output with `FaithfulnessScorer`
- ✅ Traced and logged with **Judgeval**
- ✅ Modular and easy to extend with other models

---

## 📁 Project Structure

```
goal-decomposer-agent/
├── main.py                            # CLI entry script
├── .env                               # Store API keys securely
├── requirements.txt                   # Python dependencies
└── src/
    └── agents/
        └── goal_decomposer.py        # Agent + evaluation logic
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/goal-decomposer-agent.git
cd goal-decomposer-agent
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
JUDGMENT_API_KEY=your_judgment_api_key
JUDGMENT_ORG_KEY=your_judgment_org_key
```

---

## 🚀 Running the Program

To launch the goal decomposer:

```bash
python main.py
```

You’ll be asked to:

- Select the API provider (Groq or OpenAI)
- Enter your goal (e.g. "I want to become an AI Engineer")
- Enter a timeframe (e.g. "6 months")

### 🧠 Sample Output

```json
[
  {
    "step": "Learn Python basics",
    "priority": "High",
    "duration": "2 weeks",
    "resources": ["https://realpython.com", "Automate the Boring Stuff with Python"],
    "depends_on": []
  },
  {
    "step": "Study Machine Learning fundamentals",
    "priority": "High",
    "duration": "4 weeks",
    "resources": ["Coursera ML by Andrew Ng", "Hands-On ML with Scikit-Learn"],
    "depends_on": ["Learn Python basics"]
  }
]
```

---

## 🧪 Evaluation Logic

After decomposition, the result is **scored for faithfulness** using:

```python
retrieval_context = [
  "To become an AI Engineer, you typically need to learn Python, machine learning, deep learning, and build projects."
]
```

Evaluation is run using:

```python
FaithfulnessScorer(threshold=0.5)
```

And handled by:

```python
JudgmentClient.assert_test(...)
```

You’ll see:

```bash
✅ Evaluation passed successfully!
```

---

## 🛠️ Tech Stack

| Tool         | Role                         |
|--------------|------------------------------|
| Groq API     | LLM backend (LLaMA 3.3 70B)  |
| OpenAI       | LLM backend (GPT-4.1)        |
| Judgeval     | Scoring, tracing, evaluation |
| dotenv       | Env config loader            |

---


---

## 🤝 Contributing

Want to improve this? PRs are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feature/new-idea`
3. Commit changes: `git commit -am 'Add something cool'`
4. Push: `git push origin feature/new-idea`
5. Open a Pull Request

---

## 👨‍💻 Author

Developed with 🤔 by [Aakash Reddy Nuthalapati](https://github.com/aakash-73)

---

