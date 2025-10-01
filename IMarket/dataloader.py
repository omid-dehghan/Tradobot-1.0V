import pandas as pd
import os


class DataLoader:

    def __init__(self, file_path=r".src\.data.csv"):
        self.file_path = file_path
        default_data = {
            'asks': [],
            'bids': [],
        }
        if not os.path.exists(file_path):
            self.df = pd.df(data=default_data).to_csv(
                self.file_path, encoding='utf-8-sig', index=False)

        self.df = pd.read_csv(self.file_path, encoding='utf-8-sig')

    def load_to_df(self):
        return pd.read_csv(self.file_path, encoding='utf-8-sig')

    def save(self):
        self.df.to_csv(
            self.file_path, encoding='utf-8-sig', index=False)
    
    def add_newrow(self, prices:list):
        self.df.loc[self.len] = prices
        self.save()

    def remove(self, index):
        self.df.drop(self.df.index[index], inplace=True)
        self.save()

    def pop(self):
        self.remove(-1)  # Drop the last index   

    def clear_all(self):
        self.df = self.df.iloc[0:0]  # Keep column structure but remove all data
        self.save()

    @property
    def len(self):
        return len(self.df)
    
    def __str__(self):
        return str(self.df)
    
    def __repr__(self):
        return str(self.df)

if __name__ == "__main__":
    pass
