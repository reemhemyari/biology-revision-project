import './App.css';
import React from 'react';
import { Link } from 'react-router-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import { Home } from './Home';
import { NoMatch } from './NoMatch';

import { Layout } from './components/Layout';

function App() {
  return (
//    <React.Fragment>
//        <Router>
//            <Routes>
//                <Route exact path='/' component={Home} /> //is the main path, takes you to the home page
//                <Route component={NoMatch} /> //takes you to an error page if path not found
//            </Routes>
//        </Router>
//    </React.Fragment>
    <>
    <Layout>
        <Router>
            <Routes>
                <Route exact path='/' component={Home} />
                <Route component={NoMatch} />
            </Routes>
        </Router>
    </Layout>
    </>
  );
}

export default App;
