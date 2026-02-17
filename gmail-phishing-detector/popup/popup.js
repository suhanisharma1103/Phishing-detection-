document.addEventListener('DOMContentLoaded', () => {
  chrome.runtime.sendMessage({ type: 'GET_LATEST_RESULT' }, (response) => {
    const resultDiv = document.getElementById('result');
    if (response.result) {
      resultDiv.innerHTML = `
        <p class="${response.result.label === 'Phishing' ? 'warning' : 'safe'}">
          ${response.result.label}<br>
        </p>
      `;
    } else {
      resultDiv.textContent = 'No email analyzed yet';
    }
  });
});