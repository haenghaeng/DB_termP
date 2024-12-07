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


# CRUD 작업 수행 함수
def perform_crud_operations(user_name, user_password, operation, *args, **kwargs):
    conn = try_connection(user_name, user_password)
    cursor = conn.cursor()
    result = None
    try:
        if operation == 'create':
            result = create_incident(cursor, *args, **kwargs)
        else:
            print("유효하지 않은 작업입니다.")
        conn.commit()
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        cursor.close()
        conn.close()
    return result

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


# 메인 함수
def main():
    user_name = "admin"
    user_password = "admin"
    valid_units = ['무선반', '유선반', '전장반']

    while True:
        print("\n사고 보고 관리 시스템")
        print("1. 사고 접수")
        print("2. 나가기")
        
        choice = input("원하는 작업을 선택하세요: ")
        
        if choice == '1':
            create_incident(user_name, user_password, valid_units)
        elif choice == '2':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

# 실행
if __name__ == "__main__":
    main()
