import psycopg2
import psycopg2.sql
import psycopg2.errors

def crud_operation(operation_type):
    try:        
        connection = psycopg2.connect(
            database = "db_termp",
            user = 'admin',
            password = 'admin',
            host = "::1",
            port = "5432"
            )
        cursor = connection.cursor()
        
        if operation_type == 'c':
            create_soldier(cursor)
        elif operation_type == 'r':
            read_soldier(cursor)
        elif operation_type == 'u':
            update_soldier(cursor)
        elif operation_type == 'd':
            delete_soldier(cursor)
        else:
            return              
        
    except Exception as e:
        print(f"\n데이터베이스와 연결에 실패하였습니다. : {e}")
    
    finally:
        connection.commit()
        connection.close()
        
def create_soldier(cursor):
    while True:    
        army_number = input("병사의 군번을 입력해주세요 : ")
        responsible_area = input("병사의 담당구역을 입력해주세요 : ")
        phone_number = input("연락처를 입력해주세요 : ")
        yes_no = input(f"다음 입력 사항이 맞습니까?(Y/N)\n\n군번 : {army_number}\n담당구역 : {responsible_area}\n연락처 : {phone_number}\n")
        if yes_no == 'Y' or yes_no == 'y':
            break
        else:
            print("다시 입력해주세요")
            
    try:
        query = psycopg2.sql.SQL(
            '''
            insert into wireless_operator(id, responsible_area, phone_number) values (%s, %s, %s);
            '''
        )    
        cursor.execute(query, (army_number, responsible_area, phone_number))            
    
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
            
    
def read_soldier(cursor):
    army_number = input("병사의 군번을 입력해주세요 : ")
    try:
        query = psycopg2.sql.SQL(
            '''
            select wo.id, si.name, si.rank, wo.responsible_area, wo.phone_number
            from wireless_operator wo, soldier_information si 
            where wo.id = si.id and wo.id = %s;
            '''
        )    
        cursor.execute(query, (army_number,))
        
        result = cursor.fetchone()
        
        if result:
            print(result)
        else:
            print("입력하신 군번을 가진 병사가 무선반에 존재하지 않습니다.")
       
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
    
def update_soldier(cursor):
    army_number = input("병사의 군번을 입력해주세요 : ")
    responsible_area = input("병사의 담당구역을 입력해주세요 : ")
    phone_number = input("연락처를 입력해주세요 : ")
    try:
        query = psycopg2.sql.SQL(
            '''
            update wireless_operator wo
            set responsible_area = %s, phone_number = %s
            where wo.id = %s
            '''
        )    
        cursor.execute(query, (responsible_area,phone_number,army_number))        
       
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
    
    
def delete_soldier(cursor):
    army_number = input("병사의 군번을 입력해주세요 : ")
    try:
        query = psycopg2.sql.SQL(
            '''
            delete from wireless_operator wo
            where wo.id = %s;
            '''
        )    
        cursor.execute(query, (army_number, ))        
       
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
        

def main():
    while True:
        action = input("원하는 기능의 숫자를 선택해주세요\n(1) 병사 추가\n(2) 병사 확인\n(3) 병사 정보 수정\n(4) 병사 정보 삭제\n(5) 종료\n")
        
        if action == '1':
            crud_operation('c')
        elif action == '2':
            crud_operation('r')
        elif action == '3':
            crud_operation('u')
        elif action == '4':
            crud_operation('d')
        elif action == '5':
            return
        else: 
            print("잘못된 입력입니다.\n")

if __name__ == "__main__":
    main()