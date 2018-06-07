import matplotlib.pyplot as plt
import numpy as np
import shapefile as shp

from datetime import datetime
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize, rgb2hex
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap


SHAPE_FILE = "shapes/ne_110m_v4/ne_110m_admin_0_countries_lakes"
# BIGGER_SHAPE_FILE = "shapes/ne_10m_v4/ne_10m_admin_0_countries_lakes"
SHAPE_READING_FIELD = "countries"


def extract_countries():
    sf = shp.Reader(SHAPE_FILE, SHAPE_READING_FIELD)
    countries = list()
    for shape in list(sf.iterRecords()):
        country = shape[3]
        if country not in countries:
            countries.append(country)
    return countries


def draw_countries(countries, user):
    m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180, resolution='c')
    fig, ax = plt.subplots()
    m.readshapefile(SHAPE_FILE, SHAPE_READING_FIELD)

    vmin, vmax = 0, max(countries.values(), key=lambda i: i)
    norm = Normalize(vmin=vmin, vmax=vmax)
    colors = {}
    cmap = plt.cm.cool_r
    coloured_countries = list()

    for shapedict in m.countries_info:
        statename = shapedict['SOVEREIGNT']
        if statename not in coloured_countries and statename in countries.keys():
            comp = countries[statename]
            colors[statename] = cmap(np.sqrt((comp - vmin) / (vmax - vmin)))[:3]
            coloured_countries.append(statename)

    for seg, info in zip(m.countries, m.countries_info):
        if info['SOVEREIGNT'] in countries.keys():
            color = rgb2hex(colors[info['SOVEREIGNT']])
            poly = Polygon(seg, facecolor=color)
            ax.add_patch(poly)

    plt.title('Map of {}\'s most listened countries'.format(user))

    ax_c = fig.add_axes([0.2, 0.1, 0.6, 0.03])
    cb = ColorbarBase(ax_c, cmap=cmap, norm=norm, orientation='horizontal',
                      label=r'[number of scrobbles per country]')

    # plt.show()
    filename = 'maps/map_' + user + '_' + str(datetime.now().time())[:8] + '.png'
    plt.savefig(filename, dpi=800)
    return filename


if __name__ == '__main__':
    # countries = {
    #     'Russia': 4,
    #     'United States of America': 7,
    #     'Sweden': 6,
    #     'Australia': 1,
    #     'China': 3,
    #     'India': 8,
    #     'Germany': 7,
    #     'England': 9,
    #     'Poland': 4,
    #     'Egypt': 6,
    #     'Turkey': 1,
    #     'Canada': 2,
    # }
    # draw_countries(countries, 'me')
    extract_countries()
    pass
