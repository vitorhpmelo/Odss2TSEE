from objects import *


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
    
    file.close()      
    return lines        

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



