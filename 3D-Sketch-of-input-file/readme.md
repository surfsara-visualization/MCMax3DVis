# MCMax3D Sketch

## What it does
The script ```MCMax3D-sketch.py``` can generate a 3D sketch from an MCMax3D input file using Blender. The script can be executed through the command-line.

| ![](readme_images/render_from_x_direction.png?raw=true) | 
|:--:| 
| **Figure 1**: Example of a sketch from ```MCMax3D-sketch.py```  |


## How to run
- Install Blender 2.8+: www.blender.org
- Download or clone ```MCMax3D-sketch.py``` to your machine
- Run in the terminal: ```<blender executable> -b -P MCMax3D-sketch.py -- -f <your MCMax3D inputfile>```
	- ```-b```: specifies that you want to run Blender in the background
	- ```-P```: specifies that you want to run a Python script
	- ```--```: starts the command-line options that will be given to the ```MCMax3D-sketch.py``` script
	- ```-f```: this will specifies the input file to be used by the script
- This command will create an output directory: ```output_<name of your input file>```, which contains:
	- ```model.blender``` / ```model.glb``` / ```model.obj```: this is the 3D model in three different formats (Blender file, a gltf file and an obj file)
	- ```render_from_-x_direction.png```: A render by a camera located at (x,y,z) = (- Rmax * camera_distance, 0, 0). Where standard camera_distance = 5. 
	- ```render_from_x_direction.png```: A render by a camera located at (x,y,z) = (Rmax * camera_distance, 0, 0). Where standard camera_distance = 5. 
	- ```render_from_z_direction.png```: A render by a camera located at (x,y,z) = (0, 0, Rmax * camera_distance). Where standard camera_distance = 5. 
	- ```Rmax```: is the size of the radius of the largest zone in the model

## Finding your Blender executable
This depends on where you installed Blender and what OS you are running. For me on mac it is: ```/Applications/Blender.app/Contents/MacOS/Blender```. 

So an example command would look like: ```/Applications/Blender.app/Contents/MacOS/Blender -b -P MCMax3D-sketch.py -- -f <your MCMax3D inputfile>```. 

If you are having problems starting Blender from the command-line, see these docs: https://docs.blender.org/manual/en/latest/advanced/command_line/index.html

## Optional commandline options:
- You can specify your own output directory with ```-o```: ```<blender executable> -b -P MCMax3D-sketch.py -- -f <your MCMax3D inputfile> - <your output directory>```
- You can specify your own camera distance ```-c```: ```<blender executable> -b -P MCMax3D-sketch.py -- -f <your MCMax3D inputfile> -c 10``` 
	The distance if the camera is now ```10*Rmax``` instead of the default ```5*Rmax```. 