# 🔗 Tiny URL Shortener (Flask + Base62)

A minimal Python Flask API that shorten URLs, store them in data.json, and redirect from short → long URLs.

## Features
- Shortens Urls using Base62 encoding
- Deduplication : same long URL → same short URL
- Stores data locally in data.json
- Redirect from short URLs


## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>

2. **Create a Virtual Environment(optional but recommended)**
   ```bash
   python3 -m venv venv

   source venv/bin/activate (Linux)

   venv\Scripts\activate (Windows)

4. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt 

5. **Ensure data.json exists:**
   ```bash
   echo "{}" > data.json

6. **Run the app**
   ```bash
   python3 app.py

---
## Usage

1. **Run the app**
   ```bash
   python3 app.py
   ```
   - Server will start at http://127.0.0.1:5000/

2. **Shorten a url**
   ```bash
   curl -X POST http://127.0.0.1:5000/shorten \
        -H "Content-Type: application/json" \
        -d '{"url": "https://www.reddit.com"}'
    ```    

   **Response Example**   
   ```bash
   {
      "short_url": "http://localhost:5000/r/143hpe"
   }
   ```
   **Redirect using the short url**
   ```bash
   curl -L http://localhost:5000/r/d4E5f6

   OR
   
   Copy the link and paste it in your browser
   ```
   - will redirect to <b> www.reddit.com<b>

## Notes
- If you delete or clear data.json, the app will start fresh.
- Deduplication ensures the same long URL always gets the same short URL.
- Random Base62 codes make short URLs look like TinyURL/Bit.ly links.

---


  

  





   

