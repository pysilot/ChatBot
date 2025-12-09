import streamlit as st
import json
import os
import time
import uuid
from datetime import datetime
import requests

FILE_PATH = "chat_history_v2.json"

API_URL = "https://djrpk-34-187-250-25.a.free.pinggy.link/api/generate"

st.set_page_config(
    page_title="Advanced Chatbot", 
    page_icon="🤖",
    layout="wide" 
)

# #taitufilejsom
def load_data():
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    #luudulieu
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Lỗi khi lưu file: {e}")

def get_ai_response(user_input):
    payload = {
        # Đảm bảo tên model này khớp với model đang chạy trên server của bạn
        "model": "gpt-oss:20b",
        "prompt": user_input,
        "stream": False
    }
    try:
        # Gửi request POST
        r = requests.post(API_URL, json=payload, timeout=60)
        
        if r.status_code == 200:
            # Lấy nội dung trả lời từ JSON
            return r.json().get("response", "Model không trả về nội dung.")
        else:
            return f"Lỗi API ({r.status_code}): {r.text}"
    except requests.exceptions.ConnectionError:
        return "Lỗi kết nối: Không thể gọi đến server (Link Pinggy có thể sai hoặc server chưa bật)."
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"

if "all_chats" not in st.session_state:
    st.session_state.all_chats = load_data()

if "current_chat_id" not in st.session_state:
    if st.session_state.all_chats:
        st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[-1]
    else:
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {
            "title": "Cuộc trò chuyện mới", 
            "messages": [],
            "timestamp": str(datetime.now())
        }
        st.session_state.current_chat_id = new_id

def create_new_chat(chat_name):
    new_id = str(uuid.uuid4())
    st.session_state.all_chats[new_id] = {
        "title": chat_name, 
        "messages": [],
        "timestamp": str(datetime.now())
    }
    st.session_state.current_chat_id = new_id
    save_data(st.session_state.all_chats)

def delete_chat(chat_id_to_delete):
    #xoadoanchat
    if chat_id_to_delete in st.session_state.all_chats:
        del st.session_state.all_chats[chat_id_to_delete]
        save_data(st.session_state.all_chats)
        if st.session_state.current_chat_id == chat_id_to_delete:
            if st.session_state.all_chats:
                st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[-1]
            else:
                create_new_chat()
    st.rerun()

st.markdown("""
<style>
    body { background-color: #0e1117; color: #e0e0e0; }
    
    /* Style cho bong bóng chat */
    .chat-message {
        padding: 12px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 75%;
        font-family: sans-serif;
        font-size: 15px;
        line-height: 1.5;
    }
    .user-msg {
        background-color: #2e7d32; /* Màu xanh đậm hơn chút cho dễ đọc */
        color: #ffffff;
        margin-left: auto;
        border-bottom-right-radius: 2px;
    }
    .assistant-msg {
        background-color: #262730;
        border: 1px solid #374151;
        color: #e5e7eb;
        margin-right: auto;
        border-bottom-left-radius: 2px;
    }
    
    /* Hiệu ứng con trỏ nhấp nháy */
    .blink { animation: blink 1s step-start 0s infinite; }
    @keyframes blink { 50%{ opacity:0;} }
    
    /* Tùy chỉnh nút bấm trong Sidebar để trông gọn hơn */
    div[data-testid="stSidebar"] button {
        text-align: left;
        border: none;
        width: 100%;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.dialog("Xác nhận xóa")
def confirm_delete_dialog(chat_id):
    st.write("Bạn có chắc chắn xóa cuộc trò chuyện này không?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hủy"):
            st.rerun()
    with col2:
        if st.button("Xóa ngay", type="primary"):
            delete_chat(chat_id)

@st.dialog("Đặt tên cho cuộc trò chuyện")
def name_new_chat_dialog():
    chat_name = st.text_input("Nhập tên cuộc trò chuyện:", "")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Hủy"):
            st.rerun()

    with col2:
        if st.button("Tạo", type="primary"):
            if chat_name.strip() == "":
                st.warning("Vui lòng nhập tên!")
                st.stop()
            create_new_chat(chat_name)
            st.rerun()


#sidebar
with st.sidebar:
    st.title("💬 Lịch sử Chat")

    if st.button("➕ Cuộc trò chuyện mới", use_container_width=True, type="primary"):
        name_new_chat_dialog()
    
    st.divider()
    
    sorted_chat_ids = sorted(
        st.session_state.all_chats.keys(), 
        key=lambda k: st.session_state.all_chats[k].get("timestamp", ""), 
        reverse=True
    )

    st.caption("Gần đây")
    #hienthi
    for chat_id in sorted_chat_ids:
        chat_data = st.session_state.all_chats[chat_id]
        title = chat_data.get("title", "Không có tiêu đề")
        
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            button_type = "secondary" if chat_id != st.session_state.current_chat_id else "primary"
            display_title = (title[:22] + '...') if len(title) > 22 else title
            
            if st.button(f"🗨️ {display_title}", key=f"btn_{chat_id}", use_container_width=True, type=button_type):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        
        with col2:
            if st.button("🗑️", key=f"del_{chat_id}", help="Xóa chat này"):
                confirm_delete_dialog(chat_id)

current_id = st.session_state.current_chat_id
current_chat_data = st.session_state.all_chats.get(current_id, {})
current_messages = current_chat_data.get("messages", [])
current_title = current_chat_data.get("title", "Cuộc trò chuyện mới")

st.subheader(f"{current_title}")
st.divider()

for message in current_messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-msg">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-msg">{message["content"]}</div>', unsafe_allow_html=True)


if prompt := st.chat_input("Nhập tin nhắn..."):

    st.markdown(f'<div class="chat-message user-msg">{prompt}</div>', unsafe_allow_html=True)
    
    current_messages.append({"role": "user", "content": prompt})
    
    should_rerun = False
    if len(current_messages) == 1:
        st.session_state.all_chats[current_id]["title"] = prompt
        should_rerun = True

    message_placeholder = st.empty()
    # Hien thi trang thai dang suy nghi
    message_placeholder.markdown('<div class="chat-message assistant-msg">Bot đang suy nghĩ...</div>', unsafe_allow_html=True)

    # Goi API thay cho doan if/else cu
    response_text = get_ai_response(prompt)
    
    full_response = ""
    
    #hieung
    i = 0
    while i < len(response_text):
        char = response_text[i]
        full_response += char 
        message_placeholder.markdown(
            f'<div class="chat-message assistant-msg">{full_response}<span class="blink">▌</span></div>', 
            unsafe_allow_html=True
        )
        
        if char in ".!?":
            time.sleep(0.05)
            if i + 1 < len(response_text) and response_text[i+1] == " ":
                time.sleep(0.03)
        elif char in ",;:":
            time.sleep(0.03)
        else:
            time.sleep(0.01)

        i += 1
    
    #luulichsu
    current_messages.append({"role": "assistant", "content": full_response})
    
    #capnhatvaluufile
    st.session_state.all_chats[current_id]["messages"] = current_messages
    save_data(st.session_state.all_chats)
    
    message_placeholder.markdown(f'<div class="chat-message assistant-msg">{full_response}</div>', unsafe_allow_html=True)

    if should_rerun:
        st.rerun()
