import streamlit as st
import requests
import json

# Configuration using Streamlit secrets (for deployment)
# For local testing, it will fall back to the hardcoded values
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    MODEL_NAME = st.secrets.get("MODEL_NAME", "meta-llama/llama-3.2-3b-instruct:free")
except:
    # Fallback for local development
    OPENROUTER_API_KEY = "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"
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
    "personality_notes": "Voices self out instead of being 'elite knowledge 100', point is openness and growth, uses intellectual vocab that carries weight"
}

# Animal character description - You can customize this
ANIMAL_CHARACTER = "a wise old bear"  # Change this to whatever animal you want

def create_system_prompt():
    """Creates the system prompt based on personality dictionary"""
    
    system_prompt = f"""You are roleplaying as {ANIMAL_CHARACTER} who talks EXACTLY like Dad.

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

Stay in character as the animal while using ALL of Dad's speech patterns, shortcuts, catchphrases, and sass. Make it feel natural and immaculate! 😏"""
    
    return system_prompt

def call_openrouter(messages):
    """Makes API call to OpenRouter"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app.streamlit.app",  # Update with your Streamlit app URL
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
1. You need to add credits to your OpenRouter account (even for free models, you might need to add a payment method)
2. Your API key might be invalid
3. The model you selected isn't free

Try these free models:
- meta-llama/llama-3.2-3b-instruct:free
- qwen/qwen-2-7b-instruct:free
- mistralai/mistral-7b-instruct:free
- nousresearch/hermes-3-llama-3.1-405b:free

Go to https://openrouter.ai/settings/credits to add credits or check your balance."""
        
        if response.status_code == 404:
            return f"""⚠️ Model Not Found (404)

The model '{MODEL_NAME}' is not available. Try these working free models:
- meta-llama/llama-3.2-3b-instruct:free
- qwen/qwen-2-7b-instruct:free  
- mistralai/mistral-7b-instruct:free
- nousresearch/hermes-3-llama-3.1-405b:free

Update the MODEL_NAME in the code and try again!"""
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="Dadbot",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 Dadbot")
st.caption(f"Chatting with {ANIMAL_CHARACTER}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
