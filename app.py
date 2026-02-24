import streamlit as st
from groq import Groq
import random

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="✨ Vibe Check AI", page_icon="🎲", layout="centered")

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

.stApp {
    background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a1c4fd, #c2e9fb, #d4fc79, #96e6a1);
    background-size: 400% 400%;
    animation: gradientShift 10s ease infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.fun-title {
    font-family: 'Fredoka One', cursive;
    font-size: 3.2em;
    text-align: center;
    color: #fff;
    text-shadow: 3px 3px 0px #ff6b6b, 6px 6px 0px rgba(0,0,0,0.1);
    margin-bottom: 0;
    animation: bounce 2s infinite;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}
.fun-subtitle {
    font-size: 1.1em;
    text-align: center;
    color: rgba(255,255,255,0.9);
    margin-top: 5px;
    margin-bottom: 30px;
    font-weight: 600;
}
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 30px;
    margin: 10px 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    border: 2px solid rgba(255,255,255,0.6);
}
.response-bubble {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 20px 20px 20px 4px;
    padding: 20px 24px;
    font-size: 1.15em;
    font-weight: 600;
    line-height: 1.6;
    box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    margin-top: 16px;
    animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
@keyframes popIn {
    0% { transform: scale(0.8); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
.emoji-badge {
    font-size: 3.5em;
    text-align: center;
    margin: 10px 0;
    animation: spin 0.5s ease;
}
@keyframes spin {
    0% { transform: rotate(-20deg) scale(0.5); }
    100% { transform: rotate(0deg) scale(1); }
}
.sticker-row {
    text-align: center;
    font-size: 1.8em;
    letter-spacing: 8px;
    margin: 8px 0;
}
div.stButton > button {
    background: linear-gradient(135deg, #f093fb, #f5576c) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1.3em !important;
    padding: 14px 40px !important;
    width: 100% !important;
    box-shadow: 0 6px 20px rgba(245,87,108,0.4) !important;
    transition: all 0.2s !important;
}
div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 28px rgba(245,87,108,0.5) !important;
}
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.3) !important;
    backdrop-filter: blur(10px) !important;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Config ────────────────────────────────────────────────────────────────────
BUTTONS = {
    "🎲 Random Vibe Check":   "Give me a completely random, funny, and unexpected vibe check for today. Be creative, quirky, and entertaining! Use emojis.",
    "🔮 Predict My Day":      "Predict my day in the most dramatic, over-the-top, and hilarious way possible. Make it fun and unexpected! Use emojis.",
    "😂 Tell Me a Joke":      "Tell me a really funny, clever joke. Make it original and hilarious! End with a fun emoji combo.",
    "🌈 Inspire Me":          "Give me the most ridiculously uplifting and motivational message ever. Make it dramatic, fun, and over the top! Use lots of emojis.",
    "🤔 Random Fun Fact":     "Share a super surprising, mind-blowing, and fun random fact I probably don't know. Make it exciting! Use emojis.",
    "🎭 Roast Me (Nicely)":   "Give me a super gentle, friendly, and funny roast. Nothing mean — just playful and hilarious! Use emojis.",
    "🌟 My Superpower Today": "Tell me what my random superpower is today and how I should use it. Be creative and funny! Use emojis.",
    "🍕 What Should I Eat":   "Recommend the most random and unexpected meal or snack for me right now with a hilarious reason why. Use emojis.",
}

MODELS = {
    "⚡ llama-3.3-70b (Best & Fast)": "llama-3.3-70b-versatile",
    "🚀 llama-3.1-8b (Fastest)":     "llama-3.1-8b-instant",
    "🧠 mixtral-8x7b (Creative)":    "mixtral-8x7b-32768",
}

EMOJIS = ["🎉", "🚀", "✨", "🎲", "🌈", "🔥", "💫", "🎭", "🤩", "🎪", "🦄", "🍀"]

# ─── Session State ─────────────────────────────────────────────────────────────
for key, val in [("response", None), ("current_emoji", "🎲"), ("button_count", 0), ("last_button", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Setup")
    #api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="Paste your key here...")
    api_key=st.secrets["GROQ_API_KEY"]

    st.markdown("Get free key → [console.groq.com](https://console.groq.com)")
    st.markdown("---")
    st.markdown("### 🤖 Choose Model")
    model_label = st.selectbox("", list(MODELS.keys()), label_visibility="collapsed")
    selected_model = MODELS[model_label]
    st.markdown("---")
    st.markdown("### 🎮 How to Play")
    st.markdown("1. Enter your Groq API key\n2. Pick any fun button\n3. Get a hilarious response!\n4. Keep clicking for more 😄")
    st.markdown("---")
    st.markdown("### ⚡ Why Groq?")
    st.markdown("Groq uses special **LPU chips** making AI **10x faster** than normal. You'll feel the speed instantly!")
    if st.session_state.button_count > 0:
        st.markdown("---")
        st.markdown(f"### 📊 Stats\n🎯 Presses: **{st.session_state.button_count}**")
        if st.session_state.last_button:
            st.markdown(f"🕹️ Last: **{st.session_state.last_button}**")

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="fun-title">✨ Vibe Check AI ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="fun-subtitle">Your daily dose of fun, powered by Groq ⚡🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="sticker-row">🎪 🦄 🌈 🎭 🚀 🍀</div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 👇 Pick your vibe!")

# ─── Button Handler ────────────────────────────────────────────────────────────
def handle_click(label, prompt):
    if not api_key:
        st.session_state.response = "⚠️ Please enter your Groq API key in the sidebar first!"
        st.session_state.current_emoji = "😅"
        return
    try:
        client = Groq(api_key=api_key)
        result = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "You are a super fun, witty, and entertaining AI. Keep responses under 4 sentences but make every word count! Always use emojis generously."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=1.0,
        )
        st.session_state.response = result.choices[0].message.content
        st.session_state.current_emoji = random.choice(EMOJIS)
        st.session_state.button_count += 1
        st.session_state.last_button = label
    except Exception as e:
        st.session_state.response = f"Oops! Something went wrong 😅\n\n`{str(e)}`"
        st.session_state.current_emoji = "😵"

# ─── Buttons Grid ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
for i, (label, prompt) in enumerate(BUTTONS.items()):
    with (col1 if i % 2 == 0 else col2):
        if st.button(label, key=f"btn_{i}"):
            handle_click(label, prompt)

# ─── Response Display ──────────────────────────────────────────────────────────
if st.session_state.response:
    st.markdown("---")
    st.markdown(f'<div class="emoji-badge">{st.session_state.current_emoji}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-bubble">🤖 {st.session_state.response}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="text-align:center;color:rgba(255,255,255,0.9);font-weight:700;">Press another button for more fun! 🎉</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="font-size:3em;">👆</div>
        <div style="font-size:1.1em;font-weight:700;color:#555;">Pick a button above to get started!</div>
        <div style="color:#888;margin-top:8px;">Your fun AI response will appear right here ✨</div>
    </div>
    """, unsafe_allow_html=True)
    