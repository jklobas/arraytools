##############################################################################################
# Array Tools for SOCOL-AER and other NETCDF4 files using xarray




import xarray as xr
import os 
#import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import fnmatch

__version__ = "$Revision: 1.1 $"[11:-2]
__version_info__ = tuple([int(s) for s in __version__.split(".")])

class arrays():
    
    def __init__(self):
        self.dsets = {} 
        self.darrays = {}

    def new_dset_pattern(self, string):
        return xr.open_mfdataset([ f for f in os.listdir(os.getcwd()) if fnmatch.fnmatch(f,string) == True], autoclose = True).sortby('time')
    
    def new_dset(self, string):
        return xr.open_mfdataset(string, autoclose = True).sortby('time')
    
    def new_dset_nosort(self, string):
        return xr.open_mfdataset([ f for f in os.listdir(os.getcwd()) if fnmatch.fnmatch(f,string) == True], autoclose = True)
    
    def new_arr(self, dset, var):
        return self.dsets[dset][var]
    
    def new_dif(self,darray1,darray2):
        return np.multiply(np.true_divide(np.subtract(self.darrays[darray1],self.darrays[darray2]),self.darrays[darray2]),100)

    def add_dset_nosort(self, string, var):  #creates a new dataset object, keyword var, for files matching type string (e.g., *chem_m* or *01.nc*)
        self.dsets.update({var: self.new_dset_nosort(string)})
    
    def add_dset_pattern(self, string, var):  #creates a new dataset object, keyword var, for files matching type string (e.g., *chem_m* or *01.nc*)
        self.dsets.update({var: self.new_dset_pattern(string)})
    
    def add_dset(self, string, var):  #creates a new dataset object, keyword var, for files matching type string (e.g., *chem_m* or *01.nc*)
        self.dsets.update({var: self.new_dset(string)})

    def dset_app(self, string, var):
        self.dsets[var].combine_first(self.new_dset(string))
    
    def list_dset_keys(self):
        print(self.dsets.keys())
    
    def add_arr(self,dset, var1):
        self.darrays.update({str(dset)+"_"+str(var1): self.new_arr(dset,var1)})
    
    def diff_app(self,darray1, darray2):
        self.darrays.update({'diff_'+str(darray1)+'_'+str(darray2): self.new_dif(darray1,darray2)})
