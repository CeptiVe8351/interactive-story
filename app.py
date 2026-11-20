# # python -m streamlit run app.py

import streamlit as st

# STEP 1 — Initialise game values once per browser session.
# Streamlit reruns the script when the player interacts with a widget.
# These values need to survive those reruns.
if "playerName" not in st.session_state:
    st.session_state.playerName = ""
if "health" not in st.session_state:
    st.session_state.health = 100
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "scene" not in st.session_state:
    st.session_state.scene = "start"
if "result" not in st.session_state:
    st.session_state.result = ""

# STEP 2 — Show the game's title and the information the player carries.
st.title("Escape the Catle")

if st.session_state.playerName:
    st.write(f"Player: {st.session_state.playerName}")
    st.write(f"Health: {st.session_state.health}")
    st.write(f"Inventory: {st.session_state.inventory}")

# STEP 3 — Start screen: use a text input and button.
# The name is saved to session state so it is available in later scenes.
if st.session_state.scene == "start":
    st.subheader("create your character")
    st.session_state.playerName = st.text_input("What is your name?")
    if st.button("Start Adventure"):
        st.session_state.scene = "cell"
        st.rerun()

# STEP 4 — Cell scene: convert the terminal choices into buttons.
# Store the result so it stays visible after other interactions.
elif st.session_state.scene == "cell":
    st.subheader("The Cell")
    st.write("You wake up in a dark castle cell.")
    st.write("You can see a door, a window, and an old bed.")

    if st.button("Investigate the door"):
        st.session_state.result = "The door is locked. You need to find the key."
    if st.button("Investigate the window"):
        st.session_state.result = "You look through the window and see a beautiful garden outside. But it's too high to jump."
    if st.button("Investigate the Bed"):
        if "Iron Key" not in st.session_state.inventory:
            st.session_state.inventory.append("Iron Key")
            st.session_state.result = "You find an Iron Key!"
        else:
            st.session_state.result = "There is nothing else under the bed"

    if st.session_state.result:
        st.info(st.session_state.result)

# STEP 5 — Unlock progress using a condition based on inventory.
    if "Iron Key" in st.session_state.inventory:
        if st.button("Unlock the door and continue"):
            st.session_state.scene = "corridor"
            st.session_state.result = ""
            st.rerun()

# STEP 6 — Corridor scene: use the SAME inventory as in the Cell.
#Initialise the corridor scene - they player needs to notice a cabinet

elif st.session_state.scene == "corridor":
    st.subheader("The Corridor")
    st.write("You enter a long, dark corridor.")
    st.write("You notice an old wooden cabinet against the wall.")

    #Give the player options to "Open the cabinet" or "Leave the cabinet"
    #If the player opens the cabinet, they should find a rusty dagger
    if st.button("Open the cabinet"):
        if "Rusty Dagger" not in st.session_state.inventory:
            st.session_state.inventory.append("Rusty Dagger")
            st.session_state.result = "You open the cabinet and find a Rusty Dagger!"
        else:
            st.session_state.result = "The cabinet is empty."

    if st.button("Leave the cabinet"):
        st.session_state.result = "You decide to leave the cabinet alone."
        st.session_state.inventory.remove("Rusty Dagger")

    if st.session_state.result:
        st.info(st.session_state.result)

    #Allow the player to continue with or without the dagger
    if st.button("Continue down the corridor"):
        st.session_state.scene = "next_scene"
        st.session_state.result = ""
        st.rerun()