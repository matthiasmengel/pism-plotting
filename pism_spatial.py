import os
import numpy as np
import netCDF4 as nc
import collections
import glob
import matplotlib.pylab as plt
import matplotlib.colors as colors
from matplotlib import cm

def get_spatial_variable(fname,varname):

    try:
        ncf = nc.Dataset(fname,"r")
    except IOError as error:
        print(fname, "not found.")
        raise error

    try:
        var = ncf.variables[varname][:]
    except KeyError as error:
        print("availables variables are", list(ncf.variables.keys()))
        raise error

    ncf.close()

    return np.squeeze(var)


def get_spatial(exp, varname, years=[2000,2100,2200,2300]):

    var = collections.OrderedDict()
    var[1850] = get_spatial_variable(
            os.path.join(exp,"snapshots_1850.000.nc"),varname)

    for y in years:
        try:
            var[y] = get_spatial_variable(
                os.path.join(exp,"extra_"+str(y)+".000.nc"),varname)
        except IOError:
            print(y,"not available.")
            continue

    return var


def imshow_variable(variable, **kwargs):

    variable = np.ma.masked_array(variable,mask=variable==0)
    plt.imshow(variable,#[400:900,200:800],
               origin="lower", #interpolation="nearest",
               **kwargs)
    plt.colorbar(shrink=0.6)


def contour_variable(fname,varname,**kwargs):

    ncfname = os.path.join(ensemble_base_path,fname)
    try:
        ncf = nc.Dataset(ncfname,"r")
    except IOError as error:
        print(ncfname, "not found.")
        raise error
    plt.contour(np.squeeze(ncf.variables[varname][0:150,0:150]),origin="lower",
               interpolation="nearest",**kwargs)


def get_fields_of_set(varname, experiments, ncfile, reffield=None):

    """ get netcdf fields for varname.
    """

    data = collections.OrderedDict()

    for exp in experiments:

        ncf = os.path.join(exp,ncfile)
        try:
            data[exp] = get_spatial_variable(ncf,varname)
        except IOError:
            # print ncf, "not available."
            continue

        if reffield is not None:
            data[exp] = data[exp] - reffield

    return data


def imshow_set(expdata, labelgetter=None, figsize=(10,16), limiter=None, **kwargs):

    plt.figure(figsize=figsize)

    if limiter is None:
        lm = lambda field: field
    else:
        lm = limiter

    axs = [plt.subplot(np.ceil(len(expdata)/2.),2,i+1)
           for i in range(len(expdata))]

    for i,exp in enumerate(expdata):

        if labelgetter is None:
            label = exp
        else:
            label = labelgetter(exp)

        im = axs[i].imshow(lm(expdata[exp]),origin="lower", **kwargs)
        axs[i].set_title(label)
        plt.colorbar(im, ax=axs[i],shrink=0.7)
        axs[i].set_axis_off()

    # plt.tight_layout()


def imshow_vel(field, vmin=0.1, vmax=1000, label="", **kwargs):

    im = plt.imshow(field,
               origin="lower", norm=colors.LogNorm(vmin=vmin, vmax=vmax),
                **kwargs)
    plt.colorbar(im,shrink=0.8, label=label)