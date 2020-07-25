
import pandas as pd

class SLIQ_File:
    
            def __init__(self, filename):
                self.filename = filename
                self.df = pd.read_csv(filename)
                self.attributes = self.df.columns.values.tolist()
                self.no_Attributes = len(self.attributes)
                self.Classes = self.df[self.attributes[self.no_Attributes - 1]].unique().tolist()