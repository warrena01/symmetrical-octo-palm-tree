''' 
Produce a Map Showing the Closest Water Point for Each Popoulation Point in the Gulu District
'''
'''
7. Define how to calculate the distance between two points
1. Create a spatial index and fill with the well spatial data
2. Use Spatial Index to find the wells whose bounds are in the Gulu District
3. Use possible matches to define a list of wells whose geometries are 100% in the Gulu District
4. Create new spatial index filled with only the wells in the Gulu District
5. Loop through the new spatial index
	6. Find the nearest well and extract the data 	
	8. Calculate the distance between the wells and store value in list
9. Add the list of distances to the house GeoDataFrame
10. Plot
'''

from geopandas import read_file
from rtree.index import Index
from math import sqrt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import title
import matplotlib.pyplot as plt

# define distance function
def distance(x1, y1, x2, y2):
    a_squared = (x2 - x1)**2 + (y2 - y1)**2
    a = sqrt(a_squared)
    return a

# import the data
pop_points = read_file(r"Vector Data Projects\world_countries_data\gulu\pop_points.shp") #EPSG 21096
water_points = read_file(r"Vector Data Projects\world_countries_data\gulu\water_points.shp").to_crs(pop_points.crs) #EPSG 4326
gulu_district = read_file(r"Vector Data Projects\world_countries_data\gulu\district.shp").to_crs(pop_points.crs) #EPSG 21096

''' DEFINE THE WATER POINTS IN THE GULU DISTRICT '''

# initialise an instance of an rtree index object
my_spatial_index = Index()
# loop through each row in the wells dataset and load into the spatial index
for id, well_geometry in water_points.iterrows():
    my_spatial_index.insert(id, well_geometry.geometry.bounds)
    
# get the only polygon from the gulu district object
gulu_district_polygon = gulu_district.geometry.iloc[0]

# get matches for water points in gulu district using optimal speed
possible_matches_id = list(my_spatial_index.intersection(gulu_district_polygon.bounds)) # returns list of index numbers
possible_matches = water_points.iloc[possible_matches_id] # returns list of rows
precise_matches = possible_matches.loc[possible_matches.within(gulu_district_polygon)] #.loc is like sql where x = y

''' FIND THE NEAREST WATER POINT TO EACH POPULATION POINT '''

# overwrite the original spatial index with precise wells in Guru District 
my_spatial_index = Index()
for id, wells in precise_matches.iterrows():
    my_spatial_index.insert(id, wells.geometry.bounds)
    
# create an array to store the distances 
distances = []

# loop through to store the distance to nearest well for each house 
for id, house in pop_points.iterrows():
    nearest_well_calc = my_spatial_index.nearest(house.geometry.bounds, 1) # calculate nearest 1 point
    nearest_well_list = list(nearest_well_calc) # convert to list (to be able to extract data)
    nearest_well_index = nearest_well_list[0] # extract value (which is the ID as we used the spatial index)
    # extract the row using the id we found in nearest_well_index
    nearest_well = water_points.iloc[nearest_well_index]
    
    # calculate distance to nearest well using the defined function
    distance_to_nearest_well = distance((house.geometry.bounds[0]), (house.geometry.bounds[1]), (nearest_well.geometry.bounds[0]), (nearest_well.geometry.bounds[1]))
    # add to our distances array
    distances.append(distance_to_nearest_well)
    
# add the distances list to the dataset
pop_points['nearest_well'] = distances

# explore some of the data
mean = sum(distances) / len(distances)
print(f"Minimum distance to water in Gulu District is {round(min(distances))}m.")
print(f"Mean distance to water in Gulu District is {mean}m.")
print(f"Maximum distance to water in Gulu District is {round(max(distances))}m.")

''' CREATE A MAP '''

fig, my_axis = plt.subplots(1, 1, figsize=(16, 10)) # create object
my_axis.axis('off') # take off axis labels
title('Distance to Nearest Well, Gulu District, Uganda') # add a title
my_axis.add_artist(ScaleBar(dx=1, units="m", location="lower left", length_fraction=0.25)) # add scale bar
# add north arrow
x, y, arrow_length = 0.98, 0.99, 0.1
my_axis.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
	arrowprops=dict(facecolor='black', width=5, headwidth=15),
	ha='center', va='center', fontsize=20, xycoords=my_axis.transAxes)

# add the district shapefile
gulu_district.plot(
    ax = my_axis,
    color = 'lightgrey',
    linewidth = 1,
    edgecolor = 'white'
    )

# plot the points using color grading 
pop_points.plot(
    ax = my_axis,
    column = 'nearest_well',
    linewidth = 0,
    markersize = 1,
    cmap = 'RdYlBu_r',
    scheme = 'quantiles',
    legend = 'True',
    legend_kwds = {
        'loc': 'lower right',
        'title': 'Distance to Nearest Well',
        'fontsize': '7'
        }
    )

plt.show()