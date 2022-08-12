#%%
from objects import *
from lerArquivos import *

#%%
md="Sys"

sys="ckt5"

linefile="Lines_ckt5.dss"

file=open(md+'/'+sys+'/'+linefile,'r')
# %%

data=file.read()
data=data.upper()
# %%

lines=[]
i=0
while (data.find("NEW LINE") != -1):
    #find the beginin of the information about one line
    bgline=data.find("NEW LINE")
    endline=data[bgline+1:].find("NEW LINE")+bgline+1

    if (bgline==endline):
        endline=len(data)

    thisline=data[bgline:endline]

    line=lineODSS()
    # find the line name
    # print(thisline)

    line.name=getfield_obg('name',thisline)
    line.bus1=getfield_obg('bus1',thisline)
    line.bus2=getfield_obg('bus2',thisline)
    line.length=float(getfield_obg('length',thisline))
    line.units=getfield_obg('units',thisline).lower()
    line.phases=int(getfield_opt('phases',thisline))
    line.enabled=getfield_opt('enabled',thisline)
    line.geometryflag= 'GEOMETRY' in thisline
    line.linecodeflag= 'LINECODE' in thisline
    line.switch=getfield_opt('switch',thisline)
    if line.geometryflag == True:
        line.geometry=getfield_opt('GEOMETRY',thisline)
    elif line.linecodeflag ==True:
        line.geometry=getfield_opt('LINECODE',thisline)

    data=data[endline:]
    i=i+1
    lines.append(line)
# %%
for line in lines:
    if line.switch=="Y":
        print(line.name)