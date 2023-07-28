import customtkinter as ctk
from datetime import date
from time import sleep
from threading import Thread
from action import Action
from enum import Enum

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
systemFont = ('Trebuchet MS', 18, 'bold')
systemFont_heading = ('Trebuchet MS', 30, 'bold')
button_ipadx, button_ipady = 10, 10
button_padx, button_pady = 20, 20
systemTextColor = "white"
orange = "#cc6600"
blue = "#1f6aa5"
system_cornerRadius = 20


class Category(Enum):
    BOY = 0,
    GIRL = 1,
    MAN = 2,
    WOMAN = 3


reps_category = {
    Category.BOY: [10, 10, 30],
    Category.GIRL: [5, 5, 15],
    Category.MAN: [20, 20, 60],
    Category.WOMAN: [15, 15, 45],
}


class WindowsHandler(ctk.CTk):
    # data for window_inputData()
    selected_sex = None
    selected_day = None
    selected_month = None
    selected_year = None
    sex_var = None
    rbFemale = None
    rbMale = None
    menu_day = None
    menu_month = None
    menu_year = None
    bSave = None
    # data for window_modes()
    bPosture = None
    bExercise = None

    frame = None
    frame_exit = None
    frame_right = None
    t = None
    tr = None
    tr_exitFlag = False
    action = None

    lReps = None
    rep_counter = 0

    def __init__(self, sex, age, path_to_userinfo_dir):
        super().__init__()
        self.destroy_list = []
        self.sex = sex
        self.age = age
        self.path_to_userinfo_dir = path_to_userinfo_dir
        self.geometry("700x500+400+100")
        self.configure(fg_color=("#ffb266", "#1f6aa5"))
        if sex == 0:
            if age < 18:
                self.category = Category.GIRL
            else:
                self.category = Category.WOMAN
        else:
            if age < 18:
                self.category = Category.BOY
            else:
                self.category = Category.MAN

    def window_inputData(self):
        self.title("Ввод данных")
        self.selected_sex = -1
        self.selected_day = -1
        self.selected_month = -1
        self.selected_year = -1

        self.frame = ctk.CTkFrame(self, width=400, fg_color=orange)
        self.frame.pack(anchor='center', fill=None, expand=True)
        self.destroy_list.append(self.frame)

        lSex = ctk.CTkLabel(self.frame, text="Укажите ваш пол", font=systemFont, text_color=systemTextColor)
        lSex.grid(row=0, column=1, columnspan=2, pady=(30, 10))
        self.sex_var = ctk.IntVar()
        self.sex_var.set(-1)
        self.rbFemale = ctk.CTkRadioButton(self.frame, text="женский", font=systemFont, variable=self.sex_var, value=0,
                                           command=self.enableSaveButton)
        self.rbFemale.grid(row=1, column=1)
        self.rbMale = ctk.CTkRadioButton(self.frame, text="мужской", font=systemFont, variable=self.sex_var, value=1,
                                         command=self.enableSaveButton)
        self.rbMale.grid(row=1, column=2)

        lDate = ctk.CTkLabel(self.frame, text="Укажите вашу дату рождения", font=systemFont, text_color=systemTextColor)
        lDate.grid(row=2, column=1, columnspan=2, pady=(40, 15))
        self.menu_day = ctk.CTkOptionMenu(self.frame,
                                          values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                                                  '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
                                                  '25', '26', '27', '28', '29', '30', '31'],
                                          font=systemFont, text_color=systemTextColor,
                                          command=self.enableSaveButton, width=100)
        self.menu_day.set("День")
        self.menu_day.grid(row=3, column=1, columnspan=2, pady=10)
        self.menu_month = ctk.CTkOptionMenu(self.frame, values=["январь", "февраль", "март", "апрель", "май", "июнь", "июль",
                                                                "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
                                            font=systemFont, text_color=systemTextColor,
                                            command=self.enableSaveButton, width=100)
        self.menu_month.set("Месяц")
        self.menu_month.grid(row=4, column=1, columnspan=2)
        self.menu_year = ctk.CTkOptionMenu(self.frame, values=[str(year) for year in range(date.today().year, 1949, -1)],
                                           font=systemFont, text_color=systemTextColor,
                                           command=self.enableSaveButton, width=100)
        self.menu_year.set("Год")
        self.menu_year.grid(row=5, column=1, columnspan=2, pady=10)

        self.bSave = ctk.CTkButton(self.frame, text="Сохранить", font=systemFont, text_color=systemTextColor,
                                   command=self.button_inputData_save, state="disabled")
        self.bSave.grid(row=6, column=2,
                        ipadx=button_ipadx, ipady=button_ipady,
                        padx=button_padx, pady=button_pady)

        bExit = ctk.CTkButton(self.frame, text="Выйти", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        bExit.grid(row=6, column=1,
                   ipadx=button_ipadx, ipady=button_ipady,
                   padx=button_padx, pady=button_pady)

        self.mainloop()

    def window_modes(self):
        self.title("Выбор режима")

        self.frame = ctk.CTkFrame(self, height=400, fg_color="pink")
        self.frame.pack(fill='both', expand=True)
        self.destroy_list.append(self.frame)

        self.frame_exit = ctk.CTkFrame(self, height=100, fg_color="yellow")
        self.frame_exit.pack(fill='both', expand=True)
        self.destroy_list.append(self.frame_exit)

        self.bPosture = ctk.CTkButton(self.frame, text="Контроль осанки", font=systemFont, text_color=systemTextColor,
                                      command=self.button_modes_posture, width=350, height=350,
                                      corner_radius=0)
        self.bPosture.grid(row=0, column=0, ipadx=button_ipadx, ipady=button_ipady)
        self.bExercise = ctk.CTkButton(self.frame, text="Выполнение упражнений", font=systemFont, text_color=systemTextColor,
                                       command=self.button_modes_exercise, width=350, height=363,
                                       corner_radius=0)
        self.bExercise.grid(row=0, column=1)

        bExit = ctk.CTkButton(self.frame_exit, text="Выход", font=systemFont, text_color=systemTextColor,
                              command=self.button_exit, corner_radius=0, height=200)
        bExit.pack(fill='both', expand=True)

        self.mainloop()

    def window_posture(self):
        self.title("Осанка")
        self.action = Action()
        self.t = Thread(target=self.action.posture, daemon=True)
        self.t.start()

        phrase = ctk.CTkLabel(self, text="Держите ровно осанку!", font=systemFont_heading)
        phrase.pack(pady=20)
        self.destroy_list.append(phrase)

        self.frame = ctk.CTkFrame(self, fg_color=blue, width=500)
        self.frame.pack(fill='y', expand=False, pady=(0, 0))
        self.destroy_list.append(self.frame)

        bSwitch = ctk.CTkButton(self.frame, text="Переключиться на режим упражнений", font=systemFont, text_color=systemTextColor,
                                command=self.button_switchFromPosture, fg_color=orange,
                                height=100, corner_radius=system_cornerRadius)
        bSwitch.grid(row=0, column=0, columnspan=2, pady=30)

        bBack = ctk.CTkButton(self.frame, text="Назад", font=systemFont, text_color=systemTextColor,
                              command=lambda: self.button_toModes(True, False), fg_color=orange,
                              height=100, corner_radius=system_cornerRadius)
        bBack.grid(row=1, column=0, padx=10)

        bExit = ctk.CTkButton(self.frame, text="Выход", font=systemFont, text_color=systemTextColor,
                              command=lambda: self.button_exit_threads(False), fg_color=orange, height=100,
                              corner_radius=system_cornerRadius)
        bExit.grid(row=1, column=1, padx=10)

        self.mainloop()

    def window_chooseExercise(self):
        self.title("Выбор упражнения")

        lType = ctk.CTkLabel(self, text="Выберите тип упражнения:", font=systemFont_heading, text_color='white')
        lType.pack(anchor='center', pady=(30, 0))
        self.destroy_list.append(lType)

        self.frame = ctk.CTkFrame(self, width=600, height=300, fg_color=blue)
        self.frame.pack(fill='both', expand=True, pady=(0, 20))
        self.destroy_list.append(self.frame)

        self.frame_exit = ctk.CTkFrame(self, width=600, height=100, fg_color=blue)
        self.frame_exit.pack(fill='x', expand=True, pady=(0, 20))
        self.destroy_list.append(self.frame_exit)

        bPushups = ctk.CTkButton(self.frame, text="Отжимания", font=systemFont, text_color=systemTextColor,
                                 command=self.button_choosePushups, width=180, height=180, fg_color=orange,
                                 corner_radius=system_cornerRadius)
        bPushups.grid(row=0, column=0, padx=(50, 15), pady=(20, 0))

        bSquats = ctk.CTkButton(self.frame, text="Приседания", font=systemFont, text_color=systemTextColor,
                                command=self.button_chooseSquats, width=180, height=180, fg_color=orange,
                                corner_radius=system_cornerRadius)
        bSquats.grid(row=0, column=1, padx=(15, 15), pady=(20, 0))

        bPlank = ctk.CTkButton(self.frame, text="Планка", font=systemFont, text_color=systemTextColor,
                               command=self.button_choosePlank, width=180, height=180, fg_color=orange,
                               corner_radius=system_cornerRadius)
        bPlank.grid(row=0, column=2, padx=(15, 50), pady=(20, 0))

        bBack = ctk.CTkButton(self.frame_exit, text="Назад", font=systemFont, text_color=systemTextColor,
                              command=lambda: self.button_toModes(False, False), width=180, height=180,
                              corner_radius=system_cornerRadius, fg_color=orange)
        bBack.grid(row=0, column=0, padx=(155, 15))

        bExit = ctk.CTkButton(self.frame_exit, text="Выход", font=systemFont, text_color=systemTextColor,
                              command=self.button_exit, width=180, height=180,
                              corner_radius=system_cornerRadius, fg_color=orange)
        bExit.grid(row=0, column=1, padx=(15, 155))

        self.mainloop()

    def window_pushups(self):
        self.title("Отжимания")
        self.rep_counter = 0
        self.action = Action()

        self.t = Thread(target=self.action.pushups, daemon=True)
        self.t.start()

        self.tr = Thread(target=self.checkReps, args=(reps_category[self.category][0],), daemon=True)
        self.tr.start()

        self.frame = ctk.CTkFrame(self, fg_color=blue)
        self.frame.pack(side='left', fill='both', expand=True, pady=(0, 0))
        self.destroy_list.append(self.frame)

        self.frame_right = ctk.CTkFrame(self, fg_color=blue)
        self.frame_right.pack(side='right', fill='both', expand=True, pady=(0, 0))
        self.destroy_list.append(self.frame_right)

        phrase = ctk.CTkLabel(self.frame_right, text=f"Сделайте {reps_category[self.category][0]} отжиманий", font=systemFont_heading)
        phrase.pack(pady=30)

        self.lReps = ctk.CTkLabel(self.frame_right, text=f"{self.rep_counter} / {reps_category[self.category][0]}", font=('Trebuchet MS', 50, 'bold'))
        self.lReps.pack(pady=20)

        bSwitch_toSquats = ctk.CTkButton(self.frame, text="Переключиться на приседания", font=systemFont, text_color=systemTextColor, fg_color=orange,
                                         command=self.button_switchToSquats, width=100, height=100)
        bSwitch_toSquats.grid(row=0, column=0, pady=(20, 10), padx=(20, 0))

        bSwitch_toPlank = ctk.CTkButton(self.frame, text="Переключиться на планку", font=systemFont, text_color=systemTextColor, fg_color=orange,
                                        command=self.button_switchToPlank, width=286, height=100)
        bSwitch_toPlank.grid(row=1, column=0, pady=(10, 10), padx=(20, 0))

        bModes = ctk.CTkButton(self.frame, text="В главное меню", font=systemFont, text_color=systemTextColor, fg_color=orange,
                               command=self.button_toModes, width=286, height=100)
        bModes.grid(row=2, column=0, pady=(10, 10), padx=(20, 0))

        bExit = ctk.CTkButton(self.frame, text="Выход", font=systemFont, text_color=systemTextColor, fg_color=orange,
                              command=self.button_exit_threads, width=286, height=100)
        bExit.grid(row=3, column=0, pady=(10, 20), padx=(20, 0))

        self.mainloop()

    def window_squats(self):
        self.title("Приседания")
        self.rep_counter = 0
        self.action = Action()

        self.t = Thread(target=self.action.squats, daemon=True)
        self.t.start()

        self.tr = Thread(target=self.checkReps, args=(reps_category[self.category][0],), daemon=True)
        self.tr.start()

        self.frame = ctk.CTkFrame(self, fg_color=blue)
        self.frame.pack(side='left', fill='both', expand=True, pady=(0, 0))
        self.destroy_list.append(self.frame)

        self.frame_right = ctk.CTkFrame(self, fg_color=blue)
        self.frame_right.pack(side='right', fill='both', expand=True, pady=(0, 0))
        self.destroy_list.append(self.frame_right)

        phrase = ctk.CTkLabel(self.frame_right, text=f"Сделайте {reps_category[self.category][1]} приседаний", font=systemFont_heading)
        phrase.pack(pady=30)

        self.lReps = ctk.CTkLabel(self.frame_right, text=f"{self.rep_counter} / {reps_category[self.category][1]}", font=('Trebuchet MS', 50, 'bold'))
        self.lReps.pack(pady=20)

        bSwitch_toPushups = ctk.CTkButton(self.frame, text="Переключиться на отжимания", font=systemFont, text_color=systemTextColor, fg_color=orange,
                                          command=self.button_switchToPushups, width=100, height=100)
        bSwitch_toPushups.grid(row=0, column=0, pady=(20, 10), padx=(20, 0))

        bSwitch_toPlank = ctk.CTkButton(self.frame, text="Переключиться на планку", font=systemFont,
                                        text_color=systemTextColor, fg_color=orange,
                                        command=self.button_switchToPlank, width=286, height=100)
        bSwitch_toPlank.grid(row=1, column=0, pady=(10, 10), padx=(20, 0))

        bModes = ctk.CTkButton(self.frame, text="В главное меню", font=systemFont, text_color=systemTextColor,
                               fg_color=orange,
                               command=self.button_toModes, width=286, height=100)
        bModes.grid(row=2, column=0, pady=(10, 10), padx=(20, 0))

        bExit = ctk.CTkButton(self.frame, text="Выход", font=systemFont, text_color=systemTextColor, fg_color=orange,
                              command=self.button_exit_threads, width=286, height=100)
        bExit.grid(row=3, column=0, pady=(10, 20), padx=(20, 0))

        self.mainloop()

    def window_plank(self):
        self.title("Планка")
        self.rep_counter = 0
        self.action = Action()

        self.t = Thread(target=self.action.plank, daemon=True)
        self.t.start()

        self.tr = Thread(target=self.checkReps, args=(reps_category[self.category][0],), daemon=True)
        self.tr.start()

        self.frame = ctk.CTkFrame(self, fg_color=blue)
        self.frame.pack(side='left', fill='both', expand=True, pady=(0, 0))
        self.destroy_list.append(self.frame)

        self.frame_right = ctk.CTkFrame(self, fg_color=blue)
        self.frame_right.pack(side='right', fill='both', expand=True, pady=(0, 0))
        self.destroy_list.append(self.frame_right)

        phrase = ctk.CTkLabel(self.frame_right, text="Стойте в планке", font=systemFont_heading)
        phrase.pack(pady=(30, 0))
        same_phrase = ctk.CTkLabel(self.frame_right, text=f"на протяжении {reps_category[self.category][2]} секунд", font=systemFont_heading)
        same_phrase.pack(pady=(0, 30))

        self.lReps = ctk.CTkLabel(self.frame_right, text=f"{self.rep_counter} / {reps_category[self.category][2]}", font=('Trebuchet MS', 50, 'bold'))
        self.lReps.pack(pady=20)

        bSwitch_toPushups = ctk.CTkButton(self.frame, text="Переключиться на отжимания", font=systemFont,
                                          text_color=systemTextColor, fg_color=orange,
                                          command=self.button_switchToPushups, width=100, height=100)
        bSwitch_toPushups.grid(row=0, column=0, pady=(20, 10), padx=(20, 0))

        bSwitch_toSquats = ctk.CTkButton(self.frame, text="Переключиться на приседания", font=systemFont,
                                         text_color=systemTextColor, fg_color=orange,
                                         command=self.button_switchToSquats, width=286, height=100)
        bSwitch_toSquats.grid(row=1, column=0, pady=(10, 10), padx=(20, 0))

        bModes = ctk.CTkButton(self.frame, text="В главное меню", font=systemFont, text_color=systemTextColor,
                               fg_color=orange,
                               command=self.button_toModes, width=286, height=100)
        bModes.grid(row=2, column=0, pady=(10, 10), padx=(20, 0))

        bExit = ctk.CTkButton(self.frame, text="Выход", font=systemFont, text_color=systemTextColor, fg_color=orange,
                              command=self.button_exit_threads, width=286, height=100)
        bExit.grid(row=3, column=0, pady=(10, 20), padx=(20, 0))

        self.mainloop()

    def checkReps(self, overall):
        while True:
            if self.tr_exitFlag:
                break
            reps = self.action.get_reps()
            if reps != self.rep_counter:
                self.rep_counter = reps
                self.lReps.configure(text=f"{self.action.get_reps()} / {overall}")
            sleep(0.1)

    def button_toModes(self, killT=True, killTr=True):
        if killT:
            Action.exitFlag = True
            self.t.join()
            Action.exitFlag = False
        if killTr:
            self.tr_exitFlag = True
            self.tr.join()
        self.destroy_current_content()
        self.window_modes()

    def button_choosePushups(self):
        self.destroy_current_content()
        self.window_pushups()

    def button_chooseSquats(self):
        self.destroy_current_content()
        self.window_squats()

    def button_choosePlank(self):
        self.destroy_current_content()
        self.window_plank()

    def button_switchFromPosture(self):
        Action.exitFlag = True
        self.t.join()
        Action.exitFlag = False
        self.destroy_current_content()
        self.window_chooseExercise()

    def button_switchToPushups(self):
        Action.exitFlag = True
        self.t.join()
        Action.exitFlag = False
        self.destroy_current_content()
        self.window_pushups()

    def button_switchToSquats(self):
        Action.exitFlag = True
        self.t.join()
        Action.exitFlag = False
        self.destroy_current_content()
        self.window_squats()

    def button_switchToPlank(self):
        Action.exitFlag = True
        self.t.join()
        Action.exitFlag = False
        self.destroy_current_content()
        self.window_plank()

    def button_modes_posture(self):
        self.destroy_current_content()
        self.window_posture()

    def button_modes_exercise(self):
        self.destroy_current_content()
        self.window_chooseExercise()

    def enableSaveButton(self, something=None):
        self.selected_sex = self.sex_var.get()
        self.selected_day = self.menu_day.get()
        self.selected_month = self.menu_month.get()
        self.selected_year = self.menu_year.get()
        if self.selected_sex != -1 and self.selected_day != "День" and self.selected_month != "Месяц" and self.selected_year != "Год":
            self.bSave.configure(state="normal")

    def button_inputData_save(self):
        self.sex = self.selected_sex
        month_to_int = {"январь": 1, "февраль": 2, "март": 3, "апрель": 4, "май": 5, "июнь": 6, "июль": 7, "август": 8,
                        "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12}
        user_date = f"{self.selected_day}.{month_to_int[self.selected_month]}.{self.selected_year}\n"
        self.age = getAge(user_date)
        with open(f"{self.path_to_userinfo_dir}/user_info.txt", "w") as file:
            file.write(f"{user_date}{self.sex}")
        self.destroy_current_content()
        self.window_modes()

    def button_exit(self):
        self.age = -2
        self.destroy()

    def button_exit_threads(self, killTr=True):
        Action.exitFlag = True
        self.t.join()
        Action.exitFlag = False
        if killTr:
            self.tr_exitFlag = True
            self.tr.join()
        self.age = -2
        self.destroy()

    def destroy_current_content(self):
        for item in self.destroy_list:
            item.destroy()
        self.destroy_list.clear()


def getAge(dateOfBirth):
    dateOfBirth = list(map(int, dateOfBirth[:-1].split('.')))  # from '20.07.2023' to [20, 7, 2023]
    today = date.today()
    birth = date(dateOfBirth[2], dateOfBirth[1], dateOfBirth[0])
    years = today.year - birth.year
    if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
        years -= 1
    return years
