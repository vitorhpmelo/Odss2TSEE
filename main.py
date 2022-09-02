#%%
from objects import *
from lerArquivos import *
from geraArquivos import *

md="Sys"

sys="ckt5"

linefile="Lines_ckt5.dss"

lines,buses=readLines(md,sys,linefile)

linefile="Loads_ckt5.dss"

lines2,buses2=readLines(md,sys,linefile)

yprimfile="ckt5_EXP_YPRIM.CSV"

dic_lines=readYprim(md,sys,yprimfile)

trafo_files="Transformers_ckt5.dss"

trafos,busestrafo=readTrafo(md,sys,trafo_files)

# %%
for i in range(len(lines)):
    if lines[i].name in dic_lines.keys():
        lines[i].Yprim = dic_lines[lines[i].name]

# %%

loadfile="Loads_ckt5.dss"
loads=readLoads(md,sys,loadfile)
#%%
trafo_files="XFR_Loads_ckt5.dss"

trafos_XRF_LOAD,busesXFR=readTrafo(md,sys,trafo_files)

#%%
reactor_file="Transformers_ckt5.dss"

reactors,busesreactor=readReactor(md,sys,reactor_file)


# %%
##prototipo da funcao que cria DBAR
bus_dic={**buses,**buses2,**busestrafo,**busesXFR,**busesreactor}

busvfile="ckt5_EXP_VOLTAGES.CSV"

dfDBAR=pd.DataFrame.from_dict(bus_dic,orient="index",columns=["ph"])
dfDBAR["names"]=dfDBAR.index.values.tolist()
dfDBAR.reset_index(drop=True,inplace=True)

indexes=dfDBAR[dfDBAR["names"]=="SOURCEBUS"].index.tolist()

dfDBAR=pd.concat([dfDBAR[dfDBAR["names"]=="SOURCEBUS"],dfDBAR.drop(indexes)],ignore_index=True)
dfDBAR["KV"]=np.zeros(len(dfDBAR["names"]))
dfDBAR["phase"]=np.zeros(len(dfDBAR["names"]),dtype=int)
dfDBAR["con"]=np.ones(len(dfDBAR["names"]),dtype=int)
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

dfDBAR.loc[dfDBAR["ph"]=="A","phase"]=1
dfDBAR.loc[dfDBAR["ph"]=="B","phase"]=2
dfDBAR.loc[dfDBAR["ph"]=="C","phase"]=3
mask=(dfDBAR["ph"]=="AB") | (dfDBAR["ph"]=="BA")
dfDBAR.loc[mask,"phase"]=4
mask=(dfDBAR["ph"]=="CA") | (dfDBAR["ph"]=="AC")
dfDBAR.loc[mask,"phase"]=5
mask=(dfDBAR["ph"]=="BC") | (dfDBAR["ph"]=="CB")
dfDBAR.loc[mask,"phase"]=6
mask=dfDBAR["ph"].str.match(r"[A-Z][A-Z][A-Z]")
dfDBAR.loc[mask,"phase"]=7
dfDBAR.to_csv("DBAR.csv",header=None,index=True,columns=["con","phase","KV",'PA', 'PB', 'PC', 'QA', 'QB', 'QC','Va', 'Vb', 'Vc', 'Ta', 'Tb', 'Tc'])
# %%