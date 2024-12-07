import psycopg2
import psycopg2.errors

# PostgreSQL 데이터베이스에 연결
def try_connection(department):
    return psycopg2.connect(
        database="db_termp",  # 데이터베이스 이름
        user=department,       # 사용자 이름
        password=department,  # 비밀번호
        host="::1",           # 호스트 주소 (여기서는 IPv6의 localhost)
        port="5432"           # 포트 번호 (기본값 5432)
    )

# 장비 생성 함수
def create_equipment(cursor):
    name = input("장비 이름을 입력하세요: ")
    try:
        quantity = int(input("장비 수량을 입력하세요: "))
        if quantity < 0:
            raise ValueError("수량은 음수가 될 수 없습니다.")
               
        cursor.execute('''
                       SELECT id, quantity
                       FROM computer_equipment
                       WHERE name = %s;
                       ''', (name,))
        result = cursor.fetchone()

        if result:  # 장비가 존재하는 경우
            print("입력한 장비가 이미 DB에 존재합니다.")
            
        else: # 장비가 존재하지 않는 경우
            cursor.execute('''INSERT INTO computer_equipment (name, quantity) VALUES (%s, %s) RETURNING id;''', (name, quantity))
            new_id = cursor.fetchone()[0]
            print(f"{name} 장비가 생성되었습니다. 새 ID: {new_id}")

    except ValueError as e:
        print(f"잘못된 입력: {e}")
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
    except psycopg2.errors.InvalidTextRepresentation:
        print("잘못된 입력 값을 입력하였습니다.")
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")

# 장비 목록 조회 함수
def search_equipment(cursor):
    name = input("조회하고 싶은 장비의 이름을 입력하세요: ")
    
    cursor.execute('''
                   SELECT id, name, quantity
                   FROM computer_equipment
                   WHERE name = %s;
                   ''', (name,))
    result = cursor.fetchone()

    if result:
        print(f"장비 정보 - ID: {result[0]}, 이름: {result[1]}, 수량: {result[2]}")
    else:
        print("해당 이름의 장비가 없습니다.")

# 장비 수량 업데이트 함수
def update_equipment(cursor):
    sub_choice = input("무엇을 하시겠습니까?\n1. 장비 가져감.\n2. 장비 반납.\n숫자 선택: ")

    name = input("장비의 이름을 입력하세요: ")
    
    # 이름에 맞는 장비 검색
    cursor.execute('''
                   SELECT id, name, quantity
                   FROM computer_equipment
                   WHERE name = %s;
                   ''', (name,))
    result = cursor.fetchone()
    

    if result:
        available_quantity = result[2]
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
            
            equipment_id = result[0]  # ID 가져오기
        except ValueError as e:
            print(f"잘못된 입력: {e}")
            return
    else:
        print(f"{name}을 가진 이름의 장비는 없습니다.")
        return

    try:
        cursor.execute('''
                       UPDATE computer_equipment
                       SET quantity = quantity + %s
                       WHERE id = %s;
                       ''', (delta_quantity, equipment_id))
        
        # 업데이트 후 현재 수량 조회
        cursor.execute('''
                       SELECT name, quantity
                       FROM computer_equipment
                       WHERE id = %s;
                       ''', (equipment_id,))
        updated_equipment = cursor.fetchone()
        
        if updated_equipment:
            updated_name, updated_quantity = updated_equipment
            print(f"{updated_name} 장비의 수량이 업데이트되었습니다. 현재 수량: {updated_quantity}.")
            
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")

# 전장 장비 삭제 함수
def delete_equipment(cursor):
    name = input("삭제할 장비의 이름을 입력하세요: ")
    
    # 이름에 맞는 장비 검색
    cursor.execute('''
                   SELECT id, name, quantity
                   FROM computer_equipment
                   WHERE name = %s;
                   ''', (name,))
    result = cursor.fetchone()
    
    if result:
        equipment_id = result[0]  # ID 가져오기
        
        try:
            cursor.execute('''
                           DELETE FROM computer_equipment
                           WHERE id = %s;
                           ''', (equipment_id,))  # 특정 ID의 장비 삭제   
            print("장비가 삭제되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 오류: {e}")
    else:
        print("해당 이름의 장비가 존재하지 않습니다.")

# 사고 목록 조회 함수
def read_all_incidents(cursor):
    cursor.execute('''
                   SELECT id, contact, details, computer_tool_name, computer_tool_quantity, department
                   FROM incident_reports
                   WHERE computer_tool_quantity > 0;
                   ''')
    return cursor.fetchall() or []

# 사고 해결 함수
def manage_incidents(cursor):
    try:
        incident_list = read_all_incidents(cursor)
        if incident_list:
            print("현재 해결할 수 있는 사고 목록:")
            for incident in incident_list:
                print(f"ID: {incident[0]}, 사고 발생 부서: {incident[5]}, 연락처: {incident[1]}, 내용: {incident[2]}, 필요한 장비: {incident[3]}, 수량: {incident[4]}")
            
            try:
                incident_id = int(input("해결하고 싶은 사고의 ID를 입력하세요: "))
                if incident_id in [incident[0] for incident in incident_list]:
                    cursor.execute('''
                                   SELECT contact, details, computer_tool_name, computer_tool_quantity, department
                                   FROM incident_reports
                                   WHERE id = %s;
                                   ''', (incident_id,))
                    incident = cursor.fetchone()
                    
                    # 입력한 ID를 가진 사고가 존재하면                 
                    if incident:
                        contact, details, tool_name, tool_quantity, department = incident
                        print(f"사고 ID: {incident_id}, 사고 발생 부서: {department}, 연락처: {contact}, 내용: {details}, 필요한 장비: {tool_name}, 수량: {tool_quantity}")

                        cursor.execute('''
                                       SELECT quantity
                                       FROM computer_equipment
                                       WHERE name = %s;
                                       ''', (tool_name,))
                        equipment = cursor.fetchone()
                        
                        # 사고에 대응하는 장비가 존재하면
                        if equipment:
                            available_quantity = equipment[0]
                            if available_quantity >= tool_quantity:
                                new_quantity = available_quantity - tool_quantity
                                cursor.execute("UPDATE computer_equipment SET quantity = %s WHERE name = %s;", (new_quantity, tool_name))
                                cursor.execute("UPDATE incident_reports SET computer_tool_quantity = 0 WHERE id = %s;", (incident_id,))
                                print("에 대한 전장 사고 수리가 완료되었습니다.")
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

# 메시지 목록 조회 함수
def read_all_messages(cursor):
    cursor.execute("SELECT id, sender_department, message, created_at FROM incident_messages ORDER BY created_at ASC;")
    return cursor.fetchall()

# 메시지 관리 및 전송 함수
def manage_messages(cursor, department):
    while True:
        print("\n메시지 관리")
        print("1. 메시지 확인하기")
        print("2. 메시지 보내기")
        print("3. 메시지 삭제하기")
        print("4. 나가기")
        
        sub_choice = input("원하는 기능의 숫자를 입력하세요: ").strip()
        
        if sub_choice == '1':
            print("메시지 목록: ")
            try:
                messages = read_all_messages(cursor) # 메시지 목록 조회
                if messages:
                    for msg in messages:
                        print(f"{msg[1]}, 내용: {msg[2]}")
                else:
                    print("조회할 메시지가 없습니다.")
            except Exception as e:
                print(f"메시지 조회 중 오류 발생: {e}")

        elif sub_choice == '2': # 메시지 보내기
            message_content = input("보낼 메시지를 입력하세요: ").strip()
            if message_content:
                try:
                    # 메시지 보내기
                    cursor.execute('INSERT INTO incident_messages (sender_department, message) VALUES (%s, %s);', (department, message_content))
                    print("메시지가 성공적으로 전송되었습니다.")
                except Exception as e:
                    print(f"메시지 전송 중 오류 발생: {e}")
            else:
                print("메시지 내용이 비어있습니다. 다시 시도하세요.")
        
        elif sub_choice == '3': # 메시지 삭제하기
            # 삭제 가능한 메시지 조회
            delete_messages = read_all_messages(cursor)  # 메시지 목록 조회
            
            if delete_messages:
                print("\n삭제 가능한 메시지 목록:")
                for msg in delete_messages:
                    if msg[1] == department:  # 자신의 부서에서 보낸 메시지인지 확인
                        print(f"ID: {msg[0]}, 내용: {msg[2]}, 보낸 시간: {msg[3]}")
                
                try:
                    delete_id = int(input("삭제할 메시지의 ID를 입력하세요: ").strip())
                    # 해당 메시지가 자신의 부서에서 보낸 것인지 확인
                    
                    if any(msg[0] == delete_id and msg[1] == department for msg in delete_messages):
                        # 메시지 삭제하기
                        # args에는 삭제할 ID와 sender_department가 포함되어야 함
                        cursor.execute('''
                                       DELETE FROM incident_messages
                                       WHERE id = %s AND sender_department = %s;
                                       ''', (delete_id, department))
                        print("메시지가 성공적으로 삭제되었습니다.")
                    else:
                        print("해당 ID의 메시지는 자신의 부서에서 보낸 것이 아니므로 삭제할 수 없습니다.")
                except ValueError:
                    print("숫자를 입력하세요. 다시 시도하세요.")
            else:
                print("삭제할 메시지가 없습니다.")
        
        elif sub_choice == '4':  # 나가기
            print("메시지 관리에서 나갑니다.")
            break
        
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

# CRUD 작업 수행 함수
def crud_operations(operation, department):
    connection = try_connection(department)
    cursor = connection.cursor()
    
    try:
        if operation == 'create':
            create_equipment(cursor)
        elif operation == 'search':
            search_equipment(cursor)
        elif operation == 'update':
            update_equipment(cursor)
        elif operation == 'delete':
            delete_equipment(cursor)
            
        elif operation == 'manage_incidents':
            manage_incidents(cursor)
            pass
        elif operation == 'manage_message':
            manage_messages(cursor, department)
            pass            
            
    except Exception as e:
        print(f"오류 발생: {e}")
        
    finally:
        connection.commit()
        cursor.close()
        connection.close()


# 메인 함수
def main(department):

    while True:
        print("\n유선장비 관리 시스템")
        print("1. 장비 생성")
        print("2. 장비 조회")
        print("3. 장비 수량 업데이트")
        print("4. 장비 삭제")
        print("5. 사고 해결") 
        print("6. 메시지 관리")
        print("7. 나가기")
        
        choice = input("원하는 기능의 숫자를 입력하세요: ")

        if choice == '1':
            crud_operations('create', department) # 장비 생성
        elif choice == '2':
            crud_operations('search', department) # 장비 조회
        elif choice == '3':
            crud_operations('update', department) # 장비 수량 업데이트
        elif choice == '4':
            crud_operations('delete', department) # 장비 삭제
            
        elif choice == '5':
            crud_operations('manage_incidents', department) # 사고 해결
        elif choice == '6':
            crud_operations('manage_message', department) # 메세지 관리
            
        elif choice == '7':
            print("프로그램을 종료합니다.")  # 프로그램 종료 메시지
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")  # 잘못된 입력 처리

# 프로그램 시작
if __name__ == "__main__":
    main('admin')