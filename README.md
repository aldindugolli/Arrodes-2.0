# AI Assistant MCP

A powerful AI assistant with system monitoring and control capabilities, built with FastAPI and Ollama.

## Features

### AI Chat Interface
- Interactive chat with AI assistant
- Context-aware conversations
- Support for new chat sessions
- Chat history management

### System Monitoring
- Real-time system metrics dashboard
- CPU, memory, disk, and network monitoring
- Process tracking and management
- Resource usage alerts
- Interactive charts and visualizations

### System Control
- File system operations
- Process management
- System health checks
- Secure API access

### Web Interface
- Modern, responsive design
- Real-time updates
- Easy navigation between features
- User-friendly controls

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/book-writer.git
cd book-writer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with:
```
SECRET_KEY=your_secret_key_here
```

5. Start the Ollama service:
```bash
ollama serve
```

6. Run the application:
```bash
python run.py
```

## Usage

### Web Interface
Access the web interface at `http://localhost:8000`:
- Chat with the AI assistant
- Monitor system resources
- Manage files and processes
- View system alerts

### API Endpoints

#### Chat
- `POST /chat` - Send messages to the AI assistant
- `GET /` - Access the chat interface

#### System Monitoring
- `GET /monitoring` - Access the monitoring dashboard
- `GET /monitoring/metrics` - Get current system metrics
- `GET /monitoring/history` - Get historical metrics data
- `GET /monitoring/alerts` - Get system alerts

#### System Control
- `GET /system/files/list/{path}` - List directory contents
- `GET /system/files/read/{path}` - Read file contents
- `POST /system/files/write` - Write to a file
- `GET /system/processes` - List running processes
- `GET /system/processes/{pid}` - Get process details
- `DELETE /system/processes/{pid}` - Terminate a process

## Security

- API key authentication for all endpoints
- Secure file system operations
- Process management safety checks
- Environment variable configuration

## Development

### Project Structure
```
src/
├── main.py              # FastAPI application
├── ollama_client.py     # AI integration
├── monitoring.py        # System monitoring
├── system_ops.py        # System operations
├── security.py          # Security utilities
├── config.py           # Configuration
└── templates/          # HTML templates
    ├── index.html      # Chat interface
    └── monitoring.html # Monitoring dashboard
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License 