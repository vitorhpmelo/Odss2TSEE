import objects


def readLines(md,sd):
    file=open(md+sd,'r')
    

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


