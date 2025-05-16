import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'; // Make sure 'path' is imported

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Output directory relative to the vite.config.ts file (i.e., extension/dist)
    outDir: 'dist', 
    sourcemap: 'inline', // Or 'true' for separate files, good for debugging
    rollupOptions: {
      input: {
        // Each key here is an entry point. The value is the path to the source file.
        // Vite will create an output file in 'dist/' with the same name as the key.
        // e.g., 'sidebar' entry will produce 'dist/sidebar.js'.

        // Entry point for the React sidebar application
        sidebar: path.resolve(__dirname, 'src/sidebar/index.tsx'),
        
        // Entry point for the background service worker
        background: path.resolve(__dirname, 'src/background.ts'),
        
        // Entry point for the content script
        contentScript: path.resolve(__dirname, 'src/contentScript.ts'),
      },
      output: {
        // Defines the naming convention for the output files.
        entryFileNames: '[name].js',        // e.g., dist/sidebar.js, dist/background.js
        chunkFileNames: 'assets/[name].js', // For any code-split chunks
        assetFileNames: 'assets/[name].[ext]', // For other assets (e.g., CSS if extracted, images)
      },
    },
    // Set to false to prevent Vite from clearing the console during --watch mode,
    // which can be helpful for seeing persistent build messages or errors.
    clearScreen: false,
  },
  // Optional: Define path aliases if you use them in your imports (e.g., @/components/...)
  // resolve: {
  //   alias: {
  //     '@': path.resolve(__dirname, './src'),
  //   },
  // },
});
