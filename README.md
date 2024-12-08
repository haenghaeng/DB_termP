# 군대 내부 장비, 병사 관리 데이터베이스
이 프로젝트는 군 내부에서 장비를 요구하는 사건/사고가 발생 하였을경우, 사고를 DB에 등록하고 이를 해결하는 데 초점을 두었습니다. 사건/사고에 대응하는 무선/유선/전자장비를 반입/반출 할 수있고, 사건을 
해결하기 위해 각 부서간 의사소통을 원활하게 수행할 수 있도록 사건에 대한 개요나 메세지를 DB에 등록할 수 있습니다.

## 목차
1. [필요한 프로그램 및 라이브러리](#필요한-프로그램-및-라이브러리)
2. [설치](#설치)
3. [사용방법](#사용방법)
    1. [사용자](#사용자)
    2. [예제](#예제)
4. [예제 데이터 SQL](#예제-데이터-sql)

## 필요한 프로그램 및 라이브러리
- python3 : psycopg2, hashlib (필수)
- postgreSQL (필수)
- DBeaver(권장)

## 설치
1) postgreSQL을 설치합니다.

2) psycopg2, hashlib 라이브러리를 설치합니다.

3) 터미널에서 postgreSQL설치 시 등록한 슈퍼계정으로 접속합니다. 기본값은 아래와 같습니다.
```shell
psql -U postgres -h localhost
```

4) tablespace를 적절한 위치에 생성합니다. 이름은 사용자가 원하는 대로 지정하셔도 됩니다.
``` shell
CREATE tablespace ts_termp
owner postgres
location 'D:\Program Files\PostgreSQL\15\data\db_termp';
```

5) \db 명령어를 사용하여 tablespace가 생성되었는 지 확인합니다.
``` shell
\db
```

6) database를 생성합니다. 이름은 사용자가 원하는대로 지정해도 됩니다.
``` shell
CREATE database db_termp
owner postgres
tablespace ts_termp;
```

7) \l+ 명령어를 사용하여 database가 생성되었는 지 확인합니다.
``` shell
\l+
```

8) \q 명령어를 사용하여 종료합니다.
``` shell
\q
```

9) postgres 계정으로 db_termp에 접속합니다. DBeaver가 있다면 DBeaver로 연결하셔도 됩니다.
``` shell
psql -U postgres -h localhost -d db_termp
```

10) ``Code`` 폴더 내부의 ``tableInit.sql``을 실행합니다.

11) 테이블에 데이터가 잘 들어갔는 지 확인합니다.
``` SQL
select * from soldier_information;
select * from wireless_operator;
...
```

## 사용방법

### 사용자
사용자는 크게 6가지로 구분되어 있습니다. 이 중, ``login``을 제외한 5가지를 사용자가 직접 사용하게 됩니다.</br>
``login``, ``admin``, ``wireless_operator``, ``field_wireman``, ``computer_technician``, ``etc``

- login</br>
로그인 시 임시로 사용하는 사용자입니다. soldier_information 에서 군번, 비밀번호, 소속반을 view 형태로 받아와 사용자의 입력값과 비교한 뒤 접속을 허용합니다.
- admin</br>
 DB 전체를 관리하는 사용자입니다. 장비, 사고, 메세지 관리를 위해 모든 테이블에 접근
가능합니다.
- wireless_operator</br>
무선반 병사입니다. 무선반 장비 관리, 사고 해결, 메세지 등록이 가능합니다.</br>
wireless_equipment, incident_reports, incident_messages 테이블에 접근 가능합니다.
- field_wireman</br>
유선반 병사입니다. 유선반 장비 관리, 사고 해결, 메세지 등록이 가능합니다.</br>
 wireless_equipment, incident_reports, incident_messages 테이블에 접근 가능합니다.
- computer_technician</br>
전장반 병사입니다. 전자 장비반 장비 관리, 사고 해결, 메세지 등록이 가능합니다.</br>
 wireless_equipment, incident_reports, incident_messages 테이블에 접근 가능합니다.
- etc</br>
반에 소속되지 않은 일반 병사입니다. incident_reports에 사고를 등록 할 수 있습니다.

### 예제
- ``main.py``를 실행하여 프로그램을 실행합니다. 다음과 같은 메세지가 터미널에 출력됩니다.
``` terminal
원하는 기능의 숫자를 입력해주세요 
(1) 로그인
(2) 종료
```
- 1을 누르고 Enter키를 누르면 군번을 입력받는 메세지가 출력됩니다.</br>
``` termianl
군번을 입력해주세요
```

``tableInit.sql``파일을 정상적으로 실행하였다면, ``login``을 제외한 5개 역할 각각에 대한 계정이 DB에 이미 들어있습니다. 이 예제에서는 ``wireless_operator(무선반 병사)``계정으로 들어가겠습니다. 무선반 병사 이외 다른 계정으로 접속해보고 싶으시면 ``예제 데이터 SQL``을 참고해주세요.</br></br>
**기본값으로 병사의 군번과 비밀번호는 같도록 예제 데이터가 들어가 있습니다.**

``` terminal
군번을 입력해주세요 19-70007563
비밀번호를 입력해주세요 19-70007563
무선반 접속

원하는 기능의 숫자를 입력해주세요 
(1) 무선 장비 관리
(2) 종료
```
- 1을 누르고 Enter를 눌러 무선 장비 관리를 할 수 있습니다.

``` terminal
무선장비 관리 시스템
1. 장비 생성
2. 장비 조회
3. 장비 수량 업데이트
4. 장비 삭제
5. 사고 해결
6. 메시지 관리
7. 나가기
```
- 1을 입력하여 장비 생성 화면으로 넘어갑니다. 장비의 이름, 수량을 입력하고 Enter키를 누릅니다.
``` terminal
무선장비 관리 시스템
1. 장비 생성
2. 장비 조회
3. 장비 수량 업데이트
4. 장비 삭제
5. 사고 해결
6. 메시지 관리
7. 나가기
원하는 기능의 숫자를 입력하세요: 1
장비 이름을 입력하세요: 좋은무전기
장비 수량을 입력하세요: 10
좋은무전기 장비가 생성되었습니다. 새 ID: 4
```

- 장비 조회를 위해 2를 입력한 뒤 장비의 이름을 입력합니다.
``` terminal
무선장비 관리 시스템
1. 장비 생성
2. 장비 조회
3. 장비 수량 업데이트
4. 장비 삭제
5. 사고 해결
6. 메시지 관리
7. 나가기
원하는 기능의 숫자를 입력하세요: 2
조회하고 싶은 장비의 이름을 입력하세요: 좋은무전기
장비 정보 - ID: 4, 이름: 좋은무전기, 수량: 10
```

- 장비 수량 업데이트를 위해 3을 입력한 뒤, 장비를 가져가거나, 반납할 수 있습니다.
``` terminal
무선장비 관리 시스템
1. 장비 생성
2. 장비 조회
3. 장비 수량 업데이트
4. 장비 삭제
5. 사고 해결
6. 메시지 관리
7. 나가기
원하는 기능의 숫자를 입력하세요: 3
무엇을 하시겠습니까?
1. 장비 가져감.
2. 장비 반납.
숫자 선택: 1
장비의 이름을 입력하세요: 좋은무전기
수량을 입력하세요: 1
좋은무전기 장비의 수량이 업데이트되었습니다. 현재 수량: 9.
```

- DB에 등록된 장비를 삭제할 수 있습니다.
``` terminal
무선장비 관리 시스템
1. 장비 생성
2. 장비 조회
3. 장비 수량 업데이트
4. 장비 삭제
5. 사고 해결
6. 메시지 관리
7. 나가기
원하는 기능의 숫자를 입력하세요: 4
삭제할 장비의 이름을 입력하세요: 좋은무전기
장비가 삭제되었습니다.
```
- 무선 장비를 요구하는 사고를 확인하고, 장비가 충분하다면 사고에 보급할 수 있습니다.
``` terminal
무선장비 관리 시스템
1. 장비 생성
2. 장비 조회
3. 장비 수량 업데이트
4. 장비 삭제
5. 사고 해결
6. 메시지 관리
7. 나가기
원하는 기능의 숫자를 입력하세요: 5
현재 해결할 수 있는 사고 목록:
ID: 2, 사고 발생 부서: 왈왈대대, 연락처: 01087654321, 내용: 무전기 3개 분실, 필요한 장비: 무전기, 수량: 3
ID: 3, 사고 발생 부서: 무슨대대, 연락처: 01013572468, 내용: 작업 도중 케이블 끊어짐, 필요한 장비: 핸드폰, 수량: 1
ID: 1, 사고 발생 부서: 멍멍대대, 연락처: 01012345678, 내용: 전화기 수화기 선 끊어짐, 컴퓨터 모니터 깨짐, 필요한 장비: 무전기, 수량: 2
해결하고 싶은 사고의 ID를 입력하세요: 1
사고 ID: 1, 사고 발생 부서: 멍멍대대, 연락처: 01012345678, 내용: 전화기 수화기 선 끊어짐, 컴퓨터 모니터 깨짐, 필요한 장비: 무전기, 수량: 2
에 대한 무선 사고 수리가 완료되었습니다.
```
- 현재 부서에 등록된 메세지를 확인하거나 삭제하고 타 부서에 메세지를 보낼 수 있습니다.
``` terminal
무선장비 관리 시스템
1. 장비 생성
2. 장비 조회
3. 장비 수량 업데이트
4. 장비 삭제
5. 사고 해결
6. 메시지 관리
7. 나가기
원하는 기능의 숫자를 입력하세요: 6

메시지 관리
1. 메시지 확인하기
2. 메시지 보내기
3. 메시지 삭제하기
4. 나가기
```
- 부서별로 등록된 메세지를 확인할 수 있습니다.
``` terminal
메시지 관리
1. 메시지 확인하기
2. 메시지 보내기
3. 메시지 삭제하기
4. 나가기
원하는 기능의 숫자를 입력하세요: 1
메시지 목록: 
field_wireman, 내용: 전화기 선 연결 완료
wireless_operator, 내용: 전장반 지원 바람
computer_technician, 내용: 지금 작업 중
```

- 새로운 메세지를 등록할 수 있습니다.
``` termianl
메시지 관리
1. 메시지 확인하기
2. 메시지 보내기
3. 메시지 삭제하기
4. 나가기
원하는 기능의 숫자를 입력하세요: 2
보낼 메시지를 입력하세요: 테스트 메세지 입니다.
메시지가 성공적으로 전송되었습니다.
```

- 등록된 메세지를 삭제할 수 있습니다. 자신의 부서와 일치하는 메세지만 삭제할 수 있습니다.
``` terminal
메시지 관리
1. 메시지 확인하기
2. 메시지 보내기
3. 메시지 삭제하기
4. 나가기
원하는 기능의 숫자를 입력하세요: 3

삭제 가능한 메시지 목록:
ID: 2, 내용: 전장반 지원 바람, 보낸 시간: 2024-12-08 20:29:43.387931
ID: 4, 내용: 테스트 메세지 입니다., 보낸 시간: 2024-12-08 21:24:14.146701
삭제할 메시지의 ID를 입력하세요: 4
메시지가 성공적으로 삭제되었습니다.
```

기타 자세한 기능은 최종보고서를 참고 부탁드립니다.



## 예제 데이터 SQL
이 SQL 구문은 ``tableInit.sql``에 포함되어 있습니다. ``tableInit.sql``을 실행하였다면 이 구문을 별도로 실행할 필요는 없습니다.
``` SQL
-- insert data
-- 로그인 시 user_password는 army_number 같습니다.
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
```