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


if __name__ == "__main__":
    main()
