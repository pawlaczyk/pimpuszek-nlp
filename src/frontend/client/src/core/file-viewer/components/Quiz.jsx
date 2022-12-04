import { useState, useEffect } from "react";

import UserAnswer from "./UserAnswer";

import "./Quizz.scss";

const Question = ({ question }) => {
  return (
    <section className="quiz__question">
      <p>{question}</p>
    </section>
  );
};

const Answer = ({ userAnswer, answer, exampleList, handleCheckAnswer }) => {
  return (
    <section className="quiz__answer">
      {userAnswer.trim() !== answer.trim() ? (
        <p>
          <span style={{ textDecoration: "line-through" }}>{userAnswer}</span>
          <span> ≠ </span>
          <span
            style={{ color: "green", fontWeight: "bold", fontSize: "20px" }}
          >
            {answer}
          </span>
        </p>
      ) : (
        <p>{answer}</p>
      )}
      <ul className="quiz__answer-examples">
        {exampleList
          ? exampleList.map((example) => (
              <li className="quiz__answer-example" key={example}>
                {example}
              </li>
            ))
          : null}
      </ul>
      <div className="quiz__actions">
        <button onClick={() => handleCheckAnswer(-1)}>Żle</button>
        <button onClick={() => handleCheckAnswer(0)}>Średnio</button>
        <button onClick={() => handleCheckAnswer(1)}>Dobrze</button>
      </div>
    </section>
  );
};

const Quizz = ({ question, exampleList, answer, placeholder, handleNext }) => {
  const [isAnswered, setIsAnswered] = useState(false);
  const [userAnswer, setUserAnswer] = useState("");
  const [isShiftOn, setIsShiftOn] = useState(false);
  const [isCapsLockOn, setIsCapsLockOn] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false);

  const handleUserAnswer = () => {
    let mark = 0;
    if (userAnswer.trim() === answer.trim()) console.log("dobra odpowiedź");
    else {
      console.log("ZŁA odpowiedź");
      setShowAnswer(true);
    }
    setIsAnswered(true);
    // TODO API
  };

  const handleCheckAnswer = (mark) => {
    handleNext(mark);
    setShowAnswer(false);
    setIsAnswered(false);
    setUserAnswer("");
  };

  const handleKeyUp = (e) => {
    setIsShiftOn(false);
    if (e.getModifierState("CapsLock")) {
      setIsCapsLockOn(true);
    } else if (e.getModifierState("Shift")) {
      console.log("shift się trzyma");
      setIsShiftOn(true);
    } else {
      setIsCapsLockOn(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Shift") setIsShiftOn(true);
  };

  useEffect(() => {
    document.addEventListener("keydown", (e) => handleKeyDown(e), true);
    document.addEventListener("keyup", (e) => handleKeyUp(e), true);
  });

  return (
    <div className="quiz">
      <Question question={question} />

      {isAnswered ? (
        <Answer
          userAnswer={userAnswer}
          answer={answer}
          exampleList={exampleList}
          handleCheckAnswer={handleCheckAnswer}
        />
      ) : (
        <UserAnswer
          answer={answer}
          handleUserAnswer={handleUserAnswer}
          userAnswer={userAnswer}
          setUserAnswer={setUserAnswer}
          isShiftOn={isShiftOn}
          isCapsLockOn={isCapsLockOn}
          placeholder={placeholder}
        />
      )}

      {showAnswer ? (
        <p>
          Prawidłowa odpowiedź:
          <span
            style={{
              backgroundColor: "green",
              color: "white",
              fontSize: "16px",
            }}
          >
            {answer}
          </span>
        </p>
      ) : null}
    </div>
  );
};

export default Quizz;