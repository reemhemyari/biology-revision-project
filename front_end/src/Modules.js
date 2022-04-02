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
const TopicContainer = styled.div`
  display: flex;
  justify-content: left;
  align-items: center;
`;
const Module = styled.div`
  padding-top: 10pt;
  font-size: 1.6em;
`;
const TopicName = styled.div`
  min-width: 20em;
  font-size: 1.1em;
`;

function Topic({children, topicId, canCreate}) {
  const navigate = useNavigate();

  function topicClick(topicId) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic_id: topicId })
    };
    fetch(`https://api.reemhemyari.com/tests`, requestOptions)
        .then(response => response.json())
        .then(test => navigate("../test",  { state: { test: test } }))
        .catch(console.log);
  }

  return (
    <TopicContainer>
      <TopicName>{children}</TopicName>
      <TestButton onClick={() => topicClick(topicId)} disabled={!canCreate}>Create Test</TestButton>
    </TopicContainer>
  );
}

export const Modules = () => {
  const [modules, setModules] = useState([]);

  useEffect(() => {
    fetch(`https://api.reemhemyari.com/modules`)
    .then(res => res.json())
    .then((data) => setModules(data))
    .catch(console.log)
  }, []); // empty array here means that we only want to run this effect once

  return (
    <div className="container" style={{ paddingTop: 10 }}>
      {modules.map((module) => (
        <React.Fragment key={module.module_id}>
          <Module>Module {module.module_num}</Module>
          {module.topics.map((topic) => (
              <Topic key={topic.topic_id} topicId={topic.topic_id} canCreate={topic.enough_questions_for_test}>{topic.topic_name}</Topic>
          ))}
        </React.Fragment>
      ))}
    </div>
  );
}