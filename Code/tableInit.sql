/*
기존에 존재하는 database, tablespace, user를 제거해주세요 이름이 겹치면 에러가 발생할 수 있습니다.
기존에 존재하는 database, tablespace, user를 제거해주세요 이름이 겹치면 에러가 발생할 수 있습니다.
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
(터미널에서 접속도 가능하지만 DBeaver가 편하므로 추천)
(psql -U postgres -h localhost -d db_termp)

8) 아래의 SQL구문을 호출하여 테이블, 유저등 데이터 초기화
DBeaver에서 Alt+X를 누르면 모든 구문이 순차적으로 실행됩니다.

9) 테이블에 데이터가 잘 들어갔는 지 확인
select * from soldier_information si;
select * from wireless_operator wo;
select * from admin_soldier as2;
select * from computer_technician ct;
select * from field_wireman fw;
*/

-- 슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.
-- 슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.
-- 슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.
-- 슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.
-- 슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.
-- 슈퍼유저(postgres)로 db_termp에 접속한 뒤 아래 SQL 구문들을 실행해야 합니다.

-- drop view
drop view if exists id_pw_view;

-- drop table
drop table if exists wireless_operator;
drop table if exists field_wireman;
drop table if exists computer_technician;
drop table if exists admin_soldier;
drop table if exists soldier_information;

-- drop user
drop user if exists login;
drop user if exists admin;
drop user if exists wireless_operator;
drop user if exists field_wireman;
drop user if exists computer_technician;

-- define enum
drop type if exists Erank;
create type Erank as enum('이병', '일병', '상병', '병장', '기타');

-- create table
create table soldier_information(
	id serial primary key,
	name varchar(10) not null,
	rank Erank not null,
	user_name varchar(20) unique not null,
	user_password char(256) not null
	);

create table wireless_operator(
	id int primary key,
	responsible_area varchar(255) not null,
	phone_number char(10),	
	foreign key (id) references soldier_information(id) on delete cascade
	);

create table field_wireman(
	id int primary key,
	responsible_area varchar(255) not null,
	phone_number char(10),
	foreign key (id) references soldier_information(id) on delete cascade
	);

create table computer_technician(
	id int primary key,
	responsible_equipment_type varchar(255) not null,
	phone_number char(10),
	foreign key (id) references soldier_information(id) on delete cascade
	);

create table admin_soldier(
	id int primary key,
	phone_number char(10),
	foreign key (id) references soldier_information(id) on delete cascade
	);	

-- insert data
-- 로그인 시 user_password는 user_name와 같습니다.
-- 로그인 시 user_password는 user_name와 같습니다.
-- 로그인 시 user_password는 user_name와 같습니다.
-- 로그인 시 user_password는 user_name와 같습니다.
insert into soldier_information(name, rank, user_name, user_password) values ('김지훈', '이병', 'kimji', 'db7ac3a7700a1f3981c7d22492b32abfa1fd1d121861c7846281a89c94bcf197');
insert into soldier_information(name, rank, user_name, user_password) values ('박준호', '상병', 'parkj', '2cf6626d63acfe41530a6894c7a1fded4481c897721b4da6a220380659b5705b');
insert into soldier_information(name, rank, user_name, user_password) values ('한재민', '상병', 'hanjm', 'e6cb42ec2f8c19b4b59512877ee47a44b54a07447f07f23870941dbe2e60bd6f');
insert into soldier_information(name, rank, user_name, user_password) values ('최재원', '병장', 'cjw', '0fdd652011cc5d7fe74184281fe22cf9accb9c8b6319624c9817dcec32bb1965');
insert into soldier_information(name, rank, user_name, user_password) values ('멍멍이', '이병', 'doggy', '1433d68859090304120ab33c5523485492a24de68464810b770a5957b6d64ca1');
insert into soldier_information(name, rank, user_name, user_password) values ('고양이', '상병', 'cat', '77af778b51abd4a3c51c5ddd97204a9c3ae614ebccb75a606c3b6865aed6744e');
insert into soldier_information(name, rank, user_name, user_password) values ('병아리', '이병', 'ppi', '0fef65463b6dcae47253ec56684caa3cc9c3d04f5cc714d2858fa55f25adeafe');
insert into soldier_information(name, rank, user_name, user_password) values ('코끼리', '병장', 'kok', 'd6ba8bf227ba2c637c444a9f59764f28da0e06c868770f1be41278c536efb6b3');
insert into soldier_information(name, rank, user_name, user_password) values ('노트북', '상병', 'ntb', 'c9dd3c0f1d24bb73d409bf6770f2ad8e2e9077ff3c60093bba6764d5b96bb261');
insert into soldier_information(name, rank, user_name, user_password) values ('부산대', '병장', 'pnu', '9e05e9e7c7fdacac968755b0d07b035a1aca1d06501dd6921db0dd3dc73b1294');
insert into soldier_information(name, rank, user_name, user_password) values ('가오리', '상병', 'gaori', '1f9d94c463cc64a2460673b8817520063e16a78352c5b39de52410e25e494eeb');
insert into soldier_information(name, rank, user_name, user_password) values ('비빔밥', '병장', 'bibim', '44551e48c7582972cf461c7f5b9575a82f76bf4a2d9b615fe050560ed2a0fad4');
insert into soldier_information(name, rank, user_name, user_password) values ('비빔밥', '일병', 'bimbi', 'd8b8516c58c615932c0c48471edb8b5af8f98f7743f33745f2e51f7e35cdedf2');

insert into wireless_operator values (1, '지원대대', '0515671234');
insert into wireless_operator values (2, '기지전대', '0512223456');
insert into wireless_operator values (3, '헌병대대', '0519995555');

insert into field_wireman values(4, '무슨대대', '0510001111');
insert into field_wireman values(5, '멍멍대대', '0511112222');
insert into field_wireman values(6, '왈왈대대', '0512223333');

insert into computer_technician values (7, '컴퓨터', '0513334444');
insert into computer_technician values (8, '컴퓨터', '0513334444');
insert into computer_technician values (9, '마우스', '0513339999');

insert into admin_soldier values (10, '0519879876');
insert into admin_soldier values (11, '0519879876');
insert into admin_soldier values (12, '0519879876');

-- create user
create user login WITH encrypted password 'login';
create user admin WITH encrypted password 'admin';
create user wireless_operator WITH encrypted password 'wireless_operator';
create user field_wireman WITH encrypted password 'field_wireman';
create user computer_technician WITH encrypted password 'computer_technician';

-- create view
create view id_pw_view as
	select user_name, user_password
	from soldier_information;

-- set priviliage
grant select on id_pw_view to login;

grant all on soldier_information to admin;
grant all on wireless_operator to admin;
grant all on field_wireman to admin;
grant all on computer_technician to admin;
grant all on admin_soldier to admin;

grant all on sequence soldier_information_id_seq to admin;


