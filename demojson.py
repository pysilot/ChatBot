import streamlit as st
import json
import os
import time
import uuid
from datetime import datetime

# --- CẤU HÌNH ---
FILE_PATH = "chat_history_v2.json"

st.set_page_config(
    page_title="Advanced Chatbot", 
    page_icon="🤖",
    layout="wide" # Đổi sang wide để sidebar thoáng hơn
)

# --- XỬ LÝ DỮ LIỆU ---
def load_data():
    """Load toàn bộ dữ liệu chat từ file JSON"""
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    """Lưu toàn bộ dữ liệu vào file JSON"""
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Lỗi khi lưu file: {e}")

# --- QUẢN LÝ SESSION STATE ---
# Khởi tạo dữ liệu trong RAM nếu chưa có
if "all_chats" not in st.session_state:
    st.session_state.all_chats = load_data()

# Xác định ID phiên chat hiện tại
if "current_chat_id" not in st.session_state:
    # Nếu có lịch sử, lấy cái mới nhất, nếu không thì tạo mới
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

# --- HÀM HỖ TRỢ ---
def create_new_chat():
    """Tạo một phiên chat mới và chuyển hướng tới nó"""
    new_id = str(uuid.uuid4())
    st.session_state.all_chats[new_id] = {
        "title": "Cuộc trò chuyện mới", 
        "messages": [],
        "timestamp": str(datetime.now())
    }
    st.session_state.current_chat_id = new_id
    save_data(st.session_state.all_chats)

def delete_chat(chat_id_to_delete):
    """Xóa một phiên chat cụ thể theo ID"""
    if chat_id_to_delete in st.session_state.all_chats:
        del st.session_state.all_chats[chat_id_to_delete]
        save_data(st.session_state.all_chats)
        
        # Nếu đang xóa đúng đoạn chat hiện tại, phải chuyển sang đoạn khác
        if st.session_state.current_chat_id == chat_id_to_delete:
            if st.session_state.all_chats:
                st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[-1]
            else:
                create_new_chat()
    st.rerun()

# --- CSS STYLING ---
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

# --- DIALOG (POPUP) XÓA CHAT ---
@st.dialog("Xác nhận xóa")
def confirm_delete_dialog(chat_id):
    st.write("Bạn có chắc chắn muốn xóa cuộc trò chuyện này không?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hủy"):
            st.rerun()
    with col2:
        if st.button("Xóa ngay", type="primary"):
            delete_chat(chat_id)

# --- SIDEBAR: LỊCH SỬ CHAT ---
with st.sidebar:
    st.title("💬 Lịch sử Chat")
    
    # Nút tạo chat mới
    if st.button("➕ Cuộc trò chuyện mới", use_container_width=True, type="primary"):
        create_new_chat()
        st.rerun()
    
    st.divider()
    
    # Danh sách các đoạn chat cũ
    # Sắp xếp theo thời gian mới nhất lên đầu
    sorted_chat_ids = sorted(
        st.session_state.all_chats.keys(), 
        key=lambda k: st.session_state.all_chats[k].get("timestamp", ""), 
        reverse=True
    )

    st.caption("Gần đây")
    for chat_id in sorted_chat_ids:
        chat_data = st.session_state.all_chats[chat_id]
        title = chat_data.get("title", "Không có tiêu đề")
        
        # Chia cột: 85% cho tên chat, 15% cho nút xóa
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            # Highlight chat đang chọn
            button_type = "secondary" if chat_id != st.session_state.current_chat_id else "primary"
            # Cắt ngắn tiêu đề nếu quá dài
            display_title = (title[:22] + '...') if len(title) > 22 else title
            
            if st.button(f"🗨️ {display_title}", key=f"btn_{chat_id}", use_container_width=True, type=button_type):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        
        with col2:
            # Nút xóa nhỏ bên cạnh, dùng key khác để tránh trùng lặp
            if st.button("🗑️", key=f"del_{chat_id}", help="Xóa chat này"):
                confirm_delete_dialog(chat_id)

# --- MAIN CHAT AREA ---
# Lấy dữ liệu của session hiện tại
current_id = st.session_state.current_chat_id
current_chat_data = st.session_state.all_chats.get(current_id, {})
current_messages = current_chat_data.get("messages", [])
current_title = current_chat_data.get("title", "Cuộc trò chuyện mới")

# Header khu vực chat (Đã bỏ nút xóa ở đây vì đã có trong sidebar)
st.subheader(f"{current_title}")
st.divider()

# Hiển thị tin nhắn cũ
for message in current_messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-msg">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-msg">{message["content"]}</div>', unsafe_allow_html=True)

# Input xử lý tin nhắn mới
if prompt := st.chat_input("Nhập tin nhắn..."):
    # 1. Hiển thị tin nhắn User
    st.markdown(f'<div class="chat-message user-msg">{prompt}</div>', unsafe_allow_html=True)
    
    # 2. Cập nhật dữ liệu vào biến tạm
    current_messages.append({"role": "user", "content": prompt})
    
    # Cập nhật tiêu đề nếu đây là tin nhắn đầu tiên
    if len(current_messages) == 1:
        st.session_state.all_chats[current_id]["title"] = prompt
        st.rerun() # Rerun để cập nhật tên bên sidebar ngay lập tức

    # 3. Logic Bot trả lời (Giữ nguyên logic của bạn)
    message_placeholder = st.empty()
    full_response = ""
    response_text = ""

    prompt_lower = prompt.lower()
    if"xin chào" in prompt.lower() or "chào bạn" in prompt.lower():
            response_text="Chào bạn! Tôi có thể giúp gì cho bạn?"
    elif "thời tiết" in prompt.lower():
            response_text="Tôi không thể dự báo thời tiết. Bạn có thể kiếm tra trên Google hoặc ứng dụng thời tiết nhé!"
    elif"bạn là ai" in prompt.lower():
            response_text="Tôi là một chatbot được bởi Nhóm 5, 25CTT3. Rất vui được trò chuyện với bạn!"
    elif"tên bạn là gì" in prompt.lower():
            response_text="Tôi không có tên cụ thể, bạn có thể gọi tôi là Group 5 Bot."
    else:
            response_text="Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể thử hỏi câu khác không?"

    # 4. Hiệu ứng gõ chữ
    i = 0
    while i < len(response_text):
        char = response_text[i]
        full_response += char 
        message_placeholder.markdown(
            f'<div class="chat-message assistant-msg">{full_response}<span class="blink">▌</span></div>', 
            unsafe_allow_html=True
        )
        # Logic delay
        if char in ".!?": time.sleep(0.05) # Giảm delay chút cho nhanh hơn demo
        elif char in ",;:": time.sleep(0.03)
        else: time.sleep(0.01)
        i += 1

    # 5. Lưu tin nhắn Bot vào session
    current_messages.append({"role": "assistant", "content": full_response})
    
    # 6. Cập nhật vào Session State tổng và Lưu File
    st.session_state.all_chats[current_id]["messages"] = current_messages
    save_data(st.session_state.all_chats)
    
    # Xóa con trỏ nhấp nháy cuối cùng
    message_placeholder.markdown(f'<div class="chat-message assistant-msg">{full_response}</div>', unsafe_allow_html=True)