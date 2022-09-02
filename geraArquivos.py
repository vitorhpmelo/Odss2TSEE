from objects import *
import pandas as pd


def geraDBAR(md,sys,bus_dic,loads,busvfile):
    
    busvfile="ckt5_EXP_VOLTAGES.CSV"
    dfDBAR=pd.DataFrame.from_dict(bus_dic,orient="index",columns=["ph"])
    dfDBAR["names"]=dfDBAR.index.values.tolist()
    dfDBAR.reset_index(drop=True,inplace=True)

    indexes=dfDBAR[dfDBAR["names"]=="SOURCEBUS"].index.tolist()

    dfDBAR=pd.concat([dfDBAR[dfDBAR["names"]=="SOURCEBUS"],dfDBAR.drop(indexes)],ignore_index=True)
    dfDBAR["KV"]=np.zeros(len(dfDBAR["names"]))
    dfDBAR["PA"]=np.zeros(len(dfDBAR["names"]))
    dfDBAR["PB"]=np.zeros(len(dfDBAR["names"]))
    dfDBAR["PC"]=np.zeros(len(dfDBAR["names"]))
    dfDBAR["QA"]=np.zeros(len(dfDBAR["names"]))
    dfDBAR["QB"]=np.zeros(len(dfDBAR["names"]))
    dfDBAR["QC"]=np.zeros(len(dfDBAR["names"]))
    dfDBAR["Va"]=""
    dfDBAR["Vb"]=""
    dfDBAR["Vc"]=""
    dfDBAR["Ta"]=""
    dfDBAR["Tb"]=""
    dfDBAR["Tc"]=""

    for load in loads:
        for ch in [*load.phbus1]:
            dfDBAR.loc[dfDBAR["names"]==load.bus1,"P"+ch] = dfDBAR.loc[dfDBAR["names"]==load.bus1,"P"+ch]+load.kw/len(load.phbus1)
            dfDBAR.loc[dfDBAR["names"]==load.bus1,"Q"+ch] = dfDBAR.loc[dfDBAR["names"]==load.bus1,"Q"+ch] + load.kw*np.tan(np.arccos(load.pf))/len(load.phbus1)
        

    dfDBAR.loc[dfDBAR["names"]=="SOURCEBUS","Va"]=1.05
    dfDBAR.loc[dfDBAR["names"]=="SOURCEBUS","Vb"]=1.05
    dfDBAR.loc[dfDBAR["names"]=="SOURCEBUS","Vc"]=1.05
    dfDBAR.loc[dfDBAR["names"]=="SOURCEBUS","Ta"]=0
    dfDBAR.loc[dfDBAR["names"]=="SOURCEBUS","Tb"]=-120
    dfDBAR.loc[dfDBAR["names"]=="SOURCEBUS","Tc"]=120

    dfBarvolt=pd.read_csv(md+"/"+sys+"/"+busvfile)
    index=[]
    for id,row in dfBarvolt.iterrows():
        dfDBAR.loc[dfDBAR["names"]==row["Bus"],"KV"]=row["BasekV"]
        index.append(dfDBAR[dfDBAR["names"]==row["Bus"]].index[0])


    dfDBAR.reindex(index)
    dfDBAR.sort_index(ascending=True,inplace=True)
    dfDBAR.to_csv("DBAR.csv",header=None)

    return  dfDBAR     