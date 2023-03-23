# import necessary packages
import xml.etree.ElementTree as ET
import uuid
from pathlib import Path
import os
import datetime
import hashlib
import base64
import mimetypes

def hashvalue(filename):
    with open(filename,"rb") as file:
        return(base64.b64encode(hashlib.sha1(file.read()).digest())).decode('utf-8')
# To create a packinglist
def Packinglist(folderpath,uuidcommon):
    
    doc =ET.Element("PackingList",xmlns="http://www.smpte-ra.org/schemas/429-8/2007/PKL")
    #uuid
    ET.SubElement(doc,"Id").text ="urn:uuid:"+str(uuidcommon['Uuid'])
    #Annotation text
    ET.SubElement(doc,"AnnotationText").text ="Assets of "+Path(path).parts[-1]
    #current date and time
    ET.SubElement(doc,"IssueDate").text =datetime.datetime.utcnow().isoformat(timespec="seconds")+"+00:00"
    #Issuer
    ET.SubElement(doc,"Issuer").text="Qube Cinema"
    #creator
    ET.SubElement(doc,"Creator").text="Qube"
# to gothrough all the files in a folder
    AssetList =ET.SubElement(doc,"AssetList")
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            Asset =ET.SubElement(AssetList,"Asset")
            file_path = os.path.join(root,filename)
            file_size = os.path.getsize(file_path)
            ET.SubElement(Asset,"Id").text ="urn:uuid:"+str(uuidcommon[filename])
            ET.SubElement(Asset,"AnnotationText").text =Path(folderpath).parts[-1]
            ET.SubElement(Asset,"Hash").text =hashvalue(file_path)
            ET.SubElement(Asset,"Size").text =str(file_size)
            file_path = os.path.join(root,filename)
            file_Type =mimetypes.guess_type(file_path)[0]
            ET.SubElement(Asset,"Type").text =file_Type
            
            
             
    treeform =ET.ElementTree(doc)
    treeform.write(os.path.join(folderpath,"packinglist.xml"),encoding="utf-8",xml_declaration=True,short_empty_elements=False)
    
# to create a asset map file
def Assetmap(folderpath,uuidcommon):
    doc =ET.Element("AssetMap",xmlns="http://www.smpte-ra.org/schemas/429-9/2007/AM" )
    ET.SubElement(doc,"Id").text ="urn:uuid:"+str(uuidcommon['Uuid'])
    ET.SubElement(doc,"AnnotationText").text ="Assets of "+Path(folderpath).parts[-1]
    ET.SubElement(doc,"Creator").text="Qube"
    ET.SubElement(doc,"VolumeCount").text=str(int(1))
    ET.SubElement(doc,"IssueDate").text =datetime.datetime.utcnow().isoformat(timespec="seconds")+"+00:00"
    ET.SubElement(doc,"Issuer").text="Qube Cinema"
   
# to go through all the files in a folder
    AssetList =ET.SubElement(doc,"AssetList")
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            Asset =ET.SubElement(AssetList,"Asset")
            ET.SubElement(Asset,"Id").text ="urn:uuid:"+str(uuidcommon[filename])
            ET.SubElement(Asset,"AnnotationText").text =str(Path(folderpath).parts[-1])
            Chunklist =ET.SubElement(Asset,"ChunkList")
            Chunk =ET.SubElement(Chunklist,"Chunk")
            ET.SubElement(Chunk,"Path").text =str(filename)
            
            
    #to save it in an xml format        
    treeform =ET.ElementTree(doc)
    treeform.write(os.path.join(folderpath,"assetmap.xml"),encoding="utf-8",xml_declaration=True,short_empty_elements=False)
    


if __name__ == '__main__':
    # enter you DCP folder path
    folderpath=input("enter your folder path:")
    path=os.path.dirname(folderpath)

    # checking if the directory demo_folder
    # exist or not.
    if os.path.exists(folderpath):
    # to create a uuid for each file in a folder
        if len(os.listdir(path)) == 0:
            print("Directory is empty")
        else:    
            uuidcommon = {}
            uuidcommon["Uuid"]=uuid.uuid4()
            for root, dirs, files in os.walk(folderpath):
                for filename in files:
                    uuidcommon[filename] =uuid.uuid4()

            Packinglist(folderpath,uuidcommon)
            Assetmap(folderpath,uuidcommon)
    #  if the povided path is not valid then it will show an error  
    if not os.path.exists(folderpath):
        print("That the directory doesnot exists")
        print("please provide a valid directory")


        
     