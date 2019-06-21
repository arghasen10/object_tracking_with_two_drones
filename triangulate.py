from math import sin,cos

def triangulate(glat,glng,galt,lat1,lng1,alt1,yaw1,pitch1,lat2,lng2,alt2,yaw2,pitch2):

    x1, y1, z1, l1, m1, n1 = find_lenpara(glat,glng,galt,lat1,lng1,alt1,yaw1,pitch1)
    x2, y2, z2, l2, m2, n2 = find_lenpara(glat,glng,galt,lat2,lng2,alt2,yaw2,pitch2)
    h1 = l1 * l1 + m1 * m1 + n1 * n1
    h2 = l2 * l2 + m2 * m2 + n2 * n2
    k10 = (pow(x1,2)*(pow(n1,2)+pow(m1,2))+pow(y1,2)*(pow(l1,2)+pow(n1,2))+pow(z1,2)*(pow(m1,2)+pow(l1,2))-2*n1*m1*y1*z1-2*n1*l1*x1*z1-2*m1*l1*x1*y1)/h1+(pow(x2,2)*(pow(n2,2)+pow(m2,2))+pow(y2,2)*(pow(l2,2)+pow(n2,2))+pow(z2,2)*(pow(m2,2)+pow(l2,2))-2*n2*m2*y2*z2-2*n2*l2*x2*z2-2*m2*l2*x2*y2)/h2
    k4 = (-2*x1*n1*n1 - 2*x1*m1*m1 +2*n1*l1*z1+2*m1*l1*y1)/h1+(-2*x2*n2*n2 - 2*x2*m2*m2 +2*n2*l2*z2+2*m2*l2*y2)/h2
    k5 = (-2*y1*l1*l1 - 2*y1*n1*n1 +2*n1*m1*z1+2*m1*l1*x1-2*y1*l1*l1)/h1 + ((-2*y2*l2*l2 - 2*y2*n2*n2 +2*n2*m2*z2+2*m2*l2*x2-2*y2*l2*l2)/h2)
    k6 = (-2*z1*m1*m1 - 2*z1*l1*l1 +2*n1*m1*y1+2*n1*l1*x1)/h1+(-2*z2*m2*m2 - 2*z2*l2*l2 +2*n2*m2*y2+2*n2*l2*x2)/h2
    k7 = -2*m1*l1/h1 - 2*m2*l2/h2
    k8 = -2*n1*l1/h1 - 2*n2*l2/h2
    k9 = -2*n1*m1/h1 - 2*n2*m2/h2
    k1 = (n1*n1 + m1*m1)/h1 + (n2*n2+m2*m2)/h2
    k2 = (l1*l1 + n1*n1)/h1 + (n2*n2+m2*m2)/h2
    k3 = (n1*n1 + m1*m1)/h1 + (n2*n2+m2*m2)/h2
    #find px,py,pz from cramers rule.
def find_lenpara(glat,glng,galt,lat,lng,alt,yaw,pitch):
    x,y = find_dist(glat,glng,lat,lng)
    z = galt - alt
    sinp = sin(pitch)
    l = sinp*cos(yaw)
    m = sinp*sin(yaw)
    n = cos(pitch)
    return x,y,z,l,m,n



def find_dist(glat,glng,lat,lng):                   #Find distance between two lat,lng
    x = glat-lat
    y = glng-lng
    return x,y

glat = 0
glng = 0galt = 0
lat1 = 0
lng1 = 0
alt1 = 0
yaw1 = 0
pitch1 = 0
lat2 = 0
lng2 = 0
alt2 =0
yaw2 =0
pitch2 = 0

triangult(glat,glng,galt,lat1,lng1,alt1,yaw1,pitch1,lat2,lng2,alt2,yaw2,pitch2)
