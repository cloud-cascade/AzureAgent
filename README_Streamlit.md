# Azure AI Assistant - Streamlit Web Interface

A modern web-based chat interface for the Azure AI Assistant, built with Streamlit. This app provides the same functionality as the command-line version (`sk_main_agent.py`) but with a beautiful, user-friendly web interface.

## Features

- 🤖 **Web-based Chat Interface**: Modern, responsive chat UI built with Streamlit
- 🔧 **Easy Configuration**: Sidebar panel for agent initialization and status monitoring
- 💬 **Real-time Chat**: Interactive chat with the Azure AI Assistant
- 🎨 **Beautiful UI**: Custom styling with modern design elements
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔄 **Session Management**: Maintains chat history during the session
- 🧹 **Clear Chat**: Easy way to start fresh conversations

## File Structure

```
AzureAgent/
├── sk_main_agent.py          # Original command-line version
├── agent_service.py          # Core agent logic (extracted from sk_main_agent.py)
├── streamlit_app.py          # Streamlit web interface
├── requirements_streamlit.txt # Dependencies for Streamlit app
└── README_Streamlit.md       # This file
```

## Prerequisites

1. **Python 3.12+** installed on your system
2. **Azure CLI** installed and authenticated (`az login`)
3. **Node.js** and **npm** (for MCP server)
4. **Environment variables** configured in `.env` file

## Installation

### Option 1: Using pip (Recommended)

1. Navigate to the AzureAgent directory:
   ```bash
   cd AzureAgent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements_streamlit.txt
   ```

### Option 2: Using uv (if you prefer uv)

1. Install dependencies:
   ```bash
   uv pip install -r requirements_streamlit.txt
   ```

## Configuration

1. Create a `.env` file in the AzureAgent directory with your Azure OpenAI credentials:
   ```env
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key
   ```

2. Ensure you're authenticated with Azure:
   ```bash
   az login
   ```

## Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

2. The app will open in your default web browser at `http://localhost:8501`

3. If it doesn't open automatically, manually navigate to the URL shown in the terminal

## How to Use

### 1. Initialize the Agent
- Click the "🚀 Initialize Agent" button in the sidebar
- Wait for the initialization to complete
- The status indicator will show "🟢 Agent is ready" when successful

### 2. Start Chatting
- Type your questions in the chat input at the bottom
- Ask about Azure services, resources, or any Azure-related topics
- The agent will respond using the available Azure MCP tools

### 3. Manage Chat
- Use the "🗑️ Clear Chat" button to start a new conversation
- Chat history is maintained during the session
- Refresh the page to start completely fresh

## Example Questions

- "What resource groups do I have in my subscription?"
- "Show me my Azure Data Factory instances"
- "List my Key Vaults"
- "What are the available Azure regions?"
- "Help me create a new resource group"

## Architecture

The Streamlit app uses a clean separation of concerns:

- **`agent_service.py`**: Contains all the core agent logic extracted from `sk_main_agent.py`
  - `AzureAgentService` class manages the Semantic Kernel and MCP plugin lifecycle
  - Helper functions provide easy integration with the Streamlit interface
  - No Streamlit dependencies, making it reusable

- **`streamlit_app.py`**: Contains only the Streamlit UI code
  - Clean, focused web interface
  - Imports agent functions from `agent_service.py`
  - Handles user interaction and display

## Troubleshooting

### Common Issues

1. **"Missing environment variables" error**
   - Ensure your `.env` file is properly configured
   - Check that all required variables are set

2. **"Failed to initialize agent" error**
   - Make sure you're authenticated with Azure (`az login`)
   - Check your internet connection
   - Verify your Azure subscription has the necessary permissions

3. **MCP server issues**
   - Ensure Node.js and npm are installed
   - Try running the command-line version first to test MCP connectivity

4. **Port already in use**
   - Streamlit will automatically try different ports
   - Check the terminal output for the correct URL

### Getting Help

- Check the terminal output for detailed error messages
- Ensure all prerequisites are met
- Try the command-line version (`python sk_main_agent.py`) to isolate issues

## Development

To modify the app:

1. **UI Changes**: Edit `streamlit_app.py` for interface modifications
2. **Agent Logic**: Edit `agent_service.py` for core functionality changes
3. **Styling**: Modify the CSS in the `main()` function of `streamlit_app.py`
4. **Dependencies**: Update `requirements_streamlit.txt` for new packages

## Security Notes

- Never commit your `.env` file to version control
- The app runs locally and doesn't expose your credentials
- Use appropriate Azure RBAC permissions for your use case

## Comparison with Command-Line Version

| Feature | Command-Line (`sk_main_agent.py`) | Streamlit App (`streamlit_app.py`) |
|---------|-----------------------------------|-----------------------------------|
| Interface | Terminal/Console | Web Browser |
| Chat History | Session only | Session only |
| Initialization | Automatic | Manual (button) |
| Status Display | Console output | Visual indicators |
| Error Handling | Console messages | UI notifications |
| Accessibility | Terminal users | Web users |

Both versions use the same underlying agent logic, so they provide identical functionality with different user interfaces.

## License

This project follows the same license as the main AzureAgent project. 