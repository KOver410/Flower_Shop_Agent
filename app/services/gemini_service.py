"""
Gemini AI Service - Xử lý tương tác với Google Gemini API
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self):
        """Khởi tạo Gemini service với API key"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY không được tìm thấy trong file .env")
        
        # Cấu hình Gemini
        genai.configure(api_key=api_key)
        
        # Khởi tạo model (sử dụng model mới)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System prompt cho chatbot cửa hàng hoa (cơ bản)
        self.system_prompt = """
        Bạn là chatbot chuyên nghiệp của cửa hàng hoa "Flower Garden".
        
        NHIỆM VỤ:
        - Sử dụng CHÍNH XÁC thông tin từ database được cung cấp
        - Trả lời dựa trên dữ liệu thực tế, không bịa đặt
        - Cung cấp giá cả, thông tin sản phẩm cụ thể từ database
        - Hướng dẫn khách hàng đặt hàng và liên hệ
        
        CÁCH TRẢ LỜI:
        - Thân thiện, chuyên nghiệp với emoji hoa 🌹🌸🌺
        - Trích dẫn CHÍNH XÁC giá cả và thông tin từ database
        - Khi không có thông tin, thừa nhận và hướng dẫn liên hệ
        - Luôn khuyến khích đặt hàng: 0123-456-789
        
        QUAN TRỌNG: Chỉ sử dụng thông tin từ database được cung cấp, không tự thêm thông tin!
        """
    
    async def chat(self, user_message: str, context: str = "") -> str:
        """
        Gửi tin nhắn đến Gemini và nhận phản hồi
        
        Args:
            user_message: Tin nhắn từ user
            context: Thông tin từ RAG system (tùy chọn)
            
        Returns:
            str: Phản hồi từ AI
        """
        try:
            # Tạo prompt với context từ RAG (nếu có)
            if context:
                full_prompt = f"{self.system_prompt}\n\nTHÔNG TIN LIÊN QUAN:\n{context}\n\nKhách hàng: {user_message}\nChatbot:"
            else:
                full_prompt = f"{self.system_prompt}\n\nKhách hàng: {user_message}\nChatbot:"
            
            # Gửi request đến Gemini
            response = self.model.generate_content(full_prompt)
            
            # Trả về response text
            return response.text
            
        except Exception as e:
            print(f"Lỗi khi gọi Gemini API: {e}")
            # Fallback response nếu AI lỗi
            return "Xin lỗi, tôi đang gặp sự cố kỹ thuật. Vui lòng liên hệ trực tiếp để được hỗ trợ tốt nhất! 🌸"

# Tạo instance global để sử dụng
gemini_service = GeminiService()
