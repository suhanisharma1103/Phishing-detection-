// filepath: /Users/radhikaasmar/VIT/Project/gmail-phishing-detector/background.js
// use importScripts for non-module service worker
importScripts('model/model.js'); // loads and defines self.PhishingDetector

const detector = new self.PhishingDetector();
let latestResult = null;

// Minimal MV3 service worker (no DOM, no module syntax)

console.log('Gmail Phishing Detector service worker starting...');

chrome.runtime.onInstalled.addListener(() => {
  console.log('Service worker installed/updated.');
  // perform one-time setup if needed
});

// consolidated message handler (supports async sendResponse)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('SW received message:', message);

  if (!message || !message.type) {
    sendResponse({ ok: false, reason: 'no_message_type' });
    return false;
  }

  if (message.type === 'PING') {
    sendResponse({ type: 'PONG', timestamp: Date.now() });
    return false;
  }

  if (message.type === 'CHECK_EMAIL') {
    // async response: return true
    detector.detect(message.text).then(result => {
      latestResult = result;
      // Send notification if phishing detected (requires notifications permission)
      if (result.label === 'Phishing') {
        try {
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icon.png',
            title: 'Phishing Alert',
            message: 'This email appears to be a phishing attempt!'
          });
        } catch (e) {
          console.warn('Failed to create notification:', e);
        }
      }
      sendResponse({ ok: true, result });
    }).catch(err => {
      console.error('Detection error:', err);
      sendResponse({ ok: false, error: String(err) });
    });
    return true;
  }

  if (message.type === 'GET_LATEST_RESULT') {
    sendResponse({ ok: true, result: latestResult });
    return false;
  }

  // fallback
  sendResponse({ ok: false, reason: 'unknown_message_type' });
  return false;
});

// Optional action click handler
if (chrome.action && chrome.action.onClicked) {
  chrome.action.onClicked.addListener((tab) => {
    console.log('Action clicked, tab id:', tab && tab.id);
    // You can open popup or focus a tab, but avoid DOM operations here.
  });
}