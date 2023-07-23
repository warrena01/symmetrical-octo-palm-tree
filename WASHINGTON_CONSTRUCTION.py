'''
data:
    construction permits: https://opendata.dc.gov/search?q=construction%20permits 
    neighbourhood clusters: https://opendata.dc.gov/maps/neighborhood-clusters
'''

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import glob

districts = gpd.read_file(r'Vector Data Projects\washington_data\Neighborhood_Clusters.geojson') 
# cambiar crs a metros
districts.crs.to_epsg(3857)

# make a list of all the files
files = glob.glob(r'Vector Data Projects\washington_data\Construction*')
df_list = [] # initialise variable
for file in files:
    year = file.split('_')[-1].split('.')[0] # split the file at _ and . in positions [-1] and [0]
    gdf = gpd.read_file(file) # read file and store in variable
    gdf['year'] = year # add a year column
    df_list.append(gdf) # append to list

# concat all into one gdf
gdf = pd.concat(df_list) # print gdf.shape to check
print('\nAll Construction Permit gdf')
print(gdf)

# spatial join connecting gdf to districts, including 3 cols
gdf_join = gdf.sjoin(districts[['NAME', 'NBH_NAMES', 'geometry']], how='left', predicate='within')
print('\nJoin for Districts and Construction Permits')
print(gdf_join) 

# value_counts = returns a series containing counts of unique values, .to_frame = converts a series to a dataframe
counts_by_year = gdf_join.value_counts(['year', 'NAME']).to_frame().reset_index().sort_values(['NAME', 'year'])
counts_by_year.columns = ['year', 'district', 'permit_count']
# create a pivot table of the permits per year, per cluster
pivoted = counts_by_year.pivot(index='district', columns='year', values='permit_count') # pivot creates a pivot
print('\nDataFrame of Construction Permits per Year, Per District')
print(pivoted)

# merge the dataframes together and turn into a gdf
new_df = pd.merge(pivoted, districts[['NAME', 'NBH_NAMES', 'geometry']], how='left', left_index=True, right_on='NAME')
final_gdf = gpd.GeoDataFrame(new_df, geometry='geometry', crs=4326)
print('\nConnect Pivoted and Districts into one GeoDataFrame')
print(final_gdf)

# create a new column for percentage change and sort values based on this
final_gdf['perc_change'] = ((final_gdf['2021'] - final_gdf['2012']) / final_gdf['2012']) * 100
final_gdf.sort_values('perc_change', ascending=False)
print('\nPercentage Change Column Added')
print(final_gdf)

# take a look at the top 10 and plot
top_10_perc_change = final_gdf.head(10)
print('\nTop 10 Percentage Change')
print(top_10_perc_change)
years_data = top_10_perc_change.columns[0:-4] #-4 refers to the 4th last element in the list
for idx, row in top_10_perc_change.iterrows():
    plt.plot(years_data, row[years_data], label=row['NBH_NAMES'])
#             x value     where stored      line name
plt.legend()


# plot state with the change in construction permits given and perc as calculated
final_gdf.plot(column = 'perc_change', scheme = 'quantiles', k = 5, legend = True, legend_kwds = {'loc': 'upper left','title': 'Construction Permits % Change', 'fontsize': '6'})
plt.title('Percentage Change in Construction Permits Per District in Washington')
plt.axis('off')
plt.show()
