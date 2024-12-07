import psycopg2
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

# 장비 생성 또는 업데이트를 위한 입력 처리 및 데이터베이스 작업 함수
def create_or_update_computer_equipment(user_name, user_password):
    name = input("장비 이름을 입력하세요: ")
    try:
        quantity = int(input("장비 수량을 입력하세요: "))
        if quantity < 0:
            raise ValueError("수량은 음수가 될 수 없습니다.")
        
        conn = try_connection(user_name, user_password)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, quantity FROM computer_equipment WHERE name = %s;", (name,))
        result = cursor.fetchone()

        if result:  # 장비가 존재하는 경우
            equipment_id, existing_quantity = result
            new_quantity = existing_quantity + quantity  # 기존 수량에 새로운 수량 추가
            cursor.execute("UPDATE computer_equipment SET quantity = %s WHERE id = %s;", (new_quantity, equipment_id))
            print(f"{name} 장비의 수량이 {existing_quantity}에서 {new_quantity}로 업데이트되었습니다.")
        else:  # 장비가 존재하지 않는 경우
            cursor.execute("INSERT INTO computer_equipment (name, quantity) VALUES (%s, %s) RETURNING id;", (name, quantity))
            new_id = cursor.fetchone()[0]
            print(f"{name} 장비가 생성되었습니다. 새 ID: {new_id}")

        conn.commit()  # 변경 사항 커밋
    except ValueError as e:
        print(f"잘못된 입력: {e}")
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
    except psycopg2.errors.InvalidTextRepresentation:
        print("잘못된 입력 값을 입력하였습니다.")
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")
    finally:
        cursor.close()
        conn.close()

# 컴퓨터 장비 조회 함수
def search_computer_equipment(cursor, name):
    cursor.execute("SELECT id, name, quantity FROM computer_equipment WHERE name = %s;", (name,))
    return cursor.fetchall() 

# 장비 목록 조회 함수
def handle_search_computer_equipment(user_name, user_password):
    name = input("조회하고 싶은 장비의 이름을 입력하세요: ")
    equipment = perform_crud_operations(user_name, user_password, 'search_computer', name)  # 장비 목록 조회
    if equipment:
        print(f"장비 정보 - ID: {equipment[0][0]}, 이름: {equipment[0][1]}, 수량: {equipment[0][2]}")
    else:
        print("해당 이름의 장비가 없습니다.")

# 장비 수량 업데이트 및 입력 처리 함수
def update_computer_equipment_quantity(user_name, user_password, equipment_id=None, delta_quantity=None):
    if equipment_id is None or delta_quantity is None:
        sub_choice = input("무엇을 하시겠습니까?\n1. 장비 가져감.\n2. 장비 반납.\n숫자 선택: ")

        name = input("장비의 이름을 입력하세요: ")
        equipment = perform_crud_operations(user_name, user_password, 'search_computer', name)  # 장비 검색

        if equipment:
            available_quantity = equipment[0][2]
            try:
                quantity = int(input("수량을 입력하세요: "))
                if quantity < 0:
                    raise ValueError("수량은 음수가 될 수 없습니다.")
                
                if sub_choice == '1':  # 장비 가져감
                    if available_quantity >= quantity:
                        delta_quantity = -quantity
                    else:
                        print(f"{name}의 수량이 부족합니다! 현재 수량: {available_quantity}")
                        return
                elif sub_choice == '2':  # 장비 반납
                    delta_quantity = quantity
                
                equipment_id = equipment[0][0]  # ID 가져오기
            except ValueError as e:
                print(f"잘못된 입력: {e}")
                return
        else:
            print(f"{name}을 가진 이름의 장비는 없습니다.")
            return

    # 데이터베이스 작업
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE computer_equipment SET quantity = quantity + %s WHERE id = %s;", (delta_quantity, equipment_id))
        
        # 업데이트 후 현재 수량 조회
        cursor.execute("SELECT name, quantity FROM computer_equipment WHERE id = %s;", (equipment_id,))
        updated_equipment = cursor.fetchone()
        
        if updated_equipment:
            updated_name, updated_quantity = updated_equipment
            print(f"{updated_name} 장비의 수량이 업데이트되었습니다. 현재 수량: {updated_quantity}.")
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

# 컴퓨터 장비 삭제 및 입력 처리 함수
def delete_computer_equipment(user_name, user_password):
    name = input("삭제할 장비의 이름을 입력하세요: ")
    equipment = perform_crud_operations(user_name, user_password, 'search_computer', name)  # 장비 검색
    
    if equipment:
        equipment_id = equipment[0][0]  # ID 가져오기
        
        # 데이터베이스 작업
        conn = try_connection(user_name, user_password)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM computer_equipment WHERE id = %s;", (equipment_id,))  # 특정 ID의 장비 삭제
            cursor.execute("UPDATE computer_equipment SET id = id - 1 WHERE id > %s;", (equipment_id,))
            cursor.execute("SELECT setval('computer_equipment_id_seq', (SELECT MAX(id) FROM computer_equipment));")
            conn.commit()  # 변경 사항 커밋
            
            print("장비가 삭제되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 오류: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("해당 이름의 장비가 존재하지 않습니다.")

# 사고 목록 조회 함수
def read_incidents(cursor):
    cursor.execute("SELECT id, contact, details, computer_tool_name, computer_tool_quantity, department FROM incident_reports WHERE computer_tool_quantity > 0;")
    return cursor.fetchall() or []

# 장비 사용 함수 (컴퓨터 장비)
def handle_use_computer_equipment(user_name, user_password):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    try:
        incident_list = perform_crud_operations(user_name, user_password, 'read_incidents')
        if incident_list:
            # 사고 목록을 오름차순으로 정렬하여 출력
            print("현재 해결할 수 있는 사고 목록:")
            incident_list.sort(key=lambda x: x[0])  # ID를 기준으로 정렬
            for incident in incident_list:
                print(f"ID: {incident[0]}, 사고 발생 부서: {incident[5]}, 연락처: {incident[1]}, 내용: {incident[2]}, 필요한 장비: {incident[3]}, 수량: {incident[4]}")
            
            try:
                incident_id = int(input("해결하고 싶은 사고의 ID를 입력하세요: "))
                if incident_id in [incident[0] for incident in incident_list]:
                    cursor.execute("SELECT contact, details, computer_tool_name, computer_tool_quantity, department FROM incident_reports WHERE id = %s;", (incident_id,))
                    incident = cursor.fetchone()
                    
                    if incident:
                        contact, details, tool_name, tool_quantity, department = incident
                        print(f"사고 ID: {incident_id}, 사고 발생 부서: {department}, 연락처: {contact}, 내용: {details}, 필요한 장비: {tool_name}, 수량: {tool_quantity}")

                        cursor.execute("SELECT quantity FROM computer_equipment WHERE name = %s;", (tool_name,))
                        equipment = cursor.fetchone()
                        
                        if equipment:
                            available_quantity = equipment[0]
                            if available_quantity >= tool_quantity:
                                new_quantity = available_quantity - tool_quantity
                                cursor.execute("UPDATE computer_equipment SET quantity = %s WHERE name = %s;", (new_quantity, tool_name))
                                cursor.execute("UPDATE incident_reports SET computer_tool_quantity = 0 WHERE id = %s;", (incident_id,))
                                print("수리가 완료되었습니다.")
                            else:
                                shortage = tool_quantity - available_quantity
                                print(f"{tool_name}의 개수가 부족합니다! {tool_name}: {shortage}개가 필요합니다.")
                        else:
                            print("도구가 존재하지 않습니다!")
                    else:
                        print("해결할 수 있는 사고가 없습니다.")
                else:
                    print("해결할 수 없는 사고입니다. 목록에 없는 ID입니다.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력하세요.")
        else:
            print("현재 해결할 수 있는 사고가 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        conn.commit()  # 모든 작업이 끝난 후 커밋
        cursor.close()
        conn.close()

# 메시지 목록 조회 함수
def read_messages(cursor):
    cursor.execute("SELECT id, sender_department, message, created_at FROM incident_messages ORDER BY created_at ASC;")
    return cursor.fetchall()

# 메시지 관리 및 전송 함수
def manage_messages(user_name, user_password, user_department):
    while True:
        conn = try_connection(user_name, user_password)
        cursor = conn.cursor()
        messages = read_messages(cursor)  # 메시지 목록 조회

        if messages:
            print("\n메시지 목록:")
            for msg in messages:
                print(f"ID: {msg[0]}, 부서: {msg[1]}, 내용: {msg[2]}, 보낸 시간: {msg[3]}")
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
            delete_messages = read_messages(cursor)  # 메시지 목록 조회
            
            if delete_messages:
                print("\n삭제 가능한 메시지 목록:")
                for msg in delete_messages:
                    if msg[1] == user_department:  # 자신의 부서에서 보낸 메시지인지 확인
                        print(f"ID: {msg[0]}, 내용: {msg[2]}, 보낸 시간: {msg[3]}")
                
                try:
                    delete_id = int(input("삭제할 메시지의 ID를 입력하세요: ").strip())
                    # 해당 메시지가 자신의 부서에서 보낸 것인지 확인
                    if any(msg[0] == delete_id and msg[1] == user_department for msg in delete_messages):
                        perform_crud_operations(user_name, user_password, 'delete_message', delete_id, user_department)
                        print("메시지가 성공적으로 삭제되었습니다.")
                    else:
                        print("해당 ID의 메시지는 자신의 부서에서 보낸 것이 아니므로 삭제할 수 없습니다.")
                except ValueError:
                    print("숫자를 입력하세요. 다시 시도하세요.")
            else:
                print("삭제할 메시지가 없습니다.")
        
        elif sub_choice == '3':  # 나가기
            print("메시지 관리에서 나갑니다.")
            break
        
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")
        
        cursor.close()
        conn.close()

# CRUD 작업 수행 함수
def perform_crud_operations(user_name, user_password, operation, *args):
    conn = try_connection(user_name, user_password)  # 데이터베이스 연결
    cursor = conn.cursor()
    result = None
    try:
        if operation == 'create':
            create_or_update_computer_equipment(user_name, user_password)  # 장비 생성 또는 업데이트
        elif operation == 'search_computer':
            result = search_computer_equipment(cursor, *args)  # 장비 목록 조회
        elif operation == 'update_quantity':
            update_computer_equipment_quantity(user_name, user_password, *args)  # 장비 수량 업데이트
        elif operation == 'delete':
            delete_computer_equipment(user_name, user_password)  # 장비 삭제
        elif operation == 'read_incidents':
            return read_incidents(cursor)  # 사고 목록 조회
        elif operation == 'send_message':
            # 메시지 보내기
            cursor.execute("""
                INSERT INTO incident_messages (sender_department, message)
                VALUES (%s, %s);
            """, args)  # args에는 sender_department와 message가 포함되어야 함
        elif operation == 'read_messages':
            result = read_messages(cursor)
        elif operation == 'delete_message':
            # 메시지 삭제하기
            cursor.execute("""
                DELETE FROM incident_messages
                WHERE id = %s AND sender_department = %s;
            """, args)  # args에는 삭제할 ID와 sender_department가 포함되어야 함
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
    return result

# 메인 함수
def main():
    user_name = "admin"  # 사용자 이름
    user_password = "admin"  # 비밀번호
    user_department = "전장반"  # 메시지 보내는 반

    while True:
        print("\n전장반 관리 시스템")
        print("1. 장비 생성")  # 장비 추가
        print("2. 장비 목록")  # 장비 조회
        print("3. 장비 수량 업데이트")  # 장비 수량 수정
        print("4. 장비 삭제")  # 장비 삭제
        print("5. 장비 사용")  # 장비 사용
        print("6. 메시지")  # 메시지 전송
        print("7. 나가기")  # 프로그램 종료
        
        choice = input("원하는 기능의 숫자를 입력하세요: ")

        if choice == '1':
            create_or_update_computer_equipment(user_name, user_password)  # 장비 생성 또는 업데이트
        elif choice == '2':
            handle_search_computer_equipment(user_name, user_password)  # 장비 목록 조회
        elif choice == '3':
            update_computer_equipment_quantity(user_name, user_password)  # 장비 수량 업데이트
        elif choice == '4':
            delete_computer_equipment(user_name, user_password)  # 장비 삭제
        elif choice == '5':
            handle_use_computer_equipment(user_name, user_password)  # 장비 사용
        elif choice == '6':
            manage_messages(user_name, user_password, user_department)  # 메시지 관리
        elif choice == '7':
            print("프로그램을 종료합니다.")  # 프로그램 종료 메시지
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")  # 잘못된 입력 처리

# 프로그램 시작
if __name__ == "__main__":
    main()  # 메인 함수 호출
