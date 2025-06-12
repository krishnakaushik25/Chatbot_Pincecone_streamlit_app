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

4. **Configure Environment Variables (Secrets)**
   - After deployment, go to your app in the Streamlit Cloud dashboard
   - Click on your app name to open the app management page
   - Click on the **"Settings"** button (⚙️) in the top right
   - Navigate to the **"Secrets"** tab in the settings panel
   - Add your environment variables in TOML format:
     ```toml
     ENDPOINT = "https://your-api-endpoint.com"
     ```
   - Click **"Save"** to apply the secrets
   - Your app will automatically restart with the new configuration

5. **Deploy**
   - Click "Deploy!"
   - Wait for the deployment to complete
   - Your app will be available at the provided URL

### Managing Secrets in Streamlit Cloud

Your application is configured to read the `ENDPOINT` from Streamlit secrets in production. Here's how to manage secrets:

#### Adding/Updating Secrets:
1. **Access App Settings**
   - Go to [https://share.streamlit.io](https://share.streamlit.io)
   - Sign in and navigate to your apps
   - Click on your app name

2. **Open Settings**
   - Click the **"Settings"** button (⚙️) in the top-right corner
   - Select the **"Secrets"** tab

3. **Configure Secrets**
   - Add your secrets in TOML format:
     ```toml
     # API Configuration
     ENDPOINT = "https://your-api-endpoint.com"
     
     # Add other secrets as needed
     # API_KEY = "your-api-key"
     # DATABASE_URL = "your-database-url"
     ```

4. **Save and Deploy**
   - Click **"Save"**
   - Your app will automatically restart with the new configuration
   - Monitor the deployment logs for any issues

#### Important Notes:
- **TOML Format**: Streamlit Cloud uses TOML format for secrets, not `.env` format
- **Quotes Required**: Always wrap string values in quotes
- **No Comments in Production**: Remove comment lines when deploying
- **Case Sensitive**: Variable names are case-sensitive
- **Automatic Restart**: Apps restart automatically when secrets are updated

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

| Variable | Description | Required | Local (.env) | Cloud (Secrets) |
|----------|-------------|----------|--------------|-----------------|
| `ENDPOINT` | Your API backend URL | Yes | `ENDPOINT=https://your-api-endpoint.com` | `ENDPOINT = "https://your-api-endpoint.com"` |

**Note**: The application automatically detects whether it's running locally (uses `.env`) or on Streamlit Cloud (uses secrets).

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

**7. Streamlit Cloud secrets configuration**
- Error: App fails to start with "ENDPOINT environment variable not set" on Streamlit Cloud
- Solution: 
  1. Go to your app settings on Streamlit Cloud
  2. Navigate to the "Secrets" tab
  3. Add: `ENDPOINT = "https://your-api-endpoint.com"`
  4. Save and wait for app restart
- **Format**: Use TOML format with quotes, not `.env` format

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