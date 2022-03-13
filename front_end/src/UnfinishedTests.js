import React, { useState, useEffect } from 'react';
import Button from "react-bootstrap/Button";
import styled from 'styled-components';
import { useNavigate } from "react-router-dom";

const TestButton = styled(Button)`
  color: palevioletred;
  font-size: 1em;
  margin: 0.2em;
  padding: 0.25em 1em;
  border: 2px solid palevioletred;
  border-radius: 3px;
  background-color: white;
`;
const Test = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.1em;
`;

export const UnfinishedTests = () => {
  const [tests, setTests] = useState([]);

  useEffect(() => {
    fetch('https://api.reemhemyari.com/tests?complete=false')
    .then(res => res.json())
    .then((data) => setTests(data))
    .catch(console.log)
  }, []);

  const navigate = useNavigate();

  function testClick(testId) {
    fetch(`https://api.reemhemyari.com/tests/${testId}`)
        .then(response => response.json())
        .then(test => navigate("../test", { state: { test: test } }))
        .catch(console.log);
  }

  return (
    <div className="container" style={{ paddingTop: 10 }}>
      {tests.map((test) => (
        <Test key={test.test_id}>
          <div>Test: {test.test_id}</div>
          <div>{test.topic_id}</div>
          <div>Started: {test.create_time.replace('T', ' ').substr(0, 19)}</div>
          <TestButton onClick={() => testClick(test.test_id)}>Continue</TestButton>
        </Test>
      ))}
    </div>
  );
}