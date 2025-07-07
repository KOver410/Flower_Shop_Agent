from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import AI services
from app.services.gemini_service import gemini_service
from app.services.rag_service import rag_service
from app.services.multi_agent_service import get_multi_agent_orchestrator

# Tạo FastAPI app
app = FastAPI(title="Flower Chatbot", description="Chatbot chăm sóc khách hàng cửa hàng hoa")

# Cấu hình static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình templates (HTML files)
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(message: str = Form(...)):
    """
    Endpoint nhận tin nhắn từ user và trả lời bằng Multi-Agent AI System
    """
    try:
        # Debug: Log tin nhắn
        print(f"Received message: {message}")
        
        # Khởi tạo Multi-Agent Orchestrator
        orchestrator = get_multi_agent_orchestrator(gemini_service, rag_service)
        
        # Xử lý message qua Multi-Agent System
        result = await orchestrator.process_message(message)
        
        print(f"Agent used: {result['agent_used']}")
        print(f"Intent detected: {result['intent']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Response: {result['response'][:100]}...")
        
        return {"response": result['response']}
        
    except Exception as e:
        print(f"Lỗi chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return {"response": "Xin lỗi, tôi đang gặp sự cố. Vui lòng thử lại sau!"}


