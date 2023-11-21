import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tktimepicker import AnalogPicker, AnalogThemes, constants


class LocalUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("755x750")
        self.window.title("Report Generator")

        # for i in range(8): # Incorporate if you want to make a larger UI in general
        #     self.window.columnconfigure(i, weight=1)
        #
        # self.window.rowconfigure(0, weight=2)
        # for i in range(1, 10):
        #     self.window.rowconfigure(i, weight=1)

        tk.Label(master=self.window, text="Report Generator (Trade Simulator)",
                 justify="center", font=("Times New Roman", 20), fg="white", bg="black", width=50,
                 height=2).grid(column=0, row=0, columnspan=8, sticky="nsew")

        tk.Label(master=self.window, text="Underlying Ticker:", bg="#636262", font=("Times New Roman", 12),
                 justify="center", height=2).grid(column=0, row=1, columnspan=2, sticky="nsew")

        main_ticker = tk.Entry(master=self.window, bg="#9c9a9a", font=("Times New Roman", 12), justify="center")
        main_ticker.grid(column=2, row=1, columnspan=2, sticky="nsew")

        tk.Label(master=self.window, text="Day Trade Date:", bg="#636262", font=("Times New Roman", 12),
                 justify="center").grid(column=4, row=1, columnspan=2, sticky="nsew")

        day_trade_date = DateEntry(master=self.window, bg='#9c9a9a', font=("Times New Roman", 12), justify="center")
        day_trade_date.grid(column=6, row=1, columnspan=2, sticky="nsew")

        tk.Label(self.window, text="Data Retrieval Start", font=("Times New Roman", 15), justify="center",
                 height=1).grid(column=0, row=2, columnspan=4, sticky="nsew")

        tk.Label(self.window, text="Data Retrieval End", font=("Times New Roman", 15),
                 justify="center").grid(column=4, row=2, columnspan=4, sticky="nsew")

        am_default = tk.StringVar()
        am_default.set("AM")

        pm_default = tk.StringVar()
        pm_default.set("PM")

        drop_am_pm = ['AM', 'PM']
        data_start_am_pm = tk.OptionMenu(self.window, am_default, *drop_am_pm)
        data_start_am_pm.grid(column=3, row=3, sticky="nsew")

        data_end_am_pm = tk.OptionMenu(self.window, pm_default, *drop_am_pm)
        data_end_am_pm.grid(column=7, row=3, sticky="nsew")

        data_start = tk.Entry(self.window, font=("Times New Roman", 15), justify="center")
        data_start.grid(column=0, row=3, columnspan=3, sticky="nsew")

        data_end = tk.Entry(self.window, font=("Times New Roman", 15), justify="center")
        data_end.grid(column=4, row=3, columnspan=3, sticky="nsew")

        tk.Label(self.window, text="Option Contract Information", font=("Times New Roman", 15),
                 justify="center").grid(column=0, columnspan=8, row=4)

        tk.Label(self.window, text="Contract 1", font=("Times New Roman", 12), justify="center").grid(column=0,
                                                                                                      columnspan=4,
                                                                                                      row=5)

        tk.Label(self.window, text="Contract 2", font=("Times New Roman", 12), justify="center").grid(column=4, row=5,
                                                                                                      columnspan=4)

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


        self.window.mainloop()


UI = LocalUI()
