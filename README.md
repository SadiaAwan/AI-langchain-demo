# AI LangChain Agents Project

This project demonstrates various use cases and functionality in LangChain through practical agent examples.
Anotherwards each agent has a structures system prompt and solves a specific real-world problem.

---

## Project Overview

The project demostrates:

- Agent architecture using LangChain
- Structured system prompts
- Tool usuage
- File handling
- Practical AI problem solving

the three agents included:

1. CV Match Agent
2. Web Reader Agent
3. Study Planner Agent

---
 
# 🧠 Agent 1 - CV Match Agent

## Purpose
Analyzes a CV against a job description and evaluates the match.

## Functionality
- Extracts skills from both documents
- Calculates a realistic match score
- Identifies matching skills
- Identifies missing skills
- Provides improvement recommendations

## Required query_name.filter(d => d.column === 'value')
Place these files in the project root:

- `cv.txt`
- `job.txt`

### Example cv.txt

```
Sadia Awan
Junior Backend Developer

Skills:
Python
Flask
SQL
Docker
Git
```

### Example jobb.txt

```
Backend Developer

Required Skills:
Python
Flask
SQL
Docker
AWS
```

## Run the agent

```bash
uv run python cv_match_agent.py
```

---

# 🌐 Agent 2 – Web Reader Agent

## Purpose
Reads and analyzes content from a webpage.

## Functionality
- Fetches webpage content
- Summarizes text
- Extracts key topics
- Presents structured insights

## Run the agent

```bash
uv run python web_reader_agent.py
```

Enter a URL when prompted.

Example:

```
https://en.wikipedia.org/wiki/Large_language_model
```

---

# 📚 Agent 3 – Study Planner Agent

## Purpose
Breaks down a learning goal into measurable milestones and a structured study plan.

## Functionality
- Identifies required competencies
- Creates milestones
- Builds weekly study plan
- Suggests practical exercises

## Run the agent

```bash
uv run python study_planner_agent.py
```

Example input:

```
Learn Python for backend development in 3 months
```

---


# 🏗 Project Structure

```
AI-langchain-demo/
│
├── cv_match_agent.py
├── web_reader_agent.py
├── study_planner_agent.py
├── cv.txt
├── jobb.txt
├── util/
└── README.md
```

---

# 🛠 Technologies Used

- Python
- LangChain
- LangGraph
- Requests
- BeautifulSoup

---

# 🎯 Learning Outcomes

This project demonstrates:

- How to design structured system prompts
- How to build multi-purpose AI agents
- How to integrate tools
- How to handle real-world tasks using LLMs
- How to structure a modular AI project

---

# 🚀 Conclusion

The project successfully implements three independent AI agents with different functionality.  
Each agent demonstrates a practical use case and follows structured prompt engineering principles.


## Getting Started

### Prerequisites
- Python 3.13
- Ollama server with access to Llama models

### Setup

1. Clone the project
2. Create a virtual environment and install dependencies:
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Create a `.env` file with your configuration:
```bash
OLLAMA_BASE_URL=http://nackademin.icedc.se
OLLAMA_BEARER_TOKEN=your-bearer-token-here
```

### Running Examples

Make sure the virtual environment is activated and run from the project root:

```bash
source .venv/bin/activate
python -m examples.agent-lecture.simple_agent
```


