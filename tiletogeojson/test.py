from tiletogeojson import deg_to_tile_as_geojson
import json


geojson_obj = deg_to_tile_as_geojson(
    west=139.559326171875, north=35.77994251888403, south=35.36217605914681, east=140.2569580078125, zoom=10)

print(json.dumps(geojson_obj, indent=True))
