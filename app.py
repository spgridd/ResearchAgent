import streamlit as st
from agent.agent import root_agent
from vertexai.preview.reasoning_engines import AdkApp

app = AdkApp(agent=root_agent)

st.set_page_config(page_title="Research Agent", layout="centered")
st.title("Research Agent")

if "history" not in st.session_state:
    st.session_state.history = []

if "full_transcript" not in st.session_state:
    st.session_state.full_transcript = []

if prompt := st.chat_input("Ask your research question here..."):
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        trace_box = st.empty()
        final_box = st.empty()

        current_step = ""
        all_steps = []
        final_response = ""

        with st.spinner("Thinking..."):
            for event in app.stream_query(user_id="testuser", message=prompt):
                content = (
                    event.get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                ).strip()

                if content and content not in [".", "…", "..."]:
                    current_step += content

                    if content.endswith((".", "!", "?")):
                        step = current_step.strip()
                        all_steps.append(step)
                        current_step = ""

                        trace_box.markdown("**Reasoning steps:**\n" + "\n".join(
                            [f"- {s}" for s in all_steps]
                        ))
                        final_response = step

        final_box.markdown(f"**Answer:**\n*{final_response}*")

        st.session_state.history.append((prompt, all_steps, final_response))

for user_msg, _, _ in st.session_state.history[:-1]:
    with st.chat_message("user"):
        st.markdown(user_msg)
