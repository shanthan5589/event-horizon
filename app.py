import streamlit as st
import requests

st.set_page_config(page_title="Black Hole RAG", page_icon="🕳️", layout="centered")
st.title("🌌 Event Horizon")
st.caption("Ask anything about black holes, powered by Quanta Magazine articles")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about black holes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching articles..."):
            response = requests.post(
                "http://localhost:8000/query",
                json={"question": prompt}
            )
            data = response.json()
            answer = data["answer"]
            sources = data["sources"]

        st.markdown(answer)

        if sources:
            st.markdown("**Sources:**")
            for key in sources:
                s = sources[key]
                st.markdown(f"- [{s['title']}]({s['url']})")

    full_response = answer + "\n\n**Sources:** " + ", ".join([sources[k]['title'] for k in sources])
    st.session_state.messages.append({"role": "assistant", "content": full_response})