import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import numpy as np
from damask import Grid
from damask import seeds


dx = 4E-06    # grid spacing

d = 32E-06    # diameter of the grain

r = d/2.0

grain_vol = (4.0/3.0)*np.pi*(r**(3.0)) # vol of a grain

cells_per_grain = grain_vol/(dx**3.0)    # need to keep this number constant

cells_per_grain_int = round(cells_per_grain)  # rounding it off
print ("Cells per grain =>", cells_per_grain_int)

# cells for the geometry

number_of_grains = 80

total_cells_needed = number_of_grains*cells_per_grain_int

cells_x = round((total_cells_needed)**(1.0/3.0))

cells = np.array([cells_x,cells_x,cells_x])
size = cells*dx

print("Cells =>", cells)
print("Size =>", size)

# creating the actual geometry
seeds = seeds.from_random(size,number_of_grains,cells)
grid  = Grid.from_Voronoi_tessellation(cells,size,seeds,periodic=True)    #always make periodic
grid.material = grid.material + 1
grid.save(f'rves/Polycrystal_{number_of_grains}_{cells[0]}x{cells[1]}x{cells[2]}')