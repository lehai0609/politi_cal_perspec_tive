// extension/src/sidebar/Sidebar.tsx
import React, { useState, useEffect } from 'react';

/**
 * The main React component for the Political Perspectives Sidebar.
 * It displays the extension's UI within the Chrome side panel.
 */
const Sidebar: React.FC = () => {
  // State to hold the URL of the current active tab.
  const [currentUrl, setCurrentUrl] = useState<string>('Loading URL...');
  // State to hold any error messages during URL retrieval.
  const [error, setError] = useState<string | null>(null);

  // useEffect hook to fetch the current tab's URL when the component mounts.
  useEffect(() => {
    // Check if the chrome.tabs API is available (it should be in a side panel context).
    if (chrome.tabs && chrome.tabs.query) {
      // Query for the active tab in the current window.
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        // Handle potential errors from the chrome.tabs.query API.
        if (chrome.runtime.lastError) {
          const errorMessage = `Error querying tabs: ${chrome.runtime.lastError.message}`;
          console.error(errorMessage);
          setError(errorMessage);
          setCurrentUrl('Could not retrieve URL.');
          return;
        }

        // Check if any tabs were returned and if the first tab has a URL.
        if (tabs && tabs.length > 0 && tabs[0].url) {
          setCurrentUrl(tabs[0].url);
        } else {
          // Fallback if no active tab or URL is found.
          setCurrentUrl('No active tab URL found.');
          console.warn("No active tab or URL found from chrome.tabs.query.");
        }
      });
    } else {
      // Fallback or error message if chrome.tabs API is not available.
      const unavailableMessage = 'chrome.tabs API not available in this context.';
      setCurrentUrl(unavailableMessage);
      setError(unavailableMessage);
      console.warn("chrome.tabs API not available. Ensure this runs in the side panel context.");
    }
  }, []); // Empty dependency array means this effect runs once after the initial render.

  return (
    // Main container for the sidebar, using Tailwind CSS classes for styling.
    // flex flex-col: Makes this a flex container with items stacked vertically.
    // h-full: Takes up the full height of its parent (which should be the #root div).
    // bg-white: Sets a white background.
    // shadow-lg: Applies a large shadow for a lifted appearance.
    // rounded-lg: Applies rounded corners.
    // p-6: Applies padding on all sides.
    <div className="flex flex-col h-full bg-white shadow-lg rounded-lg p-6">
      {/* Header section */}
      <header className="mb-6 pb-4 border-b border-gray-200">
        <h1 className="text-2xl font-bold text-gray-800">Political Perspectives</h1>
        <p className="text-sm text-gray-500 mt-1">Diverse views on the news you read.</p>
      </header>
      
      {/* Main content area */}
      {/* flex-grow: Allows this section to take up available vertical space. */}
      {/* overflow-y-auto: Adds a scrollbar if content exceeds the height. */}
      <main className="flex-grow overflow-y-auto">
        {/* Section to display the current article's URL */}
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <h2 className="text-lg font-semibold text-blue-700 mb-1">Current Article:</h2>
          {error ? (
            // Display error message if URL retrieval failed.
            <p className="text-red-600 break-all text-sm">{error}</p>
          ) : (
            // Display the current URL as a clickable link if it's a valid HTTP/HTTPS URL.
            <a 
              href={currentUrl.startsWith('http') ? currentUrl : undefined} 
              target="_blank" 
              rel="noopener noreferrer" 
              className={`break-all text-sm ${
                currentUrl.startsWith('http') 
                  ? 'text-blue-600 hover:text-blue-800 hover:underline' 
                  : 'text-gray-700' // Style for non-link text (e.g., "Loading URL...")
              }`}
            >
              {currentUrl}
            </a>
          )}
        </div>

        {/* Placeholder for where the perspectives will be loaded */}
        <div className="p-4 bg-gray-50 border border-gray-200 rounded-md mt-4">
          <h3 className="text-md font-semibold text-gray-700">Perspectives will load here...</h3>
          <p className="text-sm text-gray-500 mt-2">
            This area will display alternative political perspectives related to the current article once the backend is integrated.
          </p>
        </div>
      </main>

      {/* Footer section */}
      <footer className="mt-6 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-400 text-center">
          Political Perspectives Sidebar v0.1.0
        </p>
      </footer>
    </div>
  );
};

export default Sidebar;
