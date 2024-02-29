import argparse
import numpy as np
import matplotlib.pyplot as plt

with open('README.md', 'r') as f:
    readme_content = f.read()
# Create the ArgumentParser and set the description
parser = argparse.ArgumentParser(description=readme_content)

# Add an argument
parser.add_argument('--filename', type=str, default="normalization_dea_exported_dea_behavior", help='Filename for export (default: %(default)s)')
parser.add_argument('--prestretch_x', type=float, default="1.5", help='Prestretch in x-direction (default: %(default)s)')
parser.add_argument('--prestretch_y', type=float, default="1.5", help='Prestretch in y-direction (default: %(default)s)')
parser.add_argument('--t_membrane', type=float, default="100e-6", help='Membrane thickness (default: %(default)s)')
parser.add_argument('--epsilon_r', type=float, default="2.8", help='Relative dielectric permittivity of the elastomer (default: %(default)s)')
parser.add_argument('--emodulus', type=float, default="1400.4e3", help='Elastic modulus of the elastomer, linearized from nonlinear elastic behavior at the working point, Unit: Pa (default: %(default)s)')
parser.add_argument('--generate_figures', type=bool, default=True, help='Export PNG images of the expansion curve and alpha coefficients (default: %(default)s)')
parser.add_argument('--actuation_min', type=float, default="0", help='Actuation minimum voltage (default: %(default)s)')
parser.add_argument('--actuation_max', type=float, default="5000", help='Actuation maximum voltage (default: %(default)s)')
parser.add_argument('--output_format', type=str, default="Abaqus", help='FEA Software, in which the expansion behavior is used (default: %(default)s)')
# Parse the arguments
args = parser.parse_args()
print(f'The filename for saving is {args.filename}!')


# %% Function definition for plotting
def all_plots(Voltage, file_savename, actuation_strain_xx, actuation_strain_yy, actuation_strain_zz, label_xx, label_yy, label_zz, x_axis_label, y_axis_label):
    figure_for_plotting = plt.figure()
    plt.plot(Voltage, actuation_strain_xx, label=label_xx, linestyle='-')
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.plot(Voltage, actuation_strain_yy, label=label_yy, linestyle='--')
    plt.plot(Voltage, actuation_strain_zz, label=label_zz, linestyle=':')
    plt.grid(True)
    plt.legend()
    plt.show()
    figure_for_plotting.savefig(file_savename, format='png')



# %% Calculation part

t_Membrane0 = args.t_membrane # m
epsilon_0 = 8.854e-12 # As/Vm
epsilon_r = args.epsilon_r # --
E_Membrane = args.emodulus # Pa
Voltage = np.arange(args.actuation_min, (args.actuation_max+1) ).reshape(-1, 1) # V

# Prestretches
prestretch_in_x_direction = args.prestretch_x
prestretch_in_y_direction = args.prestretch_y
# Conversion to prestretch in vertical direction, according to volume constancy
prestretch_in_z_direction = 1 / (prestretch_in_x_direction * prestretch_in_y_direction)
# Prestrains from prestretches
prestrain_in_x_direction = prestretch_in_x_direction - 1
prestrain_in_y_direction = prestretch_in_y_direction - 1
prestrain_in_z_direction = prestretch_in_z_direction - 1
t_Membrane_pre = t_Membrane0 * prestretch_in_z_direction  # Please note: The prestrain changes the initial height of the DEA, which leads to a higher actuation

# Actuation strain from Maxwell stress equation
actuation_strain_zz = -epsilon_0 * epsilon_r * Voltage**2 / (E_Membrane * t_Membrane_pre**2)
actuation_strain_zz_no_prestretch = -epsilon_0 * epsilon_r * Voltage**2 / (E_Membrane * t_Membrane0**2)
# From actuation strain follows strain in the x-y plane
actuation_strain_xx = (1 + actuation_strain_zz)**(-0.5) - 1
actuation_strain_xx_no_prestretch = (1 + actuation_strain_zz_no_prestretch)**(-0.5) - 1
actuation_strain_yy = (1 + actuation_strain_zz)**(-0.5) - 1
actuation_strain_yy_no_prestretch = (1 + actuation_strain_zz_no_prestretch)**(-0.5) - 1

# Plotting
all_plots(Voltage, 'normalization_dea_actuation_strain.png', actuation_strain_xx, actuation_strain_yy, actuation_strain_zz, 'actuation_strain_xx', 'actuation_strain_yy', 'actuation_strain_zz', 'Actuating Voltage V/V', 'Actuation strain')

# Inverting the prestretches
inverted_prestretch_x = prestretch_in_x_direction**(-1)
inverted_prestretch_y = prestretch_in_y_direction**(-1)
inverted_prestretch_z = prestretch_in_z_direction**(-1)
inverted_prestrain_x = inverted_prestretch_x-1
inverted_prestrain_y = inverted_prestretch_y-1
inverted_prestrain_z = inverted_prestretch_z-1

# Total strains
total_strain_xx =  actuation_strain_xx + inverted_prestrain_x
total_strain_yy =  actuation_strain_yy + inverted_prestrain_y
total_strain_zz =  actuation_strain_zz + inverted_prestrain_z

# Plotting
all_plots(Voltage, 'normalization_dea_total_strain.png', total_strain_xx, total_strain_yy, total_strain_zz, 'total_strain_xx', 'total_strain_yy', 'total_strain_zz', 'Actuating Voltage V/V', 'Total strain')


# Define reference voltage and stimulus difference
V_ref = max(Voltage)
Delta_S_range = Voltage/V_ref + 1

# Derive expansion coefficients
alpha_xx = total_strain_xx/Delta_S_range
alpha_yy = total_strain_yy/Delta_S_range
alpha_zz = total_strain_zz/Delta_S_range

# Export to file according to the chosen output format
if args.output_format == 'Abaqus':
    filename = args.filename
    all_alphas = np.column_stack((alpha_xx, alpha_yy, alpha_zz, np.zeros((len(alpha_zz), 3)), Delta_S_range))
    np.savetxt(filename+'.txt', all_alphas, delimiter=' ')
    print(all_alphas)
    print('File saved in Abaqus format as: ' + filename+'.txt')
    # Export for input
    abaqus_material_header='*Material, name=Material-hab_DEA_100_new \n'+'*Elastic' + '\n' + str(args.emodulus/1e6)+',0.45 \n'+'*Expansion, type=ANISO'
    np.savetxt(filename+'_abaqus.inp', header=abaqus_material_header, X=all_alphas, delimiter=' ', comments='')
    print('File saved as Abaqus .inp file for integration as: ' + filename+'_abaqus.inp')

else:
    print('Output format not yet defined. Please contact adrian.ehrenhofer@tu-dresden.de with the specifications.')

# Plotting
all_plots(Delta_S_range, 'normalization_dea_alpha_coefficient.png', alpha_xx, alpha_yy, alpha_zz, 'alpha_xx', 'alpha_yy', 'alpha_zz', 'Stimulus value', 'Expansion coefficient')



