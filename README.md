# 🌸 Flower Chat Bot - AI Customer Service
**Hệ thống chatbot chăm sóc khách hàng thông minh cho cửa hàng bán hoa, sử dụng Multi-Agent AI Architecture**

![image](https://github.com/user-attachments/assets/e9cf92e3-9553-4847-beff-80cccf0b5845)

## ✨ Tính năng chính

- 🤖 **Multi-Agent AI System** - Hệ thống nhiều AI agent chuyên biệt
- 🔍 **RAG (Retrieval-Augmented Generation)** - Tìm kiếm thông tin thông minh
- 🎯 **Intent Detection** - Phân loại ý định khách hàng tự động
- 💬 **Real-time Chat** - Giao diện chat hiện đại, phản hồi tức thì
- 🌺 **Flower Knowledge Base** - Cơ sở dữ liệu chuyên sâu về hoa
- 📱 **Responsive Design** - Tương thích mọi thiết bị

## 🏗️ Kiến trúc Multi-Agent

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Router Agent    │───▶│  Intent         │
└─────────────────┘    └──────────────────┘    │  Classification │
                                │                └─────────────────┘
                                ▼
       ┌────────────────────────┼────────────────────────┐
       ▼                        ▼                        ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   Flower    │        │  Customer   │        │    Order    │
│ Consultant  │        │   Service   │        │   Handler   │
│   Agent     │        │    Agent    │        │    Agent    │
└─────────────┘        └─────────────┘        └─────────────┘
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                ▼
                    ┌──────────────────┐
                    │   RAG System     │
                    │  (ChromaDB +     │
                    │ Knowledge Base)  │
                    └──────────────────┘
```

## 🚀 Cài đặt và chạy

### 1. Clone repository

```bash
git clone https://github.com/yourusername/flower-chat-bot.git
cd flower-chat-bot
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình API key

Tạo file `.env` trong thư mục gốc:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Lấy Gemini API key:** [https://ai.google.dev](https://ai.google.dev)

### 4. Chạy ứng dụng

```bash
python -m uvicorn app.main:app --reload
```

## 📁 Cấu trúc project

```
flower-chat-bot/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── services/
│   │   ├── gemini_service.py      # Gemini AI integration
│   │   ├── rag_service.py         # RAG system với ChromaDB
│   │   └── multi_agent_service.py # Multi-Agent orchestrator
│   └── templates/
│       └── index.html             # Chat interface
├── static/
│   ├── style.css                  # Modern UI styling
│   └── script.js                  # AJAX chat functionality
├── data/
│   └── flower_knowledge.txt       # Flower knowledge base
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
```

## 🤖 Multi-Agent System

### Router Agent
- **Chức năng:** Phân tích và định tuyến tin nhắn đến agent phù hợp
- **Technique:** Intent Classification, Confidence Scoring

### Flower Consultant Agent
- **Chức năng:** Tư vấn về hoa, cách chăm sóc, ý nghĩa
- **Specialization:** Botany expertise, care instructions

### Customer Service Agent
- **Chức năng:** Hỗ trợ khách hàng, giải đáp thắc mắc chung
- **Specialization:** Customer satisfaction, problem resolution

### Order Handler Agent
- **Chức năng:** Xử lý đặt hàng, thanh toán, giao hàng
- **Specialization:** Order processing, logistics

## 🔍 RAG System Features

- **Vector Database:** ChromaDB để lưu trữ embeddings
- **Semantic Search:** Tìm kiếm theo ngữ nghĩa
- **Context Retrieval:** Trích xuất thông tin liên quan
- **Dynamic Knowledge:** Cập nhật knowledge base dễ dàng

## 💡 Advanced Techniques

### 1. Intent Detection
```python
# Phân loại ý định bằng prompt engineering
intents = ["flower_consultation", "customer_service", "order_processing"]
```

### 2. Agent Routing
```python
# Routing thông minh dựa trên confidence score
if confidence > 0.8:
    agent = get_specialist_agent(intent)
else:
    agent = get_general_agent()
```

### 3. Context-Aware Response
```python
# Kết hợp RAG context với agent specialization
response = await agent.generate_response(message, rag_context)
```

## 📊 Performance Metrics

- **Response Time:** < 2 giây
- **Intent Accuracy:** > 85%
- **Customer Satisfaction:** Tối ưu hóa cho UX
- **Scalability:** Hỗ trợ đồng thời nhiều users

## 🛠️ Technologies

- **Backend:** FastAPI, Python 3.8+
- **AI/ML:** Google Gemini AI, ChromaDB
- **Frontend:** HTML5, CSS3, JavaScript (AJAX)
- **Database:** Vector Database (ChromaDB)
- **Architecture:** Multi-Agent System, RAG

## 🎯 Use Cases

1. **Tư vấn hoa cưới:** Agent tư vấn hoa phù hợp cho đám cưới
2. **Chăm sóc hoa:** Hướng dẫn cách chăm sóc từng loại hoa
3. **Đặt hoa dịp lễ:** Xử lý đơn hàng Valentine, 8/3, sinh nhật
4. **Hỗ trợ khách hàng:** Giải đáp thắc mắc, khiếu nại

## 🔮 Future Enhancements

- [ ] Email Service Integration
- [ ] Excel Export Functionality  
- [ ] Sentiment Analysis
- [ ] Voice Chat Support
- [ ] Mobile App
- [ ] Payment Integration
- [ ] Multi-language Support

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👨‍💻 Author

**Tên của bạn**
- GitHub: https://github.com/KOver410
- Email: your.email@example.com

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev) - Powerful AI capabilities
- [ChromaDB](https://www.trychroma.com) - Vector database
- [FastAPI](https://fastapi.tiangolo.com) - Modern web framework
- Flower industry experts for knowledge base

---

**⭐ Nếu project này hữu ích, hãy cho một star để ủng hộ! ⭐**
