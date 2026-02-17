// Listen for new emails being opened
// Only run if the Chrome extension APIs are available
if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.sendMessage) {
  console.log("Phishing Detector content script active...");

  const observer = new MutationObserver((mutations) => {
    mutations.forEach(() => {
      const emailBody = document.querySelector('.a3s.aiL');
      if (emailBody) {
        const emailText = emailBody.innerText;

        // Send message to background script safely
        chrome.runtime.sendMessage({
          type: 'CHECK_EMAIL',
          text: emailText
        }, (response) => {
          if (chrome.runtime.lastError) {
            console.warn("Runtime message error:", chrome.runtime.lastError);
          } else {
            console.log("Message sent successfully", response);
          }
        });
      }
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });
} else {
  console.warn("Chrome extension APIs not available in this context.");
}
