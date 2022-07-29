import re
import shutil
import requests
from splitwise import Splitwise
from json.encoder import JSONEncoder
import pytesseract
from PIL import Image
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk_sents, pos_tag_sents

class ExpenseEncoder(JSONEncoder):
    def default(self,o):
        return o.__dict__

def splitwise_login():
    try:
        s = Splitwise('xxx',
                  'xxx',
                  api_key='xxx'
                      )
        print('login successful')
    except:
        print('Unable to login, wrong credentials')
        raise Exception
    print('returning splitwise obj')
    return s

def getExpense(splitwise_obj):
    try:
        expense_list = splitwise_obj.getExpenses(limit=5000)
    except:
        print('No Expense list missing')
    return expense_list

def downloadReceipts(expenseList):
    total_receipts = 0
    for expense in expenseList:
        receipt_path = expense.receipt.original
        if receipt_path!=None:
            total_receipts += 1
            #print(receipt_path)
            folder_path = "C:\\Users\\tphaltane\\Desktop\\PyConDE\\Splitwise\\Receipt_" + str(total_receipts) + ".jpeg"
            if folder_path not in "C:\\Users\\tphaltane\\Desktop\\PyConDE\\Splitwise\\":
                with requests.get(receipt_path, stream=True) as r:
                    f = open(folder_path, 'wb')
                    shutil.copyfileobj(r.raw, f)
                    f.close()
    return total_receipts

def readReceipt(date_item,receipt_num):
    print('in read receipt')
    pytesseract.pytesseract.tesseract_cmd = r'C:\\ProgramData\\Anaconda3\\Lib\\tesseract.exe'
    text = pytesseract.image_to_string(Image.open('C:\\Users\\tphaltane\\Desktop\\PyConDE\\Splitwise\\receipts\\Receipt_'+str(receipt_num)+'.jpeg'))
    data_item = nlp(text,date_item)
    return data_item

def nlp(text,date_item):
    #print(text)
    sentences = sent_tokenize(text)
    #print('**',sentences)  #list seperated by new lines
    listSent = []
    for sent in sentences:
        s = re.split('\n',sent)
        listSent.append(s)
    #return listSent
    date_item = createDataItemsDict(listSent, data_item)
    return date_item

def sentTagging(listSent):
    keys = ("sentence","name of speech")
    tagged_sent = pos_tag_sents(listSent)
    #print('tagged sent',tagged_sent)
    mydict = {}

    for outer_list in tagged_sent:
        for inner_list in outer_list:
            sentenceIs = inner_list[0]
            posIs = inner_list[1]
            print('sent {} tag {}'.format(sentenceIs,posIs))
            mydict[posIs] = sentenceIs
    return mydict
#for k,v in mydict.items():
#    print(k,v)

def createDataItemsDict(listSent,data_item):
    value=''
    key = ''
    for sent in listSent:
        for s in sent:
            value = value + ',' + s
            if re.match('Datum:',s):
                print(s)
                key = s
    data_item[key] = value
    return data_item



if __name__ == '__main__':
    print('in main')
    splitwise_obj = splitwise_login()
    expenseList = getExpense(splitwise_obj)
    print('list of expenses obj',expenseList)
    total_numReceipts = downloadReceipts(expenseList)
    print(total_numReceipts)
    data_item = {}
    for receipt_num in range(1,189):
        data_item = readReceipt(data_item,receipt_num)
    #print(text)
    listSent = nlp(text)

    data_item = createDataItemsDict(listSent,data_item)
    fout = open('date_items.csv','w')
    for k,v in data_item.items():
        print('key {}: val {}'.format(k,v))
        fout.write('{},{}'.format(k,v))
        fout.write('\n')

