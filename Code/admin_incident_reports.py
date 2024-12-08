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

# PostgreSQL 연결 설정
def connect_to_db():
    try:
        return psycopg2.connect(
            database="db_termp",
            user='admin',
            password='admin',
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
def create_incident(cursor):
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

# 사고 조회
def read_incidents(cursor):
    """사고 보고를 조회합니다."""
    incident_id = input("특정 사고 ID를 조회하려면 입력하고, 전체 조회는 Enter: ")
    try:
        if incident_id:
            cursor.execute("SELECT * FROM incident_reports WHERE id = %s;", (int(incident_id),))
            incident = cursor.fetchone()
            if incident:
                print("[사고 보고 상세 정보]")
                print(f"사고 ID: {incident[0]}")
                print(f"연락처: {incident[1]}")
                print(f"사고 상세 내용: {incident[2]}")
                print(f"연계되는 반: {incident[3]}")
                print(f"사고 발생 부서: {incident[4]}")
                print(f"필요한 무선 도구 이름: {incident[5]}")
                print(f"필요한 무선 도구 수량: {incident[6]}")
                print(f"필요한 유선 도구 이름: {incident[7]}")
                print(f"필요한 유선 도구 수량: {incident[8]}")
                print(f"필요한 전장 도구 이름: {incident[9]}")
                print(f"필요한 전장 도구 수량: {incident[10]}")
            else:
                print("해당 사고 보고가 없습니다.")
        else:
            cursor.execute("SELECT * FROM incident_reports ORDER BY id ASC;")
            incidents = cursor.fetchall()
            print("[전체 사고 보고 목록]") if incidents else print("등록된 사고 보고가 없습니다.")
            for incident in incidents:
                print(f"사고 ID: {incident[0]}")
                print(f"연락처: {incident[1]}")
                print(f"사고 상세 내용: {incident[2]}")
                print(f"연계되는 반: {incident[3]}")
                print(f"사고 발생 부서: {incident[4]}")
                print(f"필요한 무선 도구 이름: {incident[5]}")
                print(f"필요한 무선 도구 수량: {incident[6]}")
                print(f"필요한 유선 도구 이름: {incident[7]}")
                print(f"필요한 유선 도구 수량: {incident[8]}")
                print(f"필요한 전장 도구 이름: {incident[9]}")
                print(f"필요한 전장 도구 수량: {incident[10]}\n")
                
    except ValueError:
        print("잘못된 ID입니다. 숫자를 입력하세요.")

# 사고 수정
def update_incident(cursor):
    """기존 사고 보고를 수정합니다."""
    try:
        incident_id = int(input("수정할 사고 ID를 입력하세요: "))
        fields = {
            '1': ('contact', '연락처'),
            '2': ('details', '사고 상세 내용'),
            '3': ('related_units', '연계되는 반'),
            '4': ('department', '사고 발생 부서'),
            '5': ('wireless_tool_name', '필요한 무선 도구 이름'),
            '6': ('wireless_tool_quantity', '필요한 무선 도구 수량'),
            '7': ('wired_tool_name', '필요한 유선 도구 이름'),
            '8': ('wired_tool_quantity', '필요한 유선 도구 수량'),
            '9': ('computer_tool_name', '필요한 전장 도구 이름'),
            '10': ('computer_tool_quantity', '필요한 전장 도구 수량')
        }
        print("\n".join([f"{k}. {v[1]}" for k, v in fields.items()]))
        field_choice = input("수정할 필드를 선택하세요: ")
        
        if field_choice in fields:
            new_value = input(f"{fields[field_choice][1]}의 새로운 값을 입력하세요: ")
            if field_choice == '3':  # 만약 "연계되는 반"을 수정하는 경우
                new_value = '{' + ','.join([unit_mapping[unit.strip()] for unit in new_value.split(',')]) + '}'
            cursor.execute(f"UPDATE incident_reports SET {fields[field_choice][0]} = %s WHERE id = %s;", (new_value, incident_id))
            print(f"사고 보고 ID {incident_id}가 업데이트되었습니다.")
    except ValueError:
        print("잘못된 입력입니다. 다시 시도하세요.")
    except Error as e:
        print(f"데이터베이스 오류: {e}")


# 사고 삭제
def delete_incident(cursor):
    """사고 보고를 삭제합니다."""
    try:
        incident_id = int(input("삭제할 사고 ID를 입력하세요: "))
        cursor.execute("DELETE FROM incident_reports WHERE id = %s;", (incident_id,))
        print(f"사고 보고 ID {incident_id}가 삭제되었습니다.") if cursor.rowcount else print("해당 사고 보고가 없습니다.")
    except ValueError:
        print("잘못된 ID입니다.")

# 사고 해결 (계속)
def solve_incident(cursor):
    """해결 가능한 사고를 처리합니다."""
    cursor.execute("""
        SELECT id, contact, details, department 
        FROM incident_reports
        WHERE wireless_tool_quantity = 0 AND wired_tool_quantity = 0 AND computer_tool_quantity = 0;
    """)
    incidents = cursor.fetchall()
    if not incidents:
        print("해결 가능한 사고가 없습니다.")
    for incident in incidents:
        print(f"[ID: {incident[0]}] {incident[1]} - {incident[2]} (부서: {incident[3]})")
        if input("해결 처리하시겠습니까? (y/n): ").lower() == 'y':
            cursor.execute("DELETE FROM incident_reports WHERE id = %s;", (incident[0],))
            print(f"사고 보고 ID {incident[0]}이 해결되었습니다.")

# 메인 함수
def main():
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            while True:
                print("\n[사고 보고]\n1. 생성\n2. 조회\n3. 수정\n4. 삭제\n5. 해결\n6. 종료")
                choice = input("작업 선택: ")
                if choice == '1':
                    create_incident(cursor)
                elif choice == '2':
                    read_incidents(cursor)
                elif choice == '3':
                    update_incident(cursor)
                elif choice == '4':
                    delete_incident(cursor)
                elif choice == '5':
                    solve_incident(cursor)
                elif choice == '6':
                    break
                else:
                    print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()