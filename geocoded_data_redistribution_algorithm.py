'''
Write an Algorithm That Redistributes Tweets Passively Geocoded to Greater Manchester Boroughs
with Probable Locations Based Upon Population Distribution. 
Produce Map Outputs to Show the Process and Impact of What is Done.

12. define distance using pythag.
point distribution function:
    9. define the radius of a circle around seed location as proportional to (admin_area, s)
    10. loop through a bounding square with d = 2r around a (point).
    12. if the distance is <= to r, give value using 1 - distance/r and update output layer
weighted redistribution function:
1. get raster data band and create a a transparent redistribution with .shape of (raster_data) (weighted_surface_band), create spatial index.
2. for admin_area in (admin_areas_level)
    3. find bounding box
    get all points that are within each state (geocoded_data)
    4. for each point
        5. initialise a counter variable
        initialise a variable to store the value of the highest ranked seed location 
        initialise a variable to store the row and col of the highest seed location
        6. while counter < (w):
            7. create a new seed location via a random x and y coordinate within the bounding box range
            8. if the location is inside admin_area (using spatial index), find value on weighted surface
            and if it is the highest value on the (weighted_surface) update max value and location
        13. call on the point distribution function for new seed location (uses spatial ambiguity multiplier, (s))
14. Call on the weighted redistribution function using our data and user input values for s and w for:
    (a) high_s, low_w       (d) high_s, med_w       (g) high_s, high_w
    (b) med_s, low_w       *(e) med_s, med_w*        (h) med_s, high_w
    (c) low_s, low_w        (f) low_s, med_s        (i) low_s, high_w
15. plot the data for (e) on its own axis.
16. Plot the Data for a-i

Parameters:
- w = influence of the weighted surface. Where w represents the number of seed locations 
      to be created and hence a greater chance of the chosen seed location to be in an
      area  with higher values on the weighted surface, therefore mimicking it.
- s = degree of spatial ambiguity. Where s represents a multiplier for the radius of the 
      distribution drawnn around the new seed location and hence representation on the output

'''
from geopandas import read_file
from rasterio import open as rio_open
from math import sqrt, pi
from numpy.random import uniform
from numpy import zeros
from shapely.geometry import Point
from rtree.index import Index

import matplotlib.pyplot as plt
from rasterio.plot import show as rio_show
from matplotlib.pyplot import get_cmap
from math import floor, ceil
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib_scalebar.scalebar import ScaleBar

''' calculate distance using Pythagoras theorem ''' 
def pythag_distance(x_start, y_start, x_end, y_end):
    return sqrt((x_start - x_end)**2 + (y_start - y_end)**2)

def point_distribution(new_seed_location, radius, layer_upd):
    # loop through the square made around a location, where length/width = 2r
    for each_row in range((new_seed_location[0] - radius), (new_seed_location[0] + radius + 1)):
        for each_col in range((new_seed_location[1] - radius), (new_seed_location[1] + radius + 1)):
            distance_from_seed = pythag_distance(new_seed_location[0], new_seed_location[1], each_row, each_col)

            # define the distance away from new_seed_location as <= r to capture a circle of cells
            if distance_from_seed <= radius:
                cell_value = 1 - (distance_from_seed / radius) # assign cell a value based on proximity to centre
                            
                # set the value to the raster layer (if its within the bounds)
                try:                             
                    layer_upd[each_row][each_col] += cell_value # update this value on the update layer
                                    
                except IndexError:
                    pass

    return layer_upd

''' redistribute data within administrative area based upon a weighted surface '''
def weighted_redistribution(raster_data, raster_band, admin_areas_levelx, geocoded_data, w, s):

    layer_upd = zeros(raster_band.shape) # create a blank layer to update with new distribution 

    # create a spatial index to speed up search for points in each polygon
    my_spatial_index = Index()
    for id, data in geocoded_data.iterrows():
        my_spatial_index.insert(id, data.geometry.bounds)

    for id, admin_area in admin_areas_levelx.iterrows(): # loop through each admin area at this scalar level
        
        admin_area_bounds = admin_area.geometry.bounds # find the bounding box for later use 
        area = admin_area.geometry.area # find the area for later use
        admin_area_geom = admin_area.geometry # find the geometry for later use 
        
        # use the spatial index 
        possible_matches_id = list(my_spatial_index.intersection(admin_area_bounds)) # returns the id
        possible_matches = geocoded_data.iloc[possible_matches_id] # returns the rows of data
        data_points = possible_matches.loc[possible_matches.intersects(admin_area_geom) == True]
        
        radius = int(sqrt((s*area) / pi)/raster_data.res[0]) # define radius in pixels, will be used later
    
        for p in data_points: # loop through each point in data_points

            counter = 0 # initialise a variable for the counter
            highest_value = 0 # initialise a variable to store the value of the highest ranked seed location
            new_seed_location = [] # initialise a variable to store the location of the highest ranked seed

            while counter <= w: # set the number of seed locations to be produced (i.e. the influence of the weighted surface)

                # calculate a random coordinate for the seed location
                random_x = uniform(low=admin_area_bounds[0], high=admin_area_bounds[2])
                random_y = uniform(low=admin_area_bounds[1], high=admin_area_bounds[3])
                random_xy = Point(random_x, random_y)

                if random_xy.intersects(admin_area.geometry) == True: # if the random point is within the polygon

                    row, col = raster_data.index(random_x, random_y) # transform to image space
                    value_at_randomxy = raster_band[row, col] # find value at random_xy on weighted surface
                    counter = counter + 1

                    if value_at_randomxy > highest_value: # if this is the highest value, update variables
                        
                        highest_value = value_at_randomxy
                        new_seed_location = (row, col)

            point_distribution(new_seed_location, radius, layer_upd)

    return layer_upd

''' working with the data '''

print('Input a low value for w, where low is around < 5, and high is around > 40')
loww = float(input())
print('Input a medium value for w, where low is around < 5, and high is around > 40')
medw = float(input())
print('Input a high value for w, where low is around < 5, and high is around > 40')
highw = float(input())
print('Input a low value for s, where low is around < 0.05, and high is around > 0.4')
lows = float(input())
print('Input a medium value for s, where low is around < 0.05, and high is around > 0.4')
meds = float(input())
print('Input a high value for s, where low is around < 0.05, and high is around > 0.4')
highs = float(input())

# import and access all data
with rio_open(r'Raster Data Projects\data\tweet_redist_data\100m_pop_2019.tif') as data: # EPSG 27700, 100m resolution
    
    pop_dens = data.read(1)
    geocoded_tweets = read_file(r'Raster Data Projects\data\tweet_redist_data\level3-tweets-subset.shp') # EPSG 27700
    admin_areas_level_3 = read_file(r'Raster Data Projects\data\tweet_redist_data\gm-districts.shp') # EPSG 27700

    # produce the maps for all variables
    output_loww_lows = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, loww, lows)
    print('loww, lows completed')
    output_loww_meds = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, loww, meds)
    print('loww, meds completed')
    output_loww_highs = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, loww, highs)
    print('loww, highs completed')
    output_medw_lows = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, medw, lows)
    print('medw, lows completed')
    output_medw_meds = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, medw, meds)
    print('medw, meds completed')
    output_medw_highs = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, medw, highs)
    print('medw, highs completed')
    output_highw_lows = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, highw, lows)
    print('highw, lows completed')
    output_highw_meds = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, highw, meds)
    print('highw, meds completed')
    output_highw_highs = weighted_redistribution(data, pop_dens, admin_areas_level_3, geocoded_tweets, highw, highs)
    print('highw, highs completed')

    ''' Plot the First Map Using the median of the user inputs '''

    my_fig1, my_ax1 = plt.subplots(nrows=1, ncols=1, figsize=(16,10)) # create an axis
    my_ax1.axis('off') # turn off the axis
    my_ax1.set(title = 'Weighted Redistribution of Passively Geocoded Twitter Activity\n Relating to the Royal Wedding') # set title

    # add on the administrative areas boundaries
    admin_areas_level_3.plot(
        ax = my_ax1,
        color = 'none',
        edgecolor = 'Black',
        linewidth = 0.5
    )
    # add on the new output layer
    rio_show(
        output_medw_meds,
        ax = my_ax1,
        transform = data.transform,
        cmap = 'Purples'
    )
    # set a colour bar
    cbar = my_fig1.colorbar(ScalarMappable(norm=Normalize(vmin=floor(output_medw_meds.min()), vmax=ceil(output_medw_meds.max())), cmap='Purples'), ticks=[output_medw_meds.min(), ceil(output_medw_meds.max())], ax=my_ax1, shrink = 0.7)
    cbar.ax.set_yticklabels(['Low\nActivity', 'High\nActivity'])

    # add north arrow
    x, y, arrow_length = 0.98, 0.99, 0.1
    my_ax1.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
    arrowprops=dict(facecolor='black', width=5, headwidth=15),
    ha='center', va='center', fontsize=20, xycoords=my_ax1.transAxes)

    # add scalebar
    my_ax1.add_artist(ScaleBar(dx=1, units="m", location="lower right", length_fraction=0.25))
    
    print('map 1 plotted')
    
    ''' Plot the Second Map Showing the Effects of w and s '''

    list_of_outputs = [output_loww_highs, output_loww_meds, output_loww_lows, output_medw_highs, output_medw_meds, output_medw_lows, output_highw_highs, output_highw_meds, output_highw_lows]

    my_fig2, my_ax2 = plt.subplots(nrows=3, ncols=3, sharex = True, sharey = True) # create figure
    my_fig2.suptitle("The Effects of the Inputted S and W Values\n on Data Redistribution")
    my_fig2.supxlabel('Increasing s Values')
    my_fig2.supylabel('Increasing w Values', horizontalalignment='center')
    
    x = 0
    r = 0

    for rows in my_ax2:
        c = 0 # intialise counter for column placer, resets for every row analysed due to loop positioning
        for col in rows:
            # remove the tick labels 
            col.set_xticks([])
            col.set_yticks([])

            # remove the colours of the outer box / axis
            my_ax2[r][c].spines['left'].set_color('none') 
            my_ax2[r][c].spines['right'].set_color('none')   
            my_ax2[r][c].spines['top'].set_color('none')   
            my_ax2[r][c].spines['bottom'].set_color('none') 
            
            rio_show( # plot the output with the specific data inputted
                list_of_outputs[x], 
                ax = my_ax2[r][c],
                transform = data.transform,
                cmap = 'Purples'
            )
            admin_areas_level_3.plot( # plot the admin areas for the level
            ax = my_ax2[r][c],
            color = 'none',
            edgecolor = 'Black',
            linewidth = 0.5
            )

            # add on the labels in the correct positions
            if r==0 and c==0:
                my_ax2[r][c].set_ylabel(f's = {highs}')
            if r==1 and c==0:
                my_ax2[r][c].set_ylabel(f's = {meds}')
            if r==2 and c==0:
                my_ax2[r][c].set_ylabel(f's = {lows}')
            if r==2 and c==0:
                my_ax2[r][c].set_xlabel(f'w = {loww}')
            if r==2 and c==1:
                my_ax2[r][c].set_xlabel(f'w = {medw}')
            if r==2 and c==2:
                my_ax2[r][c].set_xlabel(f'w = {highw}')

            x += 1 # keep on going through the output to be plotted for the next loop

            # update the counters 
            if c < 2:
                c += 1
            else:
                r += 1
    
    # set a colour bar
    cbar = my_fig2.colorbar(ScalarMappable(norm=Normalize(vmin=0, vmax=1), cmap='Purples'), ticks=[0, 1], ax=my_ax2, shrink = 0.7)
    cbar.ax.set_yticklabels(['Low\nActivity', 'High\nActivity'])
    
    plt.show()

    print('map 2 plotted')


