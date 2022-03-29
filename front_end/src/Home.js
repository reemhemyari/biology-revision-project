import React from 'react';
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import styled from 'styled-components';

const StyledButton = styled(Button)`
  color: black;
  font-size: 1em;
  margin: 1em;
  padding: 0.25em 1em;
  border: 2px solid #8FBC8F;
  border-radius: 3px;
  background-color: white;
`;

const Home = styled.div`
  display: flex;
  justify-content:center;
  align-items:center;
`;

export const HomePage = () => {
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

  return (
    <Home>
      <StyledButton onClick={() => navigate("modules")}>Modules</StyledButton>
      <StyledButton onClick={() => navigate("unfinished-tests")}>Unfinished Tests</StyledButton>
      <StyledButton onClick={() => newTest()}>New Test</StyledButton>
    </Home>
  );
}
