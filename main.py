#%%
from objects import *
from lerArquivos import *
import numpy as np

md="Sys"

sys="ckt5"

linefile="Lines_ckt5.dss"


lines=readLines(md,sys,linefile)

yprimfile="ckt5_EXP_YPRIM.CSV"

dic_lines=readYprim(md,sys,yprimfile)


# %%

for i in range(len(lines)):
    if lines[i].name in dic_lines.keys():
        lines[i].Yprim=dic_lines[lines[i].name]

# %%
