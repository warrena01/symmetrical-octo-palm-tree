'''
Produce a Map Showing Visability at Helvellyn
'''
'''
6. Define a line of sight algorithm
	7. Loop through cells between start point and radius edge
		8. Calculate distance in x axis
		9. Make sure it is within dataset/viewers sight range
		10. Calculate Δy/Δx and make sure its bigger than any previous cell to check it is visible
		11. Update output layer
2. Define an algorithm to calculate viewshed
3. Define start point in image space, the radius size in pixels and the observer height
4. Create a new layer to update with 1s 
5. Draw circle to represent line of sight and loop through these
	12. Call on line of sight function
1. Open dataset, read dem band, create output variable and call functions
'''

from rasterio import open as rio_open
from rasterio.plot import show as rio_show
from numpy import zeros, column_stack
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from skimage.draw import line, circle_perimeter
from sys import exit
from math import hypot
from matplotlib_scalebar import scalebar
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.cm import ScalarMappable
from geopandas import GeoSeries
from shapely.geometry import Point
from math import ceil, floor

''' Calculations '''

def line_of_sight(r_start, c_start, start_height, r_end, c_end, object_height, radius_px, raster_band, dem, output_layer):
    '''
    * Defines a function to calculate what can be seen in a straight line
      from a starting point and height
    '''
    max_dydx = -float('inf') # initialise a variable for biggest change in y/x

    # loop through pixels in the line from start to perimeter
    line_numpy_array = line(r_start, c_start, r_end, c_end)
    line_coords = column_stack(line_numpy_array)
    for r_current, c_current in line_coords[1:]: # ignore the first point as we know it can be seen

        # calculate the distance viewed so far, in pixels (2d distance travelled along line)
        dx = hypot(c_start - c_current, r_start - r_current)

        # make sure that the cell is within the dataset and also the radius
        if dx > radius_px:
            break
        if (0 <= r_current < dem.height) == False:
            break
        if (0 <= c_current < dem.width) == False: 
            break
        
        # calculate Δy/Δx with elevation at current place (+ object height) and the start height
        base_dydx = (raster_band[r_current, c_current] - start_height) / dx # work out the difference for the base height
        tip_dydx = (raster_band[r_current, c_current] + object_height - start_height) / dx # work out the difference for top of the object and the start height

        # if visible, update output later.
        if (tip_dydx > max_dydx):
            output_layer[(r_current, c_current)] = 1

		# if the base dydx is bigger than the previous max, update: this is as for other points the object wont be there and so wont be blocked
        # yet the base will always block future points and so should be updated
        max_dydx = max(max_dydx, base_dydx)

    return output_layer
        
def find_viewshed(x_start, y_start, radius_m, observer_height, object_height, raster_band, dem):
    '''
    * Defines a function to calculate the viewshed from a starting point, defined by a 
      observers height and the designated distance (create an enclosing circle)
    '''
    r_start, c_start = dem.index(x_start, y_start) # transform viewshed coordinates to image space
    # check that our starting coordinates are within the dataset
    if not 0 <= r_start < dem.height or not 0 <= c_start < dem.width:
        print(f'Sorry, {x_start, y_start} is not within the elevation dataset')
        exit()
    
    # convert the radius to pixels, where dem.res[0] shows the size of each pixel in m (because they are squares)
    radius_px = int(radius_m / dem.res[0])

    # get the starting height of the viewshed in terms of location height and the viewer
    starting_height = raster_band[(r_start, c_start)] + observer_height

    # create a layer of zeros and update starting point to 1
    update_layer = zeros(raster_band.shape) # create layer of zeros
    update_layer[(r_start, c_start)] = 1 # viewer can see where they are stood

    # create a circle (e.g. the perimeter of the viewshed) with out starting point
    circle_numpy_array = circle_perimeter(r_start, c_start, radius_px*5) # radius is increased to increase line density for further calcs
    circle_coords = column_stack(circle_numpy_array)

    # loop through each line of sight that ends with the perimeter coord
    for r, c in circle_coords:
         update_layer = line_of_sight(r_start, c_start, starting_height, r, c, object_height, radius_px, raster_band, dem, update_layer)
       
    return update_layer
    
''' Set Parameters and Open the DEM for the Project Location '''

with rio_open(r'Raster Data Projects\data\helvellyn\Helvellyn-50.tif') as d:

    elevation_data = d.read(1) # read our layer of data from the dem
    x, y = 332000, 514000
    output = find_viewshed(x, y, 5000, 1.8, 100, elevation_data, d)

''' Plotting the Map ''' 

my_fig, my_ax = plt.subplots(nrows = 1, ncols = 1, figsize=(16,10))
my_ax.set_title('Viewshed Analysis')

rio_show(
    elevation_data,
    ax = my_ax,
    transform = d.transform,
    cmap = 'viridis',
    )
rio_show(
    elevation_data,
    ax = my_ax,
    contour = True,
    transform = d.transform,
    colors = ['white'],
    linewidth = 0.5
    )
rio_show(
    output,
    ax = my_ax,
    transform = d.transform,
    cmap = LinearSegmentedColormap.from_list('binary_viewshed', [(0,0,0,0),(1,0,0,0.5)], N=2), # semi-red color scheme
    )
GeoSeries(Point(x,y)).plot(
    ax = my_ax,
    markersize = 60,
    color = 'black',
    edgecolor = 'white'
    )

# add a colour bar
my_fig.colorbar(ScalarMappable(norm=Normalize(vmin=floor(elevation_data.min()), vmax=ceil(elevation_data.max())), cmap='viridis'), ax=my_ax, pad=0.01)

# add north arrow
x, y, arrow_length = 0.97, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
	arrowprops=dict(facecolor='black', width=5, headwidth=15),
	ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

# add legend for point
my_ax.legend(
	handles=[
		Patch(facecolor=(1, 0, 0, 0.5), edgecolor=None, label=f'Visible Area'),
		Line2D([0], [0], marker='o', color=(1,1,1,0), label='Viewshed Origin', markerfacecolor='black', markersize=8)
    	], loc='lower left')

plt.show()

