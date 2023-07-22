''' 
Produce a Map Showing Flooding at Helvellyn
'''
'''
3. Define an algorithm for calculating floods from a set point
	4. Create a new layer of 0s in image space and define starting point
	5. Define two sets for cells already assessed and those not
	   (add starting point to cells to assess)
	6. While there are still cells to assess:
		7. Remove the cell from the to_assess set
		8. Update zeros layer if the cell would flood
		9. Loop through list of neighbouring cells
			10. Add to cells to assess if not already assessed
2. Define flood parameters (starting location and flood depth)
1. Open raster data, read the band and create a variable for the output layer
11. Call on flood definition made in (3) with our data
12. Plot
'''

import matplotlib.pyplot as plt
from numpy import zeros
from rasterio import open as rio_open
from rasterio.plot import show as rio_show
from matplotlib.colors import LinearSegmentedColormap
from math import floor, ceil
from geopandas import GeoSeries
from shapely.geometry import Point
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib_scalebar.scalebar import ScaleBar

''' Calculations '''

# define a function that calculates flood fill from a predefined point
def flood_fill_calc(depth, x_start, y_start, dem, dem_data):
    
    flood_layer = zeros(dem_data.shape) # add our layer which we will update
    
    r0, c0 = dem.index(x_start, y_start) # transform to image space
    
    # make a set to avoid duplicates
    cells_assessed = set()
    cells_to_assess = set()
    
    cells_to_assess.add((r0, c0)) # set the first cell to be assessed. e.g. the origin
    
    flood_extent = dem_data[(r0,c0)] + depth # work out the max elev of the flood
    
    while cells_to_assess:
    
        # remove current cell from current set and add to cells_assessed
        (r, c) = cells_to_assess.pop()
        cells_assessed.add((r, c))
        
        # if the cell is low enough to be flooded, show on output map
        if dem_data[(r, c)] <= flood_extent:
            flood_layer[(r, c)] = 1
            
            # create a list of neighbouring cells relative positions and loop through them
            for row_adj, col_adj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                neighbour = (r + row_adj, c + col_adj) # find the position relative to the cell being assessed
                # make sure this cell is within the bounds of our image space
                if 0 <= neighbour[0] < dem.height:
                    if 0 <= neighbour[1] < dem.width:
                        if neighbour not in cells_assessed:
                            cells_to_assess.add(neighbour)
                    
    return flood_layer
                
''' Define the Parameters for the Flood'''

flood_location = (332000, 514000) # set origin as a tuple
flood_depth = 2 # set the depth of the flood

''' Open the DEM for the Project Location '''

# open the raster dataset
with rio_open(r"Raster Data Projects\data\helvellyn\Helvellyn-50.tif") as dem:  # 50m resolution
    
    # read the data out of band 1 in the dataset
    elev_data = dem.read(1)
    
    # calculate the flood
    output = flood_fill_calc(flood_depth, flood_location[0], flood_location[1], dem, elev_data)
    
''' Plotting the Map '''

my_fig, my_ax = plt.subplots(1, 1, figsize=(16,10))
my_ax.set_title('Flood Fill Model for Hellvelyn')

rio_show( # plot the elevation data
    elev_data,
    ax = my_ax,
    transform = dem.transform,
    cmap = 'cividis'
    )
rio_show( # add contour lines from the elevation data
    elev_data,
    ax = my_ax,
    contour = True,
    transform = dem.transform,
    colors = ['white'],
    linewidths = [0.5]
    )
rio_show( # add the flood filled layer
    output,
    ax = my_ax,
    transform = dem.transform,
    # add a cmap which defines transparency or a blue filled cell on a scale of 0-1
    cmap = LinearSegmentedColormap.from_list('binary', [(0, 0, 0, 0), (0, 0.5, 1, 0.5)], N=2) # blue color
    )
GeoSeries(Point(flood_location)).plot(
    ax = my_ax,
    markersize = 50,
    color = 'red',
    edgecolor = 'white'
    )

# add a colour bar
my_fig.colorbar(ScalarMappable(norm=Normalize(vmin=floor(elev_data.min()), vmax=ceil(elev_data.max())), cmap='cividis'), ax=my_ax, pad=0.01)

# add north arrow
x, y, arrow_length = 0.97, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
    arrowprops=dict(facecolor='black', width=5, headwidth=15),
    ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

# add scalebar
my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower right"))

# add legend for point
my_ax.legend(
    handles=[
        Patch(facecolor=(0, 0.5, 1, 0.5), edgecolor=None, label=f'Flood Zone ({flood_depth}m)'),
        Line2D([0], [0], marker='o', color=(1,1,1,0), label='Flood Origin', markerfacecolor='red', markersize=8)
    ], loc='lower left')

plt.show()