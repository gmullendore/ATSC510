"""
This code is a modification of the regional plotting code, but modified to plot
snowfall, snow depth, and total precipitation for a selected year/month combination.
This code was also modified to have custom maxima for each variable. These maxima
are set up in the "maxs" dictionary, and the maximum value is retrieved through
indexing the dictionary using the variable name. For example, to grab the maximum
value of snow depth, use "maxs['Snow Depth'].

"""

import cdstoolbox as ct

layout = {
    'output_align': 'bottom'
}

variables = {
    'Snowfall': 'snowfall',
    'Snow Depth': 'snow_depth',
    'Total Precipitation': 'total_precipitation',
    #'Near-Surface Air Temperature': '2m_temperature',
    #'Eastward Near-Surface Wind': '10m_u_component_of_wind',
    #'Northward Near-Surface Wind': '10m_v_component_of_wind',
    #'Sea Level Pressure': 'mean_sea_level_pressure',
    #'Sea Surface Temperature': 'sea_surface_temperature',
}

# years is a dictionary that houses the year options
years = {
    '1996': '1996',
    '1997': '1997',
    '2019': '2019',
}

# months is a dictionary that houses the month options
months = {
    '01': '01',
    '02': '02',
    '03': '03',
    '04': '04',
    '05': '05',
    '06': '06',
    '07': '07',
    '08': '08',
    '09': '09',
    '10': '10',
    '11': '11',
    '12': '12',
}

# maxs is a dictionary that houses the maxima for each variable. The variable names from the 'variables' 
# dictionary are used as keys to access each max value in this dictionary.
maxs = {
    'Snowfall': 100,
    'Snow Depth': 1,
    'Total Precipitation': 100,
}

@ct.application(title='Plot Map', layout=layout)
@ct.input.dropdown('variable', label='Variable', values=variables.keys())
@ct.input.dropdown('year', label='Year', values=years.keys())
@ct.input.dropdown('month', label='Month', values=months.keys())
@ct.output.figure()
def plot_map(variable,year,month):
    """
    Application main steps:

    - set the application layout with output at the bottom
    - select a variable name from a list in the dropdown menu
    - retrieve the selected variable
    - compose a title
    - show the result on a map using the chosen title

    """

    data = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'variable': variables[variable],
            'product_type': 'monthly_averaged_reanalysis',
            'year': years[year],
            'month': months[month],
            'time': '00:00',
        }
    )

    title = '{}'.format(' '.join([text.capitalize() for text in variable.split('_')]))
    title = title+' '+year+' '+month
    fig = ct.cdsplot.geomap(data, extent=[-110,-85,30,50],title=title,pcolormesh_kwargs={'vmin': 0, 'vmax': maxs[variable]})

    return fig
