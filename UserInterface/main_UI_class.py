import tkinter as tk


class LocalUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("750x750")
        self.window.title("Report Generator")

        # for i in range(8): # Incorporate if you want to make a larger UI in general
        #     self.window.columnconfigure(i, weight=1)
        #
        # self.window.rowconfigure(0, weight=2)
        # for i in range(1, 10):
        #     self.window.rowconfigure(i, weight=1)

        main_title = tk.Label(master=self.window, text="Report Generator (Trade Simulator)", justify="center",
                              font=("Times New Roman", 20), fg="white", bg="black")
        main_title.grid(column=0, row=0, columnspan=8, sticky="nsew")

        underlying_label = tk.Label(master=self.window, text="Underlying Ticker:", bg="#636262",
                                    font=("Times New Roman", 12), justify="center")
        underlying_label.grid(column=0, row=1, columnspan=2, sticky="nsew")

        main_ticker = tk.Entry(master=self.window, bg="#9c9a9a", font=("Times New Roman", 12), justify="center")
        main_ticker.grid(column=2, row=1, columnspan=2, sticky="nsew")

        day_trade_date_label = tk.Label(master=self.window, text="Day Trade Date:", bg="#636262",
                                        font=("Times New Roman", 12), justify="center")
        day_trade_date_label.grid(column=4, row=1, columnspan=2, sticky="nsew")

        day_trade_date = tk.Entry(master=self.window, bg='#9c9a9a', font=("Times New Roman", 12), justify="center")
        day_trade_date.grid(column=6, row=1, columnspan=2, sticky="nsew")

        data_start_label = tk.Label(self.window, text="Data Retrieval Start", font=("Times New Roman", 15),
                                    justify="center", height=1)
        data_start_label.grid(column=0, row=2, columnspan=4, sticky="nsew")

        data_end_label = tk.Label(self.window, text="Data Retrieval End", font=("Times New Roman", 15),
                                  justify="center")
        data_end_label.grid(column=4, row=2, columnspan=4, sticky="nsew")

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

        option_data_section_label = tk.Label(self.window, text="Option Contract Information",
                                             font=("Times New Roman", 15), justify="center")
        option_data_section_label.grid(column=0, columnspan=8, row=4)

        contract_1_label = tk.Label(self.window, text="Contract 1", font=("Times New Roman", 12), justify="center")
        contract_1_label.grid(column=0, columnspan=4, row=5)

        contract_2_label = tk.Label(self.window, text="Contract 2", font=("Times New Roman", 12), justify="center")
        contract_2_label.grid(column=4, row=5, columnspan=4)



        self.window.mainloop()


UI = LocalUI()
