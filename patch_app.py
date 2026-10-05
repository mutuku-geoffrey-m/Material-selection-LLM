import re
import sys

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add uuid import
if "import uuid" not in content:
    content = content.replace("import streamlit as st", "import streamlit as st\nimport uuid")

# 2. Add property to safely get current messages
# Instead of replacing every instance of st.session_state.messages, we can alias it at the start of the logic
# Wait, replacing all `st.session_state.messages` with `st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"]` is better.
content = content.replace("st.session_state.messages", 'st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"]')

# 3. Handle initialization block (lines 129-146)
init_block_old = '''if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"] = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am your **Autonomous Material Selection & Mechanical Engineering Consultant**.\\n\\n"
                "I analyze non-technical requirements and translate them into rigorous **Michael Ashby performance indices**, "
                "evaluate empirical degradation (freshwater saturation, UV exposure, fatigue limits), and prescribe exact manufacturing "
                "directives across **all engineering domains**:\\n"
                "- 🚀 **Aerospace & Marine:** Lightweight spars, hydrofoil turbine blades, boat hulls, rocket nozzles\\n"
                "- 🚲 **Automotive & Sports:** Bicycle frames, racing chassis, crane hooks, suspension arms\\n"
                "- 💻 **Thermal Management:** CPU heat sinks, heat exchangers, thermal barriers\\n"
                "- 🦴 **Biomedical & Consumer:** Orthopedic hip implants, shock-absorbing phone cases, wear-resistant gears\\n\\n"
                "Type your query below or click one of the quick starter chips!"
            ),
            "payload": None
        }
    ]'''

# But since we already replaced messages with the chat_sessions dict access, the existing code looks like:
# if "messages" not in st.session_state:
#     st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"] = [ ...

# Let's just do a clean regex replacement for the init block and the sidebar block.
# Actually, it's safer to read original file, replace step by step using exact substrings.
with open("app.py", "r", encoding="utf-8") as f:
    orig = f.read()

if "import uuid" not in orig:
    orig = orig.replace("import streamlit as st", "import streamlit as st\nimport uuid")

# 4. Initialization Block Replacement
old_init = '''# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": ('''

new_init = '''# Initialize Chat History
if "chat_sessions" not in st.session_state:
    initial_id = str(uuid.uuid4())
    st.session_state.chat_sessions = {
        initial_id: {
            "title": "New Chat",
            "messages": [
                {
                    "role": "assistant",
                    "content": ('''

orig = orig.replace(old_init, new_init)

# The end of initialization block:
old_init_end = '''            "payload": None
        }
    ]'''

new_init_end = '''            "payload": None
        }
    ]}
    st.session_state.current_chat_id = initial_id'''

orig = orig.replace(old_init_end, new_init_end)

# 5. Sidebar Replacement
old_sidebar = '''st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.rerun()'''

new_sidebar = '''st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Chat History")
if st.sidebar.button("➕ New Chat", use_container_width=True):
    new_id = str(uuid.uuid4())
    st.session_state.chat_sessions[new_id] = {
        "title": f"Chat {len(st.session_state.chat_sessions)+1}",
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello! I am your **Autonomous Material Selection & Mechanical Engineering Consultant**.\\n\\n"
                    "Type your query below or click one of the quick starter chips!"
                ),
                "payload": None
            }
        ]
    }
    st.session_state.current_chat_id = new_id
    st.rerun()

st.sidebar.markdown("#### Previous Chats")
if "chat_sessions" in st.session_state:
    for chat_id, chat_data in reversed(list(st.session_state.chat_sessions.items())):
        btn_style = "primary" if chat_id == st.session_state.current_chat_id else "secondary"
        if st.sidebar.button(chat_data["title"], key=f"chat_btn_{chat_id}", type=btn_style, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

if st.sidebar.button("🗑️ Clear All History", use_container_width=True):
    del st.session_state.chat_sessions
    st.rerun()'''

orig = orig.replace(old_sidebar, new_sidebar)

# 6. Change all `st.session_state.messages` to `st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"]`
# But only those AFTER the initialization. We can just blindly replace all, except for where we just wrote them in the init block.
# Wait, it's easier to just replace `st.session_state.messages` in the whole file, but first fix the init block.
# Let's fix the init block to NOT use `st.session_state.messages`. I did that in new_init.
orig = orig.replace('st.session_state.messages', 'st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"]')

# Wait, `if "chat_sessions" not in st.session_state:` shouldn't be affected.
# Let's handle the title update.
# Where it appends user message:
append_target = '''    # Append User Message
    st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"].append({"role": "user", "content": active_prompt, "payload": None})'''

title_update = '''    # Append User Message
    current_chat = st.session_state.chat_sessions[st.session_state.current_chat_id]
    if current_chat["title"].startswith("New Chat") or current_chat["title"].startswith("Chat "):
        current_chat["title"] = (active_prompt[:25] + "...") if len(active_prompt) > 25 else active_prompt
    current_chat["messages"].append({"role": "user", "content": active_prompt, "payload": None})'''

orig = orig.replace(append_target, title_update)

# Write back
with open("app.py", "w", encoding="utf-8") as f:
    f.write(orig)

print("Patch applied.")
