import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tktimepicker import AnalogPicker, AnalogThemes, constants


class LocalUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1500x1000")
        self.window.title("Report Generator")

        # for i in range(8): # Incorporate if you want to make a larger UI in general
        #     self.window.columnconfigure(i, weight=1)
        #
        # self.window.rowconfigure(0, weight=2)
        # for i in range(1, 10):
        #     self.window.rowconfigure(i, weight=1)

        tk.Label(master=self.window, text="Report Generator (Trade Simulator)",
                 justify="center", font=("Times New Roman", 20), fg="white", bg="black", width=100,
                 height=2).grid(column=0, row=0, columnspan=16, sticky="nsew")

        tk.Label(master=self.window, text="Underlying Ticker:", bg="#636262", font=("Times New Roman", 12),
                 justify="center", height=2).grid(column=0, row=1, columnspan=2, sticky="nsew")

        main_ticker = tk.Entry(master=self.window, bg="#9c9a9a", font=("Times New Roman", 12), justify="center")
        main_ticker.grid(column=2, row=1, columnspan=2, sticky="nsew")

        tk.Label(master=self.window, text="Day Trade Date:", bg="#636262", font=("Times New Roman", 12),
                 justify="center").grid(column=4, row=1, columnspan=2, sticky="nsew")

        day_trade_date = DateEntry(master=self.window, bg='#9c9a9a', font=("Times New Roman", 12), justify="center")
        day_trade_date.grid(column=6, row=1, columnspan=2, sticky="nsew")

        tk.Label(master=self.window, text="Data Period Start", bg="#636262", font=("Times New Roman", 12),
                 justify="center", height=2).grid(column=8, row=1, columnspan=8, sticky="nsew")

        tk.Label(self.window, text="Retrieval Period Start", font=("Times New Roman", 15), justify="center",
                 bg="#9c9a9a", height=1).grid(column=8, row=2, columnspan=4, sticky="nsew")

        tk.Label(self.window, text="Retrieval Period End", font=("Times New Roman", 15), bg="#9c9a9a",
                 justify="center").grid(column=12, row=2, columnspan=4, sticky="nsew")

        data_period_start = AnalogPicker(self.window, type=constants.HOURS12)
        data_period_start.grid(column=8, row=3, sticky="nsew", columnspan=4)
        data_period_start.setHours(9)
        data_period_start.setMinutes(30)

        theme = AnalogThemes(data_period_start)
        theme.setDracula()

        data_period_end = AnalogPicker(self.window, type=constants.HOURS12, period=constants.PM)
        data_period_end.grid(column=12, row=3, sticky="nsew", columnspan=4)
        data_period_end.setHours(4)
        data_period_end.setMinutes(00)

        theme = AnalogThemes(data_period_end)
        theme.setDracula()

        tk.Label(self.window, text="Option Contract Information", font=("Times New Roman", 15), bg="#9c9a9a",
                 justify="center").grid(column=0, columnspan=16, row=4, sticky="nsew")

        tk.Label(self.window, text="Contract 1", font=("Times New Roman", 12), bg="gray",
                 justify="center").grid(column=0, columnspan=8, row=5, sticky="nsew")

        tk.Label(self.window, text="Contract 2", font=("Times New Roman", 12), bg="gray",
                 justify="center").grid(column=8, row=5, columnspan=8, sticky="nsew")

        tk.Label(self.window, text="Strike:", font=("Times New Roman", 12), justify="center").grid(column=0, row=6,
                                                                                                   columnspan=2)

        contract_1_strike = tk.Entry(self.window, font=("Times New Roman", 12), justify="center")
        contract_1_strike.grid(column=2, row=6, columnspan=2, sticky="nsew")

        tk.Label(self.window, text="Strike:", font=("Times New Roman", 12), justify="center").grid(column=4, row=6,
                                                                                                   columnspan=2)

        contract_2_strike = tk.Entry(self.window, font=("Times New Roman", 12), justify="center")
        contract_2_strike.grid(column=6, row=6, columnspan=2, sticky="nsew")

        tk.Label(self.window, text="Expiration Date:", font=("Times New Roman", 12),
                 justify="center").grid(column=0, row=7, columnspan=2)

        contract_1_expiration = DateEntry(self.window, font=("Times New Roman", 12), justify="center")
        contract_1_expiration.grid(column=2, row=7, columnspan=2, sticky="nsew")

        tk.Label(self.window, text="Expiration Date:", font=("Times New Roman", 12),
                 justify="center").grid(column=4, row=7, columnspan=2)

        contract_2_expiration = DateEntry(self.window, font=("Times New Roman", 12), justify="center")
        contract_2_expiration.grid(column=6, row=7, columnspan=2, sticky="nsew")

        tk.Label(self.window, text="Contract Type:", font=("Times New Roman", 12),
                 justify="center").grid(column=0, row=8, columnspan=2)

        option_types = ["CALL", "PUT"]
        call_default = tk.StringVar()
        call_default.set(option_types[0])

        put_default = tk.StringVar()
        put_default.set(option_types[1])

        contract_1_type = tk.OptionMenu(self.window, call_default, *option_types)
        contract_1_type.grid(column=2, row=8, columnspan=2, sticky="nsew")

        tk.Label(self.window, text="Contract Type:", font=("Times New Roman", 12),
                 justify="center").grid(column=4, row=8, columnspan=2)

        contract_2_type = tk.OptionMenu(self.window, put_default, *option_types)
        contract_2_type.grid(column=6, row=8, columnspan=2, sticky="nsew")

        x = AnalogPicker(self.window, type=constants.HOURS12)
        x.grid(column=0, row=9, sticky="nsew", columnspan=4)

        theme = AnalogThemes(x)
        theme.setDracula()

        y = AnalogPicker(self.window, type=constants.HOURS12)
        y.grid(column=4, row=9, sticky="nsew", columnspan=4)
        self.y = y.period()  # for test data function in class

        theme = AnalogThemes(y)
        theme.setDracula()


        data_test_button = tk.Button(self.window, text="Test Data", font=("Times New Roman", 12), justify="center",
                                     command=self.grab_data)
        data_test_button.grid(column=0, row=10)

        self.window.mainloop()


    def grab_data(self):
        x = self.y
        print(x)


UI = LocalUI()
