import streamlit as st
import ollama
import PyPDF2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import random

class PDFChatbot:
    def __init__(self, model="llama3.2"):
        self.model = model
        self.documents = []
        self.chunks = []
        self.vectorizer = TfidfVectorizer()
        self.full_text = ""
        self.context_loaded = False
    
    def load_pdf(self, pdf_file):
        """
        Load PDF and extract text
        """
        reader = PyPDF2.PdfReader(pdf_file)
        self.full_text = ""
        for page in reader.pages:
            self.full_text += page.extract_text()
        
        # Split text into chunks
        self.chunks = self._split_text(self.full_text)
        
        # Vectorize chunks
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
        self.context_loaded = True
        return len(self.chunks)
    
    def _split_text(self, text, chunk_size=300, overlap=50):
        """
        Split text into overlapping chunks
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i+chunk_size])
            chunks.append(chunk)
        return chunks
    
    def generate_comprehensive_summary(self):
        """
        Generate a comprehensive summary
        """
        try:
            summary_prompt = f"""Provide a comprehensive and detailed summary of the following text. 
            The summary should:
            1. Capture the main themes and key ideas
            2. Highlight the most important points
            3. Provide a structured overview of the content
            4. Be suitable for academic or professional use

            Text: {self.full_text[:10000]}  # Limit to first 10,000 characters to avoid token limits
            """
            
            summary_response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': 'You are an expert summarizer who creates comprehensive and clear summaries.'},
                {'role': 'user', 'content': summary_prompt}
            ])
            
            return summary_response['message']['content']
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def identify_difficult_topics(self):
        """
        Identify and explain topics that might be challenging for students
        """
        try:
            difficulty_prompt = f"""Analyze the following text and identify topics that might be difficult for students to understand. 
            For each difficult topic, provide:
            1. Why the topic is challenging
            2. Simplified explanation
            3. Study tips or strategies to better comprehend the topic
            4. Potential misconceptions students might have

            Text: {self.full_text[:10000]}  # Limit to first 10,000 characters to avoid token limits
            """
            
            difficulty_response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': 'You are an experienced educator who can break down complex topics for students.'},
                {'role': 'user', 'content': difficulty_prompt}
            ])
            
            return difficulty_response['message']['content']
        except Exception as e:
            return f"Error identifying difficult topics: {str(e)}"
    
    def generate_general_query_response(self, messages):
        """
        Generate response for general queries without PDF context
        """
        try:
            # Use entire conversation history for context
            response = ollama.chat(model=self.model, messages=messages)
            return response['message']['content']
        except Exception as e:
            return f"Error generating general response: {str(e)}"
    
    def generate_pdf_response(self, query, messages):
        """
        Generate response with PDF context
        """
        # Retrieve relevant context from PDF
        context = self.retrieve_relevant_context(query)
        
        # Construct prompt with context
        system_message = {
            'role': 'system', 
            'content': 'You are a helpful assistant skilled at extracting precise information from context and explaining it in a student-friendly manner.'
        }
        context_message = {
            'role': 'system', 
            'content': f"Context from PDF: {' '.join(context)}"
        }
        
        # Combine messages with context
        context_aware_messages = [system_message, context_message] + messages
        
        try:
            # Generate response using Ollama
            response = ollama.chat(model=self.model, messages=context_aware_messages)
            return response['message']['content']
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def retrieve_relevant_context(self, query, top_k=3):
        """
        Retrieve most relevant text chunks
        """
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # Get top K most similar chunks
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [self.chunks[i] for i in top_indices]

def main():
    # Page configuration
    st.set_page_config(page_title="PDF Chatbot", layout="wide")
    st.title("🤖 Intelligent PDF Chatbot")
    
    # Initialize session state for chatbot and chat history
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = PDFChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for PDF upload and additional features
    with st.sidebar:
        st.header("📄 PDF Upload")
        uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
        
        # PDF Processing
        if uploaded_file is not None:
            # Load PDF
            num_chunks = st.session_state.chatbot.load_pdf(uploaded_file)
            st.success(f"PDF loaded successfully! Split into {num_chunks} chunks.")
            
            # Additional PDF-specific buttons
            if st.button("Generate Comprehensive Summary"):
                summary = st.session_state.chatbot.generate_comprehensive_summary()
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"📋 PDF Summary:\n{summary}"
                })
            
            if st.button("Identify Difficult Topics"):
                difficult_topics = st.session_state.chatbot.identify_difficult_topics()
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"🧩 Difficult Topics:\n{difficult_topics}"
                })
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            # Prepare messages for context
            conversation_history = [
                msg for msg in st.session_state.messages 
                if msg['role'] in ['user', 'assistant']
            ]
            
            # Determine response generation method
            if st.session_state.chatbot.context_loaded:
                # PDF context available
                response = st.session_state.chatbot.generate_pdf_response(
                    prompt, 
                    conversation_history
                )
            else:
                # General query
                response = st.session_state.chatbot.generate_general_query_response(
                    conversation_history
                )
            
            # Display and store assistant response
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()