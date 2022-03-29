import React from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";
import { BrowserRouter as Router } from 'react-router-dom';
import styled from 'styled-components';

const Styles = styled.div`
  .navbar {
    background-color: #3CB371;
  }

  .navbar-brand, .navbar-nav .nav-link {
    color: white;

    &:hover {
      color: #D3D3D3;
    }
  }
`;

export const NavigationBar = () => {
  const navigate = useNavigate();


  function newTest() {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    };
    fetch(`https://api.reemhemyari.com/tests`, requestOptions)
        .then(response => response.json())
        .then(test => navigate("../test", { state: { test: test } }))
        .catch(console.log);
    }

  return(
    <Styles>
      <Navbar expand="lg">
        <Navbar.Brand href="/" style={{ padding: 10 }}>BioRevise</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="justify-content-end" style={{ width: "100%" }}>
            <Nav.Item><Nav.Link href="/">Home</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link href="/modules">Modules</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link href="/unfinished-tests">Unfinished Tests</Nav.Link></Nav.Item>
            <Nav.Item><Nav.Link onClick={() => newTest()}>New Test</Nav.Link></Nav.Item>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    </Styles>
  )
};