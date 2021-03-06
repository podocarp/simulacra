import json
import sys

import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from pylab import *

with open('settings.json') as f:
    settings = json.load(f)
    R = settings['R']   # helmholtz coil radius
    sR = settings['sR']  # small coil radius
    viewport = settings['viewport']  # plot goes -v to v.
    helmholtz = settings['helmholtz']
    dipole = settings['dipole']
    contoursettings = settings['contour']
    quiversettings = settings['quiver']

# These control the spacing of the coils. The 3 arguments (a, b, n) specify the
# coils are made up of n turns of wire evenly spaced from coordinates z=a to
# z=b. Setting n=0 turns off that coil.
coilspacing = linspace(helmholtz['from'], helmholtz['to'], helmholtz['number'])
smallcoilspacing = linspace(dipole['from'], dipole['to'], dipole['number'])

# Ratio of strength of large coil to small coil to compensate. For example if
# the large coil has 1000 turns and the small coil only 1 turn, we can set this
# to 200, while simulating only 5 turns for the large coil (using the options
# above). Or, we can just simulate 1 turn and set this to 1000. It can also be
# used to compensate for current settings.
ratio = helmholtz['ratio']

xaxis, yaxis, zaxis = None, None, None
x, y, z = None, None, None

def initaxes(nx, ny, nz):
    global x, y ,z
    global xaxis, yaxis, zaxis
    xaxis = linspace(-viewport, viewport, nx)
    yaxis = linspace(-viewport, viewport, ny)
    zaxis = linspace(-viewport, viewport, nz)
    x, y, z = meshgrid(xaxis, yaxis, zaxis)

def simulate(nx, ny, nz, dtheta):
    initaxes(nx,ny,nz)
    bx = zeros((nx, ny, nz))
    by = zeros((nx, ny, nz))
    bz = zeros((nx, ny, nz))

    def biotsavart(R, n, coilspacing, I = 1):
        nonlocal bx,by,bz

        for theta in range(0, 360, dtheta):
            theta = theta / 180 * pi
            xc = R * cos(theta)
            yc = R * sin(theta)
            for loop in coilspacing:
                z0 = z - n * (R / 2 + loop)
                mag = I / sqrt((x - xc)**2 + (y - yc)**2 + z0**2)**3
                bx += -z0 * cos(theta) * mag
                by += -z0 * sin(theta) * mag
                bz += ((x - xc) * cos(theta) + (y - yc) * sin(theta)) * mag

    biotsavart(R, -1, coilspacing, ratio)
    biotsavart(R, 1, coilspacing, ratio)
    biotsavart(sR, 0, smallcoilspacing)

    return bx,by,bz

# spherical coordinates used later
phi = mgrid[0:2*pi:30j]
#### CONTOUR PLOTTING (CROSS SECTION)
def contourplot():
    plt.figure(num = 1, figsize = (8, 8))
    div = contoursettings['resolution']
    bx,by,bz = simulate(div, div, div, contoursettings['dtheta'])

    # magnitudes
    c = sqrt(bx**2 + by**2 + bz**2)

    # We are plotting the magnitude in a plane parallel to the yz axis down the
    # middle of the setup.
    c = c[div//2-1]
    c /= c[div//2-1,div//2-1]

    # draw contour lines and also dots to represent the cross section of the coil
    cp = contour(yaxis, zaxis, c, levels=contoursettings['levels'])
    scatter((R/2,-R/2,R/2,-R/2), (R,R,-R,-R), s = 20, color = "black")
    # small circle for dipole
    plot(sR*cos(phi), sR*sin(phi), color="black")

    clabel(cp, manual=True, inline=False, fmt="%1.2f", fontsize="20", rightsize_up=False)
    savefig("coil_contour.svg")
    plt.show()

def quiverplot():
    global viewport
    viewport = 20
    div = quiversettings['resolution']
    fig_3d = plt.figure(num = 2, figsize = (10, 8))
    ax = fig_3d.gca(projection='3d')
    bx,by,bz = simulate(div, div, div, quiversettings['dtheta'])

    # dark magic to make the colors work
    c = sqrt(bx**2 + by**2 + bz**2)
    c = c.ravel()
    c = concatenate((c, np.repeat(c, 2)))
    norm = matplotlib.colors.LogNorm()
    norm.autoscale(c)
    cmap = plt.get_cmap("inferno")
    c = cmap(norm(c))
    sc = cm.ScalarMappable(norm=norm, cmap=cmap)
    sc.set_array([])

    ax.quiver(x,y,z,bx,by,bz, colors = c, length=3, normalize = True)
    colorbar(sc)

    # draw the coils and sphere dipole traces when rotating
    for n in -1, 1:
        for loop in coilspacing:
            ax.plot(R*cos(phi), R*sin(phi), n * (R/2 + loop), color='#c75d12')
    for loop in smallcoilspacing:
        ax.plot(sR*cos(phi), sR*sin(phi), sR/2 + loop, color='#694734')

    xlabel('x (cm)')
    ylabel('y (cm)')
    savefig("coil_multiple.svg")
    plt.show()

if (contoursettings['plot?'] == 1):
    contourplot()
if (quiversettings['plot?'] == 1):
    quiverplot()
