import streamlit as st
from utils import ingestion, RagChain
import os

def format_chat_history(messages):
    if not messages:
        return []

    formatted = []
    for i in range(0, len(messages), 2):
        if i + 1 < len(messages):
            user_msg = messages[i]["content"]
            assistant_msg = messages[i + 1]["content"]
            formatted.append(f"Human: {user_msg}\nAssistant: {assistant_msg}")

    return "\n\n".join(formatted)

def main():
    st.header("Chat with PDF")
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    if pdf:
        temp_path = os.path.join("temp", pdf.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_path, 'wb') as f:
            f.write(pdf.read())

        st.session_state.vectorstore = ingestion(temp_path)

        os.remove(temp_path)
        st.success("PDF processed successfully!")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know about the PDF?"):
        if st.session_state.vectorstore is None:
            st.error("Please upload a PDF first!")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        chat_history = format_chat_history(st.session_state.messages[:-1])

        with st.chat_message("assistant"):
            response = RagChain(prompt, st.session_state.vectorstore, chat_history)
            st.markdown(response.content)

        st.session_state.messages.append({"role": "assistant", "content": response.content})


if __name__ == "__main__":
    main()
