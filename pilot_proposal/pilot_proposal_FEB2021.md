# Pilot project: 3D visualizations of circumstellar and circumplanetary disks

**Team members**: Bayron Portilla (RUG), Michiel Min (SRON), Christian Rab (Max Planck), Inga Kamp (RUG), Rens Waters (RU), Carsten Dominik (UvA)

**SURF advisor**: BL de Vries

Proto-planetary disks are disk-like structures around young and newly formed stars. Planets can form from the dust and gas in these disks. Studying the infrared radiation of these systems can help us understand many properties of the disk (disk mass, composition, disk structure to name a few) which is important to understand how and in what form planets are formed. Observed infrared spectra are modelled using increasingly complicated software packages. One such a package is MCMax3D. It uses Monte-Carlo techniques to determine the temperature and pressure in the disk using different radiations sources in the system (for example a star in the center). The geometry that MCMax3D is able to model is more complex than was possible with the 2D variant MCMax2D, used a few years ago. In Fig. 1 a visualization of a model from MCMax2D is shown. It has a central star surrounded by two disks (an inner and outer disk with a gap in between). 

| ![](images/fig1.png?raw=true) | 
|:--:| 
| **Figure 1**: Visualization of a MCMax2D model with a cutout using Blender. Explore in 3D: https://sketchfab.com/3d-models/making-a-disk-test-5e9e641264a04c44a1ae8508d070a7b1  |

In MCMax3D the user is able to define several circumstellar disks centered either on a central star or on another point. The different disks can also have different angles with respect to the equatorial plane. One example of such a model in which we are interested is a star with several disks centered on the central star and a disk surrounding a planet in the system. 

The complicated models that come from MCMax3D, make defining, checking and analyzing these models difficult and possibly error-prone. 3D visualizations are a way to inspect and analyze such complex 3D models. Being able to inspect the model from all angles and make cutouts to see the interior (see Fig. 1 as an example of a simpler model) will help tremendously. Making 3D models of the calculations, its computational complex grids and rich outputs requires special expertise not present in the research team and the expertise from SURF to help tackle this problem is requested.

We envision a software package that is able to generate a full 3D model from the output files of MCMax3D which works for all possible input parameters of MCMax3D. Likely this would be outside the scope of this pilot project, but such a general solution would be ideal. This pilot project will function as a first test to see if such a thing would be possible for MCMax3D. We propose an agile approach and first make a 3D “sketch” model of an input file. This is already useful to inspect what the geometry of your model looks like and if it is correct. Then we will make a 3D model of a computed model from one interesting and specific star. This model will use several of the complicating geometrical features of MCMax3D.

## Summary of goals
-	Generate a 3D model based on the MCMax3D input file to better understand the orientation of the zones before needing to run expensive computations.
-	If useful, make a general and easy to use tool of the input file visualization.
-	Generate a 3D model of PDS70 visualizing pressure and temperature of one species.
-	Investigate how to add several other dust and gas species into the 3D visualization.
-	(Build towards a general tool to visualize MCMax3D output files)
