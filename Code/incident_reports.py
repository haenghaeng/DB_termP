import psycopg2
from psycopg2 import Error

# 반 이름 매핑
unit_mapping = {
    '무선반': 'wireless_operator',
    '유선반': 'field_wireman',
    '전장반': 'computer_technician'
}

# 한글 매핑 
unit_mapping_korean = { 
    'wireless_operator': '무선반', 
    'field_wireman': '유선반', 
    'computer_technician': '전장반'
}

# PostgreSQL 데이터베이스 연결 함수
def connect_to_db(user_name, user_password):
    try:
        return psycopg2.connect(
            database="db_termp",
            user=user_name,
            password=user_password,
            host="::1",
            port="5432"
        )
    except Error as e:
            print(f"데이터베이스 연결 오류: {e}")
            raise

# 데이터 검증 유틸리티
def validate_input(tool_name, tool_quantity, tool_type):
    """도구 입력 값이 유효한지 확인합니다."""
    if tool_name is None and tool_quantity != 0:
        raise ValueError(f"{tool_type} 이름이 없는데 수량이 입력되었습니다.")
    if tool_quantity < 0:
        raise ValueError(f"{tool_type} 수량은 음수가 될 수 없습니다.")

# 연계 부서 확인
def validate_department(units, valid_units):
    """연계 부서가 유효한지 확인합니다."""
    invalid_units = [unit for unit in units if unit not in valid_units]
    if invalid_units:
        raise ValueError(f"유효하지 않은 부서: {', '.join(invalid_units)}. 유효한 부서: {', '.join(valid_units)}")

# 사고 생성
def create_incident(cursor, valid_units):
    """새로운 사고 보고를 생성합니다."""
    try:
        contact = input("연락처를 입력하세요: ")
        details = input("사고 상세 내용을 입력하세요: ")
        related_units_korean = input("연계되는 반을 쉼표로 구분하여 입력하세요 (유선반, 무선반, 전장반): ").split(",")
        related_units_korean = [unit.strip() for unit in related_units_korean]
        related_units = [unit_mapping[unit] for unit in related_units_korean if unit in unit_mapping]
        validate_department(related_units_korean, list(unit_mapping.keys()))
        department = input("사고 발생 부서를 입력하세요: ")

        tools = {unit: {'name': None, 'quantity': 0} for unit in unit_mapping.values()}
        for unit in related_units:
            tools[unit]['name'] = input(f"{unit_mapping_korean[unit]} 필요한 도구 이름: ") or None
            tools[unit]['quantity'] = int(input(f"{unit_mapping_korean[unit]} 필요한 도구 수량: ") or 0)
            validate_input(tools[unit]['name'], tools[unit]['quantity'], f"{unit_mapping_korean[unit]} 도구")

        cursor.execute("""
            INSERT INTO incident_reports (
                contact, details, related_units, department, 
                wireless_tool_name, wireless_tool_quantity, 
                wired_tool_name, wired_tool_quantity, 
                computer_tool_name, computer_tool_quantity
            ) VALUES (%s, %s, ARRAY[%s]::Edepartment[], %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            contact, details, ', '.join(related_units), department,
            tools['wireless_operator']['name'], tools['wireless_operator']['quantity'],
            tools['field_wireman']['name'], tools['field_wireman']['quantity'],
            tools['computer_technician']['name'], tools['computer_technician']['quantity']
        ))
        new_id = cursor.fetchone()[0]
        print(f"새로운 사고 보고가 생성되었습니다. ID: {new_id}")
    except (ValueError, Error) as e:
        print(f"오류 발생: {e}")


# 메인 함수
def main():
    user_name = "admin"
    user_password = "admin"
    valid_units = ['무선반', '유선반', '전장반']

    with connect_to_db(user_name, user_password) as conn:
        with conn.cursor() as cursor:
            while True:
                print("\n사고 보고 관리 시스템")
                print("1. 사고 접수")
                print("2. 나가기")
                
                choice = input("원하는 작업을 선택하세요: ")
                
                if choice == '1':
                    create_incident(cursor, valid_units)
                elif choice == '2':
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("잘못된 입력입니다. 다시 시도하세요.")

# 실행
if __name__ == "__main__":
    main()
