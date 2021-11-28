import './App.css';
import React from 'react';
import { Link } from 'react-router-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import { Home } from './Home';
import { NoMatch } from './NoMatch';

import { Layout } from './components/Layout';
import { NavigationBar } from './components/NavigationBar';

function App() {
  return (
      <>
      <NavigationBar/>
      <Layout>
          <Router>
              <Routes>
                  <Route exact path='/' element={<Home />} />
                  <Route component={NoMatch} />
              </Routes>
          </Router>
      </Layout>
      </>
  );
 }

export default App;
