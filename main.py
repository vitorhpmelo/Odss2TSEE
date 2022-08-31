#%%
from objects import *
from lerArquivos import *
import pandas as pd

md="Sys"

sys="test"

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

dfDBAR=pd.DataFrame.from_dict(bus_dic,orient="index",columns=["ph"])
dfDBAR["names"]=dfDBAR.index.values.tolist()
dfDBAR.reset_index(drop=True,inplace=True)

indexes=dfDBAR[dfDBAR["names"]=="SOURCEBUS"].index.tolist()

dfDBAR=pd.concat([dfDBAR[dfDBAR["names"]=="SOURCEBUS"],dfDBAR.drop(indexes)],ignore_index=True)
dfDBAR["PA"]=np.zeros(len(dfDBAR["names"]))
dfDBAR["PB"]=np.zeros(len(dfDBAR["names"]))
dfDBAR["PC"]=np.zeros(len(dfDBAR["names"]))
dfDBAR["QA"]=np.zeros(len(dfDBAR["names"]))
dfDBAR["QB"]=np.zeros(len(dfDBAR["names"]))
dfDBAR["QC"]=np.zeros(len(dfDBAR["names"]))

for load in loads:
     if len(load.phbus1) == 1:
        dfDBAR.loc[dfDBAR["names"]==load.bus1,"P"+load.phbus1] = dfDBAR.loc[dfDBAR["names"]==load.bus1,"P"+load.phbus1]+load.kw
        dfDBAR.loc[dfDBAR["names"]==load.bus1,"Q"+load.phbus1] = dfDBAR.loc[dfDBAR["names"]==load.bus1,"Q"+load.phbus1] + load.kw*np.tan(np.arccos(load.pf))
    


# %%
