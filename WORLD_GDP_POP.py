'''
TASK
Q1: PRODUCE A MAP THAT SHOWS RELATIVE GLOBAL POPULATION DENSITY 
Q2: PRODUCE A MAP THAT SHOWS RELATIVE GLOBAL GDP PER CAPITA
'''
'''
1. Import data and reproject to appropriate crs
2. Calculate GDP per capita and add column to the GeoDataFrame
3. Plot 
'''
''' IMPORTING AND MANIPULATING THE DATA '''

# import libraries
from geopandas import read_file  
import matplotlib.pyplot as plt

# load all of the necessary date
world = read_file(r"Vector Data Projects\world_countries_data\natural-earth\ne_50m_admin_0_countries.shp")
graticule = read_file(r"Vector Data Projects/world_countries_data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file(r"Vector Data Projects\world_countries_data\natural-earth\ne_110m_wgs84_bounding_box.shp")

# define our projection, and then reproject the data being represented
ea_proj = '+proj=eqearth +lon_0=0 +datum=WGS84 +units=m +no_defs'
world = world.to_crs(ea_proj)
graticule = graticule.to_crs(ea_proj)
bbox = bbox.to_crs(ea_proj)

# calculate the population density, /1000000 to convert m^2 to km^2
world['pop_density'] = world.POP_EST / (world.area / 1000000)

# calculate the GDP
world['gdp_pc'] = world.GDP_MD_EST / world.POP_EST

''' PLOTTING THE DATA FOR POPULATION DENSITY '''

# create map figure and axis objects
# figure, axis           r  c  figuresize
my_fig, my_ax = plt.subplots(1, 1, figsize=(15, 8))

my_ax.axis('off')

# add title
my_ax.set_title("Population Density: Equal Earth Coordinate Reference System")

# add a bounding box which will be used as a background for the sea
bbox.plot(
    ax = my_ax, # set the axis to plot it to
    color = 'lightgrey', # set the colour
    linewidth = 0 # set the line width
    )

# plot the countries
world.plot(
    ax = my_ax, # set the axis to plot it to
    column = 'pop_density', # field whose data will
    linewidth = 0.3, # width of lines
    edgecolor = 'Black', # colour of edge lines
    cmap = 'OrRd', # colour ramp that will be used
    scheme = 'quantiles', # classification scheme to set each group for colour ramp
    legend = 'True', # insert a legend
    legend_kwds = {
        'loc': 'lower left', # choose location for legend
        'title': 'Population Density' # legend title
        }
    )

# plot the graticule
graticule.plot(
    ax = my_ax,
    color = 'black',
    linewidth = 0.4,
    )

# save the result
# savefig('./data/outputs/output_1_global_pop_density')
print("POPULATION DENSITY COMPLETED")

''' PLOTTING THE DATA FOR GDP '''

# create map figure and axis objects
# figure, axis             r  c  figuresize
my_fig1, my_ax1 = plt.subplots(1, 1, figsize=(15, 8))

my_ax1.axis('off')

# add title
my_ax1.set_title("GDP PER CAPITA: Equal Earth Coordinate Reference System")

# add a bounding box which will be used as a background for the sea
bbox.plot(
    ax = my_ax1, # set the axis to plot it to
    color = 'lightgrey', # set the colour
    linewidth = 0 # set the line width
    )

# plot the countries
world.plot(
    ax = my_ax1, # set the axis to plot it to
    column = 'gdp_pc', # field whose data will
    linewidth = 0.3, # width of lines
    edgecolor = 'Black', # colour of edge lines
    cmap = 'OrRd', # colour ramp that will be used
    scheme = 'quantiles', # classification scheme to set each group for colour ramp
    legend = 'True', # insert a legend
    legend_kwds = {
        'loc': 'lower left', # choose location for legend
        'title': 'GDP' # legend title
        }
    )

# plot the graticule
graticule.plot(
    ax = my_ax1,
    color = 'black',
    edgecolor = 'black',
    linewidth = 0.4,
    )

# savefig('./data/outputs/output_1_gdp_pc')
print("GDP PER CAPITA COMPLETED")

plt.show()
   

