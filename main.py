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
        lines[i].Yprim=dic_lines[lines[i].name]

# %%

loadfile="Loads_ckt5.dss"
loads=readLoads(md,sys,loadfile)
#%%


trafo_files="XFR_Loads_ckt5.dss"

trafos_XRF_LOAD,busesXFR=readTrafo(md,sys,trafo_files)


# %%
##prototipo da funcao que cria DBAR
bus_dic={**buses,**buses2,**busestrafo,**busesXFR}


dfDBAR=pd.DataFrame.from_dict(bus_dic,orient="index",columns=["ph"])
dfDBAR.reset_index()
# %%
