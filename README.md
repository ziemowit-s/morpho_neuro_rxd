Morphological model of neuron with RxD ionic diffusion. Based on NEURON.

# Prerequisites

* Install requirements.txt
* Install NEURON

## MOD compilation
* Before run you must compile mod files and copy compiled folder to the main folder (where run Python files are located)
```bash
nrmivmodl
```

* To help with compilation use compile_mods.sh (Linux only)
  * first param is folder from which to copy files fo current_mods folder
  * Don't forget to add /* at the end, eg.:
```bash
sh compile_mods.sh mods/4p_ach_da_syns/*
``` 
  * If you auto-run from PyCharm - you can config to run compile_mods.sh before each run


# Run

## morpho_diffusion
* Shows how morphological Ca2+ diffusion with RxD and PMCA, NXC pumps works
* Shows diffusion on neuron model in real time
* pumps in this example are naively "floating", meaning - they are not attached to the membrane
```bash
python morpho_diffusion_run.py
```

* Example of Ca2+ diffusion from the spine head to the dendrite
![ca2_diff](img/dendrite_ca2_gif.gif)

## membrane_flux_example
* Shows how membrane pumps works when they are "attached" to the membrane wit RxD
```bash
python membrane_flux_example.py
```

## ebner_cell
* Shows how Ebner2019 cell works
```bash
python ebner_cell_run.py
```

## ebner_ach_da
* Shows how Ebner2019 cell works with additional ACh and DA 
```bash
python ebner_ach_da_run.py
```