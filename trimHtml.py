'''
This module searchs all HTML files and removes the given columns from all tables. 
'''
import os
# import xml.etree.ElementTree as et
#from pathlib import Path
from bs4 import BeautifulSoup
import re


columnsToBeRemoved = ["R_Owner", "index_Owner", "OWNER","REFERENCED_OWNER"]

def getAllHtmlFiles(folderName):
    fileList=[]
    for root, dirs, files in os.walk(folderName):
        for file in files:
            if (file.endswith(".html")):
                fileList.append(os.path.join(root, file))
    return fileList


def trimHtml(htmlFile):
    tabIndexRemoved = [2,3,4,6,7,8]
    soup = BeautifulSoup(open(htmlFile), "html.parser"); 
    
    # Remove unwanted Tabs
    mainTabs = []
    currentmaintab = soup.find("div", {"class":"currentmaintab"})
    if currentmaintab!=None:
        mainTabs.append(currentmaintab)

    otherMainTabs = soup.find_all("div", {"class":"maintab"})
    if otherMainTabs!=None:
       mainTabs.extend(otherMainTabs)
    if len(mainTabs)<4: # File already trimmed.
        return

    for index in tabIndexRemoved:
        tab = mainTabs[index]
        if tab!=None:
           tab.decompose()
        masterDivId = "Master.{}".format(index)
        masterDiv = soup.find("div", id=masterDivId)
        if masterDiv!=None:
            masterDiv.decompose()
    
    masters = []
    mainTabs.append(soup.find("div", {"class":"currentmaintab"}))
    mainTabs.extend(soup.find_all("div", {"class":"maintab"}))
    for index in tabIndexRemoved:
        mainTabs[index].decompose()

    
    for column in columnsToBeRemoved:
        removeTableColumn(column.upper(), soup)
   

    # print(soup.prettify('utf-8'))
    
    with open(htmlFile,"wb") as fp:
        fp.write(soup.prettify('utf-8'))
    

def parseTabIndex(clickEvent):
    m = re.match(r'onSelectMainTab\(this, (\d+)\)', clickEvent)
    return m.group(1)


'''
Remove the table columns from all tables
'''
def removeTableColumn(columnText, soup):
    thList = soup.find_all("th",text=columnText)
    
    for th in thList:
        tr = th.parent
        thArr = tr.find_all("th")
        ind =  thArr.index(th) # Get the index of the header
        th.decompose()

        if ind > -1: # found the ind
            trSiblings = tr.find_next_siblings()
            for trRow in trSiblings:
                tdList  = trRow.find_all("td")
                tdList[ind].decompose(); 
            pass

        
        
        


def main():
    root_path = os.path.dirname(os.path.realpath(__file__))
    files = getAllHtmlFiles(root_path)
    for file in files:
        print("Processing {} ... ".format(file), end='', flush=True)
        trimHtml(file)
        print("Done")

def test(): 
    html = '''
    <table id="Table.19" cellpadding="0" cellspacing="0" summary="">
            <tr>
            <th>OWNER</th>
            <th>NAME</th>
            <th>TYPE</th>
            <th>REFERENCED_OWNER</th>
            <th>REFERENCED_NAME</th>
            <th>REFERENCED_TYPE</th>
            </tr>
            <tr onclick="table_onSelectMasterRow(this, 19, 0)" class="currentrow">
            <td class="currentcell">TR_USER_S_WRDSB</td>
            <td class="currentcell">BGR_GROUP</td>
            <td class="currentcell">SYNONYM</td>
            <td class="currentcell">S_WRDSB</td>
            <td class="currentcell">BGR_GROUP</td>
            <td class="currentcell">TABLE</td>
            </tr>
            </table>
'''
    soup = BeautifulSoup(html, "html.parser"); 
    removeTableColumn("REFERENCED_OWNER",soup)
    print(soup.prettify('utf-8'))

if __name__=="__main__":
   main()
