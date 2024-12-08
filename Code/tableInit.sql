/*
기존에 존재하는 database, tablespace, user를 제거해주세요 이름이 겹치면 에러가 발생할 수 있습니다.

1) 터미널에서 postgres 계정으로 접속
psql -U postgres -h localhost

2) tablespace를 적절한 위치에 생성
CREATE tablespace ts_termp
owner postgres
location 'D:\Program Files\PostgreSQL\15\data\db_termp'; 위치는 사용자 마음대로 변경하실 수 있습니다.

3) \db 명령어를 사용하여 tablespace가 생성되었는 지 확인

4) database 생성
CREATE database db_termp
owner postgres
tablespace ts_termp;

5) \l+ 명령어를 사용하여 database가 생성되었는 지 확인

6) 종료
\q

7) postgres 계정으로 db_termp에 접속
DBeaver에서 postgres 계정으로 위에서 만든 db_termp에 연결
(슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.)
(터미널에서 접속도 가능하지만 DBeaver가 편하므로 추천)
(psql -U postgres -h localhost -d db_termp)

8) 아래의 SQL구문을 호출하여 테이블, 유저등 데이터 초기화
DBeaver에서 Alt+X를 누르면 모든 구문이 순차적으로 실행됩니다.

9) 테이블에 데이터가 잘 들어갔는 지 확인
select * from soldier_information si;
select * from wireless_operator wo;
...
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

SELECT rolname FROM pg_roles;
*/

-- 슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.

-- drop table
drop table if exists soldier_information cascade;
drop table if exists soldier_information_id_seq cascade;
drop table if exists incident_reports cascade;
drop table if exists incident_messages cascade;
drop table if exists computer_equipment cascade;
drop table if exists wired_equipment cascade;
drop table if exists wireless_equipment cascade;

-- drop user
drop user if exists login;
drop user if exists admin;
drop user if exists wireless_operator;
drop user if exists field_wireman;
drop user if exists computer_technician;
drop user if exists etc;

-- define enum
drop type if exists Erank;
create type Erank as enum('이병', '일병', '상병', '병장', '기타');

drop type if exists Edepartment;
create type Edepartment as enum('wireless_operator', 'field_wireman', 'computer_technician', 'admin', 'etc');

-- create table
create table soldier_information(
	army_number char(11) primary key,
	name varchar(10) not null,
	rank Erank not null,
	department Edepartment not null,
	phone_number varchar(10),
	user_password char(256) not null
	check (army_number ~ '^\d{2}-\d{8}$') -- ex)18-70007543
	);

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
            incident_id INT REFERENCES incident_reports(id) on delete cascade,
            sender_department VARCHAR(20),
            message VARCHAR(1024),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );






-- create user
create user login WITH encrypted password 'login';
create user admin WITH encrypted password 'admin';
create user wireless_operator WITH encrypted password 'wireless_operator';
create user field_wireman WITH encrypted password 'field_wireman';
create user computer_technician WITH encrypted password 'computer_technician';
create user etc with encrypted password 'etc';



-- create view
create view army_number_pw_dept_view as
	select army_number, user_password, department
	from soldier_information;

-- 무선 장비 뷰 생성 
CREATE VIEW wireless_equipment_view AS 
	SELECT id, name, quantity 
	FROM wireless_equipment 
	ORDER BY id ASC;
CREATE VIEW incident_reports_view AS
	SELECT id, contact, details, wireless_tool_name, wireless_tool_quantity, department
	FROM incident_reports
	WHERE wireless_tool_quantity > 0
	ORDER BY id ASC;
CREATE VIEW incident_details_view AS
	SELECT id, contact, details, wireless_tool_name, wireless_tool_quantity, department
	FROM incident_reports
	WHERE wireless_tool_quantity > 0
	ORDER BY id ASC;

-- set priviliage
grant select on army_number_pw_dept_view to login;

grant all on soldier_information to admin;

-- 사고 테이블 권한
GRANT SELECT ON incident_reports_view TO admin;
GRANT SELECT ON incident_details_view TO admin;

grant all on incident_reports to admin;
grant all on incident_reports to field_wireman;
grant all on incident_reports to computer_technician;
grant all on incident_reports to wireless_operator;

grant all on incident_messages to admin;
grant all on incident_messages to field_wireman;
grant all on incident_messages to computer_technician;
grant all on incident_messages to wireless_operator;

grant all on incident_messages_id_seq to admin;
grant all on incident_messages_id_seq to field_wireman;
grant all on incident_messages_id_seq to computer_technician;
grant all on incident_messages_id_seq to wireless_operator;

grant all on incident_reports_id_seq to admin;
grant all on incident_reports_id_seq to field_wireman;
grant all on incident_reports_id_seq to computer_technician;
grant all on incident_reports_id_seq to wireless_operator;

grant insert, select on incident_reports to etc;
grant all on incident_reports_id_seq to etc;

-- 유선반 테이블 관련 권한
grant all on wired_equipment to admin;
grant all on wired_equipment_id_seq to admin;
grant all on wired_equipment to field_wireman;
grant all on wired_equipment_id_seq to field_wireman;

-- 전장반 테이블 관련 권한 
grant all on computer_equipment to admin;
grant all on computer_equipment_id_seq to admin;
grant all on computer_equipment to computer_technician;
grant all on computer_equipment_id_seq to computer_technician;

-- 무선반 테이블 관련 권한
grant all on wireless_equipment to admin;
grant all on sequence wireless_equipment_id_seq to admin;
grant all on wireless_equipment to wireless_operator;
grant all on sequence wireless_equipment_id_seq to wireless_operator;

-- insert data
-- 로그인 시 user_password는 user_name와 같습니다.
-- 로그인 시 user_password는 user_name와 같습니다.
-- ex. id가 '19-70007563'이면 비밀번호도 '19-70007563'입니다.
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('19-70007563', '김지훈', '이병', 'wireless_operator', '0508', 	'4170478182a252b7412d2dd51f00b3c34d546b8396bd4096f47d134f64c91918');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('18-70007563', '박준호', '상병', 'wireless_operator', '0508', 	'98e982c5ebbe62db749eb930303dd2f6ca600683bca9ba5d5637b87609735bba');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('18-70007511', '한재민', '상병', 'wireless_operator', '0508', 	'39a095d71c4505ac07cdb9097ade9ebabe7853039aeb6895d5dde9b16f5c804c');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('17-70000010', '최재원', '병장', 'field_wireman', '0637', 		'3ff29c29b2f9b174713e2852d3a7b16fca5105da779c2b669a516ecf73a8ef6d');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('19-70006563', '멍멍이', '이병', 'field_wireman', '0637', 		'ce73ef26e5e966db02e0dddc1d073540272f3485349a4696355e647c3c4880a2');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('18-70000963', '고양이', '상병', 'field_wireman', '0637', 		'4740479383c1e35d0ff61a55d24a9bd25a120f2b0c4e383e31cea85d492e6e94');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('19-70001163', '병아리', '이병', 'computer_technician', '0701', 	'116c9742516e1a1775782d8b4dbfbeee2880c7354d031bf04326df615aa5db92');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('17-70007691', '코끼리', '병장', 'computer_technician', '0701', 	'a60f15c8fcf3c38be99856a599e40637c8f88c11a41d92d3ef4635e32a1e9b47');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('18-70117563', '노트북', '상병', 'computer_technician', '0701', 	'34356849e00f9e787e2656d70108ab1bb3808d886f81f5aeaf374c28f4ed8fd2');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('17-71107563', '부산대', '병장', 'admin', '9932',				'84a33fb5a09696530036938bef7fd119f34df6727855993542bb7359f4965a7c');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('18-70015563', '가오리', '상병', 'admin', '9932', 				'80ccd8713ef4efaaa40d77203524d1ff3510057cc79b1c606675639ac3020394');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('17-70006560', '비빔밥', '병장', 'admin', '9932', 				'1897fce6cac5da9d9a9e6a8b24331134402f276a3a03d6a5e7ffe65a6cc0ff6b');
insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values ('19-75007563', '비빔밥', '일병', 'etc', '1739', 					'92ca9bd18c126e4295d5591d323cec80b57c087ec57bff858c9370604bd203f7');

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
INSERT INTO incident_reports ( contact, details, related_units, department, wireless_tool_name, wireless_tool_quantity, wired_tool_name, wired_tool_quantity, computer_tool_name, computer_tool_quantity ) VALUES
('01012345678', '전화기 수화기 선 끊어짐, 컴퓨터 모니터 깨짐', '{"field_wireman", "computer_technician"}', '멍멍대대', '무전기', 2, 'UTP 케이블', 3, '모니터', 1);
INSERT INTO incident_reports ( contact, details, related_units, department, wireless_tool_name, wireless_tool_quantity, wired_tool_name, wired_tool_quantity, computer_tool_name, computer_tool_quantity ) VALUES
('01087654321', '무전기 3개 분실', '{"wireless_operator"}', '왈왈대대', '무전기', 3, '전화기', 0, '프린터기', 0);
INSERT INTO incident_reports ( contact, details, related_units, department, wireless_tool_name, wireless_tool_quantity, wired_tool_name, wired_tool_quantity, computer_tool_name, computer_tool_quantity ) VALUES
('01013572468', '작업 도중 케이블 끊어짐', '{"field_wireman", "computer_technician"}', '무슨대대', '핸드폰', 1, 'UTP 케이블', 1, '본체', 1);

-- incident_messages 테이블 입력
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (1, 'field_wireman', '전화기 선 연결 완료');
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (2, 'wireless_operator', '전장반 지원 바람');
INSERT INTO incident_messages (incident_id, sender_department, message) VALUES (3, 'computer_technician', '지금 작업 중');