import shutil
import os
import hashlib 
import re



#The source folder
path_source = "/home/alvaro/Documents/python/original_folder"
#list with the files in the source
source_list=os.listdir(path_source)
#source_list=[i for i in (os.path.join(path_source, f) for f in os.listdir(path_source)) if os.path.isfile(i)]


#The destination folder
path_destination ='/home/alvaro/Documents/python/backup_folder'
#list with the files in the destination
dest_list=os.listdir(path_destination)
#dest_list=[i for i in (os.path.join(path_destination, f) for f in os.listdir(path_destination)) if os.path.isfile(i)]


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




def copy(source, destination):
  if files not in dest_list:
#This command will copy everything that is not a folder
    if os.path.isdir(os.path.join(path_source,files)):
      shutil.copytree(src=os.path.join(source,files), dst=os.path.join(destination,files))

#== md5_folders(os.path.join(destination, files),1))
 
 
#print('The checksum for the file:',files, 'is:', md5(os.path.join(path_source,files))== md5(os.path.join(path_destination, files)))
      print('The files inside directories are:', files,'and the checksum is:',md5_folders(os.path.join(source,files)) == md5_folders(os.path.join(destination,files)))
    else:
      shutil.copy(src=os.path.join(source,files), dst=destination)
      print('The files copied are:', files,'and the checksum is :', md5_files(os.path.join(source,files))== md5_files(os.path.join(destination, files)))


dic_source_md5 = {}


for files in source_list:
  if os.path.isfile(os.path.join(path_source,files)) == True:
    dic_source_md5[files]=md5_files(os.path.join(path_source,files))
  else:
    dic_source_md5[files]=md5_folders(os.path.join(path_source,files))




#Dic source

dic_source_size = {}

for files in source_list:
  dic_source_size[files]= os.stat(os.path.join(path_source,files)).st_size
  




#size dest

dic_destination_size = {}
for files in dest_list:
  dic_destination_size[files]= os.stat(os.path.join(path_destination,files)).st_size
  


#md5
dic_destination_md5= {}

for files in dest_list:
  if os.path.isfile(os.path.join(path_source,files)) == True:
    dic_destination_md5[files]=md5_files(os.path.join(path_destination,files))
  else:
    dic_destination_md5[files]=md5_folders(os.path.join(path_destination,files))



#Creating dictionaries
print()
print('**********************Checking if the file is present*****************************')
print()

files_copied=0
folder_copied=0
#Check if the file is present in the destination
for key in dic_source_size:
  if key in dic_destination_size:
    print(key, 'it is in backup folder already.')
    print()

  elif key not in dic_destination_size:
    
    
 
    
    if os.path.isfile(os.path.join(path_source,key)) == True:
      print('The file:',key, ' is not present in the backup folder and it will be copied.' )

      shutil.copy(os.path.join(path_source,key),os.path.join(path_destination,key))
      print(key,'copied succesfully.')

      dic_destination_md5[key] = md5_files(os.path.join(path_destination,key))

      files_copied +=1

    else:
      print('The folder',key, ' is not present in the backup folder and it will be copied, together with its content.' )
      shutil.copytree(os.path.join(path_source,key),os.path.join(path_destination,key))
      print(key, 'copied succesfully.')
      folder_copied +=1
      
      dic_destination_md5[key] = md5_folders(os.path.join(path_destination,key))

    dic_destination_size[key]= os.stat(os.path.join(path_destination,key)).st_size


   
print()    
print('The number of files copied are:', files_copied)
print( 'The number of folders copied are:', folder_copied)
print()
print('**************Checking if the files have the same size****************************')
print()

files_copied2=0
folder_copied2=0

for key, value in dic_source_size.items():
 
  if value == dic_destination_size[key]:
    print(key,'Has the same size in both folders') 
    print()


 
  elif value != dic_destination_size[key]:
    
 
    if os.path.isfile(os.path.join(path_source,key)) == True:
      print('The file:',key, ' has not the same size  in the backup folder and it will be copied.' )

      shutil.copy(os.path.join(path_source,key),os.path.join(path_destination,key))
      files_copied2+=1
      print(key,'copied succesfully.')

      dic_destination_md5[key] = md5_files(os.path.join(path_destination,key))

    else:
      print('The folder:',key, ' has not the same size  in the backup folder and it will be copied.' )
      

      shutil.copytree(os.path.join(path_source,key),os.path.join(path_destination,key))
      folder_copied2+=1
      print(key, 'copied succesfully.')

      
      dic_destination_md5[key] = md5_folders(os.path.join(path_destination,key))
      

    dic_destination_size[key]= os.stat(os.path.join(path_destination,key)).st_size


print()    
print('The number of files copied are:', files_copied2)
print( 'The number of folders copied are:', folder_copied2)
print()
print('*************************Checking the md5 checksums*******************************')
print()
files_copied3=0
folder_copied3=0



for key, value in dic_source_md5.items():

 

  if value == dic_destination_md5[key]:
    

    print(key, 'passed the md5 check. And will not be copied')
    print()

  elif value != dic_destination_md5[key]:
    
 
    
    if os.path.isfile(os.path.join(path_source,key)) == True:
     


      print('The file', key, 'did not pass the md5 check, and it will be copied')
      shutil.copy(os.path.join(path_source,key),os.path.join(path_destination,key))
      print(key, 'copied succesfully.')
      files_copied3+=1




      dic_destination_md5[key] = md5_files(os.path.join(path_destination,key))
      

    else:
      


      print('The folder', key, 'did not pass the md5 check, and it will be copied.')
      shutil.copytree(os.path.join(path_source,key),os.path.join(path_destination,key))
      print(key, 'copied succesfully.')
      folder_copied3+=1
      p
      dic_destination_md5[key] = md5_folders(os.path.join(path_destination,key))
      

    dic_destination_size[key]= os.stat(os.path.join(path_destination,key)).st_size
    


print()    
print('The number of files copied are:', files_copied3)
print( 'The number of folders copied are:', folder_copied3)
print()
print('*****************Checking the md5 of the whole folder*******************')
print()


if md5_folders(path_source)==md5_folders(path_destination):
  print('The backup was successful, md5 checked for every file.')

else:
  print('The md5 of the whole folder was not correct.')
  print('It does not mean that the backup was not correct, maybe a file was removed from the original folder')
 



