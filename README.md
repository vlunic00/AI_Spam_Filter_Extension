# PhishGuard AI

PhishGuard AI is a project that uses a machine learning model to detect phishing emails directly within your Gmail inbox. It consists of a local Python backend that runs the prediction model and a browser extension that integrates with Gmail to provide real-time scanning.

## How It Works

The system is composed of two main parts:

1.  **Backend Server**: A lightweight Python server built with FastAPI. It exposes a single API endpoint (`/check-email`) that accepts email content. The server uses a pre-trained scikit-learn model (`phishing_model.pkl`) to classify the text as either "spam" (phishing) or "ham" (legitimate).

2.  **Browser Extension**: A simple browser extension that runs on Gmail. It automatically detects when a new email is being viewed, extracts its text content, and sends it to the local backend for analysis. If the email is flagged as phishing, the extension injects a prominent warning banner at the top of the page.

## How to Run the Application

Follow these steps to get the PhishGuard AI running on your local machine.

### Prerequisites

- Python 3.x
- pip (Python package installer)
- A modern web browser that supports unpacked extensions (e.g., Google Chrome, Microsoft Edge, Firefox).

### 1. Backend Setup

First, set up and run the Python backend server.

1.  **Install Dependencies**:
    Open your terminal or command prompt and install the required Python libraries using pip.

    ```bash
    pip install "fastapi[all]" uvicorn scikit-learn joblib
    ```

2.  **Start the Server**:
    In the same terminal, navigate to the project's root directory and run the server.

    ```bash
    python server_backend.py
    ```

    The server will start and listen on `http://127.0.0.1:8000`. You should see a confirmation message from `uvicorn`. Keep this terminal window open.

### 2. Browser Extension Setup

Next, install the browser extension. The process is similar for most Chromium-based browsers.

1.  **Open Browser Extensions Page**:
    - In Google Chrome or Edge, type `chrome://extensions` in the address bar and press Enter.

2.  **Enable Developer Mode**:
    - Look for a "Developer mode" toggle in the top-right corner of the extensions page and turn it on.

3.  **Load the Extension**:
    - Click the **"Load unpacked"** button that appears.
    - In the file selection dialog, navigate to the project's root directory and select the `extension` folder.
    - Click "Select Folder".

The "PhishGuard AI Auto" extension should now appear in your list of installed extensions.

## Usage

1.  **Open Gmail**: Navigate to `https://mail.google.com/`.
2.  **View an Email**: Click on any email to open it.
3.  **Automatic Scanning**: The extension will automatically scan the content of the opened email in the background.
4.  **See the Warning**: If an email is classified as phishing, a red banner will appear at the top of the Gmail interface, warning you about the potential threat. Click the banner to dismiss it.

## Project Structure

- `server_backend.py`: The FastAPI application that serves the ML model.
- `phishing_model.pkl`: The pre-trained machine learning model for phishing detection.
- `extension/`: The folder containing the browser extension files.
  - `manifest.json`: Defines the extension's properties and permissions.
  - `content.js`: The core script that runs on Gmail to extract text and inject banners.
- `email_adapter.py` / `email_aggregator.py` / `pipeline.ipynb`: Scripts and notebooks used for processing raw email data and training the model. These are not required for running the application.
