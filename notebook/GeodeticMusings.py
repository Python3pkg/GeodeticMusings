# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Geodetic musings
# 
# This is a litle benchmark of three Python libraries to compute geodesic distance distances:
# - Pyproj.
# - Pygc.
# - GeographicLib.

# <markdowncell>

# ##Pyproj
# Geodesic distance computation with Pyproj
# (python interface to PROJ4 C library).
# 
# https://github.com/jswhit/pyproj
# 
# Geodesic distance calculations using Charles Karney 
# geodesic algorithms:
#     C. F. F. Karney, Algorithms for Geodesics, 
#         J. Geodesy 87(1), 43–55 (Jan. 2013)
# 
# PROJ4 C library routines used to compute 
# geodesic distance are a simple transcription from 
# C. Karney Geographiclib C++ Library.
# 
# https://trac.osgeo.org/proj/browser/trunk/proj/src/geodesic.h
# 
# Default values used (WGS84):
# https://github.com/jswhit/pyproj/blob/master/lib/pyproj/__init__.py
#    
#    - Semi-major axis: 6378137.0
#    - Inverse flattening: 298.257223563
#    
# Therefore:
#    - Semi-minor axis: 6356752.314245179
#    - Flattening: 0.0033528106647474805

# <codecell>

from pyproj import Geod

# <codecell>

def grcrcl1(lon_1, lat_1, lon_2, lat_2):
    
    g = Geod(ellps='WGS84')
    
    az, az_inv, dist = g.inv(lon_1, lat_1, lon_2, lat_2)
    
    return dist

# <markdowncell>

# ##Pygc
# Geodesic distance computation with Pygc.
# 
# https://github.com/axiom-data-science/pygc
# 
# Geodesic distance calculations using Vincenty's formulae:
#     http://en.wikipedia.org/wiki/Vincenty%27s_formulae
# 
# Default values used (WGS84):
# https://github.com/axiom-data-science/pygc/blob/master/pygc/gc.py
#     
#    - Semi-major axis: 6378137.0
#    - Semi-minor axis: 6356752.3142
# 
# Therefore:
#    - Flattening: 0.0033528106718309896
#    - Inverse flattening: 298.2572229328697

# <codecell>

from pygc import great_distance

# <codecell>

def grcrcl2(startlong, startlat, endlong, endlat):
    
    res = great_distance(start_latitude=startlat, start_longitude=startlong, 
                        end_latitude=endlat, end_longitude=endlong)
    
    return float(res['distance'])

# <markdowncell>

# ##GeographicLib
# Geodesic distance computation with GeographicLib 
# (python interface to GeographicLib C++ library).
# 
# http://geographiclib.sourceforge.net/html/other.html#python
# 
# Geodesic distance calculations using Charles Karney 
# geodesic algorithms:
#     C. F. F. Karney, Algorithms for Geodesics, 
#     Journal of Geodesy 87(1), 43–55 (Jan. 2013)
# 
# Default values used (WGS84):
# http://geographiclib.sourceforge.net/html/Constants_8hpp_source.html
#    - Semi-major axis: 6378137.0
#    - Inverse flattening: 298.257223563
# 
# Therefore:
#    - Semi-minor axis: 6356752.314245179
#    - Flattening: 0.0033528106647474805

# <codecell>

from geographiclib.geodesic import Geodesic

# <codecell>

def grcrcl3(lon_1, lat_1, lon_2, lat_2):
    
    res = Geodesic.WGS84.Inverse(lat_1,lon_1,lat_2,lon_2)
    
    return res['s12']

# <markdowncell>

# ##Results
# Function to print results from Geodesic distance functions:

# <codecell>

def printResults(input_coords):
    
    lon_1, lat_1, lon_2, lat_2 = input_coords
    
    dist1 = grcrcl1(lon_1, lat_1, lon_2, lat_2)
    dist2 = grcrcl2(lon_1, lat_1, lon_2, lat_2)
    dist3 = grcrcl3(lon_1, lat_1, lon_2, lat_2)
    
    print "Distances for: lon_1 {0}, lat_1 {1}, lon_2 {2}, lat_2 {3}\n".format(lon_1, lat_1, lon_2, lat_2)
    print "Pyproj___________________________{:,.10f} m\n".format(dist1)
    print "Pygc_____________________________{:,.10f} m\n".format(dist2)
    print "GeographicLib____________________{:,.10f} m\n".format(dist3)
    print "Difference Pyproj,Pygc___________{:.15f} m\n".format(abs(dist1 - dist2))
    print "Difference Pyproj,GeographicLib__{:.15f} m\n".format(abs(dist1 - dist3))
    print "Difference GeographicLib,Pygc____{:.15f} m\n".format(abs(dist3 - dist2))
    print "------------------------------------------\n"

# <markdowncell>

# Creating test data. Test data is a list of lists. Each inner list contains:
#  - Start longitude.
#  - Start latitude.
#  - End longitude.
#  - End latitude.

# <codecell>

data = [
        [-3.6,40.5,-118.4,33.9],
        [-6.,37.,-145.,11.],
        [-150.,37.,140.,11.],
        [-50.,7.,40.,11.],
        [-100.,80.,-140.,30.]
    ]

# <markdowncell>

# Printing three functions results with created test data:

# <codecell>

map(printResults, data)

# <markdowncell>

# ##Discussion
# 
# There are minor differences in outcomes though curiously the most puzzling is that the highest dissimilarity occur between Pyproj and GeographicLib which in theory using the same algorithms. More study of each library is needed to solve this mistery...

# <codecell>


