import subprocess

# Chemin vers l'exécutable Vivado
vivado_path = "C:\\Xilinx\\Vivado\\2022.2\\bin\\vivado"

# Commandes TCL à exécuter dans Vivado
tcl_commands = """
close_design
read_vhdl -vhdl2008 ./sources/utilitaires_inf3500_pkg.vhd
read_vhdl -vhdl2008 ./sources/generateur_horloge_precis.vhd
read_vhdl -vhdl2008 ./sources/monopulseur.vhd
read_vhdl -vhdl2008 ./sources/ascenseur_bonus.vhd
read_vhdl -vhdl2008 ./sources/top_labo_3.vhd
read_xdc ./xdc/basys_3_top.xdc
synth_design -top top_labo_3 -part xc7a35tcpg236-1 -assert
place_design
route_design
write_bitstream -force top_labo_3.bit
open_hw_manager
connect_hw_server
get_hw_targets
open_hw_target
current_hw_device [get_hw_devices xc7a35t_0]
set_property PROGRAM.FILE {top_labo_3.bit} [get_hw_devices xc7a35t_0]
program_hw_devices [get_hw_devices xc7a35t_0]
close_hw_manager
"""

# Générer le fichier de script TCL
with open("commands.tcl", "w") as script_file:
    script_file.write(tcl_commands)

# Construire la commande pour exécuter Vivado avec le script TCL
command = f'{vivado_path} -mode tcl -source commands.tcl'

# Exécuter la commande
process = subprocess.run(command, shell=True)

if process.returncode == 0:
    print("Les commandes TCL ont été exécutées avec succès.")
else:
    print("Il y a eu une erreur lors de l'exécution des commandes TCL.")
