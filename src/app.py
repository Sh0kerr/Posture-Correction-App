from training import Training
from working import work
from gui import WindowsHandler, getAge
import os

path_to_userinfo_dir = "../app_data"


def main():
    sex, age = -1, -1

    if not os.path.exists(path_to_userinfo_dir):
        os.mkdir(path_to_userinfo_dir)
    elif os.path.exists(f"{path_to_userinfo_dir}/user_info.txt"):
        with open(f"{path_to_userinfo_dir}/user_info.txt") as file:
            age = getAge(file.readline())
            sex = int(file.readline())

    app = WindowsHandler(sex, age, path_to_userinfo_dir)

    if age == -1:
        app.window_inputData()
    else:
        app.window_modes()
    if age == -2:
        exit(0)

    # print(f"age: {age}\nsex: {'male' if sex == 1 else 'female'}")


if __name__ == "__main__":
    main()
    # print("""
    # Выберите режим работы:
    #     1. Режим работы.
    #     2. Режим упражнений.
    #     """)
    #
    # modes = {1: "Сидеть", 2: "Ебашить"}
    # operating_mode = 0
    # while True:
    #     try:
    #         operating_mode = int(input())
    #         if operating_mode in range(1, 3):
    #             break
    #         else:
    #             print("Еблан?? Два числа, выбери одно.")
    #     except ValueError:
    #         print("Введите целое число!")

    # @TODO Занести следующие три строки куда-нибудь в проги training и working наверное хз
    # print("Выберите камеру:\n")
    # url = 'http://192.168.1.64:8080/video'
    # cap = cv2.VideoCapture(0)

    # Training.plank()
