import time
from openai import AzureOpenAI
from dotenv import dotenv_values
import streamlit as st


with st.columns(5)[2]:
    logo_path = "next-step-logo.png"  
    st.image(logo_path, caption="Next-Step AI", use_column_width=True)

# Load environment variables
config = dotenv_values(verbose=True)


client = AzureOpenAI(
azure_endpoint = config["AZURE_OPENAI_ENDPOINT"],
  api_key= config["AZURE_OPENAI_API_KEY"],
  api_version="2024-05-01-preview"
)

prompt = ""
with open("prompt.txt", "r") as file:
    prompt = file.read()


assistant = client.beta.assistants.create(
  model="gpt-4o", # replace with model deployment name.
  instructions=prompt,
  tools=[{"type":"file_search"}],
  tool_resources={"file_search":{"vector_store_ids":["vs_q8bLBYwgc76ug39g4HfVnhvi"]}},
  temperature=1,
  top_p=1
)

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
        # data = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
        # extracted_data = [{'role': item.role, 'content': [content_item.text.value for content_item in item.content]} for item in data]
        # extracted_data.reverse()
        # extracted_data.insert(0, [{"role": "assistant", "content": "How can I help you?"}])

    
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
        # st.write(messages.data[0].content[0].text.value)
    else:
        st.write("The run did not complete successfully.")