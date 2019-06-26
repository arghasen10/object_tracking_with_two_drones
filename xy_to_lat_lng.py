import math

R = 6378.1 #Radius of the Earth
brng = 1.57 #Bearing is 90 degrees converted to radians.
d = 15

lat1 = math.radians(52.20472) #Current lat point converted to radians
lon1 = math.radians(0.14056) #Current long point converted to radians

lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
     math.cos(lat1)*math.sin(d/R)*math.cos(brng))

lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
             math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

lat2 = math.degrees(lat2)
lon2 = math.degrees(lon2)

print(lat2)
print(lon2)
