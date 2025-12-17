import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Gemini Chatbot")

# --- THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.header("Cấu hình")
    
    # Nhập API Key
    api_key = st.text_input(
        "Nhập Google API Key", 
        type="password", 
        placeholder="Bắt đầu bằng AIza...",
        help="Lấy key miễn phí tại https://aistudio.google.com/"
    )
    
    # Chọn Model (Giúp khắc phục lỗi 404 bằng cách cho phép user đổi tên model)
    model_options = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-001",
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest"
    ]
    selected_model = st.selectbox("Chọn Model", model_options, index=1)
    
    st.info(f"Đang dùng model: `{selected_model}`")
    st.markdown("---")
    if st.button("Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

# --- KHỞI TẠO LỊCH SỬ CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HIỂN THỊ LỊCH SỬ ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- XỬ LÝ KHI NGƯỜI DÙNG NHẬP TIN NHẮN ---
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    
    # 1. Hiển thị tin nhắn người dùng
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Kiểm tra API Key
    if not api_key:
        st.error("⚠️ Vui lòng nhập API Key ở menu bên trái để bắt đầu.")
        st.stop()

    # 3. Gọi Google Gemini API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(selected_model)
        
        with st.chat_message("assistant"):
            with st.spinner("Đang suy nghĩ..."):
                # Gọi hàm generate_content
                response = model.generate_content(prompt)
                text_response = response.text
                
                st.markdown(text_response)
        
        # Lưu câu trả lời vào lịch sử
        st.session_state.messages.append({"role": "assistant", "content": text_response})

    except Exception as e:
        st.chat_message("assistant").error(f"❌ Đã xảy ra lỗi: {e}")
        
        # Gợi ý cụ thể nếu gặp lỗi 404
        if "404" in str(e):
            st.warning(
                "💡 **Gợi ý:** Lỗi 404 thường do tên Model không đúng hoặc chưa được hỗ trợ trên tài khoản của bạn. "
                "Hãy thử chọn một tên model khác (ví dụ: `gemini-1.5-flash-001`) ở menu bên trái."
            )