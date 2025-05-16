// extension/src/contentScript.ts

console.log("Political Perspectives Content Script Loaded on this page.");

/**
 * Listener for messages from other parts of the extension (e.g., sidebar).
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // Log all received messages for easier debugging.
  // It's useful to see if the message is coming from the expected extension ID.
  console.log("Content script received message:", request, "from sender:", sender);

  if (request.action === "PP_GET_PAGE_DETAILS_FOR_SIDEBAR") {
    console.log("Content script: Action 'PP_GET_PAGE_DETAILS_FOR_SIDEBAR' received. Responding with page details.");
    // Construct the response object with current page URL and title.
    const pageDetails = {
      url: window.location.href,
      title: document.title,
    };
    // Send the response back to the caller (the sidebar).
    sendResponse({ status: "success", data: pageDetails });
    // Return true to indicate that sendResponse will be called asynchronously.
    // This is important if your response logic involves any async operations,
    // though in this simple case it might not be strictly necessary, it's good practice.
    return true; 
  }

  // If you have other actions, add more 'if' blocks here.
  // e.g., if (request.action === "PP_EXTRACT_ARTICLE_CONTENT") { /* ... */ }

  // If the message isn't handled by this listener, you can optionally return false
  // or simply do nothing to let other listeners (if any) handle it.
});

// --- Placeholder for Future Functionality (as before) ---
// 1.  Extract Article Content (using Readability.js or similar).
// 2.  More complex communication if needed.
// -------------------------------------------------------
