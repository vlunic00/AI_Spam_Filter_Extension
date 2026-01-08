document.getElementById('scanBtn').addEventListener('click', async () => {
    const resultDiv = document.getElementById('result');
    resultDiv.innerText = "Analyzing email content...";
    resultDiv.style.color = "black";

    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
            // a3s.aiL is the Gmail email body container
            const gmailBody = document.querySelector('.a3s.aiL');
            if (gmailBody) return gmailBody.innerText;

            const mainContent = document.querySelector('[role="main"]');
            if (mainContent) return mainContent.innerText;

            return document.body.innerText;
        }
    }, async (injectionResults) => {
        if (!injectionResults || !injectionResults[0].result) {
            resultDiv.innerText = "Error: Could not read email content.";
            return;
        }

        const emailText = injectionResults[0].result;

        try {
            const response = await fetch('http://127.0.0.1:8000/check-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: emailText })
            });

            if (!response.ok) throw new Error("Backend response error");

            const data = await response.json();

            resultDiv.innerText = `Result: ${data.label} (${(data.confidence * 100).toFixed(1)}%)`;
            resultDiv.style.color = data.is_phishing ? "#cc0000" : "#008800";

            if (data.is_phishing) {
                chrome.scripting.executeScript({
                    target: { tabId: tab.id },
                    args: [data.label, data.confidence],
                    func: (label, confidence) => {
                        if (document.getElementById("phish-guard-banner")) return;

                        const banner = document.createElement('div');
                        banner.id = "phish-guard-banner";
                        banner.style.cssText = `
                            background-color: #ffeeee;
                            color: #cc0000;
                            padding: 20px;
                            text-align: center;
                            font-family: Arial, sans-serif;
                            font-weight: bold;
                            border: 3px solid #cc0000;
                            margin: 15px;
                            border-radius: 10px;
                            font-size: 16px;
                            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                        `;
                        banner.innerHTML = `
                            <span style="font-size: 24px; margin-right: 10px;">⚠️</span> 
                            PHISHGUARD AI ALERT: This email is flagged as ${label.toUpperCase()} 
                            (${(confidence * 100).toFixed(1)}% Confidence). Proceed with extreme caution!
                        `;
                        
                        document.body.prepend(banner);
                    }
                });
            }

        } catch (error) {
            console.error(error);
            resultDiv.innerText = "Error: Connection to API failed. Is main.py running?";
            resultDiv.style.color = "red";
        }
    });
});