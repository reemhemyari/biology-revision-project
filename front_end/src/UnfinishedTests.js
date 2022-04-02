import React, { useState, useEffect } from 'react';
import Button from "react-bootstrap/Button";
import styled from 'styled-components';
import { useNavigate } from "react-router-dom";

const TestButton = styled(Button)`
  color: black;
  font-size: 1em;
  margin: 0.2em;
  padding: 0.25em 1em;
  border: 2px solid #8FBC8F;
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
  const [modules, setModules] = useState([]);

  useEffect(() => {
    fetch(`https://api.reemhemyari.com/modules`)
    .then(res => res.json())
    .then((data) => setModules(data))
    .catch(console.log)
  }, []);

  useEffect(loadTests, []);

  const navigate = useNavigate();

  function loadTests() {
    fetch(`https://api.reemhemyari.com/tests?complete=false`)
          .then(res => res.json())
          .then((data) => setTests(data))
          .catch(console.log)
  }


  function testClick(testId) {
    fetch(`https://api.reemhemyari.com/tests/${testId}`)
        .then(response => response.json())
        .then(test => navigate("../test", { state: { test: test } }))
        .catch(console.log);
  }

  function deleteClick(test_id) {
    const requestOptions = {
        method: 'DELETE'
    };
    fetch(`https://api.reemhemyari.com/tests/${test_id}`, requestOptions)
        .then(response => loadTests())
        .catch(console.log);
  }


  function getTopicName(topic_id) {
    var allTopics = [];
    console.log(topic_id)
    modules.forEach((module) => allTopics.push(module.topics))

    var flattenedTopicList = allTopics.flat(Infinity)
    var topic = flattenedTopicList.find((topic) => topic.topic_id === topic_id)
    const topicName = topic?.topic_name;

    if (topicName == null) {
      console.log('hi')
      return 'Random'
    } else {
      return topicName
    };
  };

  return (
    <div className="container" style={{ paddingTop: 10 }}>
      {tests.map((test) => (
        <Test key={test.test_id}>
          <div>Test: {test.test_id}</div>
          <div>{getTopicName(test.topic_id)}</div>
          <div>Started: {test.create_time.replace('T', ' ').substr(0, 19)}</div>
          <TestButton onClick={() => testClick(test.test_id)}>Continue</TestButton>
          <TestButton onClick={() => deleteClick(test.test_id)}>Delete</TestButton>
        </Test>
      ))}
    </div>
  );
}
