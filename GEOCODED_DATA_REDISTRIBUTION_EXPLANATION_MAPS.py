
from numpy import zeros
from geopandas import read_file, GeoSeries
from shapely import Polygon, Point
import matplotlib.pyplot as plt
from numpy.random import uniform
from rasterio import open as rio_open
from rasterio.plot import show as rio_show
from matplotlib.pyplot import get_cmap
from math import sqrt, pi
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.lines import Line2D
from matplotlib.patches import Patch 
import math

def pythag_distance(x_start, y_start, x_end, y_end):
    return sqrt((x_start - x_end)**2 + (y_start - y_end)**2)

# load data and adjust crs if necessary
geocoded_tweets = read_file(r'Raster Data Projects\data\tweet_redist_data\level3-tweets-subset.shp') # EPSG 27700
admin_areas_level_3 = read_file(r'Raster Data Projects\data\tweet_redist_data\gm-districts.shp') # EPSG 27700
bng = "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +towgs84=446.448,-125.157,542.06,0.15,0.247,0.842,-20.489 +units=m +no_defs"


fig1, ax1 = plt.subplots(nrows=2, ncols=2, figsize = (11,15)) # create figure and axis
fig1.subplots_adjust(hspace=0.2, wspace=0)

fig1.suptitle("The Stages of Redistribution for Each Point")
# add legend for point
fig1.legend(
    handles=[
        Line2D([0], [0], marker='o', color=(1,1,1,0), label='Accepted Random Points', markerfacecolor='black', markersize=8),
        Line2D([0], [0], marker='o', color=(1,1,1,0), label='Original Data Points', markerfacecolor='blue', markersize=8),
        Line2D([0], [0], marker='o', color=(1,1,1,0), label='Declined Random Points', markerfacecolor='red', markersize=8),
        Line2D([0], [0], marker='o', color=(1,1,1,0), label='Redistributed Point', markerfacecolor='purple', markersize=8),
        Line2D([0], [0], color='red',  lw=1.5, label='Bounding Box')
        ]
        , 
        loc='lower center', 
        ncols=3, 
        bbox_to_anchor=(0.5,0),
        fontsize = '8')




'''Map 1'''



# draw the bounding box for the polygon we will focus on later
oldham_gdf = admin_areas_level_3.loc[admin_areas_level_3.NAME == 'Oldham District (B)']
oldham_bounds = (oldham_gdf.geometry.bounds).iloc[0]
oldham_bb_coord_list = (oldham_bounds[0], oldham_bounds[1]), (oldham_bounds[2], oldham_bounds[1]), (oldham_bounds[2], oldham_bounds[3]), (oldham_bounds[0], oldham_bounds[3])
oldham_bb = Polygon(oldham_bb_coord_list)
admin_areas_level_3.plot( # plot the borders
    ax = ax1[0][0],
    edgecolor = 'black',
    color = 'None',
    linewidth = 0.5
)
geocoded_tweets.plot( # plot the data
    ax = ax1[0][0],
    color = 'blue',
    markersize = 3,
)
GeoSeries(oldham_bb, crs=bng).plot(
    ax=ax1[0][0],
    color='None',
    edgecolor='Red',
    linewidth=0.5,
)
ax1[0][0].set_title('All Original Points', color='black', loc='center')
# add scalebar
ax1[0][0].add_artist(ScaleBar(dx=1, units="m", location="lower right", length_fraction=0.2, box_color='none'))
x, y, arrow_length = 0.97, 0.98, 0.15
ax1[0][0].annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=0.5, headwidth=5),
            ha='center', va='center', fontsize=8,
            xycoords=ax1[0][0])
for i in ['left', 'right', 'top', 'bottom']:
    ax1[0][0].spines[i].set_color('none') 
ax1[0][0].set_xticks([])
ax1[0][0].set_yticks([])




'''Map 2'''



# get all of the points in oldham
points_in_oldham = []
np_in_oldham = []
np_out_oldham = []
for p in geocoded_tweets.geometry:
    if p.intersects(oldham_gdf.geometry.iloc[0]):
        points_in_oldham.append(p)
print('Input your w value')
w = float(input())
counter = 0
for i in points_in_oldham:
        while counter <= (w): 
            random_x = uniform(low=oldham_bounds[0], high=oldham_bounds[2])
            random_y = uniform(low=oldham_bounds[1], high=oldham_bounds[3])
            random_xy = Point(random_x, random_y)

            if random_xy.intersects(oldham_gdf.geometry.iloc[0]):
                np_in_oldham.append(random_xy)
                counter += 1
            else:
                np_out_oldham.append(random_xy)
oldham_gdf.geometry.plot(
    ax=ax1[0][1],
    color='None',
    edgecolor='Black',
    linewidth=0.5
)
GeoSeries(np_in_oldham).set_crs(bng).plot(
    ax = ax1[0][1],
    markersize = 3,
    color = 'black',
)
GeoSeries(np_out_oldham).set_crs(bng).plot(
    ax = ax1[0][1],
    markersize = 3,
    color = 'red',
)
GeoSeries(oldham_bb, crs=bng).plot(
    ax=ax1[0][1],
    color='None',
    edgecolor='Red',
    linewidth=0.5,
    )
ax1[0][1].set_title('Randomly Generated Points', color='black', loc='center')
ax1[0][1].set_xlim([oldham_bounds[0]-100, oldham_bounds[2]+100])
ax1[0][1].set_ylim([oldham_bounds[1]-100, oldham_bounds[3]+100])
ax1[0][1].add_artist(ScaleBar(dx=1, units="m", location="lower center", length_fraction=0.2, box_color='none'))
x, y, arrow_length = 0.97, 0.98, 0.15
ax1[0][1].annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=0.5, headwidth=5),
            ha='center', va='center', fontsize=8,
            xycoords=ax1[0][1])
for i in ['left', 'right', 'top', 'bottom']:
        ax1[0][1].spines[i].set_color('none') 
ax1[0][1].set_xticks([])
ax1[0][1].set_yticks([])



'''Map 3'''



exterior = [(oldham_bounds[0]-100000, oldham_bounds[1]-100000), (oldham_bounds[2]+100000, oldham_bounds[1]-100000), (oldham_bounds[2]+100000, oldham_bounds[3]+100000), (oldham_bounds[0]-10000, oldham_bounds[3]+10000)]
interior_coord = list(oldham_gdf.geometry.iloc[0].boundary.coords)
poly = Polygon(exterior, holes = [interior_coord])
with rio_open(r'Raster Data Projects\data\tweet_redist_data\100m_pop_2019.tif') as data: 
    highest_value = 0
    new_point = []
    new_pointt = []
    pop_dens = data.read(1)
    for x in np_in_oldham:
        row, col = data.index(x.x, x.y)
        value_at_x = pop_dens[row, col]
        if value_at_x > highest_value:
            highest_value = value_at_x
            new_point = x
            new_pointt = (row, col)

    rio_show(
        pop_dens,
        ax = ax1[1][0],
        transform = data.transform,
        cmap = (get_cmap('hsv')),
    )
    admin_areas_level_3.geometry.plot(
            ax=ax1[1][0],
            color='None',
            edgecolor='Black',
            linewidth=0.5
        )
    GeoSeries(np_in_oldham).set_crs(bng).plot(
        ax = ax1[1][0],
        markersize = 3,
        color = 'black',
    )
    # here we can add a polygon on top to block anything else.
    GeoSeries(poly).set_crs(bng).plot(
        ax = ax1[1][0],
        color = 'white'
    )
    GeoSeries(new_point).set_crs(bng).plot(
        ax = ax1[1][0],
        color = 'black',
        markersize = 4,
    )
    ax1[1][0].set_title('Evaluating Against Weighted Surface', color='black', loc='center')
    ax1[1][0].set_xlim([oldham_bounds[0]-100, oldham_bounds[2]+100])
    ax1[1][0].set_ylim([oldham_bounds[1]-100, oldham_bounds[3]+100])
    # add on scalebar, cbar.
    ax1[1][0].add_artist(ScaleBar(dx=1, units="m", location="lower center", length_fraction=0.2, box_color='none'))

    cbar = fig1.colorbar(ScalarMappable(norm=Normalize(vmin=62, vmax=17100), cmap='hsv'), ticks=[62, 17100], ax=ax1[1][0], shrink=0.5)
    cbar.ax.set_yticklabels(['Low\nPopulation', 'High\nPopulation'])
    x, y, arrow_length = 0.97, 0.98, 0.15
    ax1[1][0].annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=0.5, headwidth=5),
            ha='center', va='center', fontsize=8,
            xycoords=ax1[1][0])
    for i in ['left', 'right', 'top', 'bottom']:
        ax1[1][0].spines[i].set_color('none') 
    ax1[1][0].set_xticks([])
    ax1[1][0].set_yticks([])
    ax1[1][0].set_xlabel('fake\nfake\nfake', color='none')



    '''Map 4'''


    print('Input your s Value')
    radius = int(sqrt(((float(input()))*oldham_gdf.area) / pi)/data.res[0])
    layer = zeros(pop_dens.shape)
    for each_row in range((new_pointt[0] - radius), (new_pointt[0] + radius + 1)):
        for each_col in range((new_pointt[1] - radius), (new_pointt[1] + radius + 1)):
            distance_from_seed = pythag_distance(new_pointt[0], new_pointt[1], each_row, each_col)
            if distance_from_seed <= radius:
                cell_value = 1 - (distance_from_seed / radius)
                # set the value to the raster layer (if its within the bounds)
                try:                             
                    layer[each_row][each_col] += cell_value # update this value on the update layer
                                    
                except IndexError:
                    pass
    rio_show(
        layer,
        ax = ax1[1][1],
        transform = data.transform,
        cmap = (get_cmap('Purples')),
    )
    GeoSeries(points_in_oldham).set_crs(bng).plot(
        ax = ax1[1][1],
        markersize = 2,
        color = 'blue',
    )
    oldham_gdf.geometry.plot(
                ax=ax1[1][1],
                color='None',
                edgecolor='Black',
                linewidth=0.5
            )
    GeoSeries(poly).set_crs(bng).plot(
        ax = ax1[1][1],
        color = 'white',
    )
    ax1[1][1].set_title('New Dispersed Point', color='black', loc='center')
    ax1[1][1].set_xlim([oldham_bounds[0]-100, oldham_bounds[2]+100])
    ax1[1][1].set_ylim([oldham_bounds[1]-100, oldham_bounds[3]+100])
    ax1[1][1].add_artist(ScaleBar(dx=1, units="m", location="lower center", length_fraction=0.2, box_color='none'))
    x, y, arrow_length = 0.97, 0.98, 0.15
    ax1[1][1].annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=0.5, headwidth=5),
            ha='center', va='center', fontsize=8,
            xycoords=ax1[1][1])
    for i in ['left', 'right', 'top', 'bottom']:
        ax1[1][1].spines[i].set_color('none') 
    ax1[1][1].set_xticks([])
    ax1[1][1].set_yticks([])
    ax1[1][1].set_xlabel('fake\nfake\nfake', color='none')

plt.show()
print('done')