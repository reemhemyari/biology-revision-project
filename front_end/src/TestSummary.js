import React from 'react';
import { useLocation } from "react-router-dom";

const header = {
  padding: '0.25em',
  fontSize: '1.7em'
};

function TestSummaryHeader({testId, totalScore, maxTestScore, correctAnswers, totalQuestions}) {
  return (
    <>
      <div style={header} className="d-flex justify-content-around">
        <div>Test: {testId}</div>
        <div>Score: {totalScore}/{maxTestScore}</div>
      </div>
      <div style={header} className="d-flex justify-content-center">{correctAnswers.length} correct out of {totalQuestions} questions</div>
    </>
  );
}

function Answer({correct}) {
  if (correct) {
    return (<img className="p-2" alt="correct" src={'./checkmark-24.png'} />);
  } else {
    return (<img className="p-2" alt="incorrect" src={'./x-mark-24.png'} />);
  }
}

export const TestSummary = () => {
  const { state } = useLocation();
  const { test } = state;
  const totalQuestions = test.questions.length
  const maxTestScore = test.questions.reduce((score, question) => score + question.points, 0)
  const correctAnswers = test.questions.filter(question => question.option_id === correctOption(question))
  const correctAnswerIds = correctAnswers.map(question => question.question_id)
  const totalScore = correctAnswers.reduce((score, answer) => score + answer.points, 0)

  function correctOption(question) {
    return question.options.find(option => option.correct).option_id;
  }
  return (
    <>
    <TestSummaryHeader testId={test.test_id}
                       totalScore={totalScore}
                       maxTestScore={maxTestScore}
                       correctAnswers={correctAnswers}
                       totalQuestions={totalQuestions} />
    <div className="d-flex justify-content-center">
    {test.questions.map((question) => (
      <Answer key={question.question_id} correct={correctAnswerIds.includes(question.question_id)} />
    ))}
    </div>
    </>
  );
}