import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from google import genai
import random

# ================================================================
# 1. PAGE SETUP
# ================================================================

st.set_page_config(
    page_title="Space Station Heist",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 SPACE STATION HEIST")
st.caption("MISSION: STEAL THE STAR CORE")

# ================================================================
# 2. GEMINI SETUP
# ================================================================

load_dotenv(Path(__file__).resolve().with_name(".env"))
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# ================================================================
# 3. GAME SETUP
# ================================================================

if "game_started" not in st.session_state:
    st.session_state.game_started = False


def start_game(name):
    """Start a new game and initialise all values."""

    st.session_state.game_started = True
    st.session_state.player_name = name

    st.session_state.health = 5
    st.session_state.max_health = 5

    st.session_state.security = 0
    st.session_state.inventory = ["Hacking Device"]

    st.session_state.rooms = [
        "docking_bay",
        "engineering",
        "storage",
        "security",
        "control_room",
        "vault",
        "escape_bay"
    ]

    st.session_state.room_number = 0

    st.session_state.action_complete = False
    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""

    st.rerun()


def increase_security(amount):
    st.session_state.security += amount
    if st.session_state.security > 100:
        st.session_state.security = 100


def restart_game():
    st.session_state.clear()
    st.rerun()


def get_current_room():
    return st.session_state.rooms[st.session_state.room_number]


def continue_game():
    """Move to the next location."""

    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.session_state.action_complete = False

    st.session_state.room_number += 1
    st.rerun()


def retry_action():
    st.session_state.action_complete = False
    st.session_state.result_type = ""
    st.session_state.result_message = ""
    st.session_state.result_value = ""
    st.rerun()


# ================================================================
# 4. INVENTORY FUNCTIONS
# ================================================================

def add_item(item):
    if item not in st.session_state.inventory:
        st.session_state.inventory.append(item)


def has_item(item):
    return item in st.session_state.inventory


def remove_item(item):
    if item in st.session_state.inventory:
        st.session_state.inventory.remove(item)



def use_medkit():
    if has_item("Medkit"):

        healed = heal_player(2)

        # Only use the Medkit if health was actually restored
        if healed > 0:
            remove_item("Medkit")

        return healed

    return 0



# ================================================================
# 5. HEALTH AND SECURITY FUNCTIONS
# ================================================================

def take_damage(amount):
    st.session_state.health = max(
        0,
        st.session_state.health - amount
    )


def heal_player(amount):
    old_health = st.session_state.health

    st.session_state.health = min(
        st.session_state.max_health,
        st.session_state.health + amount
    )

    return st.session_state.health - old_health

# ================================================================
# 6. GEMINI STORY GENERATION
# ================================================================

def generate_story(room, action, outcome, fallback_message):

    if client is None:
        return fallback_message

    inventory_text = ", ".join(st.session_state.inventory)

    prompt = f"""
    You are the storyteller for a science fiction adventure
    game called Space Station Heist.

    The setting is a futuristic space station.
    The atmosphere should be exciting and suspenseful.

    Player: {st.session_state.player_name}
    Location: {room}
    Health: {st.session_state.health}
    Security Alert: {st.session_state.security}
    Inventory: {inventory_text}

    Player action: {action}

    Outcome already decided by Python: {outcome}

    Describe what happens in 30-50 words.

    Use second person.
    Make the story exciting and futuristic.
    Do not change the outcome.
    Do not change health or inventory.
    Do not introduce new choices.
    """

    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
            generation_config={"thinking_level": "minimal"}
        )

        if interaction.output_text:
            return interaction.output_text

        return fallback_message

    except Exception:
        return fallback_message


# ================================================================
# 7. DICE ROLLS AND CHALLENGES
# ================================================================

def roll_dice():
    return random.randint(1, 6)


def chance_encounter(
    button_text,
    room,
    action,
    success_number,
    success_outcome,
    success_fallback,
    failure_outcome,
    failure_fallback,
    damage,
    bonus_item=""
):

    if st.button(button_text):

        roll = roll_dice()

        if bonus_item != "" and has_item(bonus_item):
            roll += 2

        st.session_state.last_roll = roll

        if roll >= success_number:

            story = generate_story(
                room,
                action,
                success_outcome,
                success_fallback
            )

            set_result("success", story)

        else:

            take_damage(damage)
            increase_security(20)

            story = generate_story(
                room,
                action,
                failure_outcome,
                failure_fallback
            )

            set_result("damage", story, damage)


def combat_encounter(button_text, enemy, room, difficulty,
                     damage, security_increase, bonus_item=""):

    if st.button(button_text):
        roll = roll_dice()

        # Give the player a bonus if they have the correct item
        if bonus_item != "" and has_item(bonus_item):
            roll += 2

        # Fighting makes noise, so security always increases
        increase_security(security_increase)

        if roll >= difficulty:
            outcome = f"You defeat the {enemy}."
            fallback = (
                f"You successfully defeat the {enemy}, "
                "but the sound of the fight alerts nearby security."
            )

            story = generate_story(
                room,
                f"fighting the {enemy}",
                outcome,
                fallback
            )

            set_result("success", story)

        else:
            take_damage(damage)

            outcome = f"The {enemy} injures you before you escape."
            fallback = (
                f"The {enemy} strikes you. You manage to escape, "
                "but the station's security systems are now alerted."
            )

            story = generate_story(
                room,
                f"fighting the {enemy}",
                outcome,
                fallback
            )

            set_result("damage", story, damage)


# ================================================================
# 8. DISPLAY FUNCTIONS
# ================================================================

def show_room(title, description):
    st.header(title)
    st.write(description)



def show_player_info():

    st.subheader(f"🧑‍🚀 {st.session_state.player_name}")

    # MEDKIT BUTTON
    if has_item("Medkit"):

        if st.button(
            "🧪 Use Medkit (+2 Health)",
            disabled=st.session_state.health >= st.session_state.max_health
        ):

            healed = use_medkit()

            if healed > 0:
                st.success(
                    f"💚 Your Medkit restored {healed} health!"
                )

    elif st.session_state.health >= st.session_state.max_health:
        st.caption("❤️ Your health is already full.")

    left, right = st.columns(2)

    with left:
        st.write(
            f"❤️ Health: {st.session_state.health}/"
            f"{st.session_state.max_health}"
        )

    with right:
        st.write(
            f"🚨 Security: {st.session_state.security}/100"
        )

    st.progress(st.session_state.security / 100)

    st.write("🎒 Inventory:")
    st.write(", ".join(st.session_state.inventory))

    st.caption(
        f"Location {st.session_state.room_number + 1} "
        f"of {len(st.session_state.rooms)}"
    )

    st.divider()

def set_result(result_type, message, value=""):

    st.session_state.result_type = result_type
    st.session_state.result_message = message
    st.session_state.result_value = value
    st.session_state.action_complete = True

    st.rerun()


def show_result():

    kind = st.session_state.result_type
    value = st.session_state.result_value

    if kind == "item":
        st.success(f"🎒 NEW ITEM: {value}")

    elif kind == "damage":
        st.error(f"💔 DAMAGE: You lose {value} health.")

    elif kind == "heal":
        st.success(f"💚 You recovered {value} health.")

    elif kind == "success":
        st.success("✅ Challenge successful!")

    else:
        st.info("The mission continues...")

    if "last_roll" in st.session_state:
        st.write(f"🎲 Your dice roll: {st.session_state.last_roll}")
        del st.session_state.last_roll

    st.write(st.session_state.result_message)


def show_continue_button(text="Continue"):

    if st.button(text):
        continue_game()


# ================================================================
# 9. START SCREEN
# ================================================================

if not st.session_state.game_started:

    st.subheader("MISSION BRIEFING")

    st.write(
        "Year 2349. You are a professional space thief "
        "hired to steal the legendary Star Core from "
        "NovaCorp's heavily guarded space station."
    )

    st.write(
        "Sneak aboard, collect equipment, avoid security "
        "and escape before the station locks down."
    )

    st.warning("You have limited health. Don't get caught!")

    name = st.text_input("Enter your space thief name:")

    if st.button("🚀 BEGIN MISSION"):

        if name.strip():
            start_game(name.strip())

        else:
            st.warning("Please enter your name first!")


# ================================================================
# 10. MAIN GAME
# ================================================================

else:

    show_player_info()

    room = get_current_room()

    # GAME OVER CONDITIONS

    if st.session_state.health <= 0:

        show_room(
            "💀 MISSION FAILED",
            "Your injuries are too severe. NovaCorp security "
            "has captured you."
        )

        if st.button("🔄 Try Again"):
            restart_game()

        st.stop()

    if st.session_state.security >= 100:

        show_room(
            "🚨 YOU HAVE BEEN CAPTURED!",
            "The station security system has locked down. "
            "Armed guards surround you."
        )

        if st.button("🔄 Try Again"):
            restart_game()

        st.stop()


    # ============================================================
    # SCENE 1 — DOCKING BAY
    # ============================================================

    if room == "docking_bay":

        show_room(
            "🛸 Docking Bay",
            "Your stolen shuttle docks at Elysium-9. "
            "Two security guards are checking arriving ships."
        )

        if not st.session_state.action_complete:

            chance_encounter(
                "🥷 Sneak past the guards",
                "Docking Bay",
                "sneaking past the security guards",
                4,
                "The player successfully sneaks aboard.",
                "You slip behind a cargo container and "
                "make it past the guards unnoticed.",
                "The player is spotted by a guard.",
                "A guard spots you and raises the alarm!",
                1
            )

        else:
            show_result()
            show_continue_button("Enter Engineering Room")


    # ============================================================
    # SCENE 2 — ENGINEERING ROOM
    # ============================================================

    elif room == "engineering":

        show_room(
            "🔧 Engineering Room",
            "Machines fill the room. A technician has left "
            "some equipment beside the control panel."
        )

        if not st.session_state.action_complete:

            left, right = st.columns(2)

            with left:

                if st.button("🔎 Search the equipment"):

                    add_item("Security Keycard")

                    story = generate_story(
                        "Engineering Room",
                        "searching the equipment",
                        "The player finds a Security Keycard.",
                        "You search through the equipment "
                        "and discover a Security Keycard."
                    )

                    set_result("item", story, "Security Keycard")

            with right:

                if st.button("🚪 Leave the room"):

                    story = generate_story(
                        "Engineering Room",
                        "leaving without searching",
                        "The player leaves without collecting equipment.",
                        "You leave the equipment behind and "
                        "continue through the station."
                    )

                    set_result("story", story)

        else:
            show_result()
            show_continue_button("Enter Storage Bay")


    # ============================================================
    # SCENE 3 — STORAGE BAY
    # ============================================================

    elif room == "storage":

        show_room(
            "📦 Storage Bay",
            "You discover several supply crates. One contains "
            "medical supplies."
        )

        if not st.session_state.action_complete:

            left, right = st.columns(2)

            with left:

                if st.button("🧪 Search for medical supplies"):

                    add_item("Medkit")

                    story = generate_story(
                        "Storage Bay",
                        "searching for medical supplies",
                        "The player finds a Medkit.",
                        "Inside a supply crate you find a "
                        "Medkit that could save your life."
                    )

                    set_result("item", story, "Medkit")

            with right:

                if st.button("➡️ Continue onwards"):

                    story = generate_story(
                        "Storage Bay",
                        "leaving the storage bay",
                        "The player leaves without collecting supplies.",
                        "You leave the crates behind and head "
                        "towards security."
                    )

                    set_result("story", story)

        else:
            show_result()
            show_continue_button("Enter Security Corridor")


    # ============================================================
    # SCENE 4 — SECURITY CORRIDOR
    # ============================================================

    elif room == "security":

        show_room(
            "🤖 Security Corridor",
            "A powerful security robot blocks the corridor. "
            "Its red scanning light moves across the walls."
        )

        if not st.session_state.action_complete:

            combat_encounter(
                "⚔️ Fight the Security Robot",
                "security robot",
                "Security Corridor",
                5,       
                1,       
                20,      
                "Hacking Device"
            )

            if has_item("Hacking Device"):

                chance_encounter(
                    "💻 Hack the security robot",
                    "Security Corridor",
                    "hacking the security robot",
                    4,
                    "The player successfully disables the robot.",
                    "The robot powers down as your hacking "
                    "device takes control.",
                    "The hacking attempt fails.",
                    "The robot detects your device and fires "
                    "a laser blast!",
                    1,
                    "Hacking Device"
                )

            else:

                chance_encounter(
                    "🏃 Sneak past the robot",
                    "Security Corridor",
                    "sneaking past the robot",
                    5,
                    "The player sneaks past the robot.",
                    "You carefully move through the shadows "
                    "and avoid the robot's scanner.",
                    "The robot detects the player.",
                    "The robot detects your movement and "
                    "fires a laser blast!",
                    2
                )

        else:
            show_result()
            show_continue_button("Enter Control Room")


    # ============================================================
    # SCENE 5 — CONTROL ROOM
    # ============================================================

    elif room == "control_room":

        show_room(
            "🖥️ Control Room",
            "You reach the main computer system. The vault "
            "access code is stored somewhere inside."
        )

        if not st.session_state.action_complete:

            if has_item("Hacking Device"):

                if st.button("💻 Hack the main computer"):

                    add_item("Vault Access Code")

                    story = generate_story(
                        "Control Room",
                        "hacking the main computer",
                        "The player discovers the Vault Access Code.",
                        "You bypass the computer's security "
                        "and discover the vault access code."
                    )

                    set_result("item", story, "Vault Access Code")

            if st.button("🔎 Search the desk"):

                add_item("Vault Access Code")

                story = generate_story(
                    "Control Room",
                    "searching the computer desk",
                    "The player finds the Vault Access Code.",
                    "Hidden beneath a computer terminal, "
                    "you discover a written vault access code."
                )

                set_result("item", story, "Vault Access Code")

        else:
            show_result()
            show_continue_button("Enter the Star Core Vault")


    
    # ============================================================
    # SCENE 6 — STAR CORE VAULT
    # ============================================================

    elif room == "vault":

        show_room(
            "💎 Star Core Vault",
            "The enormous vault stands before you. The Star Core "
            "glows brightly in the centre of the room."
        )

        # If the player already has the Star Core
        if has_item("Star Core"):

            st.success("💎 You have stolen the Star Core!")

            if st.button("➡️ Enter Escape Bay"):
                continue_game()

        # If the player has not completed an action yet
        elif not st.session_state.action_complete:

            # Option 1: Use the access code
            if has_item("Vault Access Code"):

                st.success("🔓 You have the Vault Access Code!")

                if st.button("💎 Take the Star Core"):

                    add_item("Star Core")
                    increase_security(20)

                    story = generate_story(
                        "Star Core Vault",
                        "taking the Star Core",
                        "The player successfully steals the Star Core.",
                        "You grab the glowing Star Core. "
                        "An alarm begins to sound throughout the station!"
                    )

                    set_result("item", story, "Star Core")

            # Option 2: Force the vault open
            else:

                st.warning(
                    "You don't have the Vault Access Code. "
                    "You will need to force the vault open."
                )

                if st.button("🔨 Force the vault open"):

                    roll = roll_dice()

                    st.session_state.last_roll = roll

                    if roll >= 6:

                        # SUCCESS: Award the Star Core
                        add_item("Star Core")
                        increase_security(20)

                        story = generate_story(
                            "Star Core Vault",
                            "forcing open the vault",
                            "The player successfully opens the vault "
                            "and steals the Star Core.",
                            "After a desperate struggle, the vault "
                            "door opens. You grab the Star Core!"
                        )

                        set_result("item", story, "Star Core")

                    else:

                        # FAILURE: Damage the player and increase security
                        take_damage(2)
                        increase_security(20)

                        story = generate_story(
                            "Star Core Vault",
                            "trying to force open the vault",
                            "The player fails to open the vault "
                            "and is injured by its defence system.",
                            "The vault's defence system strikes you. "
                            "The alarm begins to sound!"
                        )

                        set_result("damage", story, 2)

            # Option 3: Fight the elite security officer
            combat_encounter(
                "⚔️ Fight the Elite Security Officer",
                "elite security officer",
                "Star Core Vault",
                7,
                2,
                30,
                "Security Keycard"
            )

        # Show the result after an action
        else:

            show_result()

            # Only allow the player to continue if they have the Star Core
            if has_item("Star Core"):

                show_continue_button("Enter Escape Bay")

            else:

                st.warning(
                    "You haven't stolen the Star Core yet. "
                    "You must try another approach."
                )

                if st.button("🔁 Try again in the vault"):
                    retry_action()

    # ============================================================
    # SCENE 7 — ESCAPE BAY
    # ============================================================

    elif room == "escape_bay":

        show_room(
            "🚀 Escape Bay",
            "The station is on lockdown. Security guards "
            "are approaching. Your stolen shuttle is nearby."
        )

        if has_item("Star Core"):

            st.success("💎 You have stolen the Star Core!")

            if not st.session_state.action_complete:

                chance_encounter(
                    "🚀 Escape using your shuttle",
                    "Escape Bay",
                    "escaping aboard the stolen shuttle",
                    4,
                    "The player successfully escapes with the Star Core.",
                    "You launch your shuttle just as the station "
                    "locks down. The Star Core is yours!",
                    "The shuttle fails to launch in time.",
                    "Security fire hits your shuttle. "
                    "You struggle to escape the station.",
                    1,
                    "Security Keycard"
                )

            else:

                show_result()

                if st.session_state.result_type == "success":

                    st.header("🏆 HEIST COMPLETE!")

                    st.balloons()

                    st.write(
                        "Congratulations! You escaped Elysium-9 "
                        "with the legendary Star Core!"
                    )

                    if st.button("🔄 Play Again"):
                        restart_game()

                else:
                    if st.button("🔄 Try to escape Again"):
                        retry_action()

        else:

            st.error(
                "You haven't stolen the Star Core. "
                "You cannot complete the mission!"
            )

            if st.button("🔄 Try Again"):
                restart_game()