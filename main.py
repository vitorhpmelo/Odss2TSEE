#%%
from objects import *
from lerArquivos import *


md="Sys"

sys="test"

linefile="Lines_ckt5.dss"


lines=readLines(md,sys,linefile)

linefile="Loads_ckt5.dss"

lines2=readLines(md,sys,linefile)

yprimfile="ckt5_EXP_YPRIM.CSV"



dic_lines=readYprim(md,sys,yprimfile)
# %%

for i in range(len(lines)):
    if lines[i].name in dic_lines.keys():
        lines[i].Yprim=dic_lines[lines[i].name]

# %%

loadfile="Loads_ckt5.dss"
loads=readLoads(md,sys,loadfile)
# %%
