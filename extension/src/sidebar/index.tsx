// extension/src/sidebar/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import Sidebar from './Sidebar'; // Importing the Sidebar component we created

// This is the main entry point for the sidebar's React application.

// 1. Get the root HTML element.
// The 'root' div is defined in 'extension/public/sidebar.html'.
// This is where our React application will be attached.
const rootElement = document.getElementById('root');

// 2. Ensure the root element exists before trying to render into it.
if (rootElement) {
  // 3. Create a React root for concurrent mode.
  // This is the modern way to initialize a React application.
  const root = ReactDOM.createRoot(rootElement);
  
  // 4. Render the main Sidebar component into the root.
  // React.StrictMode is a wrapper that helps with identifying potential problems in an application.
  // It activates additional checks and warnings for its descendants.
  root.render(
    <React.StrictMode>
      <Sidebar />
    </React.StrictMode>
  );
} else {
  // Log an error to the console if the root element isn't found.
  // This is a common issue if the ID in sidebar.html doesn't match
  // or if this script runs before the DOM is fully loaded (though 'type="module"' helps).
  console.error("Sidebar entry point: Failed to find the root element with ID 'root'. Ensure it exists in sidebar.html.");
}