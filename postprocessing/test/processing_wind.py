import pandas as pd
import os


current_dir = os.path.dirname(__file__)
print(current_dir)

list_files = os.listdir(current_dir)
print(list_files)

if 'promedio_viento.xlsx' in list_files:
    print('File exists')
    file_path = os.path.join(current_dir, 'promedio_viento.xlsx')
    average_wind = pd.read_excel(file_path)


print(average_wind)

