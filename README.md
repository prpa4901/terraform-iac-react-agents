# terraform-iac-react-agents
# 🛠️ AI Terraform ReAct Assistant

This project is a **Streamlit-based AI assistant** powered by LangGraph’s `create_react_agent`, OpenAI's GPT-4o, and LangChain tools. It enables natural language-driven Infrastructure-as-Code (IaC) operations using **Terraform**.

Ask the assistant to:
- 🔧 Generate Terraform files
- 📄 Read or list Terraform files in the workspace
- 💡 Plan Terraform infrastructure changes
- 🚀 Apply those changes conditionally
- ✅ Understand and explain plan outputs interactively

---

## ✨ Features

- 🧠 ReAct agent built using `LangGraph` + `ChatOpenAI`
- 📁 Terraform file generation, listing, reading
- 📊 Runs `terraform plan` and parses output into summaries
- ✅ Confirms with user before `terraform apply`
- 💬 Friendly conversational UI powered by Streamlit
- 🧠 Supports multi-turn conversations with memory and threading

---

## 📦 Tools Used

| Tool Name | Description |
|-----------|-------------|
| `generate_tf_file_tool` | Generates Terraform code from natural language |
| `read_tf_file_tool` | Reads specific Terraform files from the workspace |
| `list_tf_workspace_files_tool` | Lists all `.tf` files in the current working directory |
| `run_terraform_operation_tool` | Executes `terraform init`, `plan`, or `apply` as requested |

---

## 🚀 How It Works

1. You ask: _"Create a VPC with 2 subnets in us-east-1"_
2. Agent uses `generate_tf_file_tool` to write code
3. You say: _"Can you plan it?"_
4. Agent runs `terraform plan` and explains results
5. You approve → Agent applies the infrastructure!

---

## 🧰 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/terraform-agent.git
   cd terraform-agent

    Set up a Python virtual environment

python3 -m venv venv
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Set environment variables

Create a .env file:

OPENAI_API_KEY=your_openai_key_here

Run the app

    streamlit run app.py

🧪 Example Prompts

    💬 "Create a VPC with 3 public subnets and 2 private ones"
    💬 "Run a terraform plan and summarize it"
    💬 "What are the files in my Terraform workspace?"
    💬 "Apply the current plan if it's safe"

📂 File Structure

.
├── app.py                        # Main Streamlit app
├── assistant_template.py        # LLM system prompt
├── agent_tools/
│   ├── terraform_file_manager.py     # Tools to manage .tf files
│   └── iac_operator.py               # Tool to run Terraform commands
├── requirements.txt
├── .env
└── README.md

🧠 Built With

    LangGraph

    LangChain

    OpenAI

    Streamlit

    Terraform CLI

📌 Future Ideas

    🔒 Vault integration for secure secret management

    🧾 Versioning of generated Terraform

    📦 GCP/Azure multi-cloud support

    📸 Terraform state visualization

    🤝 Git integration for PR-based apply

🤝 Contributing

Feel free to fork, clone, or open issues and PRs!
📜 License

MIT License — feel free to use, modify, and share.