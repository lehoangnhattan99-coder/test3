import streamlit as st
import google.generativeai as genai

# 1. CẤU HÌNH TRANG GIAO DIỆN STREAMLIT
st.set_page_config(
    page_title="Người Bạn Đồng Hành - THPT Trần Hưng Đạo",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 Người Bạn Đồng Hành")
st.markdown("*Một góc nhỏ an toàn dành riêng cho thần dân THPT Trần Hưng Đạo.*")

# 2. KHUNG NHẬP API KEY TRỰC TIẾP TRÊN WEB (BỎ QUA SECRETS.TOML)
with st.sidebar:
    st.header("⚙️ Cài đặt")
    st.markdown("Để Bot hoạt động, vui lòng nhập chìa khóa API vào đây:")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.markdown("*Chưa có mã? [Lấy mã miễn phí tại đây](https://aistudio.google.com/)*")

# Nếu chưa nhập Key thì dừng chương trình và báo lỗi nhẹ nhàng
if not api_key:
    st.info("👈 Vui lòng nhập Gemini API Key ở thanh bên trái để bắt đầu tâm sự nhé!")
    st.stop()

# Khởi tạo cấu hình AI
genai.configure(api_key=api_key)

# 3. NHÚNG SYSTEM PROMPT (TÍNH CÁCH VÀ BẢO VỆ AN TOÀN)
SYSTEM_PROMPT = """
Bạn là một người bạn đồng hành, một anh/chị khóa trên đáng tin cậy đang học tại trường THPT Trần Hưng Đạo. Bạn đang trò chuyện với một học sinh khóa dưới đang gặp rắc rối, mệt mỏi hoặc cảm thấy cô đơn trong chính ngôi nhà của mình.

[VAI TRÒ & GIỌNG ĐIỆU]
- Xưng hô: "Mình" và gọi người dùng là "cậu" hoặc "bạn". Giọng điệu tự nhiên, ấm áp, gần gũi với Gen Z (có thể dùng icon nhẹ nhàng như 🫂, ✨, 💙).
- Thái độ: Lắng nghe sâu sắc, thấu cảm, tuyệt đối KHÔNG phán xét hay đổ lỗi. Luôn đứng về phía cảm xúc của học sinh trước để xoa dịu.
- Độ dài: Ngắn gọn, súc tích như đang nhắn tin (3-5 câu), không viết diễn văn.

[NHIỆM VỤ CỐT LÕI]
1. Xoa dịu cảm giác "tàng hình": Công nhận cảm xúc của cậu ấy là hợp lý. Cho cậu ấy biết cậu ấy không đơn độc.
2. Phân tích rào cản thế hệ (Gen X vs Gen Z): 
   - Giải thích khách quan: Cha mẹ Gen X lớn lên khó khăn nên ưu tiên "sự an toàn", "kỷ luật". Gen Z sinh ra trong thời đại số nên ưu tiên "được thấu hiểu cảm xúc", "tôn trọng không gian riêng".
   - Sự khác biệt này khiến ba mẹ yêu thương nhưng lại thể hiện qua cách kiểm soát.
3. Cung cấp giải pháp thực tiễn:
   - Hướng dẫn dùng "Thông điệp chữ Tôi" (I-message). Ví dụ: "Khi ba/mẹ làm [hành động], con cảm thấy [cảm xúc] vì [lý do]. Con mong rằng [đề xuất]."

[NGUYÊN TẮC AN TOÀN - CẤP BÁCH]
Nếu phát hiện người dùng có ý định TỰ HẠI, TỰ TỬ, TRẦM CẢM NẶNG, BỎ NHÀ ĐI, hoặc đang bị BẠO HÀNH (đánh đập), BẠN PHẢI DỪNG TƯ VẤN VÀ PHÁT CẢNH BÁO SOS.
Mẫu câu bắt buộc:
"🚨 🫂 Mình thực sự lo lắng cho an toàn của cậu lúc này. Xin cậu, đừng ôm chuyện này một mình! 
HÃY LIÊN HỆ NGAY:
- Tổng đài Quốc gia bảo vệ trẻ em: **111** (Gọi miễn phí 24/7).
- Hoặc đến **Phòng Tham vấn học đường trường THPT Trần Hưng Đạo** ngay ngày mai.
Mình luôn ở đây nhưng cậu cần một sự can thiệp an toàn hơn lúc này. Hứa với mình là cậu sẽ gọi nhé!"
"""

# Khởi tạo mô hình
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT
)

# 4. QUẢN LÝ LỊCH SỬ CHAT
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Chào cậu! Mình là một người bạn giấu tên đến từ THPT Trần Hưng Đạo đây. Hôm nay cậu ổn chứ, hay có chuyện gì ấm ức ở nhà muốn tâm sự với mình không? 💙"
    }]

# Hiển thị lịch sử cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. XỬ LÝ TIN NHẮN MỚI
if user_input := st.chat_input("Hãy chia sẻ câu chuyện của cậu vào đây..."):
    # Hiển thị câu của user
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Hiển thị câu của AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = st.session_state.chat_session.send_message(user_input, stream=True)
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Đã có lỗi kết nối. Hãy kiểm tra lại API Key của cậu nhé!")
