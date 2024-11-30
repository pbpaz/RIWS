import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from "./App";
import Details from "./Details";

const AuxApp = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/viewDetails" element={<Details />} />
        </Routes>
      </div>
    </Router>
  );
};

export default AuxApp;
