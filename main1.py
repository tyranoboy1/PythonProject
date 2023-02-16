from mainscreen import SelectMenu
from mainscreen import theory
from mainscreen import areap
from mainscreen import dayp
from mainscreen import graphchose
from mainscreen import corona19_graph
from mainscreen import vaccination_graph
from mainscreen import machine_running_graph
from mainscreen import clearconsole


def main():
    while True:
        key = SelectMenu()
        if key == '0':
            break
        elif key == '1':
            theory()
            clearconsole()
        elif key == '2':
            areap()
            clearconsole()
        elif key == '3':
            dayp()
            clearconsole()
        elif key == '4':
            graphchose()
            num=int(input("번호를 입력하세요: "))
            if num == 1:
                corona19_graph()
                clearconsole()
            elif num == 2:
                vaccination_graph()
                clearconsole()
            elif num == 3:
                machine_running_graph()
                clearconsole()
            else:
                print("잘못된 입력 값입니다.")
                clearconsole()
        else:
            print("잘못 선택하였습니다.")
        main()
if __name__ == '__main__':
    main()
