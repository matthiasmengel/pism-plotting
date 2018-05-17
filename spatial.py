

def get_spatial_variable(fname,varname):

    try:
        ncf = nc.Dataset(fname,"r")
    except IOError as error:
        print fname, "not found."
        raise error

    var = ncf.variables[varname][:]
    ncf.close()

    return np.squeeze(var)



def imshow_variable(variable, **kwargs):

    plt.imshow(variable, origin="lower", interpolation="nearest",
               **kwargs)
    plt.colorbar()

def contour_variable(fname,varname,**kwargs):

    ncfname = os.path.join(ensemble_base_path,fname)
    try:
        ncf = nc.Dataset(ncfname,"r")
    except IOError as error:
        print ncfname, "not found."
        raise error
    plt.contour(np.squeeze(ncf.variables[varname][0:150,0:150]),origin="lower",
               interpolation="nearest",**kwargs)

