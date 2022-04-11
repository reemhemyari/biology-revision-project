-- Two tests from two topics: both completed at the same time, one with a better score than the other
INSERT INTO test (test_id, student_id, topic_id, points_earned, num_questions, complete, create_time) VALUES (1, 245, 25, 3, 5, true, NOW());

INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (161, 1, 1, 1240, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (162, 1, 2, 1244, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (166, 1, 3, 1261, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (167, 1, 4, 1264, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (168, 1, 5, 1271, NOW());

INSERT INTO test (test_id, student_id, topic_id, points_earned, num_questions, complete, create_time) VALUES (2, 245, 33, 4, 5, true, NOW());

INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (129, 2, 1, 1116, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (130, 2, 2, 1122, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (163, 2, 3, 1251, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (164, 2, 4, 1252, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (165, 2, 5, 1258, NOW());


-- Two tests from two topics: both completed at the same time, one has more questions that the other
INSERT INTO test (test_id, student_id, topic_id, points_earned, num_questions, complete, create_time) VALUES (1, 245, 25, 1, 3, true, NOW());

INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (161, 1, 1, 1240, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (162, 1, 2, 1244, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (166, 1, 3, 1261, NOW());


INSERT INTO test (test_id, student_id, topic_id, points_earned, num_questions, complete, create_time) VALUES (2, 245, 33, 4, 5, true, NOW());

INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (129, 2, 1, 1116, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (130, 2, 2, 1122, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (163, 2, 3, 1251, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (164, 2, 4, 1252, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (165, 2, 5, 1258, NOW());


-- Two tests from one topic: one completed earlier than the other
INSERT INTO test (test_id, student_id, topic_id, points_earned, num_questions, complete, create_time) VALUES (1, 245, 25, 2, 5, true, NOW());

INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (161, 1, 1, 1240, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (162, 1, 2, 1244, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (166, 1, 3, 1260, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (167, 1, 4, 1264, NOW());
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (168, 1, 5, 1271, NOW());

INSERT INTO test (test_id, student_id, topic_id, points_earned, num_questions, complete, create_time) VALUES (2, 245, 33, 4, 5, true, NOW() - INTERVAL '8 MONTHS');

INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (129, 2, 1, 1116, NOW() - INTERVAL '8 MONTHS');
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (130, 2, 2, 1122, NOW() - INTERVAL '8 MONTHS');
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (163, 2, 3, 1251, NOW() - INTERVAL '8 MONTHS');
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (164, 2, 4, 1252, NOW() - INTERVAL '8 MONTHS');
INSERT INTO testquestion (question_id, test_id, question_num, option_id, update_time) VALUES (165, 2, 5, 1258, NOW() - INTERVAL '8 MONTHS');