import cdstoolbox as ct
"""
This program is a modification of "Calculate zonal means". It has been modified to generate monthly zonal means from of one of five variables for the time period between 2017 and 2019. 

Two dropdown menus are generated: the first, "Month", lets the user select which month to generate a zonal mean for. NOTE: the Yearly option is a "Hail Mary" attempt at making a total climatology. Under the months dictionary, the "Yearly" option contains all the months, with the hope that the time averaging code below would work. However, initial testing has not worked out as well as planned, so it doesn't work right now.

The second dropdown menu, "Variable", lets the user select which variable to find the zonal mean of. The options are Temperature, Zonal Wind, Meridional Wind, Vertical Velocity, and Vorticity.

At the end, a netCDF file containing the data in the figure is made available to download and work with independently.

"""


layout = {
    'input_ncols': 2,
    'output_align': 'bottom'
}

variables = {
    'Temperature': 'temperature',
    'Zonal Wind': 'u_component_of_wind',
    'Meridional Wind': 'v_component_of_wind',
    'Vertical Velocity': 'vertical_velocity',
    'Vorticity': 'vorticity',
}

months = {
    'Yearly': ['01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
           ],
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12',
}


@ct.application(title='Calculate zonal means', layout=layout)
@ct.input.dropdown('month', label='Month', help='Choose a month', values=months.keys())
@ct.input.dropdown('variable', label='Variable', help='Choose a variable', values=variables.keys())

@ct.output.figure()
@ct.output.dataarray()
def temp(month,variable):
    """
    Application main steps:

    - retrieve a sample dataset (Total Column Ozone)
    - compute its climatology
    - compute its zonal mean (e.g. average over all longitudes)
    - plot the global Total Column Ozone zonal mean climatology in meters
    - compare the Total Column Ozone map over the South Pole area

    """
    temp = ct.catalogue.retrieve(
    'reanalysis-era5-pressure-levels-monthly-means',
    {
        'format': 'grib',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': variables[variable],
        'pressure_level': [
            '1', '2', '3',
            '5', '7', '10',
            '20', '30', '50',
            '70', '100', '125',
            '150', '175', '200',
            '225', '250', '300',
            '350', '400', '450',
            '500', '550', '600',
            '650', '700', '750',
            '775', '800', '825',
            '850', '875', '900',
            '925', '950', '975',
            '1000',
        ],
        'year': [
            #'1979', '1980', '1981',
            #'1982', '1983', '1984',
            #'1985', '1986', '1987',
            #'1988', '1989', '1990',
            #'1991', '1992', '1993',
            #'1994', '1995', '1996',
            #'1997', '1998', '1999',
            #'2000', '2001', '2002',
            #'2003', '2004', '2005',
            #'2006', '2007', '2008',
            #'2009', '2010', '2011',
            #'2012', '2013', '2014',
            #'2015', '2016', '2017',
            '2017','2018', '2019',
        ],
        'month': months[month],
        'time': '00:00',
    },)

    #temp_clima = ct.climate.climatology_mean(temp)
    temp_mean = ct.cube.average(temp, 'lon')
    temp_mean = ct.cube.average(temp_mean,'time')

    figa = ct.cdsplot.pcolormesh(
        temp_mean, cmap='coolwarm', x='lat', y='plev',
        title=variable+' '+month+' Climatology Mean (2017-2019)'
    )


    return figa,temp_mean
