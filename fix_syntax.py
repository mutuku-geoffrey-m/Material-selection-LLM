with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the missing brace
bad_end = """            "payload": None
        }
    ]}
    st.session_state.current_chat_id = initial_id"""
    
good_end = """            "payload": None
        }
    ]}}
    st.session_state.current_chat_id = initial_id"""
content = content.replace(bad_end, good_end)

# Fix the f-string quote issue
bad_fstring = 'key=f"active_plotly_chart_{len(st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"])}"'
good_fstring = "key=f'active_plotly_chart_{len(st.session_state.chat_sessions[st.session_state.current_chat_id][\"messages\"])}'"
content = content.replace(bad_fstring, good_fstring)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('app.py', doraise=True)
    print("Syntax is now correct.")
except Exception as e:
    print(f"Still syntax error: {e}")
