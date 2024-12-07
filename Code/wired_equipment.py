import psycopg2
import psycopg2.sql
import psycopg2.errors

# PostgreSQL 데이터베이스에 연결
def try_connection(user_name, user_password):
    return psycopg2.connect(
        database="db_termp",  # 데이터베이스 이름
        user=user_name,       # 사용자 이름
        password=user_password,  # 비밀번호
        host="::1",           # 호스트 주소 (여기서는 IPv6의 localhost)
        port="5432"           # 포트 번호 (기본값 5432)
    )

# 장비 생성 또는 업데이트 함수
def create_or_update_wired_equipment(cursor, name, quantity):
    try:
        cursor.execute("SELECT id, quantity FROM wired_equipment WHERE name = %s;", (name,))
        result = cursor.fetchone()

        if result:  # 장비가 존재하는 경우
            equipment_id, existing_quantity = result
            new_quantity = existing_quantity + quantity  # 기존 수량에 새로운 수량 추가
            cursor.execute("""
                UPDATE wired_equipment SET quantity = %s WHERE id = %s;
            """, (new_quantity, equipment_id))
            print(f"{name} 장비의 수량이 {existing_quantity}에서 {new_quantity}로 업데이트되었습니다.")
        else:  # 장비가 존재하지 않는 경우
            cursor.execute("""
                INSERT INTO wired_equipment (name, quantity) VALUES (%s, %s)
                           RETURNING id;
                """, (name, quantity))
            new_id = cursor.fetchone()[0]
            print(f"{name} 장비가 생성되었습니다. 새 ID: {new_id}")
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
    except psycopg2.errors.InvalidTextRepresentation:
        print("잘못된 입력 값을 입력하였습니다.")
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")
# 장비 생성 또는 업데이트를 위한 입력 처리 함수
def handle_create_or_update_wired_equipment(user_name, user_password):
    name = input("장비 이름을 입력하세요: ")
    try:
        quantity = int(input("장비 수량을 입력하세요: "))
        if quantity < 0:
            raise ValueError("수량은 음수가 될 수 없습니다.")
        perform_crud_operations(user_name, user_password, 'create', name, quantity)  # 장비 생성
    except ValueError as e:
        print(f"잘못된 입력: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")


# 유선 장비 조회 함수
def search_wired_equipment(cursor, name):
    cursor.execute("SELECT id, name, quantity FROM wired_equipment WHERE name = %s;", (name,))
    return cursor.fetchall() 
# 장비 목록 조회 함수
def handle_search_wired_equipment(user_name, user_password):
    name = input("조회하고 싶은 장비의 이름을 입력하세요: ")
    equipment = perform_crud_operations(user_name, user_password, 'search', name)  # 장비 목록 조회
    if equipment:
        print(f"장비 정보 - ID: {equipment[0][0]}, 이름: {equipment[0][1]}, 수량: {equipment[0][2]}")
    else:
        print("해당 이름의 장비가 없습니다.")


# 유선 장비 수량 업데이트 함수
def update_wired_equipment_quantity(cursor, equipment_id, quantity):
    try:
        quantity = int(quantity)  # 숫자인지 확인
        if quantity < 0:
            raise ValueError("수량은 0보다 크거나 같아야 합니다.")
        cursor.execute("""
            UPDATE wired_equipment SET quantity = %s WHERE id = %s;
        """, (quantity, equipment_id))
        print(f"장비 ID {equipment_id}의 수량이 {quantity}로 업데이트되었습니다.")
    except ValueError as e:
        print(f"잘못된 입력: {e}")
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")
# 장비 수량 업데이트 함수
def handle_update_wired_equipment_quantity(user_name, user_password):
    print("무엇을 하시겠습니까?\n1. 장비 가져감.\n2. 장비 반납.")
    sub_choice = input("숫자 선택: ")

    if sub_choice == '1':
        name = input("가져갈 장비의 이름을 입력하세요: ")
        equipment = perform_crud_operations(user_name, user_password, 'search', name)  # 장비 검색
        if equipment:
            available_quantity = equipment[0][2]
            try:
                quantity = int(input("가져갈 장비 수량을 입력하세요: "))
                if quantity < 0:
                    raise ValueError("수량은 음수가 될 수 없습니다.")
                if available_quantity >= quantity:
                    new_quantity = available_quantity - quantity
                    perform_crud_operations(user_name, user_password, 'update_quantity', equipment[0][0], new_quantity)  # 장비 수량 업데이트
                    print(f"{name} 장비를 {quantity}개 가져갔습니다. 남은 수량: {new_quantity}")
                else:
                    print(f"{name}의 수량이 부족합니다! 현재 수량: {available_quantity}")
            except ValueError as e:
                print(f"잘못된 입력: {e}")
        else:
            print(f"{name}을 가진 이름의 장비는 없습니다.")

    elif sub_choice == '2':
        name = input("반납할 장비의 이름을 입력하세요: ")
        equipment = perform_crud_operations(user_name, user_password, 'search', name)  # 장비 검색
        try:
            quantity = int(input("반납할 장비 수량을 입력하세요: "))
            if quantity < 0:
                raise ValueError("수량은 음수가 될 수 없습니다.")
            if equipment:
                new_quantity = equipment[0][2] + quantity
                perform_crud_operations(user_name, user_password, 'update_quantity', equipment[0][0], new_quantity)  # 장비 수량 업데이트
                print(f"{name} 장비를 {quantity}개 반납했습니다. 현재 수량: {new_quantity}")
            else:
                perform_crud_operations(user_name, user_password, 'create', name, quantity)  # 장비 생성
                print(f"{name} 장비가 {quantity}개 반납되었습니다. 현재 수량: {quantity}")
        except ValueError as e:
            print(f"잘못된 입력: {e}")
    else:
        print("잘못된 입력입니다. 다시 시도하세요.")


# 유선 장비 삭제 함수
def delete_wired_equipment(cursor, equipment_id):
    cursor.execute("DELETE FROM wired_equipment WHERE id = %s;", (equipment_id,))  # 특정 ID의 장비 삭제
    cursor.execute("""
        UPDATE wired_equipment SET id = id - 1 WHERE id > %s;
    """, (equipment_id,))
    cursor.execute("""
        SELECT setval('wired_equipment_id_seq', (SELECT MAX(id) FROM wired_equipment));
    """)
# 장비 삭제 함수
def handle_delete_wired_equipment(user_name, user_password):
    name = input("삭제할 장비의 이름을 입력하세요: ")
    equipment = perform_crud_operations(user_name, user_password, 'search', name)  # 장비 검색
    if equipment:
        equipment_id = equipment[0][0]  # ID 가져오기
        perform_crud_operations(user_name, user_password, 'delete', equipment_id)  # 장비 삭제
        print("장비가 삭제되었습니다.")
    else:
        print("해당 이름의 장비가 존재하지 않습니다.")

# 사고 목록 조회 함수
def read_incidents(cursor):
    cursor.execute("SELECT id, contact, details, wired_tool_name, wired_tool_quantity, department FROM incident_reports WHERE wired_tool_quantity > 0;")
    return cursor.fetchall() or []


# 유선 장비 사용 함수
def use_wired_equipment(cursor, incident_id):
    cursor.execute("SELECT contact, details, wired_tool_name, wired_tool_quantity, department FROM incident_reports WHERE id = %s;", (incident_id,))
    incident = cursor.fetchone()

    if incident:
        contact, details, tool_name, tool_quantity, department = incident
        print(f"사고 ID: {incident_id}, 사고 발생 부서: {department}, 연락처: {contact}, 내용: {details}, 필요한 장비: {tool_name}, 수량: {tool_quantity}")

        cursor.execute("SELECT quantity FROM wired_equipment WHERE name = %s;", (tool_name,))
        equipment = cursor.fetchone()

        if equipment:
            available_quantity = equipment[0]
            if available_quantity >= tool_quantity:
                new_quantity = available_quantity - tool_quantity
                cursor.execute("UPDATE wired_equipment SET quantity = %s WHERE name = %s;", (new_quantity, tool_name))
                cursor.execute("UPDATE incident_reports SET wired_tool_quantity = 0 WHERE id = %s;", (incident_id,))
                print("에 대한 유선 사고 수리가 완료되었습니다.")
            else:
                shortage = tool_quantity - available_quantity
                print(f"{tool_name}의 개수가 부족합니다! {tool_name}: {shortage}개가 필요합니다.")
        else:
            print("도구가 존재하지 않습니다!")
    else:
        print("해결할 수 있는 사고가 없습니다.")
# 장비 사용 함수
def handle_use_wired_equipment(user_name, user_password):
    incident_list = perform_crud_operations(user_name, user_password, 'read_incidents')
    if incident_list:
        print("현재 해결할 수 있는 사고 목록:")
        for incident in incident_list:
            print(f"ID: {incident[0]}, 사고 발생 부서: {incident[5]}, 연락처: {incident[1]}, 내용: {incident[2]}, 필요한 장비: {incident[3]}, 수량: {incident[4]}")

        try:
            incident_id = int(input("해결하고 싶은 사고의 ID를 입력하세요: "))
            # ID가 목록에 존재하는지 확인
            valid_ids = [incident[0] for incident in incident_list]
            if incident_id not in valid_ids:
                print("해결할 수 없는 사고입니다. 목록에 없는 ID입니다.")
            else:
                perform_crud_operations(user_name, user_password, 'use', incident_id)  # 장비 사용
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요.")
    else:
        print("현재 해결할 수 있는 사고가 없습니다.")


# 메시지 전송 함수
def send_message(cursor, sender_department, message):
    cursor.execute("""
        INSERT INTO incident_messages (sender_department, message)
        VALUES (%s, %s);
    """, (sender_department, message))
# 메시지 목록 조회 함수
def read_messages(cursor):
    cursor.execute("SELECT sender_department, message, created_at FROM incident_messages ORDER BY created_at ASC;")
    return cursor.fetchall()
# 메시지 관리 함수
def handle_message_management(user_name, user_password, user_department):
    while True:
        messages = perform_crud_operations(user_name, user_password, 'read_messages')
        if messages:
            print("\n메시지 목록:")
            for msg in messages:
                print(f"{msg[0]} - 내용: {msg[1]}")
        else:
            print("메시지가 없습니다.")
        print("\n메시지 관리")
        print("1. 메시지 보내기")
        print("2. 메시지 삭제하기")
        print("3. 나가기")
        
        sub_choice = input("원하는 기능의 숫자를 입력하세요: ").strip()
        
        if sub_choice == '1':  # 메시지 보내기
            message_content = input("보낼 메시지를 입력하세요: ").strip()
            if message_content:
                try:
                    perform_crud_operations(user_name, user_password, 'send_message', user_department, message_content)
                    print("메시지가 성공적으로 전송되었습니다.")
                except Exception as e:
                    print(f"메시지 전송 중 오류 발생: {e}")
            else:
                print("메시지 내용이 비어있습니다. 다시 시도하세요.")
        
        elif sub_choice == '2':  # 메시지 삭제하기
            conn = try_connection(user_name, user_password)
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT id, message, created_at FROM incident_messages
                    WHERE sender_department = %s
                    ORDER BY created_at ASC;
                """, (user_department,))
                filtered_messages = cursor.fetchall()
                
                if filtered_messages:
                    print("\n삭제 가능한 메시지 목록:")
                    for idx, msg in enumerate(filtered_messages, start=1):
                        print(f"ID: {msg[0]}, 내용: {msg[1]}, 보낸 시간: {msg[2]}")
                    
                    try:
                        delete_id = int(input("삭제할 메시지의 ID를 입력하세요: ").strip())
                        cursor.execute("""
                            DELETE FROM incident_messages
                            WHERE id = %s AND sender_department = %s;
                        """, (delete_id, user_department))
                        conn.commit()
                        print("메시지가 성공적으로 삭제되었습니다.")
                    except ValueError:
                        print("숫자를 입력하세요. 다시 시도하세요.")
                else:
                    print("삭제할 메시지가 없습니다.")
            except Exception as e:
                print(f"오류 발생: {e}")
            finally:
                cursor.close()
                conn.close()
        
        elif sub_choice == '3':  # 나가기
            print("메시지 관리에서 나갑니다.")
            break
        
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

# CRUD 작업 수행 함수
def perform_crud_operations(user_name, user_password, operation, *args):
    conn = try_connection(user_name, user_password)  # 데이터베이스 연결
    cursor = conn.cursor()
    result = None
    if operation == 'create':
        create_or_update_wired_equipment(cursor, *args)  # 장비 생성 또는 업데이트
    elif operation == 'search':
        result = search_wired_equipment(cursor, *args)  # 장비 목록 조회
    elif operation == 'update_quantity':
        update_wired_equipment_quantity(cursor, *args)  # 장비 수량 업데이트
    elif operation == 'delete':
        delete_wired_equipment(cursor, *args)  # 장비 삭제
    elif operation == 'use':
        use_wired_equipment(cursor, *args)  # 장비 사용
    elif operation == 'read_incidents':
        return read_incidents(cursor)  # 사고 목록 조회
    elif operation == 'send_message':
        send_message(cursor, *args)
    elif operation == 'read_messages':
        result = read_messages(cursor)
    else:
        print("Invalid operation.")  # 유효하지 않은 작업

    conn.commit()  # 변경 사항 커밋
    cursor.close()  # 커서 닫기
    conn.close()  # 연결 종료
    return result


# 메인 함수
def main():
    user_name = "admin"  # 사용자 이름
    user_password = "admin"  # 비밀번호
    user_department = "유선반"  # 메시지 보내는 반

    while True:
        print("\n유선장비 관리 시스템")
        print("1. 장비 생성")  # 장비 추가
        print("2. 장비 목록")  # 장비 조회
        print("3. 장비 수량 업데이트")  # 장비 수량 수정
        print("4. 장비 삭제")  # 장비 삭제
        print("5. 장비 사용")  # 장비 사용
        print("6. 메시지")
        print("7. 나가기")  # 프로그램 종료
        
        choice = input("원하는 기능의 숫자를 입력하세요: ")

        if choice == '1':
            handle_create_or_update_wired_equipment(user_name, user_password)  # 장비 생성 또는 업데이트
        elif choice == '2':
            handle_search_wired_equipment(user_name, user_password)  # 장비 목록 조회
        elif choice == '3':
            handle_update_wired_equipment_quantity(user_name, user_password)  # 장비 수량 업데이트
        elif choice == '4':
            handle_delete_wired_equipment(user_name, user_password)  # 장비 삭제
        elif choice == '5':
            handle_use_wired_equipment(user_name, user_password)  # 장비 사용
        elif choice == '6':
            handle_message_management(user_name, user_password, user_department)  # 메시지 관리
        elif choice == '7':
            print("프로그램을 종료합니다.")  # 프로그램 종료 메시지
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")  # 잘못된 입력 처리

# 프로그램 시작
if __name__ == "__main__":
    main()  # 메인 함수 호출
