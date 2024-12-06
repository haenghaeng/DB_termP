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

# 사고 보고 생성 함수
def create_incident(cursor, contact, details, related_units, department,
                    wireless_tool_name=None, wireless_tool_quantity=0,
                    wired_tool_name=None, wired_tool_quantity=0,
                    computer_tool_name=None, computer_tool_quantity=0):
    try:
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
            wireless_tool_name, wireless_tool_quantity,
            wired_tool_name, wired_tool_quantity,
            computer_tool_name, computer_tool_quantity
        ))
        new_id = cursor.fetchone()[0]
        print(f"새로운 사고 보고가 생성되었습니다. ID: {new_id}")
        return new_id
    except psycopg2.Error as e:
        print(f"데이터베이스 오류: {e}")

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
            try:
                contact = input("연락처를 입력하세요: ")
                details = input("사고 상세 내용을 입력하세요: ")
                related_units = input("연계되는 반을 쉼표로 구분하여 입력하세요 (예: 무선반, 유선반): ").split(",")
                validate_department(related_units, valid_units)
                department = input("사고 발생 부서를 입력하세요: ")
            
                wireless_tool_name = input("필요한 무선 도구 이름(없으면 Enter): ") or None
                wireless_tool_quantity = int(input("필요한 무선 도구 수량(없으면 0): ") or 0)
                validate_input(wireless_tool_name, wireless_tool_quantity, "무선 도구")

                wired_tool_name = input("필요한 유선 도구 이름(없으면 Enter): ") or None
                wired_tool_quantity = int(input("필요한 유선 도구 수량(없으면 0): ") or 0)
                validate_input(wired_tool_name, wired_tool_quantity, "유선 도구")

                computer_tool_name = input("필요한 전장 도구 이름(없으면 Enter): ") or None
                computer_tool_quantity = int(input("필요한 전장 도구 수량(없으면 0): ") or 0)
                validate_input(computer_tool_name, computer_tool_quantity, "전장 도구")

                perform_crud_operations(
                    user_name, user_password, 'create',
                    contact, details, related_units, department,
                    wireless_tool_name, wireless_tool_quantity,
                    wired_tool_name, wired_tool_quantity,
                    computer_tool_name, computer_tool_quantity
                )

            except ValueError as e:
                print(f"입력 오류: {e}")
            except Exception as e:
                print(f"오류 발생: {e}")

        elif choice == '2':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

# 실행
if __name__ == "__main__":
    main()
