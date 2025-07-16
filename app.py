import streamlit as st
from vertexai.preview.reasoning_engines import AdkApp
from langfuse import Langfuse

from agent.agent import create_agent

langfuse = Langfuse()

st.set_page_config(page_title="Research Agent", layout="centered")
st.title("Research Agent")

use_long_agent = st.toggle("Create Longer Reports", value=False)

selected_agent = create_agent(long=True) if use_long_agent else create_agent(long=False)
app = AdkApp(agent=selected_agent)

if "history" not in st.session_state:
    st.session_state.history = []

if prompt := st.chat_input("Ask your research question here..."):
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            trace = langfuse.trace(name="research_query", input={"prompt": prompt})

            final_response = ""
            for event in app.stream_query(user_id="testuser", message=prompt):
                content = (
                    event.get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                ).strip()

                agent = event.get("author", "")

                if content:
                    if agent == "SynthesizerAgent":
                        final_response = content

        st.markdown(f"**Answer:**\n*{final_response}*")

        trace.update(output={"final_response": final_response})

        st.session_state.history.append((prompt, final_response))

for user_msg, final_response in st.session_state.history[:-1]:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(f"**Answer:**\n*{final_response}*")
