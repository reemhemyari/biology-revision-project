import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import { HomePage } from './Home';
import { Modules } from './Modules';
import { UnfinishedTests } from './UnfinishedTests';
import { Test } from './Test';
import { TestSummary } from './TestSummary';
import { NavigationBar } from './components/NavigationBar'

function App() {
  return (
    <>
      <NavigationBar/>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/modules" element={<Modules />} />
          <Route path="/unfinished-tests" element={<UnfinishedTests />} />
          <Route path="/test" element={<Test />} />
          <Route path="/test-summary" element={<TestSummary />} />
        </Routes>
      </Router>
    </>
  );
}

export default App
