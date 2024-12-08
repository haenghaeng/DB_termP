import psycopg2
import psycopg2.sql
import psycopg2.errors

import hashpw

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
        print(f"\n데이터베이스와 연결에 실패하였습니다.\n{e}")
    
    finally:
        connection.commit()
        cursor.close()
        connection.close()
        
        
def reviseK2E_department_name(department):
    # department를 한국어에서 DB에 들어갈 수 있는 영어 이름으로 변경
    if department == '무선반': return 'wireless_operator'
    elif department == '유선반': return 'field_wireman'
    elif department == '전장반': return 'computer_technician'
    elif department == '운통반': return 'admin'
    elif department == '기타': return 'etc'
    else: return 0
    
def reviseE2K_department_name(department):
    # department를 영어 이름에서 한국어로 변경
    if department == 'wireless_operator': return '무선반'
    elif department == 'field_wireman': return '유선반'
    elif department == 'computer_technician': return '전장반'
    elif department == 'admin': return '운통반'
    elif department == 'etc': return '기타'
    else: return 0
    
    
def create_soldier(cursor):
    while True:
        army_number = input("병사의 군번을 입력해주세요(ex. 19-70001234) : ")
        name = input("병사의 이름을 입력해주세요(10자 이하) : ")
        rank = input("병사의 계급을 입력해주세요(이병/일병/상병/병장) : ")
        department = input("병사의 소속반을 입력해주세요(무선반/유선반/전장반/운통반/기타) : ")
        phone_number = input("병사의 연락처를 입력해주세요 : ")
        user_password = input("병사가 로그인 시 사용할 비밀번호를 입력해주세요 : ")        
        
        yes_no = input(f'''
                       다음 입력 사항이 맞습니까?(Y/N)
                       군번 : {army_number}
                       이름 : {name}
                       계급 : {rank}
                       소속반 : {department}
                       연락처 : {phone_number}
                       비밀번호 : {user_password}                       
                       ''')
        
        if yes_no == 'Y' or yes_no == 'y':
            department = reviseK2E_department_name(department)
            break
        else:
            print("다시 입력해주세요")
    
    try:
        query = psycopg2.sql.SQL(
            '''
            insert into soldier_information(army_number, name, rank, department, phone_number, user_password) values (%s, %s, %s, %s, %s, %s);
            '''
        )    
        cursor.execute(query, (army_number, name, rank, department, phone_number, hashpw.hash_password(user_password)))
    
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다. 10자 이하로 입력해야 합니다.")
        
    except psycopg2.errors.InvalidTextRepresentation:
        print("잘못된 계급을 입력하였습니다. (이병/일병/상병/병장)중 입력해야 합니다.")
        
    except psycopg2.errors.DatatypeMismatch:
        print("소속을 잘못 입력하였습니다. (무선반/유선반/전장반/운통반/기타)중 입력해야 합니다.")

def read_soldier(cursor):    
    while True:
        action = input("원하는 검색 방식의 숫자를 입력해주세요\n(1) 이름으로 검색\n(2) 군번으로 검색\n(3) 검색 종료\n")
        
        if action == '1':
            name = input("병사의 이름을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select army_number, name, rank, department, phone_number
                from soldier_information
                where name = %s;
                '''
            )
            cursor.execute(query, (name, ))
            
            results = list(cursor.fetchall())
            if len(results) > 0:
                for res in results:
                    res = list(res)
                    res[3] = reviseE2K_department_name(res[3]) # 소속반의 이름을 한글로 변경
                    print(res)
            else:
                print("입력한 이름을 가진 병사가 데이터베이스에 존재하지 않습니다.")   
            
        
        elif action == '2':
            user_name = input("병사의 군번을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select army_number, name, rank, department, phone_number
                from soldier_information
                where army_number = %s;
                '''
            )
            cursor.execute(query, (user_name, ))
            
            results = list(cursor.fetchall())
            if len(results) > 0:
                for res in results:
                    res = list(res)
                    res[3] = reviseE2K_department_name(res[3]) # 소속반의 이름을 한글로 변경
                    print(res)            
            else:
                print("입력한 군번을 가진 병사가 데이터베이스에 존재하지 않습니다.")  
        
        elif action == '3':
            return
        
        else:
            print("다시 입력해주세요") 

# 업데이트 시 계급, id, pw를 동시에 업데이트해야 함
# 기능 분리 필요
def update_soldier(cursor):
    while True:
        action = input("원하는 검색 방식의 숫자를 입력해주세요\n(1) 이름으로 검색\n(2) 군번으로 검색\n(3) 검색 종료\n")
        
        if action == '1':
            name = input("병사의 이름을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select army_number, name
                from soldier_information
                where name = %s;
                '''
            )
            cursor.execute(query, (name, ))
            
            result = cursor.fetchall()
            if len(result) > 1:
                print("데이터베이스에 동명이인이 존재합니다. 병사의 군번으로 검색 부탁드립니다.")
                
            elif len(result) == 1:
                army_number = result[0][0]
                name = result[0][1]
                while True:
                    rank = input("병사의 계급을 입력해주세요(이병/일병/상병/병장) : ")
                    department = input("병사의 소속반을 입력해주세요(무선반/유선반/전장반/운통반/기타) : ")
                    phone_number = input("병사의 연락처를 입력해주세요 : ")
                    user_password = input("병사가 로그인 시 사용할 비밀번호를 입력해주세요 : ")        
                    
                    yes_no = input(f'''
                                다음 입력 사항이 맞습니까?(Y/N)
                                군번 : {army_number}
                                이름 : {name}
                                계급 : {rank}
                                소속반 : {department}
                                연락처 : {phone_number}
                                비밀번호 : {user_password}                       
                                ''')
                    
                    if yes_no == 'Y' or yes_no == 'y':
                        break
                    else:
                        print("다시 입력해주세요")
                
                try:
                    query = psycopg2.sql.SQL(
                        '''
                        update soldier_information
                        set rank = %s, department = %s, phone_number = %s, user_password = %s
                        where army_number = %s
                        '''
                    )   
                    department = reviseK2E_department_name(department) # 한글 이름을 영어로 변경 
                    cursor.execute(query, (rank, department, phone_number, hashpw.hash_password(user_password), army_number))
        
                except psycopg2.errors.StringDataRightTruncation:
                    print("입력한 값이 너무 깁니다.")
                    
                except psycopg2.errors.InvalidTextRepresentation:
                    print("잘못된 계급을 입력하였습니다.")
                    
            else:
                print("입력한 이름을 가진 병사가 데이터베이스에 존재하지 않습니다.")   
            
        
        elif action == '2':
            army_number = input("병사의 군번을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select army_number, name
                from soldier_information
                where army_number = %s;
                '''
            )
            cursor.execute(query, (army_number, ))
            
            result = cursor.fetchone()
            if result:
                name = result[1]
                while True:
                    rank = input("병사의 계급을 입력해주세요(이병/일병/상병/병장) : ")
                    department = input("병사의 소속반을 입력해주세요(무선반/유선반/전장반/운통반/기타) : ")
                    phone_number = input("병사의 연락처를 입력해주세요 : ")
                    user_password = input("병사가 로그인 시 사용할 비밀번호를 입력해주세요 : ")        
                    
                    yes_no = input(f"""
                                다음 입력 사항이 맞습니까?(Y/N)
                                군번 : {army_number}
                                이름 : {name}
                                계급 : {rank}
                                소속반 : {department}
                                연락처 : {phone_number}
                                비밀번호 : {user_password}                       
                                """)
                    
                    if yes_no == 'Y' or yes_no == 'y':
                        break
                    else:
                        print("다시 입력해주세요")
                
                try:
                    query = psycopg2.sql.SQL(
                        '''
                        update soldier_information
                        set rank = %s, department = %s, phone_number = %s, user_password = %s
                        where army_number = %s
                        '''
                    )    
                    department = reviseK2E_department_name(department) # 한글 이름을 영어로 변경
                    cursor.execute(query, (rank, department, phone_number, hashpw.hash_password(user_password), army_number))
        
                except psycopg2.errors.StringDataRightTruncation:
                    print("입력한 값이 너무 깁니다.")
                    
                except psycopg2.errors.InvalidTextRepresentation:
                    print("잘못된 계급을 입력하였습니다.")
                             
            else:
                print("입력한 군번을 가진 병사가 데이터베이스에 존재하지 않습니다.")  
        
        elif action == '3':
            return
        
        else:
            print("다시 입력해주세요") 

def delete_soldier(cursor):
    while True:
        action = input("원하는 검색 방식의 숫자를 입력해주세요\n(1) 이름으로 검색\n(2) 군번으로 검색\n(3) 검색 종료\n")
        
        if action == '1':
            name = input("병사의 이름을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                delete from soldier_information
                where name = %s;
                '''
            )
            
            cursor.execute(query, (name, ))
            
            if cursor.rowcount > 0:
                print(f"{name} 병사가 데이터베이스에서 삭제되었습니다.")            
            else:
                print("입력한 이름을 가진 병사가 데이터베이스에 존재하지 않습니다.") 
        
        elif action == '2':
            user_name = input("병사의 군번을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                delete from soldier_information
                where army_number = %s;
                '''
            )
            
            cursor.execute(query, (user_name, ))
            if cursor.rowcount > 0:
                print(f"{user_name} 병사가 데이터베이스에서 삭제되었습니다.")            
            else:
                print("입력한 군번을 가진 병사가 데이터베이스에 존재하지 않습니다.") 
        
        elif action == '3':
            return
        
        else:
            print("다시 입력해주세요") 

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