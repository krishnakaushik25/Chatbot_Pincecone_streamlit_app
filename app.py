import streamlit as st
import requests
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ChatResponse:
    """Data class for API chat response"""
    answer: str
    show_enroll: bool
    suggested_questions: List[str]

class APIClient:
    """Handles all API communications"""
    
    def __init__(self):
        self.endpoint = os.getenv('ENDPOINT')
        if not self.endpoint:
            raise ValueError("ENDPOINT environment variable not set")
    
    def send_query(self, query: str) -> Optional[ChatResponse]:
        """Send user query to the answer endpoint"""
        try:
            url = f"{self.endpoint}/answer"
            payload = {"query": query}
            
            response = requests.post(
                url, 
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return ChatResponse(
                answer=data.get('answer', ''),
                show_enroll=data.get('show_enroll', False),
                suggested_questions=data.get('suggested_questions', [])
            )
            
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def upload_pdf(self, pdf_file) -> bool:
        """Upload PDF file to the server"""
        try:
            url = f"{self.endpoint}/uploadpdf"
            
            files = {'file': (pdf_file.name, pdf_file.getvalue(), 'application/pdf')}
            
            response = requests.post(
                url,
                files=files,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('success', False)
            
        except requests.exceptions.RequestException as e:
            st.error(f"PDF Upload Error: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Unexpected error during PDF upload: {str(e)}")
            return False

class ChatUI:
    """Handles chat interface rendering and state management"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "suggested_questions" not in st.session_state:
            st.session_state.suggested_questions = []
    
    def display_chat_history(self):
        """Display all chat messages"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
                # Display enrollment prompt if applicable
                if message["role"] == "assistant" and message.get("show_enroll"):
                    st.info("💡 Would you like to enroll for more information?")
    
    def display_suggested_questions(self):
        """Display suggested questions as clickable buttons"""
        if st.session_state.suggested_questions:
            st.write("**Suggested questions:**")
            cols = st.columns(len(st.session_state.suggested_questions))
            
            for idx, question in enumerate(st.session_state.suggested_questions):
                with cols[idx % len(cols)]:
                    if st.button(f"❓ {question[:50]}{'...' if len(question) > 50 else ''}", 
                               key=f"suggested_{idx}"):
                        self._handle_user_input(question)
    
    def _handle_user_input(self, user_input: str):
        """Process user input and get response"""
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get response from API
        with st.spinner("Thinking..."):
            response = self.api_client.send_query(user_input)
        
        if response:
            # Add assistant response to chat
            assistant_message = {
                "role": "assistant", 
                "content": response.answer,
                "show_enroll": response.show_enroll
            }
            st.session_state.messages.append(assistant_message)
            
            # Update suggested questions
            st.session_state.suggested_questions = response.suggested_questions
        else:
            # Add error message
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "I'm sorry, I encountered an error while processing your request. Please try again."
            })
    
    def render_chat_interface(self):
        """Render the main chat interface"""
        st.title("🤖 PDF Assistant Chatbot")
        
        # Display chat history
        self.display_chat_history()
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your documents..."):
            self._handle_user_input(prompt)
            st.rerun()
        
        # Display suggested questions
        self.display_suggested_questions()

class PDFUploader:
    """Handles PDF upload functionality"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    def render_upload_interface(self):
        """Render PDF upload interface in sidebar"""
        st.sidebar.title("📄 Document Upload")
        st.sidebar.markdown("Upload a PDF document to enhance the chatbot's knowledge.")
        
        uploaded_file = st.sidebar.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF document for the chatbot to analyze"
        )
        
        if uploaded_file is not None:
            # Display file info
            st.sidebar.success(f"File selected: {uploaded_file.name}")
            st.sidebar.info(f"Size: {uploaded_file.size / 1024:.1f} KB")
            
            # Upload button
            if st.sidebar.button("📤 Upload PDF", type="primary"):
                self._handle_pdf_upload(uploaded_file)
    
    def _handle_pdf_upload(self, pdf_file):
        """Handle PDF file upload"""
        with st.sidebar.spinner("Uploading PDF..."):
            success = self.api_client.upload_pdf(pdf_file)
        
        if success:
            st.sidebar.success("✅ PDF uploaded successfully!")
            st.sidebar.balloons()
        else:
            st.sidebar.error("❌ Failed to upload PDF. Please try again.")

class StreamlitApp:
    """Main application class that orchestrates all components"""
    
    def __init__(self):
        self._configure_page()
        self.api_client = self._initialize_api_client()
        self.chat_ui = ChatUI(self.api_client)
        self.pdf_uploader = PDFUploader(self.api_client)
    
    def _configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="PDF Assistant Chatbot",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def _initialize_api_client(self) -> APIClient:
        """Initialize API client with error handling"""
        try:
            return APIClient()
        except ValueError as e:
            st.error(f"Configuration Error: {str(e)}")
            st.info("Please make sure you have a `.env` file with the ENDPOINT variable set.")
            st.stop()
    
    def run(self):
        """Run the main application"""
        # Render sidebar (PDF upload)
        self.pdf_uploader.render_upload_interface()
        
        # Add sidebar info
        with st.sidebar:
            st.markdown("---")
            st.markdown("### ℹ️ How to use")
            st.markdown("""
            1. **Upload a PDF** using the file uploader above
            2. **Ask questions** about your document in the chat
            3. **Click suggested questions** for quick interactions
            4. **View enrollment prompts** when available
            """)
        
        # Render main chat interface
        self.chat_ui.render_chat_interface()

def main():
    """Application entry point"""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()