console.log("PhishGuard: Content Script Loaded.");
////////////////////////////////////////////////////////
// @brief Send text to local Python API
// @in text - The email text content
// @out JSON response from API or null if offline
////////////////////////////////////////////////////////
async function checkEmail(text) {
    try {
        const response = await fetch('http://127.0.0.1:8000/check-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: text })
        });
        return await response.json();
    } catch (err) {
        console.error("PhishGuard API Offline:", err);
        return null;
    }
}

////////////////////////////////////////////////////////
// @brief Injects a banner into the email view
// @in data - The API response data
// @out none
////////////////////////////////////////////////////////
function injectBanner(data) {
    if (document.getElementById("phish-guard-banner")) return;

    const banner = document.createElement('div');
    banner.id = "phish-guard-banner";
    banner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #cc0000;
        color: white;
        padding: 15px;
        text-align: center;
        font-family: Arial, sans-serif;
        font-weight: bold;
        z-index: 2147483647; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        cursor: pointer;
    `;
    banner.innerHTML = `⚠️ PHISHGUARD AI: This email is flagged as ${data.label.toUpperCase()} (${(data.confidence * 100).toFixed(1)}%). Click to dismiss.`;

    banner.onclick = () => banner.remove();

    document.body.appendChild(banner);
    console.log("PhishGuard: Floating Banner Injected.");
}

setInterval(async () => {
    const emailBody = document.querySelector('.a3s.aiL');
    
    if (emailBody && !emailBody.getAttribute('data-scanned')) {
        const text = emailBody.innerText.trim();
        
        if (text.length > 10) {
            emailBody.setAttribute('data-scanned', 'true');
            console.log("PhishGuard: New email content found. Scanning...");
            
            const result = await checkEmail(text);
            if (result && (result.is_phishing === true || result.is_phishing === "true")) {
                injectBanner(result);
            }
        }
    }
}, 2000);