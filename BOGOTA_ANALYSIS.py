
import geopandas as gpd
import matplotlib.pyplot as plt

barrios = gpd.read_file(r'Vector Data Projects\colombia_data\barrios_SDP.shp')
localidades = gpd.read_file(r'Vector Data Projects\colombia_data\localidades.shp')

fig, ax = plt.subplots()

barrios.plot(
            ax=ax,
            column='SHAPE_Area',
            scheme = 'quantiles',
            cmap = 'OrRd',
            legend = True,
            legend_kwds = {'loc': 'upper left','title': 'Barrio Size', 'fontsize': '7'}, 
            
            )

centroides_manzanas = gpd.read_file(r'Vector Data Projects\colombia_data\CentroidesManzas.xml.gml')
grilla = gpd.read_file(r'Vector Data Projects\colombia_data\Grilla_id.geojson')

# Este comando junta las filas de dos tablas donde se coinciden espatialmente
join = gpd.tools.sjoin(centroides_manzanas, grilla)

# Buscar por solo los manzanas que tienen poblaciones
join = join.query('DENSIDAD_P > 0')

fig2, ax2 = plt.subplots()
# aggregar las densidades poblacional para cada hexagano en la grilla
densidad_poblacional = join.groupby('ID')['DENSIDAD_P'].agg(['sum'])
densidad_poblacional.plot(ax=ax2)

fig3, ax3 = plt.subplots()
join.plot(
    column = 'DENSIDAD_P',
    scheme = 'quantiles',
    ax=ax3
)

plt.show()


