// extension/src/contentScript.ts

import { Readability } from '@mozilla/readability';

console.log("Political Perspectives Content Script Loaded on this page.");

/**
 * Extract article text using Mozilla Readability.
 */
export function extractArticleContent(): string | null {
  try {
    const docClone = document.cloneNode(true) as Document;
    const article = new Readability(docClone).parse();
    return article?.textContent ?? null;
  } catch (err) {
    console.error('Content script: failed to extract article', err);
    return null;
  }
}

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

  if (request.action === "PP_EXTRACT_ARTICLE") {
    console.log("Content script: extracting article text");
    const text = extractArticleContent();
    if (text) {
      sendResponse({ status: 'success', data: text });
    } else {
      sendResponse({ status: 'error', error: 'No article content found' });
    }
    return true;
  }

  // If you have other actions, add more 'if' blocks here.
  // e.g., if (request.action === "PP_EXTRACT_ARTICLE_CONTENT") { /* ... */ }

  // If the message isn't handled by this listener, you can optionally return false
  // or simply do nothing to let other listeners (if any) handle it.
});

// --- Placeholder for Future Functionality (as before) ---
// Additional actions can be handled here as the extension grows.
// -------------------------------------------------------
