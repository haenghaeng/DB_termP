import psycopg2
import psycopg2.errors

# PostgreSQL 데이터베이스 연결 함수
def try_connection(user_name, user_password):
    return psycopg2.connect(
        database="db_termp",
        user=user_name,
        password=user_password,
        host="::1",
        port="5432"
    )

# 사고 생성
def create_incident(user_name, user_password, valid_units):
    try:
        # 사용자로부터 입력 받기
        contact = input("연락처를 입력하세요: ")
        details = input("사고 상세 내용을 입력하세요: ")
        related_units = input("연계되는 반을 쉼표로 구분하여 입력하세요 (예: 무선반, 유선반): ").split(",")
        related_units = [unit.strip() for unit in related_units]  # 공백 제거
        validate_department(related_units, valid_units)
        department = input("사고 발생 부서를 입력하세요: ")

        # 도구 입력을 위한 초기화
        tools = {
            '무선반': {'name': None, 'quantity': 0},
            '유선반': {'name': None, 'quantity': 0},
            '전장반': {'name': None, 'quantity': 0}
        }

        # 연계되는 반에 따라 도구 입력
        for unit in related_units:
            if unit in tools:
                tools[unit]['name'] = input(f"{unit} 필요한 도구 이름(없으면 Enter): ") or None
                tools[unit]['quantity'] = int(input(f"{unit} 필요한 도구 수량(없으면 0): ") or 0)
                validate_input(tools[unit]['name'], tools[unit]['quantity'], f"{unit} 도구")

        # 데이터베이스에 사고 보고 생성
        conn = try_connection(user_name, user_password)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO incident_reports (
                contact, details, related_units, department, 
                wireless_tool_name, wireless_tool_quantity, 
                wired_tool_name, wired_tool_quantity, 
                computer_tool_name, computer_tool_quantity
            )
            VALUES (
                %s, %s, ARRAY[%s]::Edepartment[], %s, 
                %s, %s, %s, %s, %s, %s
            )
            RETURNING id;
        """, (
            contact, details, related_units, department,
            tools['무선반']['name'], tools['무선반']['quantity'],
            tools['유선반']['name'], tools['유선반']['quantity'],
            tools['전장반']['name'], tools['전장반']['quantity']
        ))
        
        new_id = cursor.fetchone()[0]
        print(f"새로운 사고 보고가 생성되었습니다. ID: {new_id}")
        conn.commit()
    except ValueError as e:
        print(f"입력 오류: {e}")
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        conn.close()



# 입력값이 올바른지 확인
def validate_input(tool_name, tool_quantity, tool_type):
    if tool_name is None and tool_quantity != 0:
        raise ValueError(f"{tool_type} 이름이 없는데 수량이 입력되었습니다.")
    if tool_quantity < 0:
        raise ValueError(f"{tool_type} 수량은 음수가 될 수 없습니다.")

# 연계되는 반이 유선반, 전장반, 무선반인지 확인
def validate_department(units, valid_units):
    for unit in units:
        unit = unit.strip()  # 앞뒤 공백 제거
        if unit not in valid_units:
            raise ValueError(f"'{unit}'은(는) 유효하지 않은 반입니다. 유효한 반: {', '.join(valid_units)}")
        
# 사고 보고 조회
def read_incidents(cursor):
    incident_id = input("특정 사고 ID를 조회하려면 입력하고, 전체 조회는 Enter: ")
    
    try:
        if incident_id:
            incident_id = int(incident_id)
            cursor.execute("SELECT * FROM incident_reports WHERE id = %s;", (incident_id,))
            incident = cursor.fetchone()
            if incident:
                print("\n[사고 보고 상세 정보]")
                print(f"ID: {incident[0]}")
                print(f"전화번호: {incident[1]}")
                print(f"사고 내용: {incident[2]}")
                print(f"관련 부서: {incident[3]}")
                print(f"사고 발생 장소: {incident[4]}")
                print(f"무선반 장비: {incident[5]}")
                print(f"무선반 장비 개수: {incident[6]}")
                print(f"유선반 장비: {incident[7]}")
                print(f"유선반 장비 개수: {incident[8]}")
                print(f"전장반 장비: {incident[9]}")
                print(f"전장반 장비 개수: {incident[10]}")
            else:
                print("해당 사고 보고가 없습니다.")
        else:
            cursor.execute("SELECT * FROM incident_reports ORDER BY id ASC;")
            incidents = cursor.fetchall()
            if incidents:
                print("\n[전체 사고 보고 목록]")
                for incident in incidents:
                    print("\n--------------------")
                    print(f"ID: {incident[0]}")
                    print(f"전화번호: {incident[1]}")
                    print(f"사고 내용: {incident[2]}")
                    print(f"관련 부서: {incident[3]}")
                    print(f"사고 발생 장소: {incident[4]}")
                    print(f"무선반 장비: {incident[5]}")
                    print(f"무선반 장비 개수: {incident[6]}")
                    print(f"유선반 장비: {incident[7]}")
                    print(f"유선반 장비 개수: {incident[8]}")
                    print(f"전장반 장비: {incident[9]}")
                    print(f"전장반 장비 개수: {incident[10]}")
                    print("--------------------")
            else:
                print("등록된 사고 보고가 없습니다.")
    except ValueError:
        print("잘못된 ID입니다. 숫자를 입력하세요.")
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")

def update_incident(user_name, user_password):
    incident_id = int(input("수정할 사고 ID를 입력하세요: "))
    print("수정할 필드를 선택하세요.")
    print("1. 연락처")
    print("2. 사고 내용")
    print("3. 관련 부서")
    print("4. 사고 발생 장소")
    print("5. 무선반 장비")
    print("6. 무선반 장비 개수")
    print("7. 유선반 장비")
    print("8. 유선반 장비 개수")
    print("9. 전장반 장비")
    print("10. 전장반 장비 개수")

    field_choice = input("수정할 필드의 숫자를 입력하세요: ")
    field_map = {
        '1': 'contact',
        '2': 'details',
        '3': 'related_units',
        '4': 'department',
        '5': 'wireless_tool_name',
        '6': 'wireless_tool_quantity',
        '7': 'wired_tool_name',
        '8': 'wired_tool_quantity',
        '9': 'computer_tool_name',
        '10': 'computer_tool_quantity'
    }

    if field_choice in field_map:
        new_value = input(f"새로운 값을 입력하세요 (기존 값: {field_map[field_choice]}): ")
        try:
            conn = try_connection(user_name, user_password)
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE incident_reports
                SET {field_map[field_choice]} = %s
                WHERE id = %s;
            """, (new_value, incident_id))
            conn.commit()
            print(f"사고 보고 ID {incident_id}의 {field_map[field_choice]}이(가) 성공적으로 업데이트되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 오류: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("잘못된 선택입니다. 다시 시도하세요.")

def delete_incident(user_name, user_password):
    incident_id = int(input("삭제할 사고 ID를 입력하세요: "))
    
    try:
        conn = try_connection(user_name, user_password)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM incident_reports WHERE id = %s;", (incident_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"사고 보고 ID {incident_id}이(가) 삭제되었습니다.")
        else:
            print(f"해당 사고 보고 ID {incident_id}이(가) 존재하지 않습니다.")
            
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")
    except ValueError:
        print("잘못된 ID입니다. 숫자를 입력하세요.")
    finally:
        cursor.close()
        conn.close()

def solve_incident(user_name, user_password):
    try:
        conn = try_connection(user_name, user_password)
        cursor = conn.cursor()

        # GROUP BY와 HAVING을 사용하여 조건에 맞는 사고만 조회
        cursor.execute("""
            SELECT id, contact, details, department, 
                   wireless_tool_quantity, wired_tool_quantity, computer_tool_quantity
            FROM incident_reports
            GROUP BY id, contact, details, department, 
                     wireless_tool_quantity, wired_tool_quantity, computer_tool_quantity
            HAVING SUM(wireless_tool_quantity) = 0 
               AND SUM(wired_tool_quantity) = 0 
               AND SUM(computer_tool_quantity) = 0;
        """)
        incidents = cursor.fetchall()

        if incidents:
            print("\n[해결 가능한 사고 목록]")
            for incident in incidents:
                print("\n--------------------")
                print(f"ID: {incident[0]}")
                print(f"전화번호: {incident[1]}")
                print(f"사고 내용: {incident[2]}")
                print(f"사고 발생 부서: {incident[3]}")
                print(f"무선반 장비 개수: {incident[4]}")
                print(f"유선반 장비 개수: {incident[5]}")
                print(f"전장반 장비 개수: {incident[6]}")
                print("--------------------")
                
                choice = input(f"사고 ID {incident[0]}를 해결하시겠습니까? (y/n): ")
                if choice.lower() == 'y':
                    cursor.execute("DELETE FROM incident_reports WHERE id = %s;", (incident[0],))
                    print(f"사고 보고 ID {incident[0]}이(가) 해결되었습니다.")
        else:
            print("해결 처리 가능한 사고가 없습니다.")
        
        conn.commit()  # 변경 사항 커밋
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")
    finally:
        cursor.close()
        conn.close()

# CRUD 작업 수행 함수
def perform_crud_operations(user_name, user_password, operation, *args, **kwargs):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    result = None
    try:
        if operation == 'create':
            result = create_incident(cursor, *args, **kwargs)
        elif operation == 'read':
            result = read_incidents(cursor, *args)
        elif operation == 'update':
            update_incident(cursor, *args)
        elif operation == 'delete':
            delete_incident(cursor, *args)
        elif operation == 'solve':
            result = solve_incident(user_name, user_password)  # solve 작업 추가
        else:
            print("유효하지 않은 작업입니다.")
        conn.commit()
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        conn.close()
    return result

def main():
    user_name = "admin"
    user_password = "admin"
    valid_units = ['무선반', '유선반', '전장반']

    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    
    while True:
        print("\n사고 보고 관리 시스템")
        print("1. 사고 보고 생성")
        print("2. 사고 보고 조회")
        print("3. 사고 보고 업데이트")
        print("4. 사고 보고 삭제")
        print("5. 사고 해결 처리")
        print("6. 나가기.")
        choice = input("원하는 작업을 선택하세요: ")

        if choice == '1':
            create_incident(user_name, user_password, valid_units)
        elif choice == '2':
            read_incidents(cursor)
        elif choice == '3':
            update_incident(user_name, user_password)
        elif choice == '4':
            delete_incident(user_name, user_password)
        elif choice == '5':
            solve_incident(user_name, user_password)
        elif choice == '6':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

    cursor.close()
    conn.close()

# 실행
if __name__ == "__main__":
    main()
