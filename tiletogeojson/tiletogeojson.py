#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import quadkey

import numpy as np

# 参考文献
# http://qiita.com/s-wakaba/items/f414bed3736dc5b368c8
from math import sin, cos, tan, acos, asin, atan2, radians, degrees, pi, log


def deg_to_num(lat_deg, lon_deg, zoom):
    lat_rad = radians(lat_deg)
    n = 2.0 ** zoom
    xtile_f = (lon_deg + 180.0) / 360.0 * n
    ytile_f = (1.0 - log(tan(lat_rad) + (1 / cos(lat_rad))) / pi) / 2.0 * n
    xtile = int(xtile_f)
    ytile = int(ytile_f)
    pos_x = int((xtile_f - xtile)*256)
    pos_y = int((ytile_f - ytile)*256)
    return (xtile, ytile, pos_x, pos_y)


def deg_to_pixel_coordinates(lat_deg, lon_deg, zoom):
    sin_lat = sin(lat_deg * pi / 180.0)
    n = 2.0 ** zoom
    pixel_x = int(((lon_deg + 180.0) / 360.0) * 256 * n)
    pixel_y = int((0.5-log((1.0+sin_lat)/(1.0-sin_lat))/(4.0*pi))*256 * n)
    return (pixel_x, pixel_y)


def meshcode_to_latlng(meshcode):
    latitude = (float(meshcode[0:2]) / 1.5)
    longtitude = (float(meshcode[2:4]) + 100.0)
    return (latitude, longtitude)


def deg_to_tile_as_geojson(west, north, east, south, zoom):

    edge_nw_x, edge_nw_y, _, _ = deg_to_num(north, west, zoom)
    edge_se_x, edge_se_y, _, _ = deg_to_num(south, east, zoom)

    # print(deg_to_num(north, west, zoom) + deg_to_num(south, east, zoom))

    features = []
    for tile_x in range(edge_nw_x, edge_se_x + 1):
        for tile_y in range(edge_nw_y, edge_se_y + 1):
            north_west_px = [tile_x, tile_y]
            south_east_px = (tile_x+1, tile_y+1)

            nw_geo = quadkey.from_tile(north_west_px, zoom).to_geo()
            se_geo = quadkey.from_tile(south_east_px, zoom).to_geo()

            coordinates = [
                [nw_geo[1], nw_geo[0]],
                [se_geo[1], nw_geo[0]],
                [se_geo[1], se_geo[0]],
                [nw_geo[1], se_geo[0]],
                [nw_geo[1], nw_geo[0]]
            ]

            feature = {
                "type": "Feature",
                "geometry": {"type": "MultiPolygon",
                             "coordinates": [
                                 [coordinates]
                             ]
                             },
                "properties": {},
            }
            features.append(feature)

    geojson_obj = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson_obj
