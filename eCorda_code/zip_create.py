from os.path import basename
import zipfile as zf, pathlib, os

def zip_create(zip_filename):
#create a ZipFile object
    with zf.ZipFile(zip_filename, 'w') as zipObj:
#Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk('/eCorda_data/'):
            for filename in filenames:
                if os.path.splitext(filename)[-1] == '.csv':
#create complete filepath of file in directory
                    filePath = os.path.join('/eCorda_data/'+ filename)
        #Add file to zip
                    zipObj.write(filePath, basename(filePath))
