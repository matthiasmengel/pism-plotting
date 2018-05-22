
def get_spatial_variable(fname,varname):

    try:
        ncf = nc.Dataset(fname,"r")
    except IOError as error:
        print fname, "not found."
        raise error
    
    var = ncf.variables[varname][:]
    ncf.close()
    
    return np.squeeze(var)


def get_spatial(exp, varname, years=[2000,2100,2200,2300]):
    
    var = {}
    var[1850] = get_spatial_variable(
            os.path.join(exp,"snapshots_1850.000.nc"),varname)

    for y in years:
        var[y] = get_spatial_variable(
            os.path.join(exp,"extra_"+str(y)+".000.nc"),varname)
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
        print ncfname, "not found."
        raise error
    plt.contour(np.squeeze(ncf.variables[varname][0:150,0:150]),origin="lower",
               interpolation="nearest",**kwargs)

