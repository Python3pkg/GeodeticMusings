# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2015.
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# 


from pyproj import Geod
from pygc import great_distance
from geographiclib.geodesic import Geodesic



def grcrcl1(lon_1, lat_1, lon_2, lat_2):
    """
    Geodesic distance computation with Pyproj
    (python interface to PROJ4 C library).
    
    https://github.com/jswhit/pyproj
    
    PROJ4 C library (>= v.4.9.0) routines used to compute 
    geodesic distances are a simple transcription from 
    C. Karney Geographiclib C++ Library.
    
    Geodesic distance calculations using Charles Karney 
    geodesic algorithms:
        C. F. F. Karney, Algorithms for Geodesics, 
            J. Geodesy 87(1), 43–55 (Jan. 2013)
    https://trac.osgeo.org/proj/browser/trunk/proj/src/geodesic.h
    
    PROJ4 C library (< v.4.9.0) routines used to compute 
    geodesic distances are:
        Paul D. Thomas, Spheroidal Geodesics, 
            Reference Systems, and Local Geometry.
            U.S. Naval Oceanographic Office, p. 162
            Engineering Library 526.3 T36s (1970)
    
    Default values used (WGS84):
    https://github.com/jswhit/pyproj/blob/master/lib/pyproj/__init__.py
        - Semi-major axis: 6378137.0
        - Inverse flattening: 298.257223563
    Therefore:
        - Semi-minor axis: 6356752.314245179
        - Flattening: 0.0033528106647474805
    
    """
    
    g = Geod(ellps='WGS84')
    
    az, az_inv, dist = g.inv(lon_1, lat_1, lon_2, lat_2)
    
    return dist


def grcrcl2(startlong, startlat, endlong, endlat):
    """
    Geodesic distance computation with Pygc
    https://github.com/axiom-data-science/pygc
    
    Geodesic distance calculations using Vincenty's formulae:
        http://en.wikipedia.org/wiki/Vincenty%27s_formulae
    
    Default values used (WGS84):
    https://github.com/axiom-data-science/pygc/blob/master/pygc/gc.py
        - Semi-major axis: 6378137.0
        - Semi-minor axis: 6356752.3142
    Therefore:
        - Flattening: 0.0033528106718309896
        - Inverse flattening: 298.2572229328697
    
    """
    
    res = great_distance(start_latitude=startlat, start_longitude=startlong, 
                        end_latitude=endlat, end_longitude=endlong)
    
    return float(res['distance'])
    

def grcrcl3(lon_1, lat_1, lon_2, lat_2):
    """
    Geodesic distance computation with GeographicLib 
    (python interface to GeographicLib C++ library)
    http://geographiclib.sourceforge.net/html/other.html#python
    
    Geodesic distance calculations using Charles Karney 
    geodesic algorithms:
        C. F. F. Karney, Algorithms for Geodesics, 
            J. Geodesy 87(1), 43–55 (Jan. 2013)
    
    Default values used (WGS84):
    http://geographiclib.sourceforge.net/html/Constants_8hpp_source.html
        - Semi-major axis: 6378137.0
        - Inverse flattening: 298.257223563
    Therefore:
        - Semi-minor axis: 6356752.314245179
        - Flattening: 0.0033528106647474805
    
    """
    
    res = Geodesic.WGS84.Inverse(lat_1,lon_1,lat_2,lon_2)
    
    return res['s12']


def printResults(input_coords):
    """
    Print formatted results
    
    """
    
    lon_1, lat_1, lon_2, lat_2 = input_coords
    
    dist1 = grcrcl1(lon_1, lat_1, lon_2, lat_2)
    dist2 = grcrcl2(lon_1, lat_1, lon_2, lat_2)
    dist3 = grcrcl3(lon_1, lat_1, lon_2, lat_2)
    
    print("Distances for: lon_1 {0}, lat_1 {1}, lon_2 {2}, lat_2 {3}\n".format(lon_1, lat_1, lon_2, lat_2))
    print("Pyproj___________________________{:,.10f} m\n".format(dist1))
    print("Pygc_____________________________{:,.10f} m\n".format(dist2))
    print("GeographicLib____________________{:,.10f} m\n".format(dist3))
    print("Difference Pyproj,Pygc___________{:.15f} m\n".format(abs(dist1 - dist2)))
    print("Difference Pyproj,GeographicLib__{:.15f} m\n".format(abs(dist1 - dist3)))
    print("Difference GeographicLib,Pygc____{:.15f} m\n".format(abs(dist3 - dist2)))
    print("------------------------------------------\n")


def main():
    
    data = [
            [-3.6,40.5,-118.4,33.9],
            [-6.,37.,-145.,11.],
            [-150.,37.,140.,11.],
            [-50.,7.,40.,11.],
            [-100.,80.,-140.,30.],
            [-3.6,40.5,-80.38,25.78],
            [-3.6,40.5,-0.5,51.5]
        ]

    list(map(printResults, data))



if __name__ == '__main__':
  main()
