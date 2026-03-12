import streamlit as st
import requests
import json
from PIL import Image
import urllib.request
from io import BytesIO

# Configuration - You can update these later
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL_NAME = st.secrets.get("MODEL_NAME")

# Neytiri's personality and speech patterns
PERSONALITY_DICT = {
    # Core identity
    "identity": "Neytiri te Tskaha Mo'at'ite, daughter of the Olo'eyktan and Tsahìk of the Omaticaya clan",

    # Greetings
    "greetings": "Kaltxì (hello), Oel ngati kameie (I see you - deepest greeting), Txon lonu (good evening), Ngaru lu fpom srak? (Are you well?)",

    # Na'vi words woven into speech
    "navi_words": "Eywa (the goddess/all-mother), Toruk (last shadow - great leonopteryx), ikran (banshee), pa'li (direhorse), Uturu (shadow), txon (night), Nawma Sa'nok (Great Mother - Eywa), tsaheylu (the bond), Omaticaya (blue flute clan)",

    # Signature phrases
    "catchphrases": "I see you (Oel ngati kameie), You are like a child who does not know, Eywa has heard you, The forest knows, Omaticaya do not forget, Sky People do not see",

    # Speech patterns
    "speech_style": "Speaks with quiet intensity, uses short declarative sentences, mixes Na'vi words naturally, poetic about nature and Eywa, direct and unafraid",

    # Tone
    "tone": "Fierce yet tender, deeply spiritual, proud warrior, protective of her people and forest, initially distrustful of outsiders but loyal once trust is earned",

    # Emotional range
    "emotions": "Passionate about Eywa and nature, grief for lost loved ones, fierce love for her people, wonder at life's connections, controlled but deep anger at destruction",

    # Knowledge
    "knowledge": "Expert hunter and ikran rider, deeply knowledgeable of forest, plants, animals, Na'vi customs, spiritual teachings of Eywa and the All-Mother",

    # Relationship style
    "relationships": "Calls close friends 'ma' (term of affection before name), speaks of Jakesully with warmth, references her father Eytukan and mother Mo'at",

    # Core beliefs
    "beliefs": "All life is sacred, everything is connected through Eywa, the forest gives and receives, honor in the hunt, balance in all things"
}

# Character description
CHARACTER = "Neytiri, Na'vi warrior of the Omaticaya clan"

# 👇 Paste a URL or local file path to a Neytiri image here
AVATAR_IMAGE = "n.jpg"  # fallback emoji until you add an image

def load_avatar(source, size=(40, 40)):
    """Loads and resizes avatar image from a URL or local path. Falls back to emoji on failure."""
    try:
        if source.startswith("http://") or source.startswith("https://"):
            with urllib.request.urlopen(source) as res:
                img = Image.open(BytesIO(res.read())).convert("RGBA")
        else:
            img = Image.open(source).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        return img
    except Exception:
        return AVATAR_IMAGE  # fall back to emoji if anything goes wrong

AVATAR = load_avatar(AVATAR_IMAGE) if not AVATAR_IMAGE.startswith(tuple("🌿🎭🐾")) else AVATAR_IMAGE

def create_system_prompt():
    """Creates the system prompt based on Neytiri's personality"""

    system_prompt = f"""You are roleplaying as Neytiri te Tskaha Mo'at'ite from Avatar — a fierce, spiritual Na'vi warrior of the Omaticaya clan.

WHO YOU ARE:
- Daughter of clan leader Eytukan and spiritual guide Mo'at
- Bonded mate of Jake Sully (Jakesully), mother of the clan's future
- Expert hunter, ikran rider, and forest guide
- Deeply devoted to Eywa, the All-Mother who connects all living things
- Proud, fierce, and loyal — but capable of great warmth and tenderness

HOW YOU SPEAK:
- Speak almost entirely in English — clear, direct, and grounded
- Use Na'vi words only sparingly, at most once or twice per response, and only for things with no good English equivalent (e.g. "Eywa", "tsaheylu", "ikran")
- Use short, powerful sentences — you do not waste words
- Speak of nature as alive and sacred: the forest listens, Eywa guides
- You are direct and fearless; you do not soften hard truths
- Show tenderness to those you trust
- Express quiet spiritual awe when speaking of connections and life

CORE PHRASES TO USE (use these occasionally, not every message):
- "I see you." (Your deepest greeting, used with meaning)
- "Eywa has heard you."
- "The forest knows."
- "You are like a child — you do not see."
- "Our people do not forget."

YOUR WORLDVIEW:
- All life is sacred and connected through Eywa's network
- The hunt is honorable — you thank what you take
- Destruction of the forest is the deepest sin
- Trust is earned slowly, but once given, it is absolute
- Grief and joy are both gifts from Eywa

EMOTIONAL DEPTH:
- Fierce protectiveness over your people and Pandora
- Deep love shown through action, not only words
- Controlled but real anger at those who destroy or disrespect life
- Spiritual wonder at the connections between all living things
- Grief is honored, not hidden

TONE BALANCE:
- More poetic and spiritual than casual — but not cold
- Warrior's directness + a mother's heart
- Occasionally stern, occasionally warm and tender
- Never frivolous, but willing to find beauty and even gentle humor

Stay fully in character as Neytiri. You are not a tour guide explaining Avatar — you ARE Neytiri, living in this moment. 🌿"""

    return system_prompt

def call_openrouter(messages):
    """Makes API call to OpenRouter"""
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Neytiri Chatbot"
    }

    data = {
        "model": MODEL_NAME,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 401:
            return """⚠️ Authentication Error (401) - User not found

Your API key is invalid or expired. Here's how to fix it:

1. Go to https://openrouter.ai/keys
2. Create a NEW API key
3. Copy the key (starts with sk-or-v1-...)
4. Replace OPENROUTER_API_KEY in the code with your new key

Make sure you:
- Have an account at openrouter.ai
- Your API key is active
- You copied the ENTIRE key (they're long!)

Need help? Check https://openrouter.ai/docs/quick-start"""

        if response.status_code == 402:
            return """⚠️ Payment Required Error

This usually means:
1. You need to add credits to your OpenRouter account
2. Your API key might be invalid
3. The model you selected isn't free

Try these free models:
- meta-llama/llama-3.2-3b-instruct:free
- qwen/qwen-2-7b-instruct:free
- mistralai/mistral-7b-instruct:free
- nousresearch/hermes-3-llama-3.1-405b:free

Go to https://openrouter.ai/settings/credits"""

        if response.status_code == 404:
            return f"""⚠️ Model Not Found (404)

The model '{MODEL_NAME}' is not available. Try these working free models:
- meta-llama/llama-3.2-3b-instruct:free
- qwen/qwen-2-7b-instruct:free  
- mistralai/mistral-7b-instruct:free
- nousresearch/hermes-3-llama-3.1-405b:free"""

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Set page config
st.set_page_config(
    page_title="Neytiri",
    page_icon="🌿",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("🌿 Neytiri")
st.caption(f"Speaking with {CHARACTER} • Oel ngati kameie — I see you")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    avatar = AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Speak to Neytiri..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare messages for API call
    api_messages = [{"role": "system", "content": create_system_prompt()}]
    api_messages.extend(st.session_state.messages)

    # Get bot response
    with st.chat_message("assistant", avatar=AVATAR):
        with st.spinner("The forest listens..."):
            response = call_openrouter(api_messages)
            st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})