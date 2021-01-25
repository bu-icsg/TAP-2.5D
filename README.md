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

## How to run TAP-2.5D
### Prerequisites
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
- **grid_thermal_map.pl**, a script for thermal map visualization
- **tofig.pl**, a script for floorplan file (.flp) visualization

### Configurations

### Usage

### Publications
[1] Yenai Ma, Leila Delshadtehrani, Cansu Demirkiran, Jose L. Abellan and Ajay Joshi, “TAP-2.5D: A Thermally-Aware Chiplet Placement Methodology for 2.5D Systems,” to appear in *Proc. Design, Automation and Test in Europe (DATE)* 2021. [pdf](http://people.bu.edu/joshi/files/Ma_TAP-2.5D-DATE2021.pdf)

[2] R. Zhang, M. R. Stan, and K. Skadron, "HotSpot 6.0: Validation, Acceleration and Extension." *University of Virginia, Tech. Report CS-2015-04*. [pdf](http://www.cs.virginia.edu/~skadron/Papers/HotSpot60_TR.pdf)

[3] A. Coskun, F. Eris, A. Joshi, A. B. Kahng, Y. Ma*, A. Narayan and V. Srinivas, “Cross-Layer Co-Optimization of Network Design and Chiplet Placement in 2.5D Systems,” in *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, vol. 39, no. 12, pp. 5183-5196*, Dec. 2020. (*Lead Author). [pdf](http://people.bu.edu/joshi/files/Ma_TCAD_2020.pdf)

[4] A. Coskun, F. Eris*, A. Joshi, A. Kahng, Y. Ma and V. Srinivas, “A Cross-Layer Methodology for Design and Optimization of Networks in 2.5D Systems,” in *Proc. International Conference on Computer-Aided Design (ICCAD)* 2018. (*Lead Author). [pdf](http://people.bu.edu/joshi/files/interposer-nw-iccad-2018.pdf)

[5] CPLEX Python API Reference Manual. [link](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/refpythoncplex/html/frames.html)


