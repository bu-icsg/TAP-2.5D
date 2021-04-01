# TAP-2.5D

## Overview
TAP-2.5D is an EDA tool to determine the thermally-aware chiplet placement for heterogeneous 2.5D systems.
This tool uses a simulated annealing based algorithm to search for a chiplet placement solution that minimizes the total inter-chiplet wirelength and the system temperature.
We use HotSpot-6.0 [2] for thermal simulation and our self-developed routing optimization tool (MILP) [1, 3, 4] for wirelength estimation.
In this document, we provide a guideline for running TAP-2.5D [1].

As a first step, clone the repository:
```
git clone https://github.com/bu-icsg/TAP-2.5D.git
```

## Prerequisites
Our TAP-2.5D is written in Python 3. A python version 3.6.5 or later will work.
Our routing optimization uses IBM CPLEX python API [5]. A python cplex package version of 12.8 or later will work.
An example of loading python and cplex (change the module names to the correct versions and package names you installed) before running TAP-2.5D:
```
$ module load python3/3.6.5
$ module load cplex/12.8_ac
```

We use HotSpot-6.0 [2] for thermal simulations. Under util/ directory, we place 4 files from the HotSpot-6.0 simulator [2], as follows:
- **hotspot**, a binary file compiled from HotSpot-6.0
- **hotspot.config**, a copy of HotSpot-6.0 default config file
- **grid_thermal_map.pl**, a script for thermal map (.grid.steady) visualization
- **tofig.pl**, a script for floorplan file (.flp) visualization

## Configurations

We use .cfg file to describe a target 2.5D system. We place three examples under configs/ directory, which we used for the case studies in our paper [1].
Here we briefly describe the options in the .cfg file.

### [general]
- **path**: the directory we save the output files.
- **placer_granularity**: the granularity of the occupation matrix grid, in unit of *mm*.
- **initial_placement**: *"bstree"* (generate initial placement using B*-tree and fastSA approach); *"given"* (a hack to evaluate temperature and wirelength for a dedicated placement, the simulated annealing process is skipped).
- **decay**: simulated annealing decay factor, it should be greater than 0 and less than 1.

### [interposer]
- **intp_type**: interposer type, currently we only support *"passive"*
- **intp_size**: interposer size, in unit of *mm*.
- **link_type**: *"nppl"* (non-pipelined repeaterless inter-chiplet link); *"ppl"* (gas-station inter-chiplet link).

### [chiplets]
- **chiplet_count**: the number of chiplets in the 2.5D system.
- **widths**: the width of each chiplet, separated by ",".
- **heights**: the height of each chiplet, separated by ",".
- **powers**: the power of each chiplet, separated by ",".
- **connections**: the connection matrix of chiplets. The i-th row and j-th column in the matrix is the bandwidth from chiplet i to chiplet j.
- **x**: the x-coordinate of each chiplet. It is not used in *"bstree"* initial placement, but is required for *"given"* initial placement.
- **y**: the y-coordinate of each chiplet. It is not used in *"bstree"* initial placement, but is required for *"given"* initial placement.

## How to run TAP-2.5D to search for thermally-aware chiplet placement solution
The usage of running TAP-2.5D is as follows:
```
$ python sim_annealing.py [-c <config-file>] [-d <outputdir>] [-g <options>] [-h]
```

The command line arguments are optional:
- **-h**: print usage information.
- **-c**: specify the target .cfg file. If not specified, the default config file is *configs/example.cfg*.
- **-d**: overwrite the output directory (*"path"* in the .cfg file).
- **-g**: overwrite the arguments in the .cfg file. For example, *"-g intp_size=45 -g decay=0.9"*. We currently support overwrite arguments of *intp_size*, *link_type*, *x*, *y*, and *decay*.

For example, to save output files to './output/ascend910/' and use system configuration of configs/ascend910.cfg, and set *intp_size* to 45 and *decay* to 0.9, we can type the command:
```
$ python sim_annealing.py -c configs/ascend910.cfg -d output/ascend910/ -g intp_size=45 -g decay=0.9
```

### How to evaluate a 2.5D system with given chiplet layout.
We provide a shortcut to help generating floorplan desciption files with provided 2.5D system configuration (.cfg), and evaluate the thermal profile and wirelength for the given 2.5D system. To do that, a user needs to provide a system configuration file (.cfg) with informations of the widths, heights, powers, x-/y-coordinates of all chiplets. To launch the evaluation of temperature and wirelength of the system, we can type the command:
```
$ python config.py [-c configs/target_system.cfg] [-d <outputdir>] [-g <options>]
```

## Publications
[1] Y. Ma, L. Delshadtehrani, C. Demirkiran, J. L. Abellan and A. Joshi, “TAP-2.5D: A Thermally-Aware Chiplet Placement Methodology for 2.5D Systems,” in *Proc. Design, Automation and Test in Europe (DATE)* 2021. [pdf](http://people.bu.edu/joshi/files/Ma_TAP-2.5D-DATE2021.pdf)

[2] R. Zhang, M. R. Stan, and K. Skadron, "HotSpot 6.0: Validation, Acceleration and Extension." *University of Virginia, Tech. Report CS-2015-04*. [pdf](http://www.cs.virginia.edu/~skadron/Papers/HotSpot60_TR.pdf)

[3] A. Coskun, F. Eris, A. Joshi, A. B. Kahng, Y. Ma*, A. Narayan and V. Srinivas, “Cross-Layer Co-Optimization of Network Design and Chiplet Placement in 2.5D Systems,” in *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, vol. 39, no. 12, pp. 5183-5196*, Dec. 2020. **(*Lead Author)**. [pdf](http://people.bu.edu/joshi/files/Ma_TCAD_2020.pdf)

[4] A. Coskun, F. Eris*, A. Joshi, A. Kahng, Y. Ma and V. Srinivas, “A Cross-Layer Methodology for Design and Optimization of Networks in 2.5D Systems,” in *Proc. International Conference on Computer-Aided Design (ICCAD)* 2018. **(*Lead Author)**. [pdf](http://people.bu.edu/joshi/files/interposer-nw-iccad-2018.pdf)

[5] CPLEX Python API Reference Manual. [link](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/refpythoncplex/html/frames.html)


