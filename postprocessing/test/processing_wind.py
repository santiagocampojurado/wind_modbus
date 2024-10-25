import pandas as pd
import os


current_dir = os.path.dirname(__file__)
print(current_dir)

list_files = os.listdir(current_dir)
print(list_files)

if 'promedio_viento.xlsx' in list_files:
    print('File exists')
    average_wind = pd.read_excel('promedio_viento.xlsx')
    print(average_wind)
