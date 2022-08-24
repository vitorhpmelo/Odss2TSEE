# -*- coding: utf-8 -*-
"""
Created on Mon Aug 8 2022

@author: vitorhpmelo

Objetos para Leitura dos arquivos do OpenDSS
"""

from cgitb import enable
import numpy as np



class wire:
    
    Nconds=-1
    def __init__(self):
        pass


class lineGeometry:
    #class to read Linegeometry
    Nconds=3 #number of conductors (default 3)
    Nphases=3 #number of phases (default 3)
    Cond=1 # Set this to number of the conductor you wish to define. Default is 1.
    Wire= "NA" #Type of conductor, read in the structure Wire
    x=0 # coordinate
    H=-1 #hight of the conductor above the earth
    Units="km" #Units for x and h: {mi|kft|km|m|Ft|in|cm } Initial default is "km"
    Normamps = 0 #Normal ampacity, amperes for the line. Defaults to first conductor if not specified
    Emergamps= 0 #Emergency ampacity, amperes. Defaults to first conductor if not specified.
    Reduce ="y" #{y | n} Default = no. Reduce from Nconds to Nphases by Kron Reduction.Reduce out neutral conductors assumed to be grounded.
    Spacing= 0 #Reference to a LineSpacing object for use in a line constants calculation
    Wires=[] #list of WireData names for use in a line constants calculation
    CNcable="xxx" #Code from CNData
    TSCable="xxx" #Code from TSData
    CNCables=[] #List of CNData names for cable parameter calculation
    TSCables=[] #List of TSData names for cable parameter calculation.
    Seasons=0 #Defines the number of ratings to be defined for the wire
    Ratings=[] #ratings to be used when the seasonal ratings flag is True
    Like="NA" #Make like another object
    def __init__(self):
        pass

class lineODSS:
   name="none" 
   phases="3"
   bus1="xx"
   bus2="xx"
   phbus1=''
   flagTNbus1=0
   phbus2=''
   flagTNbus2=0
   length=0
   phase="" 
   enabled=True
   geometryflag=False
   linecodeflag=False
   linecode={}
   geometry={}
   units="km"
   switch="N"
   Yprim=[]
   def __init__(self) -> None:
       pass

class LoadOdss:
    name="xx"
    phases=3
    bus1="xx"
    phbus1='xx'
    flagTNbus1=0
    kv=-9999.
    kw=-9999.
    pf=0.95
    con="Yg"

class TrafoOdss:
    name="xx"
    phases=3
    windings=2
    bus1="xxx"
    bus2="xxx"
    phbus1=''
    kvasbus1=''
    flagTNbus1=0
    phbus2=''
    kvasbus2=''
    flagTNbus2=0
    Connbus1="YG"
    Connbus2="YG"    
    kvbus1="xxx"
    kvbus2="xxx"
    Tapbus1=1
    Tapbus2=1
    rneubus1=0
    rneubus2=0
    XHL=0.00
    Loadloss=0.0
    Noloadloss=0.0
    imag=0.0
    