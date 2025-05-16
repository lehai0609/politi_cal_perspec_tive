// extension/src/contentScript.ts

/**
 * This content script is injected into web pages that match the patterns
 * specified in the `manifest.json` file.
 * Its primary role in this extension will be to extract article content
 * from the page and communicate it to other parts of the extension (like the sidebar).
 */

// Log a message to the console of the web page to confirm the content script is loaded.
console.log("Political Perspectives Content Script Loaded on this page.");

// --- Placeholder for Future Functionality ---
// In upcoming development steps, this script will be expanded to:
//
// 1.  **Extract Article Content:**
//     - Use a library like Mozilla's Readability.js (or a similar tool) to parse the
//       main readable content (text, title) from the current web page.
//     - Handle cases where extraction might fail or where the page content is dynamic.
//
// 2.  **Communicate with the Sidebar/Background Script:**
//     - Once the article content is extracted, send it to the sidebar (or background script)
//       for further processing and display.
//     - This communication will typically use `chrome.runtime.sendMessage`.
//
// 3.  **Respond to Messages:**
//     - Listen for messages from other parts of the extension (e.g., the sidebar asking
//       for page details or to initiate extraction).
// --------------------------------------------


/**
 * Example of listening for messages from other parts of the extension.
 * This allows the popup, sidebar, or background script to request actions
 * from the content script.
 *
 * @param {any} request - The message sent by the calling script.
 * @param {chrome.runtime.MessageSender} sender - An object containing information about the sender.
 * @param {(response?: any) => void} sendResponse - A function to call to send a response back to the sender.
 * @returns {boolean | undefined} - Return true to indicate that sendResponse will be called asynchronously.
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // Log received messages for debugging.
  console.log("Content script received message:", request, "from sender:", sender);

  // Example: Handle a request to get page details.
  if (request.action === "PP_GET_PAGE_DETAILS") {
    console.log("Content script: Action 'PP_GET_PAGE_DETAILS' received.");
    const pageDetails = {
      url: window.location.href,
      title: document.title,
      // In a real scenario, you might add extracted text here if already processed.
      // text: document.body.innerText.substring(0, 500) // Example: first 500 chars
    };
    sendResponse({ status: "success", data: pageDetails });
    return true; // Indicate that the response will be sent asynchronously.
  }

  // Add more message handlers here for other actions as the extension develops.
  // For example, an action to trigger article extraction:
  // if (request.action === "PP_EXTRACT_ARTICLE_CONTENT") {
  //   // ... extraction logic ...
  //   sendResponse({ status: "success", extractedText: "..." });
  //   return true;
  // }

  // If the message is not handled by this listener,
  // you can optionally return false or nothing.
});

// Example of how the content script could proactively send data (though less common for initial load):
// (function sendInitialPageInfo() {
//   if (chrome.runtime && chrome.runtime.sendMessage) {
//     chrome.runtime.sendMessage({
//       type: "CONTENT_SCRIPT_LOADED",
//       url: window.location.href,
//       title: document.title
//     });
//   }
// })();
