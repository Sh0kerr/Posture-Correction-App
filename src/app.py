from training import Training
from working import work

# @TODO Тут желательно вообще-то сделать интерфейс; перенести интерфейс сюда

if __name__ == "__main__":
    
    print("""
    Выберите режим работы:
        1. Режим работы.
        2. Режим упражнений.
        """)
    
    modes = {1: "Сидеть", 2: "Ебашить"}

    operating_mode = 0
    while True:
        try:
            operating_mode = int(input())
            if operating_mode in range(1, 3):
                break
            else:
                print("Еблан?? Два числа, выбери одно.")
        except ValueError:
            print("Введите целое число!")

    # @TODO Занести следующие три строки куда-нибудь в проги training и working наверное хз
    # print("Выберите камеру:\n")
    # url = 'http://192.168.1.64:8080/video'
    # cap = cv2.VideoCapture(0)

    Training.plank()
