import React, { useState } from 'react';
import Button from "react-bootstrap/Button";
import styled from 'styled-components';
import { useLocation, useNavigate } from "react-router-dom";

const Question = styled.div`
  padding-top: 0.25em;
  font-size: 1.5em;
  padding: 0.5em;
`;
const Options = styled.div`
  font-size: 1.3em;
  padding: 1em;
`;

const SubmitButton = styled(Button)`
  color: black;
  font-size: 1em;
  margin: 0.2em;
  padding: 0.25em 1em;
  border: 1px solid #8FBC8F;
  border-radius: 3px;
  background-color: white;
`;

const header = {
  padding: '0.25em',
  fontSize: '1.7em'
};

function TestHeader({testId, questionNumber, totalQuestions}) {
  return (
    <div style={header} className="header d-flex justify-content-around">
      <div>Test: {testId}</div>
      <div>{questionNumber}/{totalQuestions}</div>
    </div>
  );
}

function Option({submitted, option, selectedOption, onChange}) {
  return (
    <div className="d-flex justify-content-left">
      <label style={{minHeight:"40px"}}>
        <input id={option.option_id} type="radio"
          className="m-2"
          value={option.option_id}
          disabled={submitted}
          checked={selectedOption === option.option_id}
          onChange={onChange}/>
          { !submitted ? null : option.correct ? (
              <img className="p-2" alt="correct" src={'./checkmark-24.png'} />
            ) : (
              <img className="p-2" alt="incorrect" src={'./x-mark-24.png'} />
            )
          }
          {option.option_text}
      </label>
    </div>
  );
}

export const Test = () => {
  const navigate = useNavigate();
  const { state } = useLocation();
  const { test } = state;

  const firstUnansweredQuestion = test.questions.findIndex(question => question.option_id == null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(firstUnansweredQuestion);

  const totalQuestions = test.questions.length
  const question = test.questions[currentQuestionIndex]

  const [selectedOption, setSelectedOption] = useState(question.option_id);
  const [submitted, setSubmitted] = useState(false);

  function handleOptionChange(changeEvent) {
    setSelectedOption(Number(changeEvent.target.value));
  }
  function changeQuestion() {
    if (currentQuestionIndex === totalQuestions - 1) {
      fetch(`https://api.reemhemyari.com/tests/${test.test_id}`)
          .then(response => response.json())
          .then(test => navigate("../test-summary", { state: { test: test } }));
    } else {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSubmitted(false);
    }
  }
  function submit() {
    setSubmitted(true);
    const questionId = test.questions[currentQuestionIndex].question_id
    const requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ option_id: selectedOption })
    };
    fetch(`https://api.reemhemyari.com/tests/${test.test_id}/questions/${questionId}`, requestOptions)
        .then(() => setTimeout( function() { changeQuestion(); }, 1000))
        .catch(console.log);
  }
  return (
    <>
    <TestHeader testId={test.test_id} questionNumber={currentQuestionIndex + 1} totalQuestions={totalQuestions} />
    <div style={{paddingLeft: "10pt"}}>
      <Question>{question.question_text}</Question>
      <Options>
        {question.options.map((option) => (
          <Option key={option.option_id} submitted={submitted} option={option}
                  selectedOption={selectedOption} onChange={handleOptionChange} />
        ))}
      </Options>
      <SubmitButton disabled={submitted} onClick={() => submit()}>Submit</SubmitButton>
    </div>
    </>
  );
}