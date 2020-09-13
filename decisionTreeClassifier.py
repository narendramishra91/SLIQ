import pandas as pd

class DesisionTreeClassifier:
    
    def __init__(self):
        self.root = None
        
        
    class Node:
        def __init__(self):
            self.left = None
            self.right = None
            self.pure = False
            self.decCrit = None
            self.decValue = None
            self.decColumn = None
        
        
    @staticmethod
    def ginniIndex(fr_tab, total):
    
        """ Calculate the gini index given the initial frequency table """
    
        prob = 1
        for cls in fr_tab:
            if total != 0:
                prob = prob-(fr_tab[cls]/total)*(fr_tab[cls]/total)
            else:
                prob = 0
            
        return prob


    
    def giniIndexAgg(self, fr_tab1, fr_tab2, total1, total2, p1, p2):

        """ Calculate the gini index given the initial frequency table """
    
        prob1 = self.ginniIndex(fr_tab1, total1)
        prob2 = self.ginniIndex(fr_tab2, total2)
        
        return p1*prob1 + p2*prob2
    
    
    @staticmethod
    def setInitialFrequencyTable(fr_tab1, fr_tab2, y, y1):
    
        """ Instanciate the initial frequency table """
    
        for cls in y1:
            fr_tab1[cls] = 0
            fr_tab2[cls] = len([x for x in list(y) if x == cls])
        
        
   
    def minGiniIndex(self, fr_tab1, fr_tab2, totalNoOfData, column, y):
    
        """ Calculate the ginni index of all the partition and return the minimum gini index given the column"""
    
        total1 = 0
        n = totalNoOfData
        total2 = n
        temp = 1
        i=-1
    
        for item, cls in sorted(zip(column, y), key=lambda x: x[0]):
            fr_tab1[cls]+=1
            total1 += 1
            fr_tab2[cls]-=1
            total2 -= 1
            p = self.giniIndexAgg(fr_tab1, fr_tab2, total1, total2, total1/n, total2/n)
            i+=1
        
            if temp > p:
                temp = p
                critical_point=item
                index = i
        resultDict = {'minimumGiniIndex': temp, 'criticalPoint': critical_point, 'index': index}      
        return resultDict

    
    def decision(self, X, y):
    
        """ give X and y it retuns the all the criteria to take decicion Like index of row to split,
        name of the column ket value of the column"""
    
        fr_tab1, fr_tab2 = dict(), dict()
        y1 = set(y)
        n = y.shape[0]  
        temp = 1
        resultDict = dict()
    
    
        for column in X.columns:
            self.setInitialFrequencyTable(fr_tab1, fr_tab2, y, y1)
            minGiniValueDict = self.minGiniIndex(fr_tab1, fr_tab2, n, X[column], y)
            minGiniValueDict['column'] = column
            if minGiniValueDict['minimumGiniIndex'] < temp:
                resultDict = minGiniValueDict
                temp = minGiniValueDict['minimumGiniIndex']
            
        return resultDict

    @staticmethod
    def partitionData(index, X, y, columnName):
    
        """ Give the row index and column name partition dataframe into two parts """
    
        df = pd.concat([X, y], axis=1)
        df.sort_values(columnName, inplace = True)
        df.reset_index(drop = True, inplace = True)
        df1, df2 = df.loc[:index, :], df.loc[index+1:,:]
        df2.reset_index(drop = True, inplace = True)
    
        return (df1, df2)
    
    
    def createTree(self, X, y, node):
    
        """ retuns the list of all pure nodes """
    
        decVar = y.name
        y1 = set(y)
        if len(y1) is 1:
            df = pd.concat([X, y], axis=1)
            node.pure = True
            node.decValue = list(y1)[0]
            return 
        else:
            decDict = self.decision(X,y)
            node.decCrit, node.decColumn = decDict['criticalPoint'], decDict['column']
            node1, node2 = self.Node(), self.Node()
            node.left, node.right = node1, node2
            df1, df2 = self.partitionData(decDict['index'], X, y, decDict['column'])
            X1, y1, X2, y2 = df1.drop(decVar, axis  = 1), df1[decVar], df2.drop(decVar, axis  = 1), df2[decVar]
            self.createTree(X1, y1, node1)
            self.createTree(X2, y2, node2)
            
    def fit(self, X, y):
        
        """ Returns the root of decision Tree """
        
        self.root = self.Node()
        self.createTree(X, y, self.root)
        
        return self.root
    
    def predict(self, X):
        
        """ Given the value of X in the form of dict predicts the value at X """
        
        current_node = self.root
        
        while not current_node.pure:
            
            column = current_node.decColumn
            
            if X[column] <= current_node.decCrit:
                current_node = current_node.left
            else:
                current_node = current_node.right
        
        print(current_node.decValue) 
        
        
        
        
    