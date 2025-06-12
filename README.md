# PDF Assistant Chatbot 🤖

A Streamlit-based chatbot application that allows users to upload PDF documents and ask questions about their content. The application features a clean interface, comprehensive error handling, and real-time chat functionality.

## Features

- 📄 **PDF Upload**: Upload PDF documents (up to 50MB) for analysis
- 💬 **Interactive Chat**: Ask questions about your uploaded documents
- 🔍 **Real-time Processing**: Get instant responses powered by your API backend
- 🛡️ **Error Handling**: Comprehensive error handling with user-friendly messages
- 🐛 **Debug Mode**: Toggle debug mode for detailed error information
- 📊 **Connection Status**: Monitor API connectivity status
- 🎨 **Clean UI**: Modern, responsive interface built with Streamlit

## Prerequisites

- Python 3.7 or higher
- A running API backend with `/answer` and `/uploadpdf` endpoints
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd pdf-assistant-chatbot
```

### 2. Create a Virtual Environment

#### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**If you encounter an execution policy error in PowerShell:**
```powershell
# Check current execution policy
Get-ExecutionPolicy

# If it's "Restricted", temporarily allow script execution for current session
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate the virtual environment
venv\Scripts\Activate.ps1
```

**Alternative PowerShell activation methods:**
```powershell
# Method 1: Direct activation
& venv\Scripts\Activate.ps1

# Method 2: If above fails, use the batch file
venv\Scripts\activate.bat
```

#### macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the environment template:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file and add your API endpoint:
   ```
   ENDPOINT=https://your-api-endpoint.com
   ```

   **Important**: Replace `https://your-api-endpoint.com` with your actual API endpoint URL.

## Running Locally

1. Ensure your virtual environment is activated
2. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and navigate to `http://localhost:8501`

## Deploying to Streamlit Cloud

### Prerequisites for Deployment
- GitHub account
- Your code pushed to a GitHub repository
- Streamlit Cloud account

### Step-by-Step Deployment

1. **Prepare Your Repository**
   - Ensure all files are committed to your GitHub repository
   - Make sure your `.env` file is **NOT** committed (it should be in `.gitignore`)

2. **Login to Streamlit Cloud**
   - Go to [https://share.streamlit.io/new](https://share.streamlit.io/new)
   - Sign in with your GitHub account

3. **Create New App**
   - Click "New app"
   - Select your GitHub repository
   - Set the main file path to `app.py`
   - Choose a custom URL (optional)

4. **Configure Environment Variables**
   - In the Streamlit Cloud dashboard, go to your app settings
   - Navigate to the "Secrets" section
   - Add your environment variables in TOML format:
     ```toml
     ENDPOINT = "https://your-api-endpoint.com"
     ```

5. **Deploy**
   - Click "Deploy!"
   - Wait for the deployment to complete
   - Your app will be available at the provided URL

### Alternative: Using Streamlit Cloud Secrets

Instead of using a `.env` file in production, Streamlit Cloud uses secrets management. Update your `app.py` to handle both local `.env` files and Streamlit secrets:

```python
# In your app.py, modify the endpoint loading:
import streamlit as st

# Load environment variables
load_dotenv()

def get_endpoint():
    # Try Streamlit secrets first, then fall back to .env
    endpoint = st.secrets.get("ENDPOINT") or os.getenv('ENDPOINT')
    return endpoint
```

## Project Structure

```
pdf-assistant-chatbot/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env.template         # Environment template
├── .env                  # Your environment variables (local only)
├── .gitignore           # Git ignore file
├── README.md            # This file
└── logs/                # Application logs (created automatically)
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ENDPOINT` | Your API backend URL | Yes |

### API Requirements

Your API backend should provide:

- **POST** `/answer`
  - Accepts: `{"query": "user question"}`
  - Returns: `{"answer": "response text"}`

- **POST** `/uploadpdf`
  - Accepts: PDF file upload
  - Returns: `{"success": true/false}`

## Usage

1. **Upload a PDF**: Use the sidebar file uploader to upload your PDF document
2. **Ask Questions**: Type your questions in the chat input at the bottom
3. **View Responses**: The chatbot will provide answers based on your uploaded documents
4. **Debug Mode**: Toggle debug mode in the sidebar to see detailed error information
5. **Connection Test**: Use the "Test Connection" button to verify API connectivity

## Troubleshooting

### Common Issues

**1. "ENDPOINT environment variable not set"**
- Solution: Make sure your `.env` file exists and contains the correct `ENDPOINT` value

**2. "Cannot connect to API server"**
- Solution: Verify your API endpoint is running and accessible
- Check your internet connection
- Use the "Test Connection" button to diagnose issues

**3. PowerShell execution policy error**
- Error: `cannot be loaded because running scripts is disabled on this system`
- Solution: Run PowerShell as Administrator and execute:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Alternative: Use Command Prompt instead of PowerShell for virtual environment activation

**4. "File too large" error**
- Solution: The application supports PDF files up to 50MB
- Try compressing your PDF or use a smaller file

**5. Upload fails**
- Solution: Ensure your file is a valid PDF
- Check your internet connection
- Verify the API `/uploadpdf` endpoint is working

**6. Virtual environment activation issues**
- **Windows**: If `venv\Scripts\Activate.ps1` fails, try `venv\Scripts\activate.bat`
- **macOS/Linux**: If `source venv/bin/activate` fails, ensure you're using the correct shell (bash/zsh)
- **All platforms**: Verify Python is installed and accessible via `python --version`

### Logs

Application logs are stored in `chatbot_app.log` for debugging purposes. Check this file for detailed error information when troubleshooting issues.

### Debug Mode

Enable debug mode in the sidebar to see:
- Detailed error messages
- API response information
- Request/response timing
- Server connection status

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter issues:

1. Check the logs in `chatbot_app.log`
2. Enable debug mode for detailed error information
3. Verify your API endpoint is accessible
4. Check the troubleshooting section above

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Quick Start Checklist

- [ ] Clone the repository
- [ ] Create and activate virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Copy `.env.template` to `.env`
- [ ] Configure your `ENDPOINT` in `.env`
- [ ] Run locally (`streamlit run app.py`)
- [ ] Test PDF upload and chat functionality
- [ ] Deploy to Streamlit Cloud (optional)

**Happy chatting! 🚀**