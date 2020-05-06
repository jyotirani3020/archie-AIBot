import random
import numpy as np
import pickle

from sklearn.externals import joblib



shana = {
    
    'LogicalReasoning': 'average',
    'Verbal':'average',
    'Programming' : 'very good',
    'Performace':'good',
    'DataAnalytics':None,
    'QualityAssurance':'good',
    
    
}

shambhavi = {
   
    'LogicalReasoning': 'good',
    'Verbal':'Very good',
    'Programming' : None,
    'Performace':'good',
    'DataAnalytics':None,
    'QualityAssurance':'good',
    
    
}

shreya = {
    
    'LogicalReasoning': 'average',
    'Verbal':'excellent',
    'Programming' : 'good',
    'Performace':'very good',
    'DataAnalytics':None,
    'QualityAssurance':'good',
    
    
}
jyoti = {
    
    'LogicalReasoning': None,
    'Verbal':None,
    'Programming' : None,
    'Performace':None,
    'DataAnalytics':None,
    'QualityAssurance':None,
    
    
}
database = [shana, shambhavi, shreya, jyoti]


team_management_model= open('test/models/team_management_model.pkl','rb')
team_management = joblib.load(team_management_model)

def team(a):
    b = []
    for i in a.keys():
        if i=='Quants' or i=='LogicalReasoning' or i=='Verbal' or i== 'Programming':
            if a[i] == 'average':
                b.append(round(random.uniform(1,7), 3))
            elif a[i] == 'good':
                 b.append(round(random.uniform(7,14), 3))
            elif a[i] == 'very good':
                 b.append(round(random.uniform(14,20), 3))
            elif a[i] == 'excellent':
                 b.append(round(random.uniform(20,25), 3))
            elif a[i] == None or a[i] == '0':
                b.append(0)
        else:
            if a[i] == 'average':
                b.append(round(random.uniform(1,3), 3))
            elif a[i] == 'good':
                 b.append(round(random.uniform(3,5), 3))
            elif a[i] == 'very good':
                 b.append(round(random.uniform(5,8), 3))
            elif a[i] == 'excellent':
                 b.append(round(random.uniform(8,10), 3))
            elif a[i] == None or a[i] == 0:
                b.append(0)
    c = np.array([b])
    result = team_management.predict(c)
    skills =[]
    if result == 1:
        for i in a.keys():
            if a[i] == 'excellent' or a[i]=='very good' or a[i]=='good':
                skills.append(i)
        return "yes, employee can be taken in the team. She has got Excellent skills like : {} ".format(', '.join(skills))
    else:
        
        for i in a.keys():
            if a[i] == 'average' or a[i]==None:
                skills.append(i)
        return "She is not that productive. Employee needs to work on following skills: {}. You may like to consider shana instead she got excellent skills like: problem solving, logical reasoning".format(', '.join(skills))

def team_selection(n):
    if 'shana' in n:
            response = team(database[0])
            return str(response)
    elif 'shambhavi' in n:
        response = team(database[1])
        return str(response)
            
    elif 'shreya' in n:
        response = team(database[2])
        return str(response)
            
    elif 'jyoti' in n:
        response = team(database[3])
        return str(response)


