from langgraph.prebuilt import create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
import json
import uuid
from dotenv import load_dotenv
from agent_tools.iac_operator import run_terraform_operation_tool
from agent_tools.terraform_file_manager import (
    read_tf_file_tool, list_tf_workspace_files_tool, generate_tf_file_tool
)
from assistant_template import template
import streamlit as st
import os


from dotenv import load_dotenv
import os

load_dotenv()

memory = MemorySaver()


import re

def try_pretty_print(response):
    try:
        parsed = json.loads(response)
        st.json(parsed)  # Streamlit will pretty-print JSON
        return True
    except json.JSONDecodeError:
        # Try to extract JSON from inside the message using regex
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                st.json(parsed)
                return True
            except json.JSONDecodeError:
                pass
        return False


def get_llm_response(ai_executor, message1, config, old_messages):
    """Function to get LLM response using agent executor"""
    input_message = HumanMessage(content=message1)
    response1 = ""
    for event in ai_executor.stream({"messages": old_messages + [input_message]}, config, stream_mode="values"):
        response1 = event
    return response1


tools_list = [generate_tf_file_tool, read_tf_file_tool, list_tf_workspace_files_tool, run_terraform_operation_tool]

if st.session_state.get('openai_api_key') is None:
    local_env_api_key = os.getenv("OPENAI_API_KEY")
    st.session_state['openai_api_key'] = local_env_api_key

llm = ChatOpenAI(model="gpt-4o",
                temperature=0,  # Lower for factual accuracy  # Larger context window
                api_key=st.session_state['openai_api_key'],
)


chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("placeholder", "{messages}"),
])


agent_executor = create_react_agent(
    model=llm,
    tools = tools_list,
    debug=True,
    prompt=chat_prompt,
    checkpointer=memory,
)

def handle_assistant_response(response1, role):
    """Function to handle the assistant's response"""
    if role == "user":
        st.markdown(response1)
    elif role == "assistant":
        if isinstance(response1, dict) and response1.get("type") == "terraform_plan":
            st.markdown("### ☁️ Terraform Plan Summary")
            st.success(response1["summary"])
            with st.expander("📄 Terraform Plan Details"):
                st.code(response1["raw_plan"], language="bash")
        elif try_pretty_print(response1):
            pass
        elif "interface" in response1 or "ip address" in response1 or "Plan:" in response1:
            st.markdown("### ☁️ Terraform Plan Summary")
            st.success("Terraform Plan")
            st.markdown("#### Terraform Plan Details")
            with st.expander("📄 Terraform Plan Details"):
                st.code(response1, language="bash")
        elif "Terraform code" in response1:
            st.markdown("### ☁️ Terraform Code")
            st.success("Terraform Code")
            st.markdown("#### Terraform Code Details")
            with st.expander("📄 Terraform Code Details"):
                st.code(response1, language="bash")
        elif "Terraform output" in response1:
            st.markdown("### ☁️ Terraform Output")
            st.success("Terraform Output")
            st.markdown("#### Terraform Output Details")
            with st.expander("📄 Terraform Output Details"):
                st.code(response1, language="bash")
        elif "Terraform files" in response1:
            st.markdown("### ☁️ Terraform Workspace")
            st.success("Terraform Workspace")
            st.markdown("#### Terraform Workspace Details")
            with st.expander("📄 Terraform Details"):
                st.code(response1, language="bash")
        elif "Error occurred" in response1 or "Traceback" in response1:
            st.error(response1)
        else:
            st.markdown(response1 if isinstance(response1, str) else json.dumps(response1))

st.title("🛠️ IAC & ReAct Assistant")
st.write("Run cloud IAC operations with agents and get insights using AI!")

if st.session_state.get('conversation_history') is None:
    st.session_state['conversation_history'] = []
    st.session_state['all_messages'] = []

if st.session_state.get('thread_id') is None:
    st.session_state['thread_id'] = str(uuid.uuid4())
    st.session_state['config'] = {"configurable": {"thread_id": st.session_state['thread_id']}}

for message in st.session_state.get('conversation_history', []):
    with st.chat_message(message["role"]):
        handle_assistant_response(message["content"], message["role"])

question = st.chat_input('Ask a question on this topology')
if question:
    st.chat_message("user").markdown(question)
    st.session_state['conversation_history'].append({"role": "user", "content": question})

    placeholder = st.empty()
    placeholder.text("Thinking...")
    with st.spinner("Fetching response from model..."):
        # bot_message = agent_executor.invoke({"messages": [HumanMessage(content=question)]}, config=st.session_state['config'])
        bot_message = get_llm_response(agent_executor,question,st.session_state['config'],
                                    st.session_state['all_messages'])
        # print(bot_message)

        # response = bot_message['output']
        st.session_state['all_messages'] = bot_message["messages"]
        response = bot_message["messages"][-1].content
    placeholder.empty()  # Clear the placeholder
    with st.chat_message("assistant"):
        if response:
            handle_assistant_response(response, "assistant")
        else:
            st.error("No response from the assistant.")
    
    st.session_state['conversation_history'].append({"role": "assistant", "content": response})
    
            
    

