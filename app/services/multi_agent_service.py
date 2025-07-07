"""
Multi-Agent System cho Flower Chatbot
Technique: Agent-based Architecture, Intent Classification, Specialized Prompting
"""

import asyncio
from typing import Dict, List, Optional
from enum import Enum
import re

class AgentType(Enum):
    ROUTER = "router"
    FLOWER_CONSULTANT = "flower_consultant"
    CUSTOMER_SERVICE = "customer_service"
    ORDER_HANDLER = "order_handler"

class Intent(Enum):
    # Flower consultation intents
    FLOWER_ADVICE = "flower_advice"
    FLOWER_CARE = "flower_care"
    FLOWER_RECOMMENDATION = "flower_recommendation"
    
    # Customer service intents
    GENERAL_INFO = "general_info"
    COMPLAINT = "complaint"
    PRAISE = "praise"
    
    # Order handling intents
    ORDER_INQUIRY = "order_inquiry"
    PRICE_CHECK = "price_check"
    DELIVERY_INFO = "delivery_info"
    
    # Default
    UNKNOWN = "unknown"

class BaseAgent:
    """Base class cho tất cả agents"""
    
    def __init__(self, agent_type: AgentType, gemini_service, rag_service):
        self.agent_type = agent_type
        self.gemini_service = gemini_service
        self.rag_service = rag_service
        
    async def process(self, message: str, context: str = "", **kwargs) -> str:
        """Override trong các agent con"""
        raise NotImplementedError

class RouterAgent(BaseAgent):
    """
    Router Agent - Phân tích ý định và định tuyến
    Technique: Intent Classification using keyword matching + AI classification
    """
    
    def __init__(self, gemini_service, rag_service):
        super().__init__(AgentType.ROUTER, gemini_service, rag_service)
        
        # Intent classification keywords
        self.intent_keywords = {
            Intent.FLOWER_ADVICE: [
                "tư vấn", "gợi ý", "recommend", "đề xuất", "chọn hoa", "loại hoa nào",
                "hoa gì", "nên mua", "phù hợp", "suitable", "advice"
            ],
            Intent.FLOWER_CARE: [
                "chăm sóc", "care", "bảo quản", "tưới", "water", "giữ tươi",
                "preserve", "maintain", "how to care", "cách chăm"
            ],
            Intent.FLOWER_RECOMMENDATION: [
                "sinh nhật", "valentine", "tết", "8/3", "20/10", "anniversary",
                "wedding", "cưới", "kỷ niệm", "special occasion"
            ],
            Intent.ORDER_INQUIRY: [
                "đặt hàng", "order", "mua", "buy", "purchase", "đặt", "book"
            ],
            Intent.PRICE_CHECK: [
                "giá", "price", "cost", "bao nhiêu", "how much", "chi phí", "expense"
            ],
            Intent.DELIVERY_INFO: [
                "giao hàng", "delivery", "ship", "vận chuyển", "transport", "đến"
            ],
            Intent.COMPLAINT: [
                "khiếu nại", "complaint", "tệ", "bad", "không hài lòng", "dissatisfied",
                "problem", "vấn đề", "lỗi"
            ],
            Intent.PRAISE: [
                "tốt", "good", "excellent", "tuyệt vời", "hài lòng", "satisfied",
                "perfect", "amazing", "cảm ơn", "thank"
            ]
        }
    
    def classify_intent_by_keywords(self, message: str) -> Intent:
        """Technique: Keyword-based Intent Classification"""
        message_lower = message.lower()
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword.lower() in message_lower:
                    return intent
        
        return Intent.UNKNOWN
    
    async def classify_intent_by_ai(self, message: str) -> Intent:
        """Technique: AI-based Intent Classification"""
        classification_prompt = f"""
        Phân loại ý định của khách hàng dựa trên tin nhắn sau:
        "{message}"
        
        Các loại ý định:
        1. flower_advice - Tư vấn về loại hoa
        2. flower_care - Hướng dẫn chăm sóc hoa  
        3. flower_recommendation - Gợi ý hoa cho dịp đặc biệt
        4. order_inquiry - Hỏi về đặt hàng
        5. price_check - Hỏi về giá cả
        6. delivery_info - Hỏi về giao hàng
        7. complaint - Khiếu nại, phàn nàn
        8. praise - Khen ngợi, cảm ơn
        9. general_info - Thông tin chung
        10. unknown - Không xác định được
        
        Trả lời chỉ MỘT từ khóa ý định phù hợp nhất:
        """
        
        try:
            response = await self.gemini_service.chat(classification_prompt, "")
            intent_str = response.strip().lower()
            
            # Map AI response to Intent enum
            intent_mapping = {
                "flower_advice": Intent.FLOWER_ADVICE,
                "flower_care": Intent.FLOWER_CARE,
                "flower_recommendation": Intent.FLOWER_RECOMMENDATION,
                "order_inquiry": Intent.ORDER_INQUIRY,
                "price_check": Intent.PRICE_CHECK,
                "delivery_info": Intent.DELIVERY_INFO,
                "complaint": Intent.COMPLAINT,
                "praise": Intent.PRAISE,
                "general_info": Intent.GENERAL_INFO,
                "unknown": Intent.UNKNOWN
            }
            
            return intent_mapping.get(intent_str, Intent.UNKNOWN)
            
        except Exception as e:
            print(f"AI intent classification error: {e}")
            return Intent.UNKNOWN
    
    async def route_to_agent(self, message: str) -> Dict:
        """
        Technique: Hybrid Intent Classification (Keywords + AI)
        """
        # Step 1: Try keyword classification first (faster)
        intent = self.classify_intent_by_keywords(message)
        
        # Step 2: If uncertain, use AI classification
        if intent == Intent.UNKNOWN:
            intent = await self.classify_intent_by_ai(message)
        
        # Step 3: Map intent to appropriate agent
        if intent in [Intent.FLOWER_ADVICE, Intent.FLOWER_CARE, Intent.FLOWER_RECOMMENDATION]:
            return {
                "agent": AgentType.FLOWER_CONSULTANT,
                "intent": intent,
                "confidence": "high" if intent != Intent.UNKNOWN else "medium"
            }
        elif intent in [Intent.ORDER_INQUIRY, Intent.PRICE_CHECK, Intent.DELIVERY_INFO]:
            return {
                "agent": AgentType.ORDER_HANDLER,
                "intent": intent,
                "confidence": "high" if intent != Intent.UNKNOWN else "medium"
            }
        elif intent in [Intent.COMPLAINT, Intent.PRAISE, Intent.GENERAL_INFO]:
            return {
                "agent": AgentType.CUSTOMER_SERVICE,
                "intent": intent,
                "confidence": "high" if intent != Intent.UNKNOWN else "medium"
            }
        else:
            # Default to customer service for unknown intents
            return {
                "agent": AgentType.CUSTOMER_SERVICE,
                "intent": Intent.GENERAL_INFO,
                "confidence": "low"
            }

class FlowerConsultantAgent(BaseAgent):
    """
    Flower Consultant Agent - Chuyên gia tư vấn hoa
    Technique: Role-based Prompting, Domain-specific Knowledge
    """
    
    def __init__(self, gemini_service, rag_service):
        super().__init__(AgentType.FLOWER_CONSULTANT, gemini_service, rag_service)
    
    async def process(self, message: str, context: str = "", intent: Intent = None, **kwargs) -> str:
        """Technique: Specialized Role-based Prompting"""
        
        consultant_prompt = f"""
        Bạn là một CHUYÊN GIA TƯ VẤN HOA có 10 năm kinh nghiệm, làm việc tại cửa hàng hoa cao cấp.
        
        Đặc điểm của bạn:
        - Hiểu biết sâu về từng loại hoa, ý nghĩa, cách chăm sóc
        - Tư vấn chính xác dựa trên nhu cầu khách hàng
        - Giọng điệu chuyên nghiệp nhưng thân thiện
        - Luôn đưa ra gợi ý cụ thể và thực tế
        
        Thông tin về sản phẩm của cửa hàng:
        {context}
        
        Khách hàng hỏi: "{message}"
        
        Hãy tư vấn một cách chuyên nghiệp, bao gồm:
        1. Hiểu rõ nhu cầu của khách
        2. Đề xuất các loại hoa phù hợp
        3. Giải thích lý do tại sao phù hợp
        4. Hướng dẫn chăm sóc (nếu cần)
        5. Gợi ý thêm (phụ kiện, cách trang trí...)
        
        Trả lời:
        """
        
        response = await self.gemini_service.chat(consultant_prompt, "")
        return response

class CustomerServiceAgent(BaseAgent):
    """
    Customer Service Agent - Chăm sóc khách hàng  
    Technique: Sentiment Analysis, Empathetic Response
    """
    
    def __init__(self, gemini_service, rag_service):
        super().__init__(AgentType.CUSTOMER_SERVICE, gemini_service, rag_service)
    
    def analyze_sentiment(self, message: str) -> str:
        """Technique: Simple Sentiment Analysis"""
        positive_words = ["tốt", "good", "tuyệt", "excellent", "hài lòng", "cảm ơn", "thank"]
        negative_words = ["tệ", "bad", "không hài lòng", "khiếu nại", "complaint", "vấn đề"]
        
        message_lower = message.lower()
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    async def process(self, message: str, context: str = "", intent: Intent = None, **kwargs) -> str:
        """Technique: Sentiment-aware Response Generation"""
        
        sentiment = self.analyze_sentiment(message)
        
        if sentiment == "negative":
            service_prompt = f"""
            Bạn là một NHÂN VIÊN CHĂM SÓC KHÁCH HÀNG chuyên nghiệp, đang xử lý một tình huống KHIẾU NẠI.
            
            Thái độ của bạn:
            - Thấu hiểu và đồng cảm với khách hàng
            - Xin lỗi chân thành và nghiêm túc
            - Đưa ra giải pháp cụ thể
            - Cam kết cải thiện dịch vụ
            
            Thông tin cửa hàng:
            {context}
            
            Khách hàng phản ánh: "{message}"
            
            Hãy trả lời một cách chuyên nghiệp để:
            1. Thể hiện sự đồng cảm
            2. Xin lỗi chân thành  
            3. Đưa ra giải pháp khắc phục
            4. Cam kết cải thiện
            5. Mời khách hàng liên hệ trực tiếp nếu cần
            
            Trả lời:
            """
        elif sentiment == "positive":
            service_prompt = f"""
            Bạn là một NHÂN VIÊN CHĂM SÓC KHÁCH HÀNG đang nhận được lời khen từ khách.
            
            Thái độ của bạn:
            - Vui mừng và biết ơn
            - Khuyến khích khách hàng tiếp tục sử dụng dịch vụ
            - Giới thiệu thêm sản phẩm/dịch vụ khác
            
            Thông tin cửa hàng:
            {context}
            
            Khách hàng nói: "{message}"
            
            Hãy trả lời để:
            1. Cảm ơn khách hàng
            2. Thể hiện sự vui mừng
            3. Khuyến khích tiếp tục sử dụng dịch vụ
            4. Giới thiệu sản phẩm/dịch vụ mới (nếu phù hợp)
            
            Trả lời:
            """
        else:
            service_prompt = f"""
            Bạn là một NHÂN VIÊN CHĂM SÓC KHÁCH HÀNG thân thiện và chuyên nghiệp.
            
            Thái độ của bạn:
            - Nhiệt tình và sẵn sàng hỗ trợ
            - Cung cấp thông tin chính xác
            - Tạo cảm giác thoải mái cho khách hàng
            
            Thông tin cửa hàng:
            {context}
            
            Khách hàng hỏi: "{message}"
            
            Hãy trả lời một cách thân thiện và hữu ích.
            
            Trả lời:
            """
        
        response = await self.gemini_service.chat(service_prompt, "")
        return response

class OrderHandlerAgent(BaseAgent):
    """
    Order Handler Agent - Xử lý đơn hàng
    Technique: Structured Information Extraction, Process-oriented Response
    """
    
    def __init__(self, gemini_service, rag_service):
        super().__init__(AgentType.ORDER_HANDLER, gemini_service, rag_service)
    
    def extract_order_info(self, message: str) -> Dict:
        """Technique: Pattern Matching for Information Extraction"""
        order_info = {
            "product": None,
            "quantity": None,
            "budget": None,
            "occasion": None,
            "delivery_date": None
        }
        
        # Extract quantity
        quantity_pattern = r'(\d+)\s*(bó|cành|hoa|bunch)'
        quantity_match = re.search(quantity_pattern, message.lower())
        if quantity_match:
            order_info["quantity"] = quantity_match.group(1)
        
        # Extract budget  
        budget_pattern = r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:k|nghìn|triệu|đồng|vnd)'
        budget_match = re.search(budget_pattern, message.lower())
        if budget_match:
            order_info["budget"] = budget_match.group(1)
        
        return order_info
    
    async def process(self, message: str, context: str = "", intent: Intent = None, **kwargs) -> str:
        """Technique: Process-oriented Response with Information Extraction"""
        
        order_info = self.extract_order_info(message)
        
        if intent == Intent.ORDER_INQUIRY:
            order_prompt = f"""
            Bạn là một CHUYÊN VIÊN XỬ LÝ ĐƠN HÀNG chuyên nghiệp tại cửa hàng hoa.
            
            Nhiệm vụ của bạn:
            - Hướng dẫn khách hàng quy trình đặt hàng
            - Thu thập thông tin đơn hàng đầy đủ
            - Tư vấn sản phẩm phù hợp
            - Xác nhận thông tin giao hàng
            
            Thông tin sản phẩm:
            {context}
            
            Thông tin đã thu thập được:
            - Số lượng: {order_info.get('quantity', 'Chưa có')}
            - Ngân sách: {order_info.get('budget', 'Chưa có')}
            
            Khách hàng: "{message}"
            
            Hãy hướng dẫn khách hàng từng bước:
            1. Xác nhận nhu cầu
            2. Thu thập thông tin còn thiếu (loại hoa, số lượng, ngân sách, dịp...)
            3. Đề xuất sản phẩm phù hợp
            4. Hướng dẫn quy trình đặt hàng
            5. Thông tin liên hệ để xác nhận đơn
            
            Trả lời:
            """
        elif intent == Intent.PRICE_CHECK:
            order_prompt = f"""
            Bạn là một CHUYÊN VIÊN BÁO GIÁ tại cửa hàng hoa.
            
            Thông tin giá cả sản phẩm:
            {context}
            
            Khách hàng hỏi về giá: "{message}"
            
            Hãy:
            1. Cung cấp giá cả cụ thể và chính xác
            2. Giải thích các yếu tố ảnh hưởng đến giá (loại hoa, mùa, kích thước...)
            3. Đề xuất các lựa chọn trong tầm giá
            4. Thông tin về chính sách giá (giảm giá, khuyến mãi...)
            
            Trả lời:
            """
        else:  # DELIVERY_INFO
            order_prompt = f"""
            Bạn là một CHUYÊN VIÊN GIAO HÀNG tại cửa hàng hoa.
            
            Thông tin dịch vụ giao hàng:
            {context}
            
            Khách hàng hỏi về giao hàng: "{message}"
            
            Hãy cung cấp:
            1. Khu vực giao hàng
            2. Thời gian giao hàng
            3. Phí giao hàng
            4. Quy trình đặt hàng và giao hàng
            5. Chính sách đổi trả
            
            Trả lời:
            """
        
        response = await self.gemini_service.chat(order_prompt, "")
        return response

class MultiAgentOrchestrator:
    """
    Multi-Agent Orchestrator - Điều phối các agents
    Technique: Agent Orchestration, Fallback Mechanism
    """
    
    def __init__(self, gemini_service, rag_service):
        self.gemini_service = gemini_service
        self.rag_service = rag_service
        
        # Initialize agents
        self.router = RouterAgent(gemini_service, rag_service)
        self.flower_consultant = FlowerConsultantAgent(gemini_service, rag_service)
        self.customer_service = CustomerServiceAgent(gemini_service, rag_service)
        self.order_handler = OrderHandlerAgent(gemini_service, rag_service)
        
        # Agent mapping
        self.agents = {
            AgentType.FLOWER_CONSULTANT: self.flower_consultant,
            AgentType.CUSTOMER_SERVICE: self.customer_service,
            AgentType.ORDER_HANDLER: self.order_handler
        }
    
    async def process_message(self, message: str) -> Dict:
        """
        Main orchestration method
        Technique: Agent Routing with Fallback
        """
        try:
            # Step 1: Route message to appropriate agent
            routing_result = await self.router.route_to_agent(message)
            
            print(f"Router result: {routing_result}")
            
            # Step 2: Get relevant context from RAG
            context = self.rag_service.search_relevant_info(message)
            
            # Step 3: Process with selected agent
            selected_agent = self.agents[routing_result["agent"]]
            response = await selected_agent.process(
                message=message,
                context=context,
                intent=routing_result["intent"]
            )
            
            return {
                "response": response,
                "agent_used": routing_result["agent"].value,
                "intent": routing_result["intent"].value,
                "confidence": routing_result["confidence"]
            }
            
        except Exception as e:
            print(f"Multi-agent error: {e}")
            # Fallback to customer service
            context = self.rag_service.search_relevant_info(message)
            response = await self.customer_service.process(message, context)
            
            return {
                "response": response,
                "agent_used": "customer_service_fallback",
                "intent": "error_fallback",
                "confidence": "low"
            }

# Global instance
multi_agent_orchestrator = None

def get_multi_agent_orchestrator(gemini_service, rag_service):
    """Factory function để tạo Multi-Agent Orchestrator"""
    global multi_agent_orchestrator
    if multi_agent_orchestrator is None:
        multi_agent_orchestrator = MultiAgentOrchestrator(gemini_service, rag_service)
    return multi_agent_orchestrator
