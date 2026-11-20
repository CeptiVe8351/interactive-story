import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).resolve().with_name(".env"))
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

MODEL_NAME = "gemini-3.5-flash-lite"
exhibits = {
    "Roman coin": "The visitor reads a label explaining that the coin is about 2,000 years old.",
    "Dinosaur fossil": "The visitor learns that the fossil belongs to a plant-eating dinosaur.",
    "Ancient pottery": "The visitor discovers that the pot was used for storing food.",
    "Egyptian Sarcophagus": "The visitor discovers that this decorated coffin was used in ancient Egyptian burial traditions.",
    "Viking Helmet": "The visitor learns that Viking helmets were protective equipment used by warriors.",
    "Enchanted Crystal": "The visitor discovers that the unusual crystal was once displayed as a symbol of power and mystery."
}

def make_prompt(name, exhibit, outcome):
    """Create a prompt with a character personality and fixed outcome."""

    return f"""
Role:
You are a friendly museum exhibit narrator.

Personality:
- You are friendly, cheerful and curious.
- You sometimes use playful expressions and light humour.
- You sound excited when explaining interesting historical objects.
- You make visitors feel like they are part of an adventure.
- You are knowledgeable but never boring.

Context:
A visitor named {name} is looking at the {exhibit} exhibit.

Fixed outcome:
{outcome}

Instructions:
- Speak directly to the visitor using you and your.
- Stay in character as Professor Pemberton.
- Use a friendly, exciting and slightly dramatic tone.
- Describe the discovery in 30-50 words.
- Do not change the fixed outcome.
- Do not let the visitor take any objects.
- Do not invent new discoveries or historical facts.
- Do not introduce new decisions for the visitor.
- Keep the description suitable for a museum visitor.

Return only the short description.
"""

def generate_description(prompt, fallback):

    if client is None:
        return fallback, "No API key found. Showing fallback description."

    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
            generation_config={"thinking_level": "minimal"},
        )

        description = interaction.output_text

        if not description:
            return fallback, "Gemini returned no text. Showing the fallback."

        return description, None

    except Exception as error:
        return fallback, (
            f"The API request failed ({type(error).__name__}). "
            "Showing the fallback."
        )

st.set_page_config(page_title="Museum", page_icon="🏛️")

st.title("🏛️ The Museum of Wonders")

st.write(
    "Welcome, explorer! Step inside and discover fascinating "
    "objects from history and mystery. Professor Pemberton "
    "will guide you around the museum!"
)

name = st.text_input("What is your name, explorer?")

exhibit = st.selectbox(
    "Choose an exhibit",
    list(exhibits)
)

outcome = exhibits[exhibit]

prompt = make_prompt(name, exhibit, outcome)

if st.button("✨ Explore this exhibit"):

    if not name.strip():
        st.warning("Please enter your name first!")

    else:
        with st.spinner("Professor Pemberton is preparing your discovery..."):

            description, message = generate_description(prompt, outcome)

        st.subheader(f"🔍 {exhibit}")

        st.write(description)

        if message:
            st.warning(message)

        st.success("Thank you for exploring the museum!")