import streamlit as st
import requests

API_BASE = "http://localhost:8000"
LOGIN_URL = f"{API_BASE}/login"
CHAT_URL = f"{API_BASE}/chat"

# ▶️ Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = {"username": "", "role": ""}
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Login UI ---
st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Username", key="login_username")
password = st.sidebar.text_input("Password", type="password", key="login_password")

if st.sidebar.button("Login", key="login_btn"):
    resp = requests.get(LOGIN_URL, auth=(username, password))
    if resp.ok:
        data = resp.json()
        if "user" in data and "role" in data:
            st.session_state.logged_in = True
            st.session_state.user = {
                "username": data["user"],
                "role": data["role"]
            }
            st.sidebar.success(data.get("message", f"Welcome {data['user']}!"))
        else:
            st.sidebar.error("Unexpected login response structure.")
    else:
        st.sidebar.error("❌ Invalid credentials")

# --- Main Chat Interface ---
if st.session_state.logged_in:
    user = st.session_state.user
    st.header(f"Chatbot — {user['username']} ({user['role']})")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a question…", key="chat_input")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            st.markdown("⏳ Thinking…")
            try:
                resp = requests.post(
                    CHAT_URL,
                    json={"message": user_input},
                    auth=(user["username"], password),
                    timeout=30
                )

                if resp.ok:
                    data = resp.json()
                    response_text = data.get("response", "")
                    sources = data.get("sources", [])
                    
                    # Format sources nicely
                    if sources:
                        source_lines = ["**Sources:**"]
                        for src in sources:
                            dept = src.get("department", "Unknown Dept")
                            source_file = src.get("source", "Unknown File")
                            source_lines.append(f"- *{dept}* — `{source_file}`")
                        response_text += "\n\n" + "\n".join(source_lines)

                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    raise Exception(resp.text or f"Status {resp.status_code}")
            except Exception as e:
                st.error(f"❌ Chat API error: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
else:
    st.info("➡️ Please log in using the sidebar before chatting.")
