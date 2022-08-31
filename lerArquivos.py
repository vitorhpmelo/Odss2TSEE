
from objects import *
import re 

def readYprim(md,sys,yprimfile):
    """
    Function to read the Yprim file generated for the power delivery elements generated with the OpenDSS
    
    @param: md: string with the folder with the information about the systems
    @param: sys: string with the name of the System which the files will be converted
    @param: yprimfile: string with the name of the file with the information of the Yprim matrix
    @return: dic_lines: dictionary with the information of the primitive matricies
    """


    file=open(md+'/'+sys+'/'+yprimfile,'r')

    data=file.readlines()
    flagheader=1
    flagfirstline=1
    dic_lines={}
    for line in data:
        line=line.upper()
        if flagheader==1:
            name=''    
            for ch in line[line.find(".")+1:]:
                if ch == '\n' or ch ==  '\t' or ch == " ":
                    break
                name+=ch
            flagheader=0
        elif flagfirstline ==1:
            line=line.split(',')
            dim=int((len(line))/2)
            Yprim=np.zeros((dim,dim),dtype='complex')
            i=0
            for j in range(0,2*dim,2):
                Yprim[i][j//2]=complex(float(line[j]),float(line[j+1]))
            flagfirstline=0
        else: 
            line=line.split(',')
            i=i+1
            if i < dim-1:
                for j in range(0,2*dim,2):
                    Yprim[i][j//2]=complex(float(line[j]),float(line[j+1]))
            else:
                for j in range(0,2*dim,2):
                    Yprim[i][j//2]=complex(float(line[j]),float(line[j+1]))
                flagfirstline=1
                flagheader=1
            dic_lines[name]= Yprim
    return dic_lines   


def readLines(md,sys,linefile):
    """
    Function to read the Odss file with the information about the lines of the system to be converted
    @param: md: string with the folder with the information about the systems
    @param: sys: string with the name of the System which the files will be converted
    @param: linefile: string with the name of the file with the information of the Lines
    @return lines: list of objects with the information of the lines
    """
    
    file=open(md+'/'+sys+'/'+linefile,'r')
    data=file.read()
    data=data.upper()

    buses={}

    lines=[]
    i=0
    while (data.find("NEW LINE.") != -1):
        #find the beginin of the information about one line
        bgline=data.find("NEW LINE.")
        endline=data[bgline+1:].find("NEW LINE.")+bgline+1

        if (bgline==endline):
            endline=len(data)

        thisline=data[bgline:endline]
        line=lineODSS()
        # find the line name

        line.name=getfield_obg('name',thisline)
        [line.bus1,line.phbus1,line.flagTNbus1]=definephasesbus(getfield_obg('bus1',thisline))
        [line.bus2,line.phbus2,line.flagTNbus2]=definephasesbus(getfield_obg('bus2',thisline))
        
        if line.bus1 in buses.keys():
            buses[line.bus1]="".join(dict.fromkeys(buses[line.bus1]+line.phbus1))
        else:
            buses[line.bus1]=line.phbus1
        
        if line.bus2 in buses.keys():
            buses[line.bus2]="".join(dict.fromkeys(buses[line.bus2]+line.phbus2))
        else:
            buses[line.bus2]=line.phbus2

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

    file.close()      
    return lines,buses        


def readLoads(md,sys,loadfile):
    """
    Function to read the Odss file with the information about the lines of the system to be converted
    @param: md: string with the folder with the information about the systems
    @param: sys: string with the name of the System which the files will be converted
    @param: linefile: string with the name of the file with the information of the Lines
    @return lines: list of objects with the information of the lines
    """
    
    file=open(md+'/'+sys+'/'+loadfile,'r')
    data=file.read()
    data=data.upper()

    loads=[]
    i=0
    while (data.find("NEW LOAD.") != -1):
        #find the beginin of the information about one line
        bgline=data.find("NEW LOAD.")
        endline=data[bgline+1:].find("NEW LOAD.")+bgline+1

        if (bgline==endline):
            endline=len(data)

        thisline=data[bgline:endline]
        load=LoadOdss()
        # find the line name

        load.name=getfield_obg('name',thisline)
        [load.phbus1,load.bus1,load.flagTNbus1]=definephasesbus(getfield_obg('bus1',thisline))
        load.phases=int(getfield_opt('phases',thisline))
        load.kv=float(getfield_opt('kv',thisline))
        load.kw=float(getfield_opt('kw',thisline))
        load.pf=float(getfield_opt('pf',thisline))

        data=data[endline:]
        i=i+1
        loads.append(load)
    
    file.close()      
    return loads   



#reads obrigatory files 
def getfield_obg(field,linedata):
    """Function that reads obrigatory fields in the Odss file
    @param field: string with the name of the field to be read
    @param linedata: string with the data from the actual line
    """
    name=''
    if (field=='name'):
        field="."
    else:
        field=field.upper()+"="
    for ch in linedata[linedata.find(field)+len(field):]:
        if (ch ==' ' or ch=='\t' or ch=='\n'):
            break 
        else:
            name+=ch
    return name


def getfield_2(field,linedata):
    """Function that reads obrigatory fields in the Odss file
    @param field: string with the name of the field to be read
    @param linedata: string with the data from the actual line
    """

    field=field.upper()+"="
    beg=linedata.find(field)+len(field)
    end=linedata[beg:].find(")")
    linedata=linedata[beg:beg+end]
    if linedata.find(",")!=-1:
        linedata=linedata.split(",")
    else:
        linedata=linedata.split(" ")    

    field1=(linedata[0].replace(")","")).replace("(","").strip(' ')
    field2=(linedata[1].replace(")","")).replace("(","").strip(' ')
    return [field1,field2]

def getfield_opt(field,linedata):
    """Function that reads optional fields in the Odss file
    @param field: string with the name of the field to be read
    @param linedata: string with the data from the actual line
    """
    name=''
    if (field=='name'):
        field="."
    else:
        field=field.upper()+"="

    if(linedata.find(field)==-1):
        return -1
    for ch in linedata[linedata.find(field)+len(field):]:
        if (ch ==' ' or ch=='\t' or ch=='\n'):
            break 
        else:
            name+=ch
    return name



def definephasesbus(bus):
    """
    Funtion to extract the information into the bus name string
    @param: bus: string with the bus information like in opendss
    @return: phases: string with the pahses code
    @return: flagTN: binary number to check if ground and neutral are present (0 none; 1 Neutral; 2 ground ; both)
    """
    i=bus.find('.')
    flagTN=0b000
    phases=''
    if i==-1:
       name=bus
       phases='ABC'
       return name,phases,flagTN
    else:
       name=bus[0:i]
       ph=bus[i:]
       
       phases += 'A' if '1' in ph else '' # se tem '1' a fase a está presente
       phases += 'B' if '2' in ph else '' # se tem '2' a fase b está presente
       phases += 'C' if '3' in ph else '' # se tem '3 a fase c está presente
       flagTN+=0b01 if '4' in ph else flagTN # se tem '4' possui neutro
       flagTN+=0b10 if '0' in ph else flagTN # se tem '0' possui neutro aterrado
    return name,phases,flagTN    


def defineconn(conn,flagTN):
    """
    Funtion to extract the connectio information
    @param: conn: string with the conn information like in opendss
    @param: flagTN: bool to tell if the bus is grounded
    @return: res: the connection normalized string (Yg,D,Y)
    """
    res=''
    if conn == -1:
        res='Yg'
    elif conn.upper()=='DELTA' or conn.upper()=='D':
        res='D'
    else:
        res="Y"
        if (flagTN==0):
            res=res+'g'
    return res     

def readTrafo(md,sys,trafofiles):
    """
    Function to read the Odss file with the information about the lines of the system to be converted
    @param: md: string with the folder with the information about the systems
    @param: sys: string with the name of the System which the files will be converted
    @param: linefile: string with the name of the file with the information of the Lines
    @return lines: list of objects with the information of the lines
    """
    
    file=open(md+'/'+sys+'/'+trafofiles,'r')
    data=file.read()
    data=data.upper()
    buses={}
    trafos=[]
    while (data.find("NEW TRANSFORMER.") != -1):
        #find the beginin of the information about one line
        bgline=data.find("NEW TRANSFORMER.")
        endline=data[bgline+1:].find("NEW")+bgline+1

        if (bgline==endline):
            endline=len(data)

        thisline=data[bgline:endline]
        trafo=TrafoOdss()
        # find the line name
        
        trafo.name = getfield_obg('name',thisline)
        trafo.phases = int(getfield_obg('phases',thisline))

        
        if  (thisline.find('BUSES')!=-1):
            [bus1info,bus2info]=getfield_2('BUSES',thisline)
            [trafo.bus1,trafo.phbus1,trafo.flagTNbus1]=definephasesbus(bus1info)
            [trafo.bus2,trafo.phbus2,trafo.flagTNbus2]=definephasesbus(bus2info)
            if trafo.bus1 in buses.keys():
                buses[trafo.bus1]="".join(dict.fromkeys(buses[trafo.bus1]+trafo.phbus1))
            else:
                buses[trafo.bus1]=trafo.phbus1
            if trafo.bus2 in buses.keys():
                buses[trafo.bus2]="".join(dict.fromkeys(buses[trafo.bus2]+trafo.phbus2))
            else:
                buses[trafo.bus2]=trafo.phbus2
        else:
            [trafo.bus1,trafo.phbus1,trafo.flagTNbus1]=definephasesbus(getfield_obg('bus',thisline))
            [trafo.bus2,trafo.phbus2,trafo.flagTNbus2]=definephasesbus(getfield_obg('bus',thisline[thisline.find('BUS')+1:]))
            if trafo.bus1 in buses.keys():
                buses[trafo.bus1]="".join(dict.fromkeys(buses[trafo.bus1]+trafo.phbus1))
            else:
                buses[trafo.bus1]=trafo.phbus1
            if trafo.bus2 in buses.keys():
                buses[trafo.bus2]="".join(dict.fromkeys(buses[trafo.bus2]+trafo.phbus2))
            else:
                buses[trafo.bus2]=trafo.phbus2
        if (thisline.find('KVS')!=-1):
            [trafo.kvbus1,trafo.kvbus2]=getfield_2('kvs',thisline)
        else:
            trafo.kvbus1=getfield_opt('kv',thisline)
            trafo.kvbus2=getfield_opt('kv',thisline[thisline.find('KV')+1:])
        if (thisline.find('CONNS')!=-1):
            Connbus1,Connbus2=getfield_2('conns',thisline)
            trafo.Connbus1=defineconn(Connbus1,trafo.flagTNbus1)
            trafo.Connbus2=defineconn(Connbus2,trafo.flagTNbus1)
        else:
            trafo.Connbus1=defineconn(getfield_opt('conn',thisline),trafo.flagTNbus1)
            trafo.Connbus2=defineconn(getfield_opt('conn',thisline[thisline.find('CONN')+1:]),trafo.flagTNbus1)
        if (thisline.find('KVAS')!=-1):
            [trafo.kvasbus1,trafo.kvasbus2]=getfield_2('kvas',thisline)
        else:
            trafo.kvasbus1=getfield_opt('kva',thisline)
            trafo.kvasbus2=getfield_opt('kva',thisline[thisline.find('KVA')+1:])
        if (thisline.find('R=')!=-1):
            [Rwdg1,Rwdg2,Rwdg]=getRwdg(thisline)
            trafo.r1=Rwdg1
            trafo.r2=Rwdg2
            trafo.r=Rwdg
        if (thisline.find('XHL=')!=-1):
            trafo.XHL=getXHL(thisline)
        trafo.imag=float(getfield_opt('imag',thisline))
        trafo.Loadloss=float(getfield_opt('loadloss',thisline))
        trafo.Noloadloss=float(getfield_opt('noloadloss',thisline))
        data=data[endline:]
        trafos.append(trafo)
    
    file.close()      
    return trafos,buses    


def getXHL(field):

    beg=0
    beg=field[beg:].find("XHL=")
    endr=field[beg+4:].find('=') + beg

    if endr < beg:
        endr=-1
    if field[beg:endr].find(')') != -1:
        if endr==-1:
            aux=field[beg:]
        else:
            aux=field[beg:endr]    
        aux=aux[aux.find('('):aux.find(')')+1]
        aux=aux.replace("SQR","**2")
        aux=re.sub(r'(\d) (\d)',r'\1*\2',aux)
        aux=aux.replace(" ",'')
        aux=aux.replace("/*","/")
        aux=aux.replace("*)",")")
        value=eval(aux)
    else:
        if endr==-1:
            value=field[beg:]
        else:
            value=field[beg:endr]    
        
        value=re.sub('[^0-9.]','', value)

    return float(value)

def getRwdg(field):
    nRs=0
    Rwdg1=-1
    Rwdg2=-1 
    Rwdg=-1
    beg=0
    endr=0
    while (field[beg:].find("R=")!=-1):
        beg=beg+field[beg:].find("R=")
        nRs=nRs+1
        nWDG1=field[:beg].find("WDG=1")
        nWDG2=field[:beg].find("WDG=2")
        endr=field[beg+2:].find('=') + beg
        if endr < beg:
            endr=-1
        if nWDG1>nWDG2:
        ## the data is from wdg1
            if field[beg:endr].find(')') != -1:
                if endr==-1:
                    aux=field[beg:]
                else:
                    aux=field[beg:endr]    
                aux=aux[aux.find('('):aux.find(')')+1]
                aux=aux.replace("SQR","**2")
                aux=re.sub(r'(\d) (\d)',r'\1*\2',aux)
                aux=aux.replace(" ",'')
                aux=aux.replace("/*","/")
                aux=aux.replace("*)",")")
                value=eval(aux)
            else:
                value=field[beg:endr]
                value=re.sub('[^0-9.]','', value)
            Rwdg1=float(value)
        elif nWDG1<nWDG2:
            if field[beg:endr].find(')') != -1:
                if endr==-1:
                    aux=field[beg:]
                else:
                    aux=field[beg:endr]    
                aux=aux[aux.find('('):aux.find(')')+1]
                aux=aux.replace("SQR","**2")
                aux=re.sub(r'(\d) (\d)',r'\1*\2',aux)
                aux=aux.replace(" ",'')
                aux=aux.replace("/*","/")
                aux=aux.replace("*)",")")
                value=eval(aux)
            else:
                value=field[beg:endr].find(')')
                value=re.sub('[^0-9.]','', value)
            Rwdg2=float(value)
        else:
            if field[beg:endr].find(')') != -1:
                if endr==-1:
                    aux=field[beg:]
                else:
                    aux=field[beg:endr]   
                aux=aux[aux.find('('):aux.find(')')+1]
                aux=aux.replace("SQR","**2")
                aux=re.sub(r'(\d) (\d)',r'\1*\2',aux)
                aux=aux.replace(" ",'')
                aux=aux.replace("/*","/")
                aux=aux.replace("*)",")")
                value=eval(aux)
                value=eval(aux)
            else:
                value=field[beg:endr]
                value=re.sub('[^0-9.]','', value)
            Rwdg=float(value)
        beg=endr    
    return [Rwdg1,Rwdg2,Rwdg]