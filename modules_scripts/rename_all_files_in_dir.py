# We need to rename the files in the directory so they aren't numbered at the beginning.
# 
import os


directory = '/users/mason/NBA-SPREADS/data/team_csvs/2019-2020/'
for filename in os.scandir(directory):
    file_name = str(filename)
    print(file_name)
    csvname = file_name[11:-2]
    print(csvname)
    new_name = csvname.split('_', 1)
    print(new_name)
    new_name = new_name[1]
    print(new_name)
    old_path = os.path.join(directory, csvname)
    print(old_path)
    new_path = os.path.join(directory, new_name)
    print(new_path)
    os.rename(old_path, new_path)