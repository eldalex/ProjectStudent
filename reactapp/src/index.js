import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './components/app/App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css'

// export const API_URL = "http://127.0.0.1:8000/api/students/"
export const API_URL = "http://192.168.56.101:1337/api/students/"
export const API_STATIC_MEDIA = "http://192.168.56.101:1337/"

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>
);

reportWebVitals();
