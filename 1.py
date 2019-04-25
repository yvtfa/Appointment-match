import numpy as np
import pandas as pd
import operator
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from tkinter import *
from collections import Counter

datingTest = pd.read_table('datingTestSet.txt',header = None)
datingTest.head()

def myplot(traindata,labels):


    fig,axes = plt.subplots(nrows=2,ncols=2,sharex=False,sharey=False,figsize=(13,8))
    colorlist = []
    for i in labels:
        if i == 1:
            colorlist.append("red")
        if i == 2:
            colorlist.append("black")
        if i == 3:
            colorlist.append("orange")

    axes[0][0].scatter(x=traindata[:,0], y=traindata[:,1], color=colorlist, s=12, alpha=0.5)
    axes0_set_title = axes[0][0].set_title(u"the number of flyer miles and the video games")
    axes0_set_xlabel = axes[0][0].set_xlabel(u"Frequent flyer miles earned each year")
    axes0_set_ylabel = axes[0][0].set_ylabel(u"Time spent playing video games")
    plt.setp(axes0_set_title,size=9, weight="bold", color="red")
    plt.setp(axes0_set_xlabel,size=7, weight="bold", color="black")
    plt.setp(axes0_set_ylabel,size=7, weight="bold", color="black")

    axes[0][1].scatter(x=traindata[:,0],y=traindata[:,2], color=colorlist, s=12, alpha=0.5)
    axes1_set_title = axes[0][1].set_title(u"frequent flyer miles is proportional to ice cream")
    axes1_set_xlabel = axes[0][1].set_xlabel(u"Frequent flyer miles earned each year")
    axes1_set_ylabel = axes[0][1].set_ylabel(u"Weekly consumption of ice cream liters")
    plt.setp(axes1_set_title,size=9, weight="bold", color="red")
    plt.setp(axes1_set_xlabel,size=7, weight="bold", color="black")
    plt.setp(axes1_set_ylabel,size=7, weight="bold", color="black")

    axes[1][0].scatter(x = traindata[:,1],y=traindata[:,2], color=colorlist, s=12, alpha=0.5)
    axes2_set_title = axes[1][0].set_title(u"The percentage of video games and  ice cream")
    axes2_set_xlabel = axes[1][0].set_xlabel(u"Time spent playing video games")
    axes2_set_ylabel = axes[1][0].set_ylabel(u"Weekly consumption of ice cream liters")
    plt.setp(axes2_set_title,size=9, weight="bold", color="red")
    plt.setp(axes2_set_xlabel,size=7, weight="bold", color="black")
    plt.setp(axes2_set_ylabel,size=7, weight="bold", color="black")

    largeDoses = mlines.Line2D([],[],color="red",marker=".", markersize=6,label="largeDoses")
    smallDoses = mlines.Line2D([],[],color="black",marker=".", markersize=6, label="smallDoses")
    didntLike = mlines.Line2D([],[],color="orange",marker=".", markersize=6, label="didntLike")
    axes[0,0].legend(handles=[largeDoses,smallDoses,didntLike])
    axes[0,1].legend(handles=[largeDoses,smallDoses,didntLike])
    axes[1,0].legend(handles=[largeDoses,smallDoses,didntLike])

    plt.show()

def putinfile(file):
    putin=open(file)
    readfile=putin.readlines()
    datalength=len(readfile)
    traindata=np.zeros((datalength,3))
    labels=[]
    index=0
    for line in readfile:
        line = line.rstrip()
        line = line.split("\t")
        traindata[index,:] = line[0:3]
        if line[-1] == "largeDoses":
            labels.append(1)
        if line[-1] == "smallDoses":
            labels.append(2)
        if line[-1] == "didntLike":
            labels.append(3)
        index += 1
    return traindata, labels


def standdata(traindata):
    meandata0 = np.mean(traindata,axis=0)
    stddata0 = np.std(traindata,axis=0)
    length = traindata.shape[0]
    meandata1 = np.tile(meandata0,(length,1))
    stddata1 = np.tile(stddata0,(length,1))
    standdata = (traindata-meandata1)/stddata1
    return standdata, meandata0, stddata0



def classfy0(testdata,traindata,labels,k=10):
    length=traindata.shape[0]
    diffdata = traindata-np.tile(testdata,(length,1))
    sqrdata = diffdata**2
    sumdata = (sqrdata.sum(axis=1))**0.5
    sumdatasort = sumdata.argsort()
    classfy1 = {}
    classlist = []
    for i in range(k):
        classlist.append(labels[sumdatasort[i]])
    for i in classlist:
        classfy1[i] = classfy1.get(i,0)+1
    classfy2 = sorted(classfy1.items(),key=operator.itemgetter(1),reverse=True)
    classfy=classfy2[0][0]
    return classfy

def classfyperson():
    file="datingTestSet.txt"
    traindata, labels = putinfile(file)
    traindata, meandata0, stddata0 = standdata(traindata)

    test1=float(t0.get())
    test2=float(t1.get())
    test3=float(t2.get())
    testdata=np.array([test1,test2,test3])
    testdata=(testdata-meandata0)/stddata0
    classfy = classfy0(testdata,traindata,labels)
    text = []
    if classfy == 1:
        text.append("女嘉宾对你的感觉是：largeDoses.你很有机会哦！！！")
    elif classfy == 2:
        text.append("女嘉宾对你的感觉是：smallDoses.你需要加油努力！！")
    else:
        text.append("女嘉宾对你的感觉是：didntLike. 你没有机会,放弃吧！")
    Label(window, text=Counter(text).most_common(1)[0][0][:21]).grid(row=6, column=0)
    Label(window, text=Counter(text).most_common(1)[0][0][21:]).grid(row=6, column=1)
    return classfy



if __name__ == "__main__":



    window = Tk()
    window.title("Appointment match")
    window.geometry('500x250')
    Label(window, text='每年出差/旅行的公里数:').grid(row=0, column=0)
    Label(window, text='玩游戏消耗时间的百分比:').grid(row=1, column=0)
    Label(window, text='每周消费的冷饮公升数:').grid(row=2, column=0)
    t_0 = StringVar()
    t_1 = StringVar()
    t_2 = StringVar()
    t0 = Entry(window, textvariable=t_0)
    t1 = Entry(window, textvariable=t_1)
    t2 = Entry(window, textvariable=t_2)
    t0.grid(row=0, column=1, padx=10, pady=5)
    t1.grid(row=1, column=1, padx=10, pady=5)
    t2.grid(row=2, column=1, padx=10, pady=5)
    Button(window, text='确认', width=10, command=classfyperson).grid(row=3, column=0, sticky=W, padx=10, pady=5)
    Button(window, text='退出', width=10, command=window.quit).grid(row=3, column=1, sticky=E, padx=10, pady=5)
    window.mainloop()

    file = "datingTestSet.txt"
    traindata, labels = putinfile(file)
    myplot(traindata, labels)
    classfy = classfyperson()
