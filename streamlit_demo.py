import time
import streamlit as st
from openai import AzureOpenAI
from dotenv import dotenv_values

def load_config():
    try:
        return dotenv_values(verbose=True)
    except Exception as e:
        st.error(f"Error loading environment variables: {e}")
        return None

def load_prompt(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        st.error(f"Error reading prompt file: {e}")
        return ""

def create_client(config):
    try:
        return AzureOpenAI(
            azure_endpoint=config["AZURE_OPENAI_ENDPOINT"],
            api_key=config["AZURE_OPENAI_API_KEY"],
            api_version="2024-05-01-preview"
        )
    except Exception as e:
        st.error(f"Error creating AzureOpenAI client: {e}")
        return None

def create_assistant(client, prompt):
    try:
        return client.beta.assistants.create(
            model="gpt-4o",  # replace with model deployment name.
            instructions=prompt,
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": ["vs_q8bLBYwgc76ug39g4HfVnhvi"]}},
            temperature=1,
            top_p=1
        )
    except Exception as e:
        st.error(f"Error creating assistant: {e}")
        return None

def main():
    with st.columns(5)[2]:
        logo_path = "next-step-logo.png"  
        st.image(logo_path, caption="Next-Step AI", use_column_width=True)

    config = load_config()
    if not config:
        return

    client = create_client(config)
    if not client:
        return

    prompt = load_prompt("prompt.txt")
    if not prompt:
        return

    assistant = create_assistant(client, prompt)
    if not assistant:
        return

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi There! Welcome to Next-Step.AI. I'm here to help you think about what's next after High School.  What's your name?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Button to submit the question
    if user_question := st.chat_input():
        st.chat_message("user").write(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        # Create a thread
        if "thread_id" not in st.session_state:
            thread = client.beta.threads.create()
            st.session_state["thread_id"] = thread.id
        else:
            thread = client.beta.threads.retrieve(thread_id=st.session_state.thread_id)

        # Add a user question to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question
        )

        # Run the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Looping until the run completes or fails
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            st.session_state.messages.append({"role": "assistant", "content": messages.data[0].content[0].text.value})
            st.chat_message("assistant").write(messages.data[0].content[0].text.value)
        else:
            st.write("The run did not complete successfully.")

if __name__ == "__main__":
    main()