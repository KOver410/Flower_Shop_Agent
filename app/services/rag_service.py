"""
RAG Service - Retrieval-Augmented Generation
Tìm kiếm thông tin liên quan trong database kiến thức
"""
import chromadb
from chromadb.config import Settings
import os
from typing import List, Optional

class RAGService:
    def __init__(self, knowledge_file: str = "data/flower_knowledge.txt"):
        """
        Khởi tạo RAG service với ChromaDB
        
        Args:
            knowledge_file: Đường dẫn đến file kiến thức
        """
        # Khởi tạo ChromaDB client
        self.client = chromadb.PersistentClient(
            path="data/vector_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Tên collection
        self.collection_name = "flower_knowledge"
        
        # Load knowledge và tạo embeddings
        self.setup_knowledge_base(knowledge_file)
    
    def setup_knowledge_base(self, knowledge_file: str):
        """
        Đọc file kiến thức và tạo vector embeddings
        
        Args:
            knowledge_file: Đường dẫn file kiến thức
        """
        try:
            # Xóa collection cũ nếu có
            try:
                self.client.delete_collection(name=self.collection_name)
            except:
                pass
            
            # Tạo collection mới
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Flower shop knowledge base"}
            )
            
            # Đọc file kiến thức
            if not os.path.exists(knowledge_file):
                print(f"Warning: Knowledge file {knowledge_file} not found")
                return
            
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chia nhỏ content thành chunks
            chunks = self._split_text_into_chunks(content)
            
            # Tạo embeddings và lưu vào ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({"chunk_id": i, "source": "flower_knowledge"})
                ids.append(f"chunk_{i}")
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Đã tạo knowledge base với {len(chunks)} chunks")
            
        except Exception as e:
            print(f"Lỗi khi setup knowledge base: {e}")
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Chia văn bản thành các chunks nhỏ
        
        Args:
            text: Văn bản gốc
            chunk_size: Kích thước mỗi chunk
            
        Returns:
            List[str]: Danh sách các chunks
        """
        # Chia theo đoạn văn trước
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # Nếu đoạn văn quá dài, chia nhỏ hơn
            if len(paragraph) > chunk_size:
                # Lưu chunk hiện tại nếu có
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # Chia đoạn văn dài thành nhiều chunks
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    if len(current_chunk + sentence) > chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + ". "
                    else:
                        current_chunk += sentence + ". "
            else:
                # Kiểm tra xem có vượt quá chunk_size không
                if len(current_chunk + paragraph) > chunk_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"
                else:
                    current_chunk += paragraph + "\n\n"
        
        # Thêm chunk cuối cùng
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 50]  # Loại bỏ chunks quá ngắn
    
    def search_relevant_info(self, query: str, max_results: int = 3) -> str:
        """
        Tìm kiếm thông tin liên quan đến câu hỏi
        
        Args:
            query: Câu hỏi từ user
            max_results: Số lượng kết quả tối đa
            
        Returns:
            str: Thông tin liên quan được ghép lại
        """
        try:
            # Tìm kiếm trong vector database
            results = self.collection.query(
                query_texts=[query],
                n_results=max_results
            )
            
            # Ghép các kết quả lại
            relevant_info = ""
            if results['documents'] and results['documents'][0]:
                for doc in results['documents'][0]:
                    relevant_info += doc + "\n\n"
            
            return relevant_info.strip()
            
        except Exception as e:
            print(f"Lỗi khi search RAG: {e}")
            return ""
    
    def get_collection_info(self) -> dict:
        """
        Lấy thông tin về collection
        
        Returns:
            dict: Thông tin collection
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "status": "ready"
            }
        except Exception as e:
            return {
                "collection_name": self.collection_name,
                "document_count": 0,
                "status": f"error: {e}"
            }

# Tạo instance global
rag_service = RAGService()
