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

# 유선 장비 생성 또는 업데이트 함수
def create_or_update_computer_equipment(cursor, name, quantity):
    # 장비가 존재하는지 확인
    cursor.execute("SELECT id, quantity FROM computer_equipment WHERE name = %s;", (name,))
    result = cursor.fetchone()

    if result:  # 장비가 존재하는 경우
        equipment_id, existing_quantity = result  # 기존 장비 ID 및 수량 가져오기
        new_quantity = existing_quantity + quantity  # 기존 수량에 입력받은 수량 추가
        cursor.execute("""
            UPDATE computer_equipment SET quantity = %s WHERE id = %s;  # 수량 업데이트
        """, (new_quantity, equipment_id))
        print(f"{name} 장비의 수량이 {existing_quantity}에서 {new_quantity}로 업데이트되었습니다.")
    else:  # 장비가 존재하지 않는 경우
        # 비어있는 ID를 찾기 위해 현재 ID 목록을 가져옴
        cursor.execute("SELECT id FROM computer_equipment ORDER BY id ASC;")
        ids = cursor.fetchall()  # 현재 존재하는 ID 목록 가져오기
        available_id = None

        # ID가 연속되지 않은 경우, 가장 작은 비어있는 ID를 찾음
        for i in range(1, len(ids) + 2):
            if (i,) not in ids:  # ID가 비어있는지 확인
                available_id = i
                break

        # 새로운 장비를 데이터베이스에 삽입
        cursor.execute("""
            INSERT INTO computer_equipment (id, name, quantity) VALUES (%s, %s, %s);  # 새로운 장비 삽입
        """, (available_id, name, quantity))
        print("장비가 생성되었습니다.")

# 유선 장비 조회 함수
def read_computer_equipment(cursor):
    cursor.execute("SELECT * FROM computer_equipment ORDER BY id ASC;")  # 모든 장비 조회
    return cursor.fetchall()  # 모든 장비 데이터 반환

# 유선 장비 수량 업데이트 함수
def update_computer_equipment_quantity(cursor, equipment_id, quantity):
    cursor.execute("""
        UPDATE computer_equipment SET quantity = %s WHERE id = %s;  # 특정 ID의 수량 업데이트
    """, (quantity, equipment_id))

# 유선 장비 삭제 함수
def delete_computer_equipment(cursor, equipment_id):
    cursor.execute("DELETE FROM computer_equipment WHERE id = %s;", (equipment_id,))  # 특정 ID의 장비 삭제
    # 삭제된 ID 이후의 모든 장비 ID를 1씩 감소시킴
    cursor.execute("""
        UPDATE computer_equipment SET id = id - 1 WHERE id > %s;  # ID 연속성 유지
    """, (equipment_id,))

# 컴퓨터 장비에 대한 CRUD 작업 수행 함수
def perform_crud_operations_computer(user_name, user_password, operation, *args):
    conn = try_connection(user_name, user_password)  # 데이터베이스 연결
    cursor = conn.cursor()

    if operation == 'create':
        create_or_update_computer_equipment(cursor, *args)  # 장비 생성 또는 업데이트
    elif operation == 'read':
        return read_computer_equipment(cursor)  # 장비 목록 조회
    elif operation == 'update_quantity':
        update_computer_equipment_quantity(cursor, *args)  # 장비 수량 업데이트
    elif operation == 'delete':
        delete_computer_equipment(cursor, *args)  # 장비 삭제
    else:
        print("Invalid operation.")  # 유효하지 않은 작업 처리

    conn.commit()  # 변경 사항 커밋
    cursor.close()  # 커서 닫기
    conn.close()  # 연결 종료

# 메인 함수
def main_computer():
    user_name = "admin"  # 사용자 이름
    user_password = "admin"  # 비밀번호

    while True:
        print("\n전산장비 관리 시스템")
        print("1. 장비 생성")  # 장비 추가
        print("2. 장비 목록")  # 장비 조회
        print("3. 장비 수량 업데이트")  # 장비 수량 수정
        print("4. 장비 삭제")  # 장비 삭제
        print("5. 나가기")  # 프로그램 종료
        
        choice = input("원하는 기능의 숫자를 입력하세요: ")

        if choice == '1':
            name = input("장비 이름을 입력하세요: ")
            quantity = int(input("장비 수량을 입력하세요: "))
            perform_crud_operations_computer(user_name, user_password, 'create', name, quantity)  # 장비 생성
        
        elif choice == '2':
            equipment_list = perform_crud_operations_computer(user_name, user_password, 'read')  # 장비 목록 조회
            print("현재 전산 장비 목록:")
            for equipment in equipment_list:
                print(f"ID: {equipment[0]}, 이름: {equipment[1]}, 수량: {equipment[2]}")
        
        elif choice == '3':
            equipment_list = perform_crud_operations_computer(user_name, user_password, 'read')  # 장비 목록 조회
            print("현재 전산 장비 목록:")
            for equipment in equipment_list:
                print(f"ID: {equipment[0]}, 이름: {equipment[1]}, 수량: {equipment[2]}")
            equipment_id = int(input("업데이트할 장비의 ID를 입력하세요: "))
            quantity = int(input("새로운 장비 수량을 입력하세요: "))
            perform_crud_operations_computer(user_name, user_password, 'update_quantity', equipment_id, quantity)  # 장비 수량 업데이트
            print("장비 수량이 업데이트되었습니다.")
        
        elif choice == '4':
            equipment_list = perform_crud_operations_computer(user_name, user_password, 'read')  # 장비 목록 조회
            print("현재 전산 장비 목록:")
            for equipment in equipment_list:
                print(f"ID: {equipment[0]}, 이름: {equipment[1]}, 수량: {equipment[2]}")
            equipment_id = int(input("삭제할 장비의 ID를 입력하세요: "))
            
            # ID가 유효한지 확인
            if any(equipment[0] == equipment_id for equipment in equipment_list):
                perform_crud_operations_computer(user_name, user_password, 'delete', equipment_id)  # 장비 삭제
                print("장비가 삭제되었습니다.")
            else:
                print("입력하신 ID값을 가진 장비가 존재하지 않습니다.")
        
        elif choice == '5':
            print("프로그램을 종료합니다.")  # 프로그램 종료 메시지
            break
        
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")  # 잘못된 입력 처리

# 프로그램 시작
if __name__ == "__main__":
    main_computer()  # 메인 함수 호출
