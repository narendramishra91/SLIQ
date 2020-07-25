from FileProperty import SLIQ_File

classList=[]
keyArray=[]

def AttributeList(arr):
    n = len(arr)
    indTraker = list(range(n))
    for i in range(0, n):
           for j in range(0, n-i-1):
            if arr[j]>arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                indTraker[j], indTraker[j+1] = indTraker[j+1], indTraker[j]
    attList = []
    for k in range(0, n):
        attList.append([arr[k], indTraker[k]])
    return attList            
        
    
def ClassList(arr):
    n=len(arr)
    clasList = []
    for i in range(0, n):
        clasList.append([arr[i], 0])
    return clasList


def ClassHistogram(arr, value, dataSet):
    LB=0
    RB=0
    LG=0
    RG=0
    f = SLIQ_File(dataSet)
    Classes = f.Classes
    classList = ClassList(f.df["Class"].tolist())
    for i in range(0, len(arr)):
        if arr[i][0]>value and classList[arr[i][1]][0]=='G':
            RG+=1
        elif arr[i][0]<value and classList[arr[i][1]][0]=='G':
            LG+=1
        elif arr[i][0]<value and classList[arr[i][1]][0]=='B':
            LB+=1
        else :
            RB+=1
    return [LB, LG, RB, RG]
    
def giniIndex(arr):
    LeftTotal = arr[0]+arr[1]
    RightTotal = arr[2]+arr[3]
    total = LeftTotal + RightTotal
    gIndex = ((LeftTotal/total)*(1-(arr[0]/LeftTotal)**2 - (arr[1]/LeftTotal)**2)) + ((RightTotal/total)*(1-(arr[2]/RightTotal)**2 - (arr[3]/RightTotal)**2))
    return gIndex

def upDateClassList(arr, gini, dataFileName):
    global classList
    classList = dataFileName
    for i in range(0, len(arr)):
        if arr[i][0]<gini:
            classList[arr[i][1]][1]=classList[arr[i][1]][1]*2 + 1
        else:
            classList[arr[i][1]][1]=classList[arr[i][1]][1]*2 + 2
    return classList        
            
def key(arr):
    def sortSecond(val): 
        return val[1]
    arr.sort(key = sortSecond)
    return arr[0][0]

def partition(arr1, dataFileName):
    global classList
    arr=[]
    for k in range(0, len(arr1)):
        arr.append(arr1[k][0])
    giniArr=[]
    for j in range(0, len(arr)-1):
        splitKey = (arr[j]+arr[j+1])/2
        giniArr.append([splitKey, giniIndex(ClassHistogram(arr1, splitKey, dataFileName))])
    print("(breakpoint, gini Index) table ")    
    print(giniArr)
    print("Break Point")
    print(key(giniArr))
    global keyArray
    keyArray.append(key(giniArr))
    classList = upDateClassList(arr1, key(giniArr), classList)
    return classList

def main(dataFileName):
    global classList
    f = SLIQ_File(dataFileName)
    print(f.df)
    attrList=f.attributes
    classList = ClassList(f.df["Class"].tolist())
    noOfAttributes=f.no_Attributes
    print("Initial Class List with node")
    print(classList)
    print("---------------------------------")
    nodeTrack = -1
    TestArr = []
    for i in attrList:
        nodeTrack+=1
        if i!="Class":
            MainArr=f.df[i].tolist()
            Arr = AttributeList(MainArr)
            for l in range((2**nodeTrack)-1, 2*((2**nodeTrack)-1)+1):
                TestArr = []
                for k in range(0, len(classList)):
                    if classList[Arr[k][1]][1]==l:
                        TestArr.append(Arr[k])        
                classList = partition(TestArr, dataFileName)
                print("class list with updated node")
                print(classList)
            print("--------------------------------------------")
    testExample=[]
    print("Please Input Data in order same as attributes:")
    for i in range(0, noOfAttributes-1):
        data=input("input Data")
        testExample.append(data)
    testData(testExample, noOfAttributes, classList)       
            
def testData(arr, num, classList):
    k=0
    for i in range(0, num-1):
        m=float(arr[i])
        if m >= keyArray[k]:
            k=2*k+2
        else:
            k=2*k+1
    p=0
    while(classList[p][1]!=k):
        p=p+1
    print("data is in class:" + classList[p][0])        