from transformers import pipeline
import speech_recognition as sr
import time
import sys
import subprocess
import os
from datetime import datetime
import webbrowser
from googlesearch import search
import operator

while(1):
    tic = time.perf_counter()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source, phrase_time_limit=30)
        print("Time over, thanks")
        try:
            text = r.recognize_google(audio_text)
            print("Text: "+text)
        except:
            print("Sorry, I did not get that")
            continue

    keyword = ''
    for i in range(len(text)-1, 0, -1):

        if(text[i] == " "):
            keyword = keyword[::-1]
            break
        else:
            keyword = keyword + text[i]

    write_str = ''
    for i in range(0, 5, -1):
        write_str = write_str+text[i]
    if (write_str == "write"):

        pass


    else:
        classifier = pipeline('zero-shot-classification',
                            model='facebook/bart-large-mnli')

        labels = ["show contents", "go to folder", "go back to folder",
                "make directory","time","Date","multiply","addition","divide","substract","search","stop"]
        hypothesis_template = 'The text is about {}.'
        sequence = text

        prediction = classifier(
            sequence, labels, hypothesis_template=hypothesis_template, multi_label=True)

        print(prediction)
        l = prediction['labels']
        print("the output is: ", l[0])

    def eval_binary_expr(op1, oper, op2):
        op1,op2 = int(op1), int(op2)
        return get_operator_fn(oper)(op1, op2)   

    def get_operator_fn(op):
        return {
            '+' : operator.add,
            '-' : operator.sub,
            'x' : operator.mul,
            'divided' :operator.__truediv__,
            'Mod' : operator.mod,
            'mod' : operator.mod,
            '^' : operator.xor,
            }[op]
    def lss():
        list_files = os.system("dir")
    if l[0]=="addition" or l[0]=="substract" or l[0]=="multiply" or l[0]=="divide":
        if "and" not in text or "by" not in text:
            print(eval_binary_expr(*(text.split())))


    if l[0] == "time":
        currentDT = datetime.now()
        timeN = currentDT.strftime("%H:%M:%S")
        print("The Time right now in your location is:", timeN)
    elif l[0] == "Date":
        currentDT = datetime.now()
        print("The Date right now of your location is: ", currentDT)
    elif l[0]=="addition":
        if "and" in text:
            k = int(text[-1])
            l = int(text[-7])
            print("The result of addition is: ", l+k)
    elif l[0] == "substract":
        if "and" in text:
            k = int(text[-1])
            l = int(text[-7])
            print("The result of substraction is: ", l-k)
    elif l[0]== "multiply":
        if "and" in text:
            k = int(text[-1])
            l = int(text[-7])
            print("The result of multiplication is: ", l*k)
    elif l[0]== "divide":
        if "and" in text:
            k = int(text[-1])
            l = int(text[-7])
            print("The result of division is: ", l/k)
        elif "by" in text:
            k = int(text[-1])
            l = int(text[-6])
            print("The result of division is: ", l/k)
    elif l[0]=="search":
        pth = keyword
        url="http://www."+pth+".com"
        webbrowser.open_new_tab(url)
    elif l[0]=="stop":
        print("Glad I could help you")
        exit(0)
    else:
        if l[0]=="show contents":
            lss()
        elif l[0] == "make directory":
            pth = os.getcwd()
            pth2 = os.path.join(pth, keyword)
            mode = 0o666
            os.mkdir(pth2, mode)
            print("Directory created!")
    toc = time.perf_counter()

    print(f"total run time in {toc - tic:0.4f} seconds")

        

        