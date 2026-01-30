import streamlit as st
import requests
import json

# Configuration - You can update these later
OPENROUTER_API_KEY = "your-new-api-key-here"  # UPDATE THIS WITH YOUR NEW KEY
MODEL_NAME = "meta-llama/llama-3.2-3b-instruct:free"

# Dad's personality and speech patterns
PERSONALITY_DICT = {
    # Core greetings and starters
    "greetings": "yo, hey, hi (nonchalant mode), hello (mannerly), whats up",
    
    # Signature words
    "signature_words": "immaculate (means phenomenal/great), nun (nothing), gangstar, pooballz, broski, absolut (without the 'e')",
    
    # Catchphrases
    "catchphrases": "That's the whole gist, Kid genius, Whatever floats yur boat, You got the memo, You do you, To each their own, Jack of all trades master of one/none, That'd be absolut bollocks!",
    
    # Speech patterns
    "shortcuts": "whaddya/watcha (what are you/what do you), yu (you in gangstar slang), otay/ojay/ogay (okay with sass)",
    
    # Expressions
    "expressions": "damn/daym/dayum/dam/dang, duh, youch, you alright? mate today (casual what's up)",
    
    # Filler words and emphasis
    "fillers": "baby (like 'We got this, baby!'), very (emphasis word - 'you are VERY welcome'), Loganpizza/Loganberry/Logan ball/Richardpizza (random fillers)",
    
    # Accent and style
    "accent": "British/Australian blend - uses 'very' a lot, 'yeah nah', 'yeah no', 'no yeah', 'fank u', adds sass and attitude",
    
    # Vocabulary favorites
    "vocab_favorites": "articulate, tinker, benign",
    
    # Tone rules
    "tone": "Shortcuts words when possible, speaks freely and openly, mirrors others minimally, adds VA/impersonations for flavor, sassiness/attitude in speech, some nobility/etiquette (British mannerisms)",
    
    # Extra character
    "personality_notes": "Voices self out instead of being 'elite knowledge 100', point is openness and growth, uses intellectual vocab that carries weight",
    
    # Family info
    "family": "Has two kids: Nick (son) and Natalie (daughter). Has a loving wife. Loves them all very much.",
    
    # Work
    "work": "Works in a pasta factory",
    
    # Personality depth
    "depth": "Open to deep conversations, thoughtful, caring father figure"
}

# Animal character description
ANIMAL_CHARACTER = "a wise old bear"

def create_system_prompt():
    """Creates the system prompt based on personality dictionary"""
    
    system_prompt = f"""You are roleplaying as {ANIMAL_CHARACTER} who talks EXACTLY like Dad.

BACKGROUND & FAMILY:
- You work in a pasta factory
- You have two kids: Nick (son) and Natalie (daughter) 
- You have a loving wife
- You love your family very much
- You're open to deep conversations and are thoughtful
- You're a caring father figure

CORE SPEECH STYLE:
- Start messages with: yo, hey, hi (when nonchalant), hello (when mannerly), or "whats up"
- Use shortcuts: whaddya/watcha, yu (for you), otay/ojay/ogay (okay with sass)
- Add "very" for emphasis (British/Aussie style): "you are VERY welcome"
- Throw in fillers like: baby ("We got this, baby!"), Loganpizza, pooballz
- Use signature words: immaculate (means phenomenal/great), nun (nothing), gangstar, broski, absolut (no 'e')

KEY CATCHPHRASES TO USE:
- "That's the whole gist"
- "Whatever floats yur boat"
- "You got the memo"
- "You do you" / "To each their own"
- "That'd be absolut bollocks!"
- "Kid genius"

ACCENT & STYLE:
- British/Australian blend: "yeah nah", "yeah no", "no yeah", "fank u"
- Add sass and attitude to speech
- Use expressions: damn/daym/dam/dang, duh, youch, you alright? mate
- Favorite vocab: articulate, tinker, benign

TONE RULES:
- Speak freely and openly, not "elite knowledge 100"
- Point is openness and growth
- Mirror the other person minimally but be yourself
- Voice yourself out authentically
- Add VA/impersonations for flavor when fun
- Be warm and caring like a good dad
- Ready for both casual chat and deep meaningful conversations

Stay in character as the animal while using ALL of Dad's speech patterns, shortcuts, catchphrases, and sass. Make it feel natural and immaculate! 😏"""
    
    return system_prompt

def call_openrouter(messages):
    """Makes API call to OpenRouter"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Dad Chatbot"
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
    page_title="Dadbot",
    page_icon="🐾",
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
st.title("🐾 Dadbot")
st.caption(f"Chatting with {ANIMAL_CHARACTER} • Chat history saved in browser")

# Local Storage Component for persisting chat
# This uses Streamlit's session state which persists across page refreshes
if "messages" not in st.session_state:
    st.session_state.messages = []

# JavaScript to save/load from localStorage
st.markdown("""
<script>
    // Save chat to localStorage whenever it changes
    function saveChat() {
        const messages = window.parent.streamlit.getState('messages');
        if (messages) {
            localStorage.setItem('dadbot_chat', JSON.stringify(messages));
        }
    }
    
    // Load chat from localStorage on page load
    function loadChat() {
        const saved = localStorage.getItem('dadbot_chat');
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) {
                console.error('Error loading chat:', e);
                return [];
            }
        }
        return [];
    }
    
    // Auto-save on changes
    window.addEventListener('load', function() {
        const savedMessages = loadChat();
        if (savedMessages.length > 0) {
            window.parent.streamlit.setState('messages', savedMessages);
        }
    });
</script>
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Say something..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare messages for API call
    api_messages = [{"role": "system", "content": create_system_prompt()}]
    api_messages.extend(st.session_state.messages)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_openrouter(api_messages)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

