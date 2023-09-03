import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from rasterio import open as rio_open
from rasterio.plot import show as rio_show
import numpy

with rio_open(r"C:\Users\warre\Documents\Programming\Python\Learning GeoPandas\Free GIS Data\ASTGTMV003_N10W076_dem.tif") as data:
    print(f"There are {data.count} layers in this raster layer")
    print(f"The {data.driver} driver was used to open this dataset")
    print(f"The crs of the dataset is {data.crs.to_epsg()}")
    print(f"The height of the dataset is {data.height}")
    print(f"The width of the dataset is {data.width}")
    
    cartagena = gpd.read_file(r"C:\Users\warre\Documents\Programming\Python\Learning GeoPandas\Free GIS Data\COL_adm2.shp")
    try:
        cartagena.to_crs(data.crs)
    except ValueError:
        cartagena = cartagena.set_crs(data.crs)
    print(f"The crs of the two datasets are: {data.crs}, and {cartagena.crs.to_epsg()}")

    dem = data.read(1) # access the dem data

    land_coords = []
    for row in range(1680, 2781):
        for col in range(1160, 2261):
            value = dem[row][col]
            if value != 0:
                land_coords.append((row,col))

    # print(land_coords)        
    zeros = numpy.zeros(data.shape)

    for row, col in land_coords:
        value = dem[row][col]
        if value < 5:
            zeros[row][col] = 1
            
'''Plot'''
my_fig, my_ax = plt.subplots(1, 1, figsize=(5,7))
cartagena.plot(
    ax=my_ax,
    color= 'None',
    edgecolor='blue'
)
'''
rio_show( # plot the elevation data
    dem,
    ax = my_ax,   
    transform = data.transform,
    )
    
rio_show( # plot the elevation data
    dem,
    ax = my_ax,
    contour = True,
    transform = data.transform,
    colors = 'black',
    linewidth = 0.5
    )
    '''
rio_show(
    zeros,
    ax = my_ax,
    transform = data.transform,
    cmap = LinearSegmentedColormap.from_list('binary', [(0, 0, 0, 0), (0, 0.5, 1, 0.5)], N=2) # blue color
    )
my_ax.set_xlim([-75.65, -75.4])
my_ax.set_ylim([10.25, 10.45])

plt.show()




