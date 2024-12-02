pip install psycopg2
pip install psycopg2-binary

import psycopg2

# PostgreSQL 데이터베이스에 연결
def try_connection(user_name, user_password):
    return psycopg2.connect(
        database="db_termp",  # 데이터베이스 이름
        user=user_name,       # 사용자 이름
        password=user_password,  # 비밀번호
        host="::1",           # 호스트 주소 (여기서는 IPv6의 localhost)
        port="5432"           # 포트 번호 (기본값 5432)
    )

def create_tables(user_name, user_password):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    # 테이블 생성 SQL 쿼리
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS wireless_equipment (
            id SERIAL PRIMARY KEY,  -- 장비 고유 ID
            name VARCHAR(255) NOT NULL,  -- 장비 이름
            quantity INT NOT NULL  -- 보유량
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS wired_equipment (
            id SERIAL PRIMARY KEY,  -- 장비 고유 ID
            name VARCHAR(255) NOT NULL,  -- 장비 이름
            quantity INT NOT NULL  -- 보유량
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS computer_equipment (
            id SERIAL PRIMARY KEY,  -- 장비 고유 ID
            name VARCHAR(255) NOT NULL,  -- 장비 이름
            quantity INT NOT NULL  -- 보유량
        );
        """,
        """
        DROP TABLE IF EXISTS incident_reports;

        CREATE TABLE incident_reports (
            id SERIAL PRIMARY KEY,  -- 사고 고유 ID
            contact VARCHAR(255) NOT NULL,  -- 연락처
            details TEXT NOT NULL,  -- 사고 상세 내용
            related_units TEXT[],  -- 연계되는 반 (배열)
            department VARCHAR(255) NOT NULL  -- 사고 발생 부서
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS incident_messages (
            id SERIAL PRIMARY KEY,
            incident_id INT REFERENCES incident_reports(id),
            sender_department VARCHAR(255),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]

    for query in create_table_queries:
        cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    user_name = "admin"  # 사용자 이름
    user_password = "admin"  # 비밀번호
    create_tables(user_name, user_password)
