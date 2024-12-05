/*
무선반 장비 table,
유선반 장비 table,
전장반 장비 table,
사고접수 table,
무선반 장비 입력값,
유선반 장비 입력값,
전장반 장비 입력값,
사고접수 입력값.

테이블에 데이터가 잘 들어갔는지 확인
select * from wireless_equipment wle;
select * from wired_equipment wde;
select * from computer_equipment ce;
select * from incident_messages im;
select * from incident_reports ir;
*/


-- 외래키 제약 조건)에 의해 참조되고 있기 때문에 이러한 상황에서는 CASCADE 옵션을 사용하여 참조된 객체도 함께 삭제해야 합니다.
-- drop table with CASCADE
drop table if exists incident_reports cascade;
drop table if exists incident_messages cascade;
drop table if exists computer_equipment cascade;
drop table if exists wired_equipment cascade;
drop table if exists wireless_equipment cascade;

-- define enum
drop type if exists Edepartment;
create type Edepartment as enum('무선반', '유선반', '전장반');


-- create table
-- 무선반
 CREATE TABLE wireless_equipment (
            id SERIAL PRIMARY KEY,  -- 장비 고유 ID
            name VARCHAR(20) NOT NULL,  -- 장비 이름
            quantity INT NOT NULL CHECK (quantity >= 0) -- 보유량(음수x)
        );

-- 유선반
CREATE TABLE wired_equipment (
            id SERIAL PRIMARY KEY,  -- 장비 고유 ID
            name VARCHAR(20) NOT NULL,  -- 장비 이름
            quantity INT NOT NULL CHECK (quantity >= 0) -- 보유량(음수x)
        );

-- 전장반
CREATE TABLE computer_equipment (
            id SERIAL PRIMARY KEY,  -- 장비 고유 ID
            name VARCHAR(20) NOT NULL,  -- 장비 이름
            quantity INT NOT NULL CHECK (quantity >= 0) -- 보유량(음수x)
        );

-- 사고접수 테이블
CREATE TABLE incident_reports (
    id SERIAL PRIMARY KEY,  -- 사고 고유 ID
    contact VARCHAR(20) NOT NULL,  -- 연락처
    details VARCHAR(255) NOT NULL,  -- 사고 상세 내용
    related_units Edepartment[],  -- 연계되는 반 (배열)
    department VARCHAR(20) NOT NULL,  -- 사고 발생 부서
    wireless_tool_name VARCHAR(20),  -- 필요한 무선 도구 이름
    wireless_tool_quantity INT CHECK (wireless_tool_quantity >= 0),  -- 필요한 무선 도구 수량
    wired_tool_name VARCHAR(20),  -- 필요한 유선 도구 이름
    wired_tool_quantity INT CHECK (wired_tool_quantity >= 0),  -- 필요한 유선 도구 수량
    computer_tool_name VARCHAR(20),  -- 필요한 전장 도구 이름
    computer_tool_quantity INT CHECK (computer_tool_quantity >= 0)  -- 필요한 전장 도구 수량
);


-- 메세지 입력 테이블
CREATE TABLE incident_messages (
            id SERIAL PRIMARY KEY,
            incident_id INT REFERENCES incident_reports(id),
            sender_department VARCHAR(20),
            message VARCHAR(1024),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
-- insert data
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

-- incident_reports 테이블 입력 
-- incident_reports 테이블 입력 I
INSERT INTO incident_reports ( contact, details, related_units, department, wireless_tool_name, wireless_tool_quantity, wired_tool_name, wired_tool_quantity, computer_tool_name, computer_tool_quantity ) VALUES
('01012345678', '전화기 수화기 선 끊어짐, 컴퓨터 모니터 깨짐', '{"유선반", "전장반"}', '멍멍대대', '무전기', 2, 'UTP 케이블', 3, '모니터', 1);
INSERT INTO incident_reports ( contact, details, related_units, department, wireless_tool_name, wireless_tool_quantity, wired_tool_name, wired_tool_quantity, computer_tool_name, computer_tool_quantity ) VALUES
('01087654321', '무전기 3개 분실', '{"무선반"}', '왈왈대대', '무전기', 3, '전화기', 0, '프린터기', 0);
INSERT INTO incident_reports ( contact, details, related_units, department, wireless_tool_name, wireless_tool_quantity, wired_tool_name, wired_tool_quantity, computer_tool_name, computer_tool_quantity ) VALUES
('01013572468', '작업 도중 케이블 끊어짐', '{"유선반", "전장반"}', '무슨대대', '핸드폰', 1, 'UTP 케이블', 1, '본체', 1);


-- incident_messages 테이블 입력
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (1, '유선반', '전화기 선 연결 완료');
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (2, '무선반', '전장반 지원 바람');
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (3, '전장반', '지금 작업 중');


-- 무선 장비 뷰 생성 
CREATE VIEW wireless_equipment_view AS 
SELECT id, name, quantity 
FROM wireless_equipment 
ORDER BY id ASC;
CREATE VIEW incident_reports_view AS
SELECT id, contact, details, wireless_tool_name, wireless_tool_quantity
FROM incident_reports
WHERE wireless_tool_quantity > 0
ORDER BY id ASC;
CREATE VIEW incident_details_view AS
SELECT id, contact, details, wireless_tool_name, wireless_tool_quantity
FROM incident_reports
WHERE wireless_tool_quantity > 0
ORDER BY id ASC;


grant all on incident_reports to admin;
grant all on wired_equipment to admin;
grant all on wireless_equipment to admin;
grant all on computer_equipment to admin;
grant all on incident_messages to admin;
GRANT SELECT ON wireless_equipment_view TO admin;
GRANT SELECT ON incident_reports_view TO admin;
GRANT SELECT ON incident_details_view TO admin;
grant all on sequence wireless_equipment_id_seq to admin;  -- 시퀀스 권한 부여