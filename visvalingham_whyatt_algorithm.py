'''
Produce a Map Showing the Effects of Line Simplification using the UK Mainland Coastline as a Case Study
'''
'''
4. Create a function that defines distance using Pythagoras theorem 
5. ¬Create a function that defines a triangles area using Heron’s formula
6. Create a function defining the point elimination using Visvalingham Whyatt Algorithm
	7. Create a dictionary and store each point with its effective area
8. Remove one node from the list until desired number of nodes is met and update the effective area for the affected nodes
9. Return a list of nodes and their coordinates
1. Extract the UK row and geometry from the GeoDataFrame
2. Extract the UK mainland geometry from the UK and extract boundary coordinates
3. Define simplification percentage and the equating nodes for the boundary coords
10. Plot.
'''

from geopandas import read_file, GeoSeries
from sys import exit
from math import sqrt
from shapely.geometry import LineString
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import subplots_adjust
import matplotlib.pyplot as plt

#  define distance function
def distance(x1, y1, x2, y2):
    a_squared = (x2 - x1)**2 + (y2 - y1)**2
    a = sqrt(a_squared)
    return a
   
# calculates the area of a triangle using Heron's formula
def get_effective_area(a, b, c):
    side_a = distance(b[0], b[1], c[0], c[1])
    side_b = distance(a[0], a[1], c[0], c[1])
    side_c = distance(a[0], a[1], b[0], b[1])
    s = (side_a + side_b + side_c) / 2
    return sqrt( s* (s-side_a) * (s-side_b) * (s-side_c) )

# simplify a line using point elimination based on effective area
def visvalingham_whyatt(node_list, n_nodes):
    # https://bost.ocks.org/mike/simplify/ 
    
    point_and_areas = []
    
    '''  Create a dictionary for each point and its area '''
    
    for i in range(1, len(node_list)-1):
        area = get_effective_area(node_list[i-1], node_list[i], node_list[i+1]) # get area
        point_and_areas.append({'point': node_list[i], 'area': area}) # add each dictionary item to list
    # add back in the end points 
    point_and_areas.insert(0, {'point': node_list[0], 'area': 0}) # add in the first point at index value 0
    point_and_areas.insert(len(point_and_areas), {'point': node_list[len(node_list)-1], 'area': 0}) # add in the last point at index value length-1
   
    ''' Remove the node for each iteration with the lowest area '''

    node_list_copy = point_and_areas.copy() # copy because we will analyse the original later
    
    while len(node_list_copy) > n_nodes: # remove nodes until desired percentage nodes is achieved
        min_area = float('inf') # establish a variable to store the smallest area
        for node in range(1, len(node_list_copy)-1): # loop through each point in polygon boundary excluding the end points
            node_ea = node_list_copy[node]['area'] # extract the effective area of point
            if node_ea < min_area:
                min_area = node_ea # update the minimum area
                node_to_delete = node # delete point from node_list
        node_list_copy.pop(node_to_delete) # after each loop delete relevant point
        
        ''' Recalculate effective areas for the affected notes after the previous deletion '''
       
        # recalculate area for node to the left of the deleted node
        node_list_copy[node_to_delete-1]['area'] = get_effective_area(node_list_copy[node_to_delete-2]['point'], 
                                                                      node_list_copy[node_to_delete-1]['point'], 
                                                                      node_list_copy[node_to_delete]['point'])
        # recalculate area for node to the right of the deleted node
        if node_to_delete < len(node_list_copy)-1:    
            node_list_copy[node_to_delete]['area'] = get_effective_area(node_list_copy[node_to_delete-1]['point'], 
                                                                        node_list_copy[node_to_delete]['point'], 
                                                                        node_list_copy[node_to_delete+1]['point'])
    # returns every node left in the dictionary                                                        
    # return [ node['point'] for node in node_list_copy ] -> list comprehension, below is explanation.
    out = []
    for node in node_list_copy:
        out.append(node['point'])
    
    return out

''' Defining the Data and Paramters'''

# import the data
world_gdf = read_file(r"Vector Data Projects\world_countries_data\natural-earth\ne_10m_admin_0_countries.shp")
# get the proj string definition for British National Grid (OSGB)
osgb = "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +towgs84=446.448,-125.157,542.06,0.15,0.247,0.842,-20.489 +units=m +no_defs"

# get the UK MultiPolygon and isolate the geometry for the mainland
uk_geoseries_proj = (world_gdf.loc[world_gdf.ISO_A3 == 'GBR']).to_crs(osgb)
uk = uk_geoseries_proj.geometry.iloc[0]

coords_list = [] # initialise a variable for mainland coords
area_size = 0 # initialise a variable for area value

for each_polygon in uk.geoms: # loop through each polygon in the MultiPolygon
    if each_polygon.area > area_size:
        area_size = each_polygon.area # update and store area
        coords_list = list(each_polygon.boundary.coords) # update and store coords

full_nodes = int(len(coords_list)) # print(full_nodes) shows 3707 nodes

# define the simplification percentage 
simp_perc1 = int(input(f"Input the % you want to decrease the complexity by: "))
simp_perc2 = int(input(f"Input a second, different simplification %: "))

# define the necessary nodes needed to achieve simplification level
n_nodes1 = full_nodes * ((100-simp_perc1)/100)
if n_nodes1 < 3: # ensure it has the minimum amount
    n_nodes1 = 3
n_nodes2 = full_nodes * ((100-simp_perc2)/100)
if n_nodes2 < 3: # ensure it has the minimum amount
    n_nodes2 = 3

after_coords1 = visvalingham_whyatt(coords_list, n_nodes1)
after_coords2 = visvalingham_whyatt(coords_list, n_nodes2)

# make a linestring out of the the coordinates
before_line = LineString(coords_list)
print(f'Original Coastline Number of Points: {len(coords_list)}')
print(f'Original Coastline Length: {before_line.length/1000:.2f} km\n')
after_line1 = LineString(after_coords1)
print(f'Simplified Coastline 1 number of points {len(after_coords1)}')
print(f'Simplified Coastline 1 Length: {after_line1.length/1000:.2f} km\n')
after_line2 = LineString(after_coords2)
print(f'Simplified Coastline 2 number of points {len(after_coords2)}')
print(f'Simplified Coastline 2 Length: {after_line2.length/1000:.2f} km\n')

'''  PLOTTING THE MAPS '''

my_fig, my_axs = plt.subplots(1, 3, figsize=(16, 10))
my_fig.suptitle("The Length of the Coastline of Mainland Great Britain")
subplots_adjust(wspace=0) # reduce the gap between the subplots
my_fig.suptitle("The Length of the Coastline of Mainland Great Britain")
my_axs[0].set_title(f" Original: {before_line.length / 1000:.0f}km, {len(coords_list)} nodes.")
my_axs[1].set_title(f" Simplification 1: {after_line1.length / 1000:.0f}km, {len(after_coords1)} nodes.")
my_axs[2].set_title(f" Simplification 2: {after_line2.length / 1000:.0f}km, {len(after_coords2)} nodes.")

# add the original coastline
GeoSeries(before_line, crs=osgb).plot(
    ax=my_axs[0],
    color='blue',
    linewidth = 0.6,
	)

# add the new coastline
GeoSeries(after_line1, crs=osgb).plot(
    ax=my_axs[2],
    color='green',
    linewidth = 0.6,
	)

# add the new coastline
GeoSeries(after_line2, crs=osgb).plot(
    ax=my_axs[1],
    color='red',
    linewidth = 0.6,
	)

# edit individual axis
for my_ax in my_axs:

	# remove axes
	my_ax.axis('off')

	# add north arrow
	x, y, arrow_length = 0.95, 0.99, 0.1
	my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
		arrowprops=dict(facecolor='black', width=5, headwidth=15),
		ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

	# add scalebar
	my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower right"))

plt.show()
