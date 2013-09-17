OGR2OGR=ogr2ogr
SHP2OSM=python shp2osm.py

.PHONY: convert_to_wgs84 clean shp2osm

all: clean convert_to_wgs84 shp2osm

convert_to_wgs84:
	$(OGR2OGR) -t_srs WGS84 -s_srs "ESRI::Rutgers_Buildings6.prj" "converted.shp" "Rutgers_Buildings6.shp"

shp2osm:
	mkdir -p output
	$(SHP2OSM) converted.shp

clean:
	rm -f converted.*
	rm -rf output
