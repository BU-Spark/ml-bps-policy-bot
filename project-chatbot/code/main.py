from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from chainlit.utils import mount_chainlit

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="code/static"), name="static")

# Mount Chainlit app at /chainlit
mount_chainlit(app=app, target="code/chainlit_main.py", path="/chainlit")

# Serve the main webpage
@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI with Chainlit</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }
            #chat-popup {
                display: none;
                position: fixed;
                bottom: 80px;
                right: 20px;
                width: 400px;
                height: 600px;
                border: 2px solid #ccc;
                background: #fff;
                z-index: 1000;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
                border-radius: 10px;
            }
            iframe {
                width: 100%;
                height: 100%;
                border: none;
                border-radius: 10px;
            }
            #chat-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                z-index: 1001;
            }
            #chat-button img {
                width: 30px;  /* Increased from 10px */
                height: auto;
            }
        </style>
        <script>
            window.onload = function() {
                var popup = document.getElementById("chat-popup");
                popup.style.display = "none";
            }

            function toggleChat() {
                var popup = document.getElementById("chat-popup");
                var currentDisplay = window.getComputedStyle(popup).display;
                popup.style.display = currentDisplay === "none" ? "block" : "none";
            }
        </script>
    </head>
    <body>
        <h1>Welcome to Boston Public School Policy Chatbot</h1>
        <div id="chat-button" onclick="toggleChat()" style="cursor: pointer;">
            <img src="/static/images/chainlit.png" alt="Chat with Chainlit">
        </div>
        <div id="chat-popup">
            <iframe src="/chainlit"></iframe>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
