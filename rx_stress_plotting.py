import sys
sys.path.append('/nethome/storage/raid2/o.okewale/damask/python')
import h5py
import numpy as np
import matplotlib.pyplot as plt
import damask
import os

def createDirectory(dir:str):
    if not os.path.exists(dir):
        os.makedirs(dir)



# 0. Set the array mapping 'grain numbers' to 'cells'
all_simulations = [
[
    [20,14,5],
    [20,18,4],
    [20,24,3]
],
[
    [40,18,5],
    [40,22,4],
    [40,30,3]
],
[
    [60,20,5],
    [60,26,4],
    [60,34,3]
],
[
    [20,14,5],
    [40,18,5],
    [60,20,5]
],
[
    [20,18,4],
    [40,22,4],
    [60,26,4]
],
[
    [20,24,3],
    [40,30,3],
    [60,34,3]
],
[
    [20,70,1],
    [20,36,2],
    [20,18,4],
    [20,9,8]
],
[
    [10,14,4],
    [98,30,4],
    [955,64,4]
],
[
    [955,32,8],
    [955,64,4]
],
[
    [955,32,8,4900],
    [512,26,8,5100],
    [98,15,8,6000],
    [10,7,8,5900]
],
[
    [10,7,8,6000],
    [98,15,8,6000],
    [512,26,8,6000],
    [955,32,8,6000]
]
]

def checkSameSimulations(simulations):
    prev_number = 0
    for simu in simulations:
        if prev_number == 0:
            prev_number = simu[0]
        else:
            if (prev_number != simu[0]):
                return False
    return True

# print(checkSameSimulations(all_simulations[6]))

def plotRXTimeResults(simulations):
    simulation_base_path = '/nethome/o.okewale/examples/sim_results'
    markers = [".","o","*","v","p",">","d","+","x","s"]
    label_prefix = ""
    is_same_grains = False
    if (checkSameSimulations(simulations)):
        label_prefix = f'{simulations[0][0]} grains: '
        is_same_grains = True
    else:
        label_prefix = f'{simulations[0][2]} $\mu$m grid spacing: '

    plt_datas = []

    out_file_name_prefix = ''
    for index,simulation in enumerate(simulations):
        grains = simulation[0]
        cell = simulation[1]
        dx_spacing = simulation[2]
        stand_number = 2000 if len(simulation) < 4 else simulation[3]

        out_file_name_prefix = f'{out_file_name_prefix}{grains}-{cell}_'

        filename = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
        input_file = f'{simulation_base_path}/{filename}/{stand_number}_stand/CA_files/5.0/.fractions.txt'

        if not is_same_grains:
            legend_label = f'{grains} grains - [{cell}x{cell}x{cell}]'
        else:
            legend_label = f'{dx_spacing} $\mu$m'

        plt_data = {
            'time': [],
            'fraction': [],
            'label': legend_label,
            'markers': markers[index]
        }
        with open(input_file) as f:
            lines = f.readlines()
            plt_data['time'] = [round(float(line.split()[0]),2) for line in lines]
            plt_data['fraction'] = [round(float(line.split()[1]),2) for line in lines]
        plt_datas.append(plt_data)
        # print(plt_data)
        

    plt.figure()
    for data in plt_datas:
        plt.plot(data['time'], data['fraction'], linestyle='-', label=data['label'], marker=data['markers'])
    plt.xlabel('$t$ (s)')
    plt.ylabel('$X$')
    plt.legend(loc='lower right')
    plt.title(f"{label_prefix}RX fraction - time plot")
    plt.savefig(f'{output_folder}/{out_file_name_prefix}rx_fractions_plot.png', bbox_inches='tight')


def plotStressStrainResults(simulations):
    simulation_base_path = '/nethome/o.okewale/examples/sim_results'
    fname_suffix = 'tensionX'
    markers = [".","o","*","v","p",">","d","+","x","s"]
    label_prefix = ""
    is_same_grains = False
    if (checkSameSimulations(simulations)):
        label_prefix = f'{simulations[0][0]} grains: '
        is_same_grains = True
    else:
        label_prefix = f'{simulations[0][2]} $\mu$m grid spacing: '

    plt_datas = []
    out_file_name_prefix = ''
    for index,simulation in enumerate(simulations):
        grains = simulation[0]
        cell = simulation[1]
        dx_spacing = simulation[2]

        out_file_name_prefix = f'{out_file_name_prefix}{grains}-{cell}_'
        file_name = f'Polycrystal_{grains}_{cell}x{cell}x{cell}'
        
        if not is_same_grains:
            legend_label = f'{grains} grains - [{cell}x{cell}x{cell}]'
        else:
            legend_label = f'{dx_spacing} $\mu$m'

        plt_data = {
            'stress': [],
            'strain': [],
            'incs': [],
            'label': legend_label,
            'markers': markers[index]
        }

        input_file = f'{simulation_base_path}/{file_name}/simulation/{file_name}_{fname_suffix}.hdf5'

        d = damask.Result(input_file)

        d.add_stress_Cauchy()
        d.add_strain()
        d.add_equivalent_Mises('sigma')
        d.add_equivalent_Mises('epsilon_V^0.0(F)')
                    
        f = h5py.File(d.fname)
                    
        for path in d.get_dataset_location('sigma_vM'):
            # plt_data['incs'].append(path.split('/')[0])
            plt_data['stress'].append(np.average(f[path])/1e6)
        for path in d.get_dataset_location('epsilon_V^0.0(F)_vM'):
            plt_data['strain'].append(np.average(f[path]))
        
        # plt_data['stress'] = [np.average(s) for s in d.get('sigma_vM').values()]
        # plt_data['strain'] = [np.average(e) for e in d.get('epsilon_V^0.0(F)_vM').values()]
        
        plt_datas.append(plt_data)

    plt.figure()
    # plt.plot(strain_list, stress_list, linestyle="-.")
    for data in plt_datas:
        plt.plot(data['strain'], data['stress'], linestyle='-', label=data['label'], marker=data['markers'])
    plt.ylabel('$\sigma$ (MPa)')
    plt.xlabel('$\epsilon$')
    plt.legend(loc='lower right')
    plt.title(f"{label_prefix}stress-strain plot")
    plt.savefig(f'{output_folder}/{out_file_name_prefix}stress_strain_plot.png', bbox_inches='tight')


# 1. Create the plot directory if it doesn't exist
output_folder = 'plots'
createDirectory(output_folder)

# # 2. Run through the simulations
# for simul in all_simulations:
#     plotRXTimeResults(simul)
#     plotStressStrainResults(simul)

# # 2b. Run just one
plotRXTimeResults(all_simulations[len(all_simulations)-1])
plotStressStrainResults(all_simulations[len(all_simulations)-1])
# plotRXTimeResults(all_simulations[3])
# plotStressStrainResults(all_simulations[3])