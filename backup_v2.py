import time
import json
import shutil
import os
import hashlib
import pathlib 
from distutils.dir_util import copy_tree
import math
import errno

print('The analysis started...')

#The source folder
#path_source = "t:/Proteomics/Exploris480_E307/Xcalibur/data/"
path_source = "/home/alvaro/Documents/python/original_folder/"

#list with the files in the source
source_list=[]

#The destination folder
#path_destination ='//fgudata.fgu.local/FGU045/Proteomics/Proteomics_data/Exploris480_E307_bak/raw/'
#\\fgudata.fgu.local\FGU045\Proteomics\Proteomics_data\Exploris480_E307_bak\raw\
path_destination ='/home/alvaro/Documents/python/backup_folder/'
#list with the files in the destination
#dest_list=os.listdir(path_destination)
dest_list = []

#time in hours
time_modification =  0

for root, dirs, files in os.walk(path_source):
  for name in files:
    source_list.append(name)

for root, dirs, files in os.walk(path_destination):
  for name in files:
    dest_list.append(name)
# print(source_list)

#This functions checks the md5, it will be use before and after the copying to check that everything is correct.
def md5_files(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


#add the md5 string
def paste0(string1):
  #[-4:] to remove the .txt
  text=string1 + '_md5.md5'
  str(text)
  return text

def paste1(string1):
  text = string1[:-8]+'.txt'
  str(text)
  return text


#differences between two lists
def files_to_copy(li1, li2):
   return list(set(li1)-set(li2))


def copy_file(file):
 return shutil.copystat(os.path.join(path_source, file), os.path.join(path_destination, file))


def copy_folder(folder):
  return copy_tree(os.path.join(path_source, folder), os.path.join(path_destination,folder))

def is_file(x):
  return os.path.isfile(os.path.join(path_source,x))

source_len=[]
source_folder_len=[]

for i in source_list:
  if is_file(i):
    if not i.endswith('_md5.md5'):
      source_len.append(i)
  else:
    source_folder_len.append(i)

dest_len=[]
dest_len_folder=[]

for i in dest_list:
  if is_file(i):
    if not i.endswith('_md5.md5'):
      dest_len.append(i)
  else:
    dest_len_folder.append(i)

print('=======================================================================')
print('The number of subfolders in the original_folder:', len(source_folder_len))
print('The number of files in the original folder is:', len(source_len))
print()
print('The number of subfolders in the backup folder is:', len(dest_len_folder))
print('The number of files in the backup folder is:', len(dest_len))
print('=======================================================================')

files_modified_last_h =0

for root, dirs, files in os.walk(path_source):
  for name in files:
    time_file = file_time = os.path.getmtime(os.path.join(root,name))

    time_modi = ((time.time() - file_time) / 3600)

    if time_modi < time_modification:
      files_modified_last_h+=1
     
print('The number of files/folders modified in the last',time_modification, 'hours is:', files_modified_last_h)
print('Those files will not be backed up until the next backup.')
print('The number of files that will continue the script are:', len(source_len)- files_modified_last_h)
print('=======================================================================')

md5_source_calculated=0
md5_source_folder_calculated=0

for root, dirs, files in os.walk(path_source):
  for name in files:
    
    time_file = file_time = os.path.getmtime(os.path.join(root,name))


    time_modi = ((time.time() - file_time) / 3600)
    
#Copy the files that hasn't been modified in the last 12h
    if time_modi>time_modification:

        if name.endswith('_md5.md5'):
          pass

        elif paste0(name[:-4]) in source_list:
          pass
          
        elif name.endswith('.raw'):    
          md5_source_folder_calculated+=1

          md5_of_file2=md5_files(os.path.join(root,name))

          name_file2=paste0(name[:-4])

          write_inside=str(md5_of_file2+' *'+name)
          print(write_inside)
          with open(os.path.join(root,name_file2),'w') as file:
            file.write(write_inside)
          os.utime(os.path.join(root,name_file2),(time_file, time_file))


print('The calculation of the md5 of those files not modified in the last', time_modification ,'hours')
print('hours has been completed.')
print('The number of md5 calculated is:', md5_source_calculated)
print('The number of md5 of subfolders is:', md5_source_folder_calculated)
print('=======================================================================')
print('Checking which files are not in the backup folder already...')

source_not_modified = []

for root, dirs, files in os.walk(path_source):
  for name in files:

    time_file = file_time = os.path.getmtime(os.path.join(root,name))

    time_modi = ((time.time() - file_time) / 3600)

    if time_modi>time_modification:
      if not name.endswith('_md5.md5'):
        source_not_modified.append(name)

files_copy = files_to_copy(source_not_modified, dest_list)

files_copy2 = []

print('files to copy',files_copy)

print('There are', len(files_copy),'files to be copied, which are:')

print('=======================================================================')
print('Copying the files...')

files_copied=0

#Copying files
for root, dirs, files in os.walk(path_source):
  for name in files:
    if name in files_copy:
      #Replace the path_source with the destination to create the dir scheme
      dst_dir = root.replace(path_source, path_destination, 1)
      
      #Create a dir if it doesn't exit
      if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        
      #assign the destination names  
      src_file = os.path.join(root, name)
      dst_file = os.path.join(dst_dir, name)
          
      if os.path.exists(dst_file):
          os.remove(dst_file)

      shutil.copy2(src_file, dst_dir)
      
      files_copied+=1
      
print(files_copied, 'files copied succesfully.')

print('=======================================================================')
print('Calculating the md5 of the copied files in the backup_folder')

md5_dest_calculated =0

dest_list=[]

for root, dirs, files in os.walk(path_destination):
  for name in files:
    dest_list.append(name)

for root, dirs, files in os.walk(path_destination):
  for name in files:
    if name.endswith('_md5.md5'):
      pass
    elif paste0(name[:-4]) in dest_list:
      pass
    #files which md5 must be calculated
    elif name.endswith('.raw'):
      md5_dest_calculated+=1
      md5_of_file = md5_files(os.path.join(root, name))
      name_file = paste0(name[:-4])

      time_file2 = os.path.getmtime(os.path.join(root,name))

      write_inside=str(md5_of_file+' *'+name)
      with open(os.path.join(root , name_file ),'w') as file:
       file.write(write_inside)
      os.utime(os.path.join(root,name_file),(time_file2, time_file2))

      dest_list.append(name_file) 

print('The number of md5 calculated in the backup folder is:', md5_dest_calculated)

print('=======================================================================')
print('Checking that the md5 are the same in both the original and backup folder...')

files_passed_md5 = 0

if md5_dest_calculated >0:
  try:
    for root, dirs, files in os.walk(path_source):
      for name in files:
        #if paste1(name) in files_copy: 
          if name.endswith('_md5.md5'):
            #Replace the path_source with the destination to create the dir scheme
            dst_dir = root.replace(path_source, path_destination, 1)
            
            #assign the destination names  
            src_file = os.path.join(root, name)
            dst_file = os.path.join(dst_dir, name)

            with open(src_file,'r') as f1, open(dst_file,'r') as f2:
              for l1, l2 in zip(f1, f2):
                if l1==l2:
                  print(name,'Passed the md5 test')
                  files_passed_md5+=1

  except FileNotFoundError: 
    print(file, 'was not found in one of the folders. And could not be md5 checked.') 

else:
  print('Since no file was copied, no files will be checked')

print('The number of files that passed the md5 test are:', files_passed_md5 )            

print('Careful with files with the same name, because set() only gets uniques')

print('=======================================================================')
print('=============================== RESULTS ===============================')


print('Number of files copied:,', files_copied)
print('Number of files that passed the checksum test:', files_passed_md5)
print('Number of files in the original folder is:',len(source_list))
print('Number of files in the backup folder is:',len(dest_list))
print('Number of files modified in the last', time_modification,'hours is:', files_modified_last_h,'it was not copied.')
