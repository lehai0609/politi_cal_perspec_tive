# Extension

This folder contains the Chrome extension source for Political Perspectives.

## Article Extraction

The content script now uses `@mozilla/readability` to extract the main article text from the page. The sidebar requests this via the `PP_EXTRACT_ARTICLE` action and displays the extracted text beneath the current article information.

Run tests with `npm test` inside this directory.
