import soldier_information_table

import wired_equipment
import wireless_equipment
import computer_equipment

import admin_incident_reports
import incident_reports

def login(department):    
    if department == 'wireless_operator':
        print('무선반 접속')
        wireless_operator_ui(department)       
    
    elif department == 'field_wireman':
        print('유선반 접속')
        field_wireman_ui(department)
    
    elif department == 'computer_technician':
        print('전자장비반 접속')  
        computer_technician_ui(department)
    
    elif department == 'admin':
        print('운영통제반 접속') 
        admin_ui(department)       
    
    elif department == 'etc':
        print('기타 접속')
        etc_ui()
 
def wireless_operator_ui(department):
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 무선 장비 관리\n(2) 종료\n')
        if action == "1":
            wireless_equipment.main(department)
        elif action == "2":
            print("종료합니다.")
            break
        
def field_wireman_ui(department):
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 유선 장비 관리\n(2) 종료\n')
        if action == "1":
            wired_equipment.main(department)
        elif action == "2":
            print("종료합니다.")
            break

def computer_technician_ui(department):
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 전자 장비 관리\n(2) 종료\n')
        if action == "1":
            computer_equipment.main(department)
        elif action == "2":
            print("종료합니다.")
            break


def admin_ui(department):
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 병사 관리\n(2) 무선 장비 관리\n(3) 유선 장비 관리\n(4) 전자 장비 관리\n(5) 사고 관리\n(6) 종료\n')
        if action == "1":
            soldier_information_table.main()
        elif action == "2":
            wireless_equipment.main(department)
        elif action == "3":
            wired_equipment.main(department)
        elif action == "4":
            computer_equipment.main(department)
        elif action == "5":
            admin_incident_reports.main()
        elif action == "6":
            print("종료합니다.")
            break
        
def etc_ui():
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 사고 등록\n(2) 종료\n')
        if action == "1":
            incident_reports.main()
        elif action == "2":
            print("종료합니다.")
            break