import pandas as pd
class MEMBER():
    def __init__(self):
        self.list = []
        self.user_list = []
        self.columns = ["user_id", "Mon", "Tue", "Wed", "Thu", "Fri"]
        self.df = pd.DataFrame(columns=self.columns)
    def is_update(self, user_id):
        if user_id in self.user_list:
            return True
        else:
            self.user_list.append(user_id)
            return False
    def data_post(self, user_id, date_value):
        list_data = [0, 0, 0, 0, 0]
        for value in date_value:
            index = int(value[-1])
            list_data[index] = 1
        self.df.loc[self.df["user_id"] == user_id, ["Mon", "Tue", "Wed", "Thu", "Fri"]] = list_data

    def init_post(self, user_id, date_value):
        list_data = [user_id, 0,0,0,0,0]
        for value in date_value:
            index = int(value[-1])
            list_data[index+1] = 1
        self.df.loc[len(self.df)] = list_data


    def check_join(self):
        return [self.df["Mon"].sum(), self.df["Tue"].sum(), self.df["Wed"].sum(), self.df["Thu"].sum(), self.df["Fri"].sum()]



    def show_data(self):
        return self.list
