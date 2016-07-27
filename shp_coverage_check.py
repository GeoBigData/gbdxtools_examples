from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import fiona
from shapely.wkt import loads
from fiona import collection
import itertools

from gbdxtools import Interface


'''
This script searches the GBDX catalog for DG imagery based on a 
shapefile AOI and specified filters, then determines the percentage 
of AOI covered by the results. Result polygons are saves as a 
shapefile with properties in the attribute table. For direction
on setting search filters, please see the documentation at
http://gbdxtools.readthedocs.io/en/latest/catalog_search.html
'''

gbdx=Interface()

filters = [
"(sensorPlatformName = 'WORLDVIEW02' OR sensorPlatformName ='WORLDVIEW03')",
"cloudCover < 10",
"offNadirAngle > 10"]

startDate="2016-01-01T00:00:00.000Z"
endDate="2016-06-15T00:00:00.000Z"

def search_by_shapefile(shapefile, filters, startDate, endDate):
    with collection(shapefile, 'r') as in_shp:
        s = shape(in_shp[0]['geometry'])
        wkt_string = s.to_wkt()
        results = gbdx.catalog.search(searchAreaWkt=wkt_string, startDate=startDate,
                                   endDate=endDate, types = [ "DigitalGlobeAcquisition" ], filters=filters)
        return results
    	#Make a shapefile of the results
	schema3 = {'geometry': 'Polygon', 'properties':  {'available':'str',
															'catalogID':'str',
																'browseURL':'str',
																'cloudCover': 'float',
																'imageBands': 'str',
																'multiResolution': 'float',
																'offNadirAngle': 'float',
																'ordered': 'str',
																'panResolution': 'float',
																'sensorPlatformName': 'str',
																'sunAzimuth': 'float',
																'sunElevation': 'float',
																'targetAzimuth': 'float',
																'timestamp': 'str',
																'timestampWkt': 'str',
																'vendorName': 'str'}}
	with collection("rawSearchResults.shp", "w", "ESRI Shapefile", schema3) as output:
		for poly in results:
		        output.write({'geometry' : mapping(loads(poly['properties']['footprintWkt'])),
		                    'properties': {'available':poly['properties']['available'],
															'catalogID': poly['properties']['catalogID'],
																'browseURL': poly['properties']['browseURL'],
																'cloudCover': float(poly['properties']['cloudCover']),
																'imageBands': poly['properties']['imageBands'],
																'multiResolution': float(poly['properties']['multiResolution']),
																'offNadirAngle': float(poly['properties']['offNadirAngle']),
																'ordered': poly['properties']['ordered'],
																'panResolution': float(poly['properties']['panResolution']),
																'sensorPlatformName': poly['properties']['sensorPlatformName'],
																'sunAzimuth': float(poly['properties']['sunAzimuth']),
																'sunElevation': float(poly['properties']['sunElevation']),
																'targetAzimuth': float(poly['properties']['targetAzimuth']),
																'timestamp': poly['properties']['timestamp'],
																'timestampWkt': poly['properties']['timestampWkt'],
																'vendorName': poly['properties']['vendorName']}})
		print results
		return results


def spatial_cov_from_results(shapefile, resultsList):
	with fiona.open(shapefile) as input:
	    # preserve the schema of the original shapefile, including the crs
	    meta = input.meta
	    with fiona.open('dissolve.shp', 'w', **meta) as output:
	    	properties, geom = zip(*[(feature['properties'],shape(feature['geometry'])) for feature in input])
	    	output.write({'geometry': mapping(unary_union(geom)), 'properties': properties[0]})
	with collection(shapefile, 'r') as aoi_shp:
		with collection('dissolve.shp', 'r') as dissolve_shp:
			aoi = shape(aoi_shp[0]['geometry'])
			d = shape(dissolve_shp[0]['geometry'])
		PercentCovered = (d.area)/(aoi.area)
		print PercentCovered
		if PercentCovered == 1:
			print "Full spatial coverage at this level of filtering!"
	return PercentCovered

def main():
	results = search_by_shapefile('/Users/mollygraber/Documents/Tampa/westOutline.shp', filters, startDate, endDate)
	spatial_cov_from_results('/Users/mollygraber/Documents/Tampa/westOutline.shp', results)

if __name__ == "__main__":
    main()
