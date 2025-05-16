// extension/src/sidebar/Sidebar.tsx
import React, { useState, useEffect } from 'react';

const Sidebar: React.FC = () => {
  const [currentUrl, setCurrentUrl] = useState<string>('Requesting URL...');
  const [pageTitle, setPageTitle] = useState<string>('Loading title...');
  const [error, setError] = useState<string | null>(null);
  const [articleText, setArticleText] = useState<string>('');

  useEffect(() => {
    // Check if chrome.tabs is available (it might not be in all testing environments)
    if (chrome.tabs && chrome.tabs.query) {
      // Query for the active tab in the current window to send a message to it.
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (chrome.runtime.lastError) {
          const errorMessage = `Error querying tabs: ${chrome.runtime.lastError.message}`;
          console.error("Sidebar:", errorMessage);
          setError(errorMessage);
          setCurrentUrl('Error finding active tab.');
          setPageTitle('');
          return;
        }

        if (tabs && tabs.length > 0 && tabs[0].id) {
          const activeTabId = tabs[0].id;
          // Send a message to the content script of the active tab
          chrome.tabs.sendMessage(
            activeTabId,
            { action: "PP_GET_PAGE_DETAILS_FOR_SIDEBAR" }, // Message payload
            (response) => {
              if (chrome.runtime.lastError) {
                // This can happen if the content script isn't injected on the page,
                // or if the page is a restricted page (e.g., chrome:// pages, Web Store)
                const errorMessage = `Error sending/receiving message: ${chrome.runtime.lastError.message}. Is content script active on this page?`;
                console.error("Sidebar:", errorMessage);
                setError(errorMessage);
                setCurrentUrl('Could not get URL from page.');
                setPageTitle('Could not get title from page.');
                return;
              }
              if (response && response.status === "success" && response.data) {
                console.log("Sidebar: Received page details:", response.data);
                setCurrentUrl(response.data.url || 'URL not provided by content script.');
                setPageTitle(response.data.title || 'Title not provided by content script.');
                setError(null);

                chrome.tabs.sendMessage(
                  activeTabId,
                  { action: 'PP_EXTRACT_ARTICLE' },
                  (extractResp) => {
                    if (chrome.runtime.lastError) {
                      console.error('Sidebar:', chrome.runtime.lastError.message);
                      setArticleText('Error extracting article.');
                      return;
                    }
                    if (extractResp && extractResp.status === 'success') {
                      setArticleText(extractResp.data || '');
                    } else {
                      setArticleText('No article content found.');
                    }
                  }
                );
              } else {
                const errorMessage = "Sidebar: Invalid or no response from content script for page details.";
                console.warn(errorMessage, response);
                setError(errorMessage);
                setCurrentUrl('Failed to get URL.');
                setPageTitle('Failed to get title.');
              }
            }
          );
        } else {
          const noTabMessage = "Sidebar: No active tab found to send message to.";
          console.warn(noTabMessage);
          setError(noTabMessage);
          setCurrentUrl('No active tab identified.');
          setPageTitle('');
        }
      });
    } else {
      const noTabsApiMessage = "Sidebar: chrome.tabs API not available.";
      console.error(noTabsApiMessage);
      setError(noTabsApiMessage);
      setCurrentUrl('Cannot access tabs API.');
      setPageTitle('');
    }
  }, []); // Empty dependency array: run once on mount

  return (
    <div className="flex flex-col h-full bg-white shadow-lg rounded-lg p-6">
      <header className="mb-6 pb-4 border-b border-gray-200">
        <h1 className="text-2xl font-bold text-gray-800">Political Perspectives</h1>
        <p className="text-sm text-gray-500 mt-1">Diverse views on the news you read.</p>
      </header>
      
      <main className="flex-grow overflow-y-auto">
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <h2 className="text-lg font-semibold text-blue-700 mb-1">Current Article:</h2>
          {error && <p className="text-red-500 text-xs italic mt-1 mb-1">{error}</p>}
          <p className="text-sm text-gray-800 font-medium break-all" title={pageTitle}>{pageTitle}</p>
          <a
            href={currentUrl.startsWith('http') ? currentUrl : undefined}
            target="_blank"
            rel="noopener noreferrer"
            className={`block break-all text-xs mt-1 ${
              currentUrl.startsWith('http')
                ? 'text-blue-600 hover:text-blue-800 hover:underline'
                : 'text-gray-500'
            }`}
          >
            {currentUrl}
          </a>
          {articleText && (
            <div className="mt-2">
              <h3 className="text-sm font-semibold text-gray-700">Extracted Text</h3>
              <p className="text-xs text-gray-800 whitespace-pre-wrap">{articleText}</p>
            </div>
          )}
        </div>

        <div className="p-4 bg-gray-50 border border-gray-200 rounded-md mt-4">
          <h3 className="text-md font-semibold text-gray-700">Perspectives will load here...</h3>
          <p className="text-sm text-gray-500 mt-2">
            This area will display alternative political perspectives related to the current article.
          </p>
        </div>
      </main>

      <footer className="mt-6 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-400 text-center">
          Political Perspectives Sidebar v0.1.0
        </p>
      </footer>
    </div>
  );
};

export default Sidebar;
