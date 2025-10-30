// project-dashboard-ui/src/index.js (or main.jsx)
import React from 'react';
import { createRoot } from 'react-dom/client';
import Dashboard from './components/Dashboard'; // <--- Ensure this path is correct

const rootElement = document.getElementById('root');
if (rootElement) {
    createRoot(rootElement).render(
        <React.StrictMode>
            {/* RENDER YOUR COMPONENT HERE */}
            <Dashboard /> 
        </React.StrictMode>
    );
}