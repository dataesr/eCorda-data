from os.path import basename
import zipfile as zf, pathlib, os

def zip_create(date):   
#create a ZipFile object
    with zf.ZipFile('/eCorda_data/' + f"HE_{date}.zip", 'w') as zipObj:
#Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk('/eCorda_data/'):
            for filename in filenames:
                if os.path.splitext(filename)[-1] == '.csv':
#create complete filepath of file in directory
                    filePath = os.path.join('/eCorda_data/'+ filename)
        #Add file to zip
                    zipObj.write(filePath, basename(filePath))