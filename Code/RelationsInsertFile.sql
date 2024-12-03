delete from incident_reports;
delete from incident_messages;
delete from computer_equipment
delete from wired_equipment;
delete from wireless_equipment;
-- wireless_equipment 테이블 입력
INSERT INTO wireless_equipment (name, quantity) VALUES ('무전기', 10);
INSERT INTO wireless_equipment (name, quantity) VALUES ('스피커', 5);
INSERT INTO wireless_equipment (name, quantity) VALUES ('핸드폰', 15);

-- wired_equipment 테이블 입력
INSERT INTO wired_equipment (name, quantity) VALUES ('UTP 케이블', 20);
INSERT INTO wired_equipment (name, quantity) VALUES ('전화기', 8);
INSERT INTO wired_equipment (name, quantity) VALUES ('광케이블', 12);

-- computer_equipment 테이블 입력
INSERT INTO computer_equipment (name, quantity) VALUES ('모니터', 25);
INSERT INTO computer_equipment (name, quantity) VALUES ('본체', 30);
INSERT INTO computer_equipment (name, quantity) VALUES ('프린터기', 40);

-- incident_messages 테이블 입력
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (1, '유선반', '전화기 선 연결 완료');
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (2, '무선반', '전장반 지원 바람');
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (3, '전장반', '지금 작업 중');


-- incident_reports 테이블 입력 
INSERT INTO incident_reports (contact, details, related_units, department) VALUES
('010-1234-5678', '전화기랑 컴퓨터 분실', '{"유선반", "전장반"}', '제조부서');
INSERT INTO incident_reports (contact, details, related_units, department) VALUES
('010-8765-4321', '무전기 3개 분실', '무선반', '안전부서');
INSERT INTO incident_reports (contact, details, related_units, department) VALUES
('010-1357-2468', '작업 도중 케이블 끊어짐', '{"유선반", "전장반"}', '생산부서');
