
# MailPorter API

## Overview

MailPorter is a FastAPI-based multi-SMTP email sending API that supports different SMTP providers and brand-specific configurations. It dynamically renders email content using Jinja2 templates and secures requests via API key authentication.

## Features

- **Multiple SMTP Providers:**  
  - *Hostinger:* Supports brands such as LegalVala and Startfinity (or Brchub, etc.)
  - *Gmail:* Uses a default configuration.
  - *New Provider:* Example configuration for other SMTP services.

- **Dynamic Email Templates:**  
  Email content is rendered using Jinja2 templates. Each SMTP configuration specifies its own template to personalize the appearance.

- **CORS Support:**  
  Only allowed origins (configured via environment variables) can access the API.

- **API Key Authentication:**  
  Every request must include a valid API key in the `x-api-key` header.

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` package manager

### Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd MailPorter
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**

   Create a `.env` file in the project root with the following example values (update them as needed):

   ```ini
   # .env – DO NOT COMMIT THIS FILE TO VERSION CONTROL

   API_KEY=ExampleLongkey

   # Hostinger credentials for LegalVala (brand: legalvala)
   HOSTINGER_LEGALVALA_USERNAME=your_legalvala_email@legalvala.com
   HOSTINGER_LEGALVALA_PASSWORD=verylongpassword

   # Hostinger credentials for another brand (e.g., Startfinity)
   HOSTINGER_STARTFINITY_USERNAME=your_startfinity_email@example.com
   HOSTINGER_STARTFINITY_PASSWORD=YourStartfinityPassword

   # Gmail credentials (used with key "default")
   GMAIL_USERNAME=your_gmail_email@example.com
   GMAIL_PASSWORD=YourGmailPassword

   # New Provider credentials (if needed; key "default")
   NEWPROVIDER_USERNAME=your_newprovider_email@example.com
   NEWPROVIDER_PASSWORD=YourNewProviderPassword
   ```

### Running the Application

Start the API server on port 8000:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Using the API

### Endpoint

**POST** `/api/email/send-email/{smtp_provider}`

- **Path Parameter:**
  - `smtp_provider`: The SMTP provider key (e.g., `hostinger`, `gmail`, or `newprovider`).

- **Request Body (JSON):**

  ```json
  {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "message": "This is a test email from MailPorter.",
      "mobile": "+11234567890",
      "brand": "legalvala"
  }
  ```

  - **name:** Recipient's name.
  - **email:** Recipient's email address.
  - **message:** Email content.
  - **mobile:** Contact number.
  - **brand:** The key for SMTP configuration (e.g., `"legalvala"`, `"startfinity"`, etc.).

- **Headers:**
  - `Content-Type: application/json`
  - `x-api-key: SuperSecretApiKey123!@#` (matches the value set in your `.env`)

### Example cURL Request

```bash
curl -X POST "http://localhost:8000/api/email/send-email/hostinger" \
  -H "Content-Type: application/json" \
  -H "x-api-key: SuperSecretApiKey123!@#" \
  -d '{
        "name": "John Doe",
        "email": "john.doe@example.com",
        "message": "This is a test email from MailPorter.",
        "mobile": "+11234567890",
        "brand": "legalvala"
      }'
```

## Deployment

### Vercel Deployment

1. **Create a `vercel.json` File**

   Create a file named `vercel.json` in the project root with the following content:

   ```json
   {
     "builds": [
       {
         "src": "app/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app/main.py"
       }
     ]
   }
   ```

2. **Configure Environment Variables on Vercel**

   In your Vercel project dashboard, set the same environment variables as in your local `.env` file.

3. **Deploy**

   Push your repository to GitHub and connect it to Vercel. Vercel will automatically deploy your FastAPI application with the Python preset.

## Additional Information

- **Logging:**  
  Detailed debug logs for the SMTP communication are output to the console.
  
- **Email Templates:**  
  Email content is rendered using Jinja2 templates located in the `app/email` directory.
  
- **CORS:**  
  Only allowed origins (configured in `Settings`) can access the API.
  
- **API Security:**  
  Every request must have the correct API key in the `x-api-key` header.

## License

This project is licensed under the MIT License.
