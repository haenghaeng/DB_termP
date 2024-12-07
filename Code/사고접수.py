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

# 사고 보고서 생성 함수
def create_incident_report(user_name, user_password, department, contact, details, related_units):
    conn = try_connection(user_name, user_password)  # 데이터베이스 연결
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO incident_reports (contact, details, related_units, department)
    VALUES (%s, %s, %s, %s) RETURNING id;  # 삽입 후 생성된 ID 반환
    """
    cursor.execute(insert_query, (contact, details, related_units, department))
    incident_id = cursor.fetchone()[0]  # 생성된 사고 보고서 ID 가져오기
    
    conn.commit()  # 변경 사항 커밋
    cursor.close()  # 커서 닫기
    conn.close()  # 연결 종료
    
    return incident_id  # 생성된 사고 보고서 ID 반환

# 사고 보고서 조회 함수
def read_incident_report(user_name, user_password, incident_id):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    select_query = "SELECT * FROM incident_reports WHERE id = %s;"  # 특정 ID의 사고 보고서 선택
    cursor.execute(select_query, (incident_id,))
    report = cursor.fetchone()  # 사고 보고서 데이터 가져오기
    
    cursor.close()
    conn.close()
    
    return report  # 사고 보고서 데이터 반환

# 모든 사고 보고서 목록 조회 함수
def list_all_incident_reports(user_name, user_password):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    select_query = "SELECT id, department FROM incident_reports;"  # 사고 보고서 ID와 부서 선택
    cursor.execute(select_query)
    reports = cursor.fetchall()  # 모든 사고 보고서 데이터 가져오기
    
    cursor.close()
    conn.close()
    
    return reports  # 사고 보고서 목록 반환

# 사고 보고서 업데이트 함수
def update_incident_report(user_name, user_password, incident_id, contact, details, related_units, department):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    update_query = """
    UPDATE incident_reports
    SET contact = %s, details = %s, related_units = %s, department = %s
    WHERE id = %s;  # 특정 ID의 사고 보고서 정보 업데이트
    """
    cursor.execute(update_query, (contact, details, related_units, department, incident_id))
    
    conn.commit()  # 변경 사항 커밋
    cursor.close()
    conn.close()

# 사고 보고서 삭제 함수
def delete_incident_report(user_name, user_password, incident_id):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    delete_query = "DELETE FROM incident_reports WHERE id = %s;"  # 특정 ID의 사고 보고서 삭제
    cursor.execute(delete_query, (incident_id,))
    
    # ID를 연속적으로 유지하기 위해 삭제된 ID 이후의 모든 ID를 1씩 감소시킴
    cursor.execute("""
        UPDATE incident_reports
        SET id = id - 1
        WHERE id > %s;
    """, (incident_id,))
    
    conn.commit()  # 변경 사항 커밋
    cursor.close()
    conn.close()

# 메시지 전송 함수
def send_incident_message(user_name, user_password, incident_id, sender_department, message):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO incident_messages (incident_id, sender_department, message)
    VALUES (%s, %s, %s);  # 새로운 메시지 삽입
    """
    cursor.execute(insert_query, (incident_id, sender_department, message))
    
    conn.commit()  # 변경 사항 커밋
    cursor.close()
    conn.close()

# 메시지 조회 함수
def read_incident_messages(user_name, user_password, incident_id):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    select_query = "SELECT id, sender_department, message, created_at FROM incident_messages WHERE incident_id = %s ORDER BY created_at ASC;"  # 특정 사고 보고서에 대한 메시지 조회
    cursor.execute(select_query, (incident_id,))
    messages = cursor.fetchall()  # 모든 메시지 데이터 가져오기
    
    cursor.close()
    conn.close()
    
    return messages  # 메시지 목록 반환

# 메시지 삭제 함수
def delete_incident_message(user_name, user_password, message_id, sender_department):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    # 메시지가 해당 부서에서 작성되었는지 확인
    select_query = "SELECT sender_department FROM incident_messages WHERE id = %s;"
    cursor.execute(select_query, (message_id,))
    result = cursor.fetchone()
    
    if result and result[0] == sender_department:  # 부서가 일치하는 경우
        delete_query = "DELETE FROM incident_messages WHERE id = %s;"  # 메시지 삭제
        cursor.execute(delete_query, (message_id,))
        print("메시지가 삭제되었습니다.")
    else:
        print("삭제 권한이 없습니다.")
    
    conn.commit()  # 변경 사항 커밋
    cursor.close()
    conn.close()

def main():
    user_name = "admin"  # 사용자 이름
    user_password = "admin"  # 비밀번호

    while True:
        print("\n사고 보고서 관리 시스템")
        print("1. 사고 보고서 생성")
        print("2. 사고 보고서 조회 및 메시지")
        print("3. 사고 보고서 업데이트")
        print("4. 사고 보고서 삭제")
        print("5. 나가기")

        choice = input("원하는 기능의 숫자를 입력하세요: ")

        if choice == '1':
            department = input("사고가 발생한 부서를 입력하세요: ")
            contact = input("연락처를 입력하세요: ")
            details = input("사고 상세 내용을 입력하세요: ")
            related_units = input("연계되는 반(쉼표로 구분)을 입력하세요: ").split(',')
            related_units = [unit.strip() for unit in related_units]  # 공백 제거
            report_id = create_incident_report(user_name, user_password, department, contact, details, related_units)
            print(f"사고 보고서 생성됨: ID {report_id}")
        
        elif choice == '2':
            # 기존 사고 보고서 ID와 부서 이름을 먼저 표시
            reports = list_all_incident_reports(user_name, user_password)
            print("\n전체 사고 보고서 목록:")
            for report in reports:
                print(f"ID: {report[0]}, 부서: {report[1]}")
            
            # 사용자가 조회할 사고 보고서 ID를 선택할 수 있게 함
            incident_id = int(input("조회할 사고 보고서의 ID를 입력하세요: "))
            report = read_incident_report(user_name, user_password, incident_id)
            if report:
                # 보고서 내용 출력
                print(f"보고서 내용:\nID: {report[0]},\n연락처: {report[1]},\n상세 내용: {report[2]},\n연계되는 반: {report[3]},\n발생 부서: {report[4]}")
                
                # 메시지 조회
                messages = read_incident_messages(user_name, user_password, incident_id)
                if messages:
                    print("\n메시지 목록:")
                    for msg in messages:
                        print(f"ID: {msg[0]} [{msg[3]}] {msg[1]}: {msg[2]}")
                else:
                    print("해당 사고 보고서에 대한 메시지가 없습니다.")
                
                # 메시지 전송 선택
                send_message = input("메시지를 보내시겠습니까? (y/n): ")
                if send_message.lower() == 'y':
                    sender_department = input("보내는 부서를 입력하세요: ")
                    message = input("메시지를 입력하세요: ")
                    send_incident_message(user_name, user_password, incident_id, sender_department, message)
                    print("메시지가 전송되었습니다.")
                
                # 메시지 삭제 선택
                delete_message = input("메시지를 삭제하시겠습니까? (y/n): ")
                if delete_message.lower() == 'y':
                    message_id = int(input("삭제할 메시지의 ID를 입력하세요: "))
                    sender_department = input("삭제 권한을 확인하기 위한 부서를 입력하세요: ")
                    delete_incident_message(user_name, user_password, message_id, sender_department)
            else:
                print("해당 ID의 사고 보고서가 존재하지 않습니다.")
        
        elif choice == '3':
            incident_id = int(input("업데이트할 사고 보고서의 ID를 입력하세요: "))
            contact = input("새로운 연락처를 입력하세요: ")
            details = input("새로운 사고 상세 내용을 입력하세요: ")
            related_units = input("새로운 연계되는 반(쉼표로 구분)을 입력하세요: ").split(',')
            related_units = [unit.strip() for unit in related_units]  # 공백 제거
            department = input("새로운 사고가 발생한 부서를 입력하세요: ")
            # 사고 보고서 업데이트 함수 호출
            update_incident_report(user_name, user_password, incident_id, contact, details, related_units, department)
            print("사고 보고서 업데이트 완료")
        
        elif choice == '4':
            # 모든 사고 보고서 목록 조회
            reports = list_all_incident_reports(user_name, user_password)
            print("\n전체 사고 보고서 목록:")
            for report in reports:
                print(f"ID: {report[0]}, 부서: {report[1]}")
                
            # 사용자가 삭제할 사고 보고서 ID 입력
            incident_id = int(input("삭제할 사고 보고서의 ID를 입력하세요: "))
            report = read_incident_report(user_name, user_password, incident_id)
            if report:
                # 사고 보고서 삭제 함수 호출
                delete_incident_report(user_name, user_password, incident_id)
                print("사고 보고서 삭제 완료")
            else:
                print("해당 ID의 사고 보고서가 존재하지 않습니다.")
        
        elif choice == '5':
            # 프로그램 종료
            print("프로그램을 종료합니다.")
            break
        
        else:
            # 잘못된 입력 처리
            print("잘못된 입력입니다. 다시 시도하세요.")

# 프로그램 시작
if __name__ == "__main__":
    main()
