# Normalization_DEA: A tool for the normalization of Dielectric Elastomer Actuator (DEA) behavior for implementation in Finite Element Software

The provided software tool is a Python script. It performs the normalization procedure according to [Ehrenhofer2018] and [Franke2020] for prestretched Dielectric Elastomer Actuators (DEAs).

The following input parameters are required:
(1) The actuation range in Volts
(2) Possibly in-plane pre-stretches in x- and y-position.
(3) Mechanical properties, including: The elastic modulus, linearized at the working point. The working point can be (i) the pre-stretched state, or (ii) the relaxed position. Please note that only the elastic modulus of the membrane is taken into account, future versions can also include the influence of electrodes, which are neglected here.
(4) The electrical properties of the membrane.
(5) The required output format: Depending on the Finite Element Analysis tool, the format might differ. By default, a formatting for Abaqus will be given.

The output file is a list of stimulus values and corresponding expansion coefficients, which model the stimulus-active behavior of the pre-stretched DEA. This list is imported to Finite Element tools like Abaqus or Ansys. The temperature change corresponds to a driving voltage that is applied to the pre-stretched DEA, where 0V leads to a pure pre-stretch state.

## Target group:
The tool is provided to engineers and scientists working with Dielectric Elastomer Actuators. For understanding the code, basic math and Python programming is required. Furthermore, the tool is only helpful when the behavior is later applied in a Finite-Element tool like Abaqus, Ansys, FeNICs, etc. The model is very basic (linearized in kinematics and in material behavior, for details see [Franke2020]). For the implementation of other active materials, please refer to [Normalization_Monosensitive].

## Getting started:
The script is run by the following command
```bash
python3 Normalization_DEA.py 
```
which will output a default behavior of a biaxially prestretched DEA with lambda_x=lambda_y=1.5 and Elastosil. The behavior will also be plotted in PNG format. 

The list of arguments can be obtained by
```bash
python3 Normalization_DEA.py --help
```

## Example for Abaqus integration
The file exported by the script can either (i) be read into a material definition in Abaqus CAE, or (ii) referenced in a job-file. 

For (i), perform the following steps: Define a new material, add Mechanical -> Expansion (Type: Anisotropic, Use temperature-dependent data, Rerefence Temperature=0) -> Right click on the Data-table and choose "Read from File" -> Choose the exported .txt file. Furthermore, a material orientation must be defined, such that the z-direction is the DEA out-of-plane-direction. In the LOAD step, create a predefined field at initial step with temperature=0. In the STEP for actuation, add a temperature 1 < T < 2, where 1 stands for a voltage of V=0 (purely pre-stretched state) and 2 stands for V=V_max (maximum actuated state). Please note that this is the implementation of a linear behavior, i.e., the STEP must be defined as NLGEOM=OFF. 

For (ii), the _abaqus.inp-file can directly be added to the Job file. The predefined field definition, material orientation etc. is according to (i). 

## Contributing
I'm happy about any contributions from the community. Besides the usual contribution in the form of forking, creating a branch and pushing it to the repository, you can also contact me directly, e.g., if you need a new output format implemented. I also work on implementing other active materials, the software tools can be found in the current repository. 


## Sources:
[Ehrenhofer2018] Ehrenhofer, A.; Elstner, M. & Wallmersperger, T.
Normalization of Hydrogel Swelling Behavior for Sensoric and Actuatoric Applications, Sensors and Actuators B: Chemical, 2018, 255(2), 1343 - 1353   
[![DOI](https://img.shields.io/badge/DOI-10.1016/j.snb.2017.08.120-blue)](https://doi.org/10.1016/j.snb.2017.08.120)

[Franke2020] Franke, M.; Ehrenhofer, A.; Lahiri, S.; Henke, E.-F. M.; Wallmersperger, T. & Richter, A. Dielectric Elastomer Actuator Driven Soft Robotic Structures with Bioinspired Skeletal and Muscular Reinforcement, Frontiers in Robotics and AI, 2020, 7, 178
[![DOI](https://img.shields.io/badge/DOI-10.3389/frobt.2020.510757-blue)](https://doi.org/10.3389/frobt.2020.510757)


## Final notes:
The software is referenced in Zenodo.
I would be happy about your feedback and comments via Github.
I thank for the DFG for funding the Research Training Group 'Hydrogel-based microsystems', the Free State of Saxony & TU Dresden for the funding of the Dresden Center for Intelligent Materials, and my colleagues at the Institute of Solid Mechanics and the Institute of Semiconductors at TU Dresden for their support. 
