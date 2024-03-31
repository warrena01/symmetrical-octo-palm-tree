''' 
Write an Algotithm that Calculates the Worlds Shortest Border and then Produce a Map to Show These 
'''
'''
3. Write a function to define bordering countries utilizing a spatial index
7. Write a function to define the geometry and border length of two countries
1. Create a spatial index for the countries and populate it
2. Loop through each country
	4. Find bordering countries using the spatial index
	5. Loop through the list of bordering countries (without duplicates)
		6. Find the border geometry and length
		7. Update variables to store if it’s the smallest length
8. Plot
'''

from time import time
start_time = time()

from rtree.index import Index
from geopandas import read_file, GeoSeries
from pyproj import Geod
from matplotlib.pyplot import Line2D
from matplotlib.patches import Patch
from matplotlib_scalebar.scalebar import ScaleBar
from threading import Thread
import  matplotlib.pyplot as plt

''' CALCULATING THE SHORTEST BORDER '''

# use a spatial index to find a list of countries whos bounding boxes intersect (possible countries)
def find_bordering_countries(variable, spatial_index, dataset):
    
    # spatial index return index numbers and so make a list of intersecting bounds
    possible_matches_id = list(spatial_index.intersection(variable.geometry.bounds))
    # use index to locate which row in the geodataframe these refer to
    possible_matches = dataset.iloc[possible_matches_id]
    # remove possible matches that intersect bounds but not polygons
    precise_matches = possible_matches.loc[(possible_matches.geometry).intersects(variable.geometry)]
    # returns geodataframe of possible_matches
    return precise_matches

def get_border_length(shape1, shape2):
    
    # find the border geometry
    border_geometry = (shape1.geometry).intersection(shape2.geometry) 
    border_length = 0 # intialise a variable for border_length
    g = Geod(ellps='WGS84') # set geodey
    
    # calculate border length for multilinestring borders
    if ((border_geometry.geom_type) == 'MultiLineString'):
        for segment in border_geometry.geoms:
            distance = g.inv(segment.coords[0][0], segment.coords[0][1], segment.coords[1][0], segment.coords[1][1])[2] 
            border_length += distance
    # calculate border length for linestring borders
    elif ((border_geometry.geom_type) == 'LineString'): 
        distance = g.inv(border_geometry.coords[0][0], border_geometry.coords[0][1], border_geometry.coords[1][0], border_geometry.coords[1][1])[2] 
        border_length += distance
        
    # ignore points as they cannot be crossed working (infinitely precise concept)
    else: border_length = float('inf') # make the algorithm ignore 'point' intersections
    
    return border_geometry, border_length

# import the dataset 
world = read_file(r".\Vector Data Projects\world_countries_data\natural-earth\ne_10m_admin_0_countries.shp")

# initialise variables
shortest_border_length = float('inf')
shortest_border_geometry = ()
countries = ()

# create a spatial Index
my_spatial_index = Index()
for id, country in world.iterrows():
    my_spatial_index.insert(id, country.geometry.bounds) # fill the spatial index with our dataframe

# loop through each country in the dataframe
for c_id, country in world.iterrows():
    t1 = Thread(target=get_border_length)
    t1.start()
    # find countries which it shares a border with
    bordering_countries = find_bordering_countries(country, my_spatial_index, world)
    # loop through each country of the matches
    for b_id, border_country in bordering_countries.iterrows():
        # use an if statement to ensure each border is only assessed once 
        if c_id < b_id:
            # calculate the border length
            border_geometry, border_length = get_border_length(country, border_country)
            # if the border length is less than the border_length
            if border_length < shortest_border_length:
             # store the border length 
                shortest_border_length = border_length
                # store the border geometry 
                shortest_border_geometry = border_geometry
                # store the countries                 
                countries = world.loc[(c_id == world.index)], world.loc[(b_id == world.index)]
                
print(f'The shortest border in the world is {shortest_border_length:.2f}m long')

''' PLOTTING THE MAP '''

# create map axis object
my_fig, my_ax = plt.subplots(1, 1, figsize=(16, 10))
my_ax.axis('off')
my_ax.set_title(f'The shortest border in the world is {shortest_border_length:.2f}m long')
# add legend
my_ax.legend(handles=[
        Patch(facecolor='green', edgecolor='#4daf4a', label=countries[0].iloc[0].NAME),
        Patch(facecolor='orange', edgecolor='#ff7f00', label=countries[1].iloc[0].NAME),
        Line2D([0], [0], color='#984ea3',  lw=2, label='Border')
        ], 
        loc='lower left')
# add north arrow
x, y, arrow_length = 0.98, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
arrowprops=dict(facecolor='black', width=5, headwidth=15),
ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)
# add scalebar
my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower right", length_fraction=0.25))

# project border
proj = '+proj=eqearth +lon_0=0 +datum=WGS84 +units=m +no_defs'
shortest_border_geometry = GeoSeries(shortest_border_geometry, crs=world.crs).to_crs(proj)

# set bounds to give some context
buffer = 50
my_ax.set_xlim([shortest_border_geometry.iloc[0].bounds[0] - buffer, shortest_border_geometry.iloc[0].bounds[2] + buffer])
my_ax.set_ylim([shortest_border_geometry.iloc[0].bounds[1] - buffer, shortest_border_geometry.iloc[0].bounds[3] + buffer])

countries[0].to_crs(proj).plot(
    ax = my_ax,
    color = 'green'
    )
countries[1].to_crs(proj).plot(
    ax = my_ax,
    color = 'orange'
    )
shortest_border_geometry.plot(
    ax = my_ax,
    color = 'black'
    )

plt.show()

print(f"completed in: {time() - start_time} seconds")
