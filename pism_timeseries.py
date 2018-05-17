
import os
import netCDF4 as nc


def get_timeseries_data(datapath, ts_variables = ["slvol","ice_area_glacierized_floating",
                                                  "ice_area_glacierized_grounded",
                                                 "basal_mass_flux_floating"
                                                 ],
                        ts_file_name="timeseries.nc"):

    """ get time series variables ts_variables from PISM timeseries
    file in datapath. """

    try:
        ncf = nc.Dataset(os.path.join(datapath,ts_file_name),"r")
    except IOError as error:
        print datapath.split("/")[-1], "has no timeseries file, skip"
        print os.path.join(datapath,ts_file_name)
        raise error
    try:
        nct = ncf.variables["time"]
    except KeyError as error:
        print os.path.join(datapath,ts_file_name), "contains no data, skip."
        raise error

    ts_data = {}

    for var in ts_variables:
        ts_data[var] = ncf.variables[var][:]
    ts_data = da.Dataset(ts_data)

    datetm = nc.num2date(nct[:],units = nct.units,calendar = nct.calendar)
    # takes long for long timeseries
    years = [d.year for d in datetm]
    ts_data.set_axis(years)
    ts_data.rename_axes({"x0":"time"})

    return ts_data


def get_last_common_time(ts_data):

    lasttm = []
    for tsd in ts_data:
        lasttm.append(ts_data[tsd].time[-1])
    lasttm = np.array(lasttm)

    last_common_time = lasttm.min()
    longest_run_time = lasttm.max()

    name_of_shortest_run = ts_data.keys()[
        np.where(lasttm == last_common_time)[0][0]]

    name_of_longest_run = ts_data.keys()[
        np.where(lasttm == longest_run_time)[0][0]]

    print "longest run is", name_of_longest_run
    print "shortest run is", name_of_shortest_run

    return last_common_time, longest_run_time


def get_several_timeseries_data(datapath,ts_variables = ["slvol","ice_area_glacierized_floating",
                                                         "ice_area_glacierized_grounded",],
                                ts_file_pattern="timeseries_*nc",
                                latest_ts_file="timeseries.nc"):

    """ for restarted runs: concatenate datasets from several files."""

    # the standard file name if not restarted
    latest_ts_file = os.path.join(datapath,latest_ts_file)
    restarted_ts_files = sorted(glob.glob(os.path.join(datapath,ts_file_pattern)))

    ts_data_per_file = []
    for ts_file in restarted_ts_files+[latest_ts_file]:
#         print ts_file
        try:
            ts_data_per_file.append(get_timeseries_data(
                datapath,ts_variables,ts_file_name=ts_file.split("/")[-1]))
        except KeyError:
            pass

    concatenated_ts = da.concatenate_ds(ts_data_per_file, axis='time', align=True)

    conts = {}
    for k in concatenated_ts.keys():
        conts[k] = concatenated_ts[k][np.unique(concatenated_ts.time)]

    return da.Dataset(conts)
