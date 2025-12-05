# Shadows Backend

This is the Python FastAPI backend for the Shadows Medical AI Agent.

## Setup

1.  **Install Python 3.10+**
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment:**
    -   Copy `env.example` to `.env`
    -   Add your `OPENAI_API_KEY`

## Running the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`.
Docs are at `http://localhost:8000/docs`.

## Integration

To connect the frontend to this real backend:
1.  Go to `hooks/useUpload.ts`, `hooks/useChat.ts`, etc.
2.  Change the API base URL from `/api/mock` to `http://localhost:8000/api`.
