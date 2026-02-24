import streamlit as st
import anthropic

# Page config
st.set_page_config(page_title="My Claude AI App", page_icon="🤖")
st.title("🤖 My Personal Claude AI")

# Sidebar for API key input
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Claude API Key", type="password")
    st.markdown("Get your key at [console.anthropic.com](https://console.anthropic.com)")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    if not api_key:
        st.error("Please enter your API key in the sidebar.")
    else:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get Claude's response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",  # Free-friendly model
                    max_tokens=1024,
                    messages=st.session_state.messages
                )
                reply = response.content[0].text
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})