import pandas as pd
class MEMBER():
    def __init__(self):
        self.user_list = []
        self.columns = ["user_id", "Mon", "Tue", "Wed", "Thu", "Fri", "sorry"]
        self.df = pd.DataFrame(columns=self.columns)


    def get_data_frame(self):
        self.df = pd.read_csv("data.csv")
        self.user_list = self.df["user_id"].to_list()

    def is_update(self, user_id):
        if user_id in self.user_list:
            return True
        else:
            self.user_list.append(user_id)
            return False

    def data_post(self, user_id, date_value):
        self.df = pd.read_csv("data.csv")
        list_data = [0, 0, 0, 0, 0, 0]
        for value in date_value:
            index = int(value[-1])
            list_data[index] = 1
        self.df.loc[self.df["user_id"] == user_id, ["Mon", "Tue", "Wed", "Thu", "Fri", "sorry"]] = list_data
        self.df.to_csv("data.csv")

    def init_post(self, user_id, date_value):
        self.df = pd.read_csv("data.csv")
        list_data = [user_id, 0,0,0,0,0, 0]
        for value in date_value:
            index = int(value[-1])
            list_data[index+1] = 1
        self.df.loc[len(self.df)] = list_data
        self.df.to_csv("data.csv")

    def check_join(self):
        return [self.df["Mon"].sum(),
                self.df["Tue"].sum(),
                self.df["Wed"].sum(),
                self.df["Thu"].sum(),
                self.df["Fri"].sum(),
                self.df["sorry"].sum()]

    def check_user(self, user):
        print(user)

    def total_num(self):
        return len(self.user_list)

    def reset(self):
        self.user_list = []
        self.columns = ["user_id", "Mon", "Tue", "Wed", "Thu", "Fri", "sorry"]
        self.df = pd.DataFrame(columns=self.columns)

