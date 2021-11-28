import React from 'react';
import { Nav, Navbar, Form, FormControl, Button } from 'react-bootstrap';
import styled from 'styled-components';

const Styles = styled.div`
    .navbar {
        background-color: #222;
    }

    .navbar-brand, .navbar-nav .nav-link {
        color: #bbb;

        &:hover {
        color: white;
        }
    }
`;

export const NavigationBar = () => {
    return(
        <Styles>
            <Navbar expand="lg">
                <Navbar.Brand href="/">BioRevise</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="justify-content-end" style={{ width: "100%" }}>
                        <Nav.Item><Nav.Link href="/">Home</Nav.Link></Nav.Item>
                        <Nav.Item><Nav.Link href="/page-one">Dashboard</Nav.Link></Nav.Item>
                        <Nav.Item><Nav.Link href="/page-two">Exam Qs</Nav.Link></Nav.Item>
                        <Nav.Item><Nav.Link href="/page-three">Personalised Papers</Nav.Link></Nav.Item>
                    </Nav>
                    <Form className="d-flex">
                      <FormControl type="search" placeholder="Search" className="mr-2" aria-label="Search"/>
                      <Button variant="outline-warning">Search</Button>
                    </Form>
                </Navbar.Collapse>
            </Navbar>
        </Styles>
    )
};