-- One Complete Test
INSERT INTO test (test_id, student_id, points_earned, num_questions, complete, create_time) VALUES (1, 245, 1, 10, true, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (161, 1, 1, 1240, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (162, 1, 2, 1244, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (166, 1, 3, 1260, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (167, 1, 4, 1264, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (168, 1, 5, 1268, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (169, 1, 6, 1272, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (170, 1, 7, 1276, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (129, 1, 8, 1116, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (130, 1, 9, 1120, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (163, 1, 10, 1248, NOW());

-- Two Incomplete Tests
INSERT INTO test (test_id, student_id, points_earned, num_questions, complete, create_time) VALUES (2, 245, 2, 10, false, NOW());
INSERT INTO test (test_id, student_id, points_earned, num_questions, complete, create_time) VALUES (3, 245, 2, 10, false, NOW());

INSERT INTO testquestion (question_id, test_id, question_num) VALUES (161, 2, 1);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (162, 2, 2);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (166, 2, 3);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (167, 2, 4);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (168, 2, 5);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (169, 2, 6);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (170, 2, 7);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (129, 2, 8);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (130, 2, 9);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (163, 2, 10);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (161, 3, 1);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (162, 3, 2);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (166, 3, 3);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (167, 3, 4);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (168, 3, 5);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (169, 3, 6);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (170, 3, 7);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (129, 3, 8);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (130, 3, 9);
INSERT INTO testquestion (question_id, test_id, question_num) VALUES (163, 3, 10);

-- One Complete Test for second user
INSERT INTO test (test_id, student_id, points_earned, num_questions, complete, create_time) VALUES (4, 872, 1, 10, true, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (161, 4, 1, 1240, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (162, 4, 2, 1244, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (166, 4, 3, 1260, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (167, 4, 4, 1264, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (168, 4, 5, 1268, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (169, 4, 6, 1272, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (170, 4, 7, 1276, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (129, 4, 8, 1116, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (130, 4, 9, 1120, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (163, 4, 10, 1248, NOW());