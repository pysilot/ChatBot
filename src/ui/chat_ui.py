import streamlit as st
import random
import time

st.set_page_config(
    page_title="Test Streamlit", 
    page_icon="🤖",
    layout="centered"
)
st.title("Test")
st.write("Chào mừng bạn đến với chatbot demo! Hãy bắt đầu trò chuyện nhé.")
st.markdown("""

<style>

body {
background-color: #0e1117;
color: #e0e0e0;
}

.chat-message {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    width: fit-content;
    max-width: 70%;
    font-family: sans-serif;
    font-size: 14px;
    }

.user-msg {
    background-color: #4caf50;
    color: #ffffff;
    margin-left: auto;
    }

.assistant-msg {
    background-color: #1f2937;
    border: 1px solid #374151;
    color: #e5e7eb;
    margin-right: auto;
    }

.blink {
    animation: blink 1s step-start 0s infinite;
    }

@keyframes blink {
    50%{ opacity:0;}
}
</style>

""", unsafe_allow_html = True)

if "messages" not in st.session_state:
    st.session_state.messages=[]

if st.sidebar.button("🗑️", help="Xóa lịch sử trò chuyện"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-msg">{message["content"]}</div>', unsafe_allow_html = True)
    else:
        st.markdown(f'<div class="chat-message assistant-msg">{message["content"]}</div>', unsafe_allow_html = True)

if prompt := st.chat_input("Bạn muốn hỏi gì?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.markdown(f'<div class="chat-message user-msg">{prompt}</div>', unsafe_allow_html=True)

    message_placeholder=st.empty()
    full_response=""

    if"xin chào" in prompt.lower() or "chào bạn" in prompt.lower():
            response_text="Chào bạn! Tôi có thể giúp gì cho bạn?"
    elif "thời tiết" in prompt.lower():
            response_text="Tôi không thể dự báo thời tiết. Bạn có thể kiếm tra trên Google hoặc ứng dụng thời tiết nhé!"
    elif"bạn là ai" in prompt.lower():
            response_text="Tôi là một chatbot được tạo bằng Streamlit. Rất vui được trò chuyện với bạn!"
    elif"tên bạn là gì" in prompt.lower():
            response_text="Tôi không có tên cụ thể, bạn có thể gọi tôi là Streamlit Bot."
    else:
            response_text="Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể thử hỏi câu khác không?"

    i= 0

    while i < len(response_text):
        char = response_text[i]
        full_response += char 
        message_placeholder.markdown(
            f'<div class="chat-message assistant-msg">{full_response}<span class="blink">▌</span></div>', unsafe_allow_html=True
            )

        if char in ".!?":
                time.sleep(0.4)
                if i + 1 < len(response_text) and response_text[i+1] == " ":
                    time.sleep(0.3)
        elif char in ",;:":
                time.sleep(0.2)
        elif i < 5:
                time.sleep(0.08)
        elif i < len(response_text) - 5:
                time.sleep(0.02)
        else:
                time.sleep(0.03)

        i += 1

    st.session_state.messages.append({"role":"assistant","content":full_response})

    message_placeholder.markdown(f'<div class="chat-message assistant-msg">{full_response}</div>', unsafe_allow_html=True)

            
