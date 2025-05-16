// extension/src/background.ts

/**
 * This is the service worker for the Chrome extension.
 * It runs in the background and handles events such as extension icon clicks,
 * installation, and messages from other parts of the extension.
 */

/**
 * Listener for when the extension's action icon (toolbar icon) is clicked.
 * When clicked, this function will attempt to open the side panel for the currently active tab.
 * @param {chrome.tabs.Tab} tab - The tab that was active when the action was clicked.
 */
chrome.action.onClicked.addListener(async (tab) => {
  // Log that the action icon was clicked.
  console.log("Extension icon clicked.");

  // The tab object might not have an ID in some rare cases (e.g., if it's not a normal tab).
  // We need the tab ID to associate the side panel with a specific tab.
  if (tab.id) {
    try {
      // Programmatically open the side panel for the specific tab.
      // The `chrome.sidePanel.open()` function takes an object with the `tabId`.
      await chrome.sidePanel.open({ tabId: tab.id });
      console.log(`Side panel opened successfully for tab ID: ${tab.id}`);
    } catch (error) {
      // Log any errors that occur while trying to open the side panel.
      console.error(`Error opening side panel for tab ID ${tab.id}:`, error);
    }
  } else {
    // Log an error if the tab ID is not available.
    console.error("Cannot open side panel: Tab ID is undefined.");
  }
});

/**
 * Listener for when the extension is first installed or updated to a new version.
 * This is a good place to set up initial configurations or behaviors.
 */
chrome.runtime.onInstalled.addListener(() => {
  // Set the default behavior for the side panel.
  // `openPanelOnActionClick: true` means the side panel will open automatically
  // when the extension's action icon is clicked, without needing the explicit
  // `chrome.action.onClicked` listener above to call `chrome.sidePanel.open()`.
  // However, having both provides a robust way to ensure the panel opens
  // and allows for more complex logic in the onClicked listener if needed later.
  chrome.sidePanel
    .setPanelBehavior({ openPanelOnActionClick: true })
    .then(() => {
      console.log("Side panel behavior set to open on action click.");
    })
    .catch((error) => console.error("Failed to set side panel behavior:", error));

  // Log a message to confirm the extension has been installed or updated.
  console.log("Political Perspectives Sidebar extension has been installed or updated.");
});

// A simple log to indicate that the background service worker script has started.
console.log("Background service worker started.");