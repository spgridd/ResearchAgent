import streamlit as st
from vertexai.preview.reasoning_engines import AdkApp
from agent.agent import create_agent

st.set_page_config(page_title="Research Agent", layout="centered")
st.title("Research Agent")

if "use_long_agent" not in st.session_state:
    st.session_state.use_long_agent = False
if "history" not in st.session_state:
    st.session_state.history = []

new_toggle = st.toggle("Create Longer Reports", value=st.session_state.use_long_agent)
if new_toggle != st.session_state.use_long_agent:
    st.session_state.use_long_agent = new_toggle

selected_agent = create_agent(long=st.session_state.use_long_agent)
app = AdkApp(agent=selected_agent)

for user_msg, assistant_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(assistant_msg)

prompt = st.chat_input("Ask your research question here...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            final_response = ""

            for event in app.stream_query(user_id="testuser", message=prompt):
                content = (
                    event.get("content", {})
                         .get("parts", [{}])[0]
                         .get("text", "")
                ).strip()

                agent = event.get("author", "")
                if content and agent == "SynthesizerAgent":
                    final_response = content

        st.markdown(final_response or "*No response received.*")

    st.session_state.history.append((prompt, final_response))
