import time
import json
import shutil
import os
import hashlib
import pathlib 
from distutils.dir_util import copy_tree
import math



print('The analysis started...')

#The source folder
path_source = "/home/alvaro/Documents/python/original_folder/"
#list with the files in the source
source_list=os.listdir(path_source)



#The destination folder
path_destination ='/home/alvaro/Documents/python/backup_folder/'
#list with the files in the destination
dest_list=os.listdir(path_destination)



time_modification = 1 

#This functions checks the md5, it will be use before and after the copying to check that everything is correct.
def md5_files(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5_folders(directory, verbose=0):
  import hashlib, os
  SHAhash = hashlib.md5()
  if not os.path.exists (directory):
    return -1

  try:
    for root, dirs, files in os.walk(directory):
      for names in files:
        if verbose == 1:
          print( 'Hashing', names)
        filepath = os.path.join(root,names)
        try:
          f1 = open(filepath, 'rb')
        except:
          # You can't open the file for some reason
          f1.close()
          continue

        while 1:
          # Read file in as little chunks
          buf = f1.read(4096)
          if not buf : break
          SHAhash.update(hashlib.md5(buf).hexdigest().encode('utf-8'))
        f1.close()

  except:
    import traceback
    # Print the stack traceback
    traceback.print_exc()
    return -2

  return SHAhash.hexdigest()

def paste0(string1):
	#[-4:] to remove the .txt
	text=string1 + '_md5.md5'
	str(text)
	return text

def time_mod(file, days=1):

    file_time = os.path.getmtime(os.path.join(path_source,file))
    # Check against 24 hours 
    return ((time.time() - file_time) / 3600)

def files_to_copy(li1, li2): 
    lst3 = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return lst3 

def copy_file(file):
 return shutil.copy(os.path.join(path_source, file), os.path.join(path_destination, file))

source_len=[]

for i in source_list:
  if not i.endswith('_md5.md5'):
    source_len.append(i)

dest_len=[]
for i in dest_list:
  if not i.endswith('_md5.md5'):
    dest_len.append(i)

print('=======================================================================')
print('The number of files in the original folder is:', len(source_len))
print('The number of files in the backup folder is:', len(dest_len))
print('=======================================================================')


files_modified_last_12h =0

for files in source_list:
  if not files.endswith('_md5.md5'):
    if time_mod(files)<time_modification:
      files_modified_last_12h+=1

        
print('The number of files modified in the last',time_modification, 'hours is:', files_modified_last_12h)
print('Those files will not be backed up until the next backup.')
print('The number of files that will continue the script are:', len(source_len)- files_modified_last_12h)
print('=======================================================================')

md5_source_calculated=0


for file in source_list:
  #Copy the files that hasn't been modified in the last 12h
    if time_mod(file)>time_modification:
            #Ignore the files ending with md5:
      if file.endswith('_md5.md5'):
#        print(file)
        pass
      #check if the file has already an _md5.md5 file associated,
      #if so, ignore them
      elif paste0(file[:-4]) in source_list:
        pass
      #files which md5 must be calculated and probably copied.
      else:
        md5_source_calculated+=1
        md5_of_file = md5_files(os.path.join(path_source, file))
        with open(os.path.join(path_source,paste0(file[:-4])),'w') as file:
         file.write(md5_of_file)

print('The calculation of the md5 of those files not modified in the last 12 ')
print('hours has been completed.')
print('The number of md5 calculated is:', md5_source_calculated)
print('=======================================================================')
print('Checking which files are not in the backup folder already...')

source_not_modified = []

for file in source_list:
  if time_mod(file)>time_modification:
    if not file.endswith('_md5.md5'):
        source_not_modified.append(file)

files_copy = files_to_copy(source_not_modified, dest_list)

files_copy2 = []

files_to_be_copied=0

for i in files_copy:
  if not i.endswith('_md5.md5'):
    files_copy2.append(i)
    files_to_be_copied+=1


print('The files to be copied are:', files_to_be_copied)

for i in files_copy2:
  print(i)

print('=======================================================================')
print('Copying the files...')

files_copied=0

for file in files_copy2:
  copy_file(file)
  files_copied+=1
  #updating the list
  dest_list.append(file)
print(files_copied, 'files copied succesfully.')


print('=======================================================================')
print('Calculating the md5 of the copied files in the backup_folder')



md5_dest_calculated =0

for file in   dest_list:
    #Ignore the files ending with md5:
    if file.endswith('_md5.md5'):
      pass
    #check if the file has already an _md5.md5 file associated,
    #if so, ignore them
    elif paste0(file[:-4]) in dest_list:
      pass
    #files which md5 must be calculated and probably copied.
    else:
      md5_dest_calculated+=1
      md5_of_file = md5_files(os.path.join(path_destination, file))
      name_file = paste0(file[:-4])
      with open(os.path.join(path_destination , name_file ),'w') as file:
       file.write(md5_of_file)
      dest_list.append(name_file) 

# for file in   dest_list:
#     #Ignore the files ending with md5:
#     if file.endswith('_md5.md5'):
#       pass
#     #check if the file has already an _md5.md5 file associated,
#     #if so, ignore them
#     elif paste0(file[:-4]) in dest_list:
#       pass
#     #files which md5 must be calculated and probably copied.
#     else:
#       md5_dest_calculated+=1
#       md5_of_file = md5_files(os.path.join(path_destination, file))
#       name_file = paste0(file[:-4])
#       with open(os.path.join(path_destination,paste0(file[:-4])),'w') as file:
#        file.write(md5_of_file)
#       dest_list.append(paste0(file[:-4]))

print('The number of md5 calculated is:', md5_dest_calculated)
print('=======================================================================')
print('Checking that the md5 are the same in both the original and backup folder')

files_passed_md5 = 0

if md5_dest_calculated>0:
  for file in dest_list:
      if file.endswith("_md5.md5"):
        with open(os.path.join(path_destination, file),'r') as f1, open(os.path.join(path_source, file),'r') as f2:
          for l1, l2 in zip(f1, f2):
            if l1==l2:
              print(file,'Passed the md5 test')
              files_passed_md5+=1

print('The number of files that passed the md5 test are:', files_passed_md5 )            
