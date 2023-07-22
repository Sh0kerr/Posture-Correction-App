import customtkinter as ctk
from datetime import date
from time import sleep
from functools import partial

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
systemFont = ('Arial', 18)
systemTextColor = "black"


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

    def __init__(self, sex, age, path_to_userinfo_dir):
        super().__init__()
        self.destroy_list = []
        self.sex = sex
        self.age = age
        self.path_to_userinfo_dir = path_to_userinfo_dir
        self.geometry("700x500+400+100")

    def window_chooseExercise(self):
        pidor = ctk.CTkLabel(self, text="Дорогой пидорас, выбери тип упражнения:", font=('Arial', 30, 'bold'))
        pidor.pack(pady=20)
        self.destroy_list.append(pidor)

        bPushups = ctk.CTkButton(self, text="Анжуманя", font=systemFont, text_color=systemTextColor, command=self.button_choosePushups)
        bPushups.pack(pady=20)
        self.destroy_list.append(bPushups)

        bSquats = ctk.CTkButton(self, text="Приседания на бутылку", font=systemFont, text_color=systemTextColor, command=self.button_chooseSquats)
        bSquats.pack(pady=20)
        self.destroy_list.append(bSquats)

        bPlank = ctk.CTkButton(self, text="Планка", font=systemFont, text_color=systemTextColor, command=self.button_choosePlank)
        bPlank.pack(pady=20)
        self.destroy_list.append(bPlank)

        bExit = ctk.CTkButton(self, text="Выход", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        bExit.pack(pady=20)
        self.destroy_list.append(bExit)

        self.mainloop()

    def window_pushups(self):
        syka = ctk.CTkLabel(self, text="Отжимайся 500 раз сука", font=('Arial', 30, 'bold'))
        syka.pack(pady=20)
        self.destroy_list.append(syka)

        bSwitch_toSquats = ctk.CTkButton(self, text="Переключиться на приседания", font=systemFont, text_color=systemTextColor,
                                         command=self.button_switchToSquats)
        bSwitch_toSquats.pack(pady=20)
        self.destroy_list.append(bSwitch_toSquats)

        bSwitch_toPlank = ctk.CTkButton(self, text="Переключиться на планку", font=systemFont, text_color=systemTextColor,
                                        command=self.button_switchToPlank)
        bSwitch_toPlank.pack()
        self.destroy_list.append(bSwitch_toPlank)

        bModes = ctk.CTkButton(self, text="В главное меню", font=systemFont, text_color=systemTextColor, command=self.button_toModes)
        bModes.pack(pady=20)
        self.destroy_list.append(bModes)

        bExit = ctk.CTkButton(self, text="Выход", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        bExit.pack()
        self.destroy_list.append(bExit)

        self.mainloop()

    def window_squats(self):
        syka = ctk.CTkLabel(self, text="Приседай 1200 раз сука", font=('Arial', 30, 'bold'))
        syka.pack(pady=20)
        self.destroy_list.append(syka)

        bSwitch_toSquats = ctk.CTkButton(self, text="Переключиться на отжимания", font=systemFont, text_color=systemTextColor,
                                         command=self.button_switchToPushups)
        bSwitch_toSquats.pack(pady=20)
        self.destroy_list.append(bSwitch_toSquats)

        bSwitch_toPlank = ctk.CTkButton(self, text="Переключиться на планку", font=systemFont, text_color=systemTextColor,
                                        command=self.button_switchToPlank)
        bSwitch_toPlank.pack()
        self.destroy_list.append(bSwitch_toPlank)

        bModes = ctk.CTkButton(self, text="В главное меню", font=systemFont, text_color=systemTextColor, command=self.button_toModes)
        bModes.pack(pady=20)
        self.destroy_list.append(bModes)

        bExit = ctk.CTkButton(self, text="Выход", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        bExit.pack()
        self.destroy_list.append(bExit)

        self.mainloop()

    def window_plank(self):
        syka = ctk.CTkLabel(self, text="Становись в планку сука", font=('Arial', 30, 'bold'))
        syka.pack(pady=20)
        self.destroy_list.append(syka)

        bSwitch_toPlank = ctk.CTkButton(self, text="Переключиться на отжимания", font=systemFont, text_color=systemTextColor,
                                        command=self.button_switchToPushups)
        bSwitch_toPlank.pack(pady=20)
        self.destroy_list.append(bSwitch_toPlank)

        bSwitch_toSquats = ctk.CTkButton(self, text="Переключиться на приседания", font=systemFont, text_color=systemTextColor,
                                         command=self.button_switchToSquats)
        bSwitch_toSquats.pack()
        self.destroy_list.append(bSwitch_toSquats)

        bModes = ctk.CTkButton(self, text="В главное меню", font=systemFont, text_color=systemTextColor, command=self.button_toModes)
        bModes.pack(pady=20)
        self.destroy_list.append(bModes)

        bExit = ctk.CTkButton(self, text="Выход", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        bExit.pack()
        self.destroy_list.append(bExit)

        self.mainloop()

    def button_toModes(self):
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

    def window_posture(self):
        syka = ctk.CTkLabel(self, text="Держи осанку сука", font=('Arial', 30, 'bold'))
        syka.pack(pady=20)
        self.destroy_list.append(syka)

        bSwitch = ctk.CTkButton(self, text="Переключиться на режим упражнений", font=systemFont, text_color=systemTextColor,
                                command=self.button_switchFromPosture)
        bSwitch.pack(pady=20)
        self.destroy_list.append(bSwitch)

        bBack = ctk.CTkButton(self, text="Назад", font=systemFont, text_color=systemTextColor,
                              command=self.button_toModes)
        bBack.pack()
        self.destroy_list.append(bBack)

        bExit = ctk.CTkButton(self, text="Выход", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        bExit.pack(pady=30)
        self.destroy_list.append(bExit)

        self.mainloop()

    def button_switchFromPosture(self):
        self.destroy_current_content()
        self.window_chooseExercise()

    def button_switchToPushups(self):
        self.destroy_current_content()
        self.window_pushups()

    def button_switchToSquats(self):
        self.destroy_current_content()
        self.window_squats()

    def button_switchToPlank(self):
        self.destroy_current_content()
        self.window_plank()

    def window_modes(self):
        self.title("Выбор режима")

        self.bPosture = ctk.CTkButton(self, text="Контроль осанки", font=systemFont, text_color=systemTextColor, command=self.button_modes_posture)
        self.bPosture.pack(pady=20)
        self.destroy_list.append(self.bPosture)
        self.bExercise = ctk.CTkButton(self, text="Выполнение упражнений", font=systemFont, text_color=systemTextColor,
                                       command=self.button_modes_exercise)
        self.bExercise.pack()
        self.destroy_list.append(self.bExercise)

        bExit = ctk.CTkButton(self, text="Выход", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        bExit.pack(pady=30)
        self.destroy_list.append(bExit)

        self.mainloop()

    def button_modes_posture(self):
        self.destroy_current_content()
        self.window_posture()

    def button_modes_exercise(self):
        self.destroy_current_content()
        self.window_chooseExercise()

    def window_inputData(self):
        self.title("Ввод данных")
        self.selected_sex = -1
        self.selected_day = -1
        self.selected_month = -1
        self.selected_year = -1

        lSex = ctk.CTkLabel(self, text="Укажите ваш пол", font=systemFont)
        lSex.pack(pady=20)
        self.destroy_list.append(lSex)
        self.sex_var = ctk.IntVar()
        self.sex_var.set(-1)
        self.rbFemale = ctk.CTkRadioButton(self, text="женский", font=systemFont, variable=self.sex_var, value=0,
                                           command=self.enableSaveButton)
        self.rbFemale.pack()
        self.destroy_list.append(self.rbFemale)
        self.rbMale = ctk.CTkRadioButton(self, text="мужской", font=systemFont, variable=self.sex_var, value=1,
                                         command=self.enableSaveButton)
        self.rbMale.pack()
        self.destroy_list.append(self.rbMale)

        lDate = ctk.CTkLabel(self, text="Укажите вашу дату рождения", font=systemFont)
        lDate.pack(pady=20)
        self.destroy_list.append(lDate)
        self.menu_day = ctk.CTkOptionMenu(self,
                                          values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                                                  '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
                                                  '25', '26', '27', '28', '29', '30', '31'],
                                          font=systemFont, text_color=systemTextColor, command=self.enableSaveButton)
        self.menu_day.set("День")
        self.menu_day.pack(pady=20)
        self.destroy_list.append(self.menu_day)
        self.menu_month = ctk.CTkOptionMenu(self, values=["январь", "февраль", "март", "апрель", "май", "июнь", "июль",
                                                          "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
                                            font=systemFont, text_color=systemTextColor, command=self.enableSaveButton)
        self.menu_month.set("Месяц")
        self.menu_month.pack(pady=20)
        self.destroy_list.append(self.menu_month)
        self.menu_year = ctk.CTkOptionMenu(self, values=[str(year) for year in range(date.today().year, 1949, -1)],
                                           font=systemFont, text_color=systemTextColor, command=self.enableSaveButton)
        self.menu_year.set("Год")
        self.menu_year.pack(pady=20)
        self.destroy_list.append(self.menu_year)

        self.bSave = ctk.CTkButton(self, text="Сохранить", font=systemFont, text_color=systemTextColor, 
                                   command=self.button_inputData_save, state="disabled")
        # bSave.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.bSave.pack(pady=20)
        self.destroy_list.append(self.bSave)

        bExit = ctk.CTkButton(self, text="Выйти", font=systemFont, text_color=systemTextColor, command=self.button_exit)
        # bExit.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        bExit.pack()
        self.destroy_list.append(bExit)

        self.mainloop()

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
