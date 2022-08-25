import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  BrowserRouter,
  Routes, 
  Route 
} from "react-router-dom"; 

import Main from "./pages/main/main"; 
import ExpressionConverter from "./pages/expression-converter/expression-converter";

// css 
import "./css/index.css"

// fonts 
import '@fontsource/roboto/300.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Main />} /> 
      <Route path="/expression-converter" element={<ExpressionConverter />} /> 
    </Routes>
  </BrowserRouter>
);