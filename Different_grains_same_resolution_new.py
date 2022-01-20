import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import numpy as np
from damask import Grid
from damask import seeds

""" 
Note:
    There are two ways to increase size:
    1. by increasing the number of grains relative to a constant number of cells per grain (grid spacing and grain volume remain constant)
    2. by increasing the number of cells per grain relative to a constant number of grains (increase grain volume - grid spacing remains constant)

    To increase resolution:
    1. decrease/increase the grid spacing (dx) and keep the grain volume constant thereby increasing/decreasing the number of cells per grain
"""

dx = 3E-06    # grid spacing

d = 32E-06    # diameter of the grain

r = d/2.0

grain_vol = (4.0/3.0)*np.pi*(r**(3.0)) # vol of a grain

cells_per_grain = grain_vol/(dx**3.0)    # need to keep this number constant

cells_per_grain_int = round(cells_per_grain)  # rounding it off
print ("Cells per grain =>", cells_per_grain_int)

# cells for the geometry
def generateRVE(start=20,end=60,increment=20, iteration_count=0, initial_volume=0):
    number_of_grains = start + (increment * iteration_count)
    if (number_of_grains <= end):
        
        total_cells_needed = number_of_grains*cells_per_grain_int
        print("Total cells needed =>", total_cells_needed)

        cells_x = round((total_cells_needed)**(1.0/3.0))

        cells = np.array([cells_x,cells_x,cells_x])
        size = cells*dx
        if initial_volume == 0:
            initial_volume = (cells_x ** 3.0)/number_of_grains
        else:
            number_of_grains = round((cells_x ** 3.0)/initial_volume)

        print("Cells =>", cells)
        print("Size =>", size)
        print("Number of grains =>", number_of_grains)

        # creating the actual geometry
        genrated_seeds = seeds.from_random(size,number_of_grains,cells)
        grid  = Grid.from_Voronoi_tessellation(cells,size,genrated_seeds,periodic=True)    #always make periodic
        grid.material = grid.material + 1
        grid.save(f'rves/mid_hd/Polycrystal_{number_of_grains}_{cells[0]}x{cells[1]}x{cells[2]}')

        generateRVE(start, end, increment, iteration_count+1,initial_volume)

generateRVE(20,60,20) # generate the RVEs for the grain number passed