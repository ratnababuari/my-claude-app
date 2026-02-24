import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(page_title="My Gemini AI App", page_icon="✨")
st.title("✨ My Personal Gemini AI")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    model_choice = st.selectbox("Choose Model", [
        "gemini-2.0-flash",        # ✅ Best free option - fast & capable
        "gemini-2.0-flash-lite",   # ✅ Lightest & fastest
        "gemini-2.5-flash",        # ✅ Most powerful free model
    ])
    
    system_prompt = st.text_area(
        "System Prompt (optional)",
        placeholder="E.g. You are a helpful assistant who replies concisely.",
        height=100
    )
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("Get your free key at [aistudio.google.com](https://aistudio.google.com)")

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
        st.error("⚠️ Please enter your Gemini API key in the sidebar.")
    else:
        # Configure Gemini
        genai.configure(api_key=api_key)

        generation_config = genai.GenerationConfig(
            max_output_tokens=1024,
            temperature=0.7,
        )

        model = genai.GenerativeModel(
            model_name=model_choice,
            generation_config=generation_config,
            system_instruction=system_prompt if system_prompt else None
        )

        # Add and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build chat history in Gemini format
        gemini_history = []
        for msg in st.session_state.messages[:-1]:
            gemini_history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            })

        # Get Gemini response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chat = model.start_chat(history=gemini_history)
                    response = chat.send_message(prompt)
                    reply = response.text
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")