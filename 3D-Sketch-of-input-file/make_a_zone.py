import bpy
import math
import random

zones = [
{
"denstype":'SURFDENSFILE',
"densfile":'surface_density_PDS70.dat',
"Rin":0.05,
"Rout":20.0,
"nr":60,
"nt":50,
"np":60,
"shpow":1.1,
"sh":16.8,
"rsh":120,
"zone_theta":0.0,
"zone_phi":0.0,
"alpha":1.0e-3,
"zone_x":0,
"zone_y":0,
"zone_z":0
},
]


zones = {}

with open('input_with_cpd_spicy.dat', 'r') as reader:
    line = reader.readline()
    while line != '':
        if line.startswith('zone'):#"zone" in line and line[0] != "*":
#            line_splitted = line.split("zone")[1]
            line_splitted = line.split(':')
            zone_nr = line_splitted[0][4].rstrip()
            
            if not zone_nr in zones.keys():
                zones.update({zone_nr:{}}) 
            
            
            zone_par = line_splitted[1].split('=')
            zone_key = zone_par[0].rstrip()
            zone_val = zone_par[1].rstrip()
            
            try:
                zone_val = float(zone_val.replace('d', 'E'))
            except ValueError:
                pass

            if not zone_key in zones[zone_nr].keys():
                zones[zone_nr].update({zone_key:zone_val})

        line = reader.readline()
print(zones)

def drawZone(zone_nr, Rin, Rout, shpow, sh, rsh, zone_theta, zone_phi, zone_x, zone_y, zone_z, rgb_color):

    # First we make the disk in the local coordinates of the zone
    # (Later we will translate the zone using zone_x, zone_y and zone_z 
    # and rotate it using zone_theta and zone_phi)
    vertices = []
    edges = []
    faces = []

    zone_theta = zone_theta/360 * 2*math.pi
    zone_phi = zone_phi/360 * 2*math.pi
    
    r_step = (Rout - Rin)/30

    phi_values = range(0,360, 20)
    # Then we make a slice in the yz-plane
    for phi in phi_values:
        # convert to radians    
        phi = phi/360 * 2*math.pi
        
        # We remember the amount of vertices in the last iteration
        prevLenVerts = len(vertices)
        
        # At every phi value we calculate the x,y,z values of vertices
        # for the different R and theta values. This upper part can then 
        # be mirrored in the xy-plane to make the lower part of the disk
        vertices_upper = []
        vertices_lower = []
        
        # We walk over all the R values and calculate 
        # the x, y, z values of the vertices    
        r=Rin # we start at Rin    
        while r<=Rout:
            z = sh*(r/rsh)**shpow
            theta_up = math.acos(z/r)
            theta_down = math.acos(-z/r)
            
#            theta_up += 2*math.pi * zone_theta/360
#            theta_down += 2*math.pi * zone_theta/360
#            phi += 2*math.pi * zone_phi/360
            
            x_up = r * math.cos(phi) * math.sin(theta_up)
            y_up = r * math.sin(phi) *math.sin(theta_up)
            z_up = r * math.cos(theta_up)

            x_down = r * math.cos(phi) * math.sin(theta_down)
            y_down = r * math.sin(phi) *math.sin(theta_down)
            z_down = r * math.cos(theta_down)

            # Rotation of theta around Y-axis, counter clockwise
            Rx_up = x_up*math.cos(zone_theta) + z_up*math.sin(zone_theta)
            Ry_up = y_up
            Rz_up = -1*x_up*math.sin(zone_theta) + z_up*math.cos(zone_theta)
            Rx_down = x_down*math.cos(zone_theta) + z_down*math.sin(zone_theta)
            Ry_down = y_down
            Rz_down = -1*x_down*math.sin(zone_theta) + z_down*math.cos(zone_theta)            
            
            # Rotation of theta around x-axis, counter clockwise / righthanded
#            Rx_up = x_up
#            Ry_up = y_up*math.cos(zone_theta) - z_up*math.sin(zone_theta)
#            Rz_up = y_up*math.sin(zone_theta) + z_up*math.cos(zone_theta)
#            Rx_down = x_down
#            Ry_down = y_down*math.cos(zone_theta) - z_down*math.sin(zone_theta)
#            Rz_down = y_down*math.sin(zone_theta) + z_down*math.cos(zone_theta)
##            
#            # Rotation of phi around z-axis, counter clockwise / righthanded
            x_up = Rx_up*math.cos(zone_phi) - Ry_up*math.sin(zone_phi)
            y_up = Rx_up*math.sin(zone_phi) + Ry_up*math.cos(zone_phi)
            z_up = Rz_up
            x_down = Rx_down*math.cos(zone_phi) - Ry_down*math.sin(zone_phi)
            y_down = Rx_down*math.sin(zone_phi) + Ry_down*math.cos(zone_phi)
            z_down = Rz_down
            
            
            x_up += zone_x
            y_up += zone_y
            z_up += zone_z
            
            x_down += zone_x
            y_down += zone_y
            z_down += zone_z
            
            vertices_upper.append((x_up,y_up,z_up))
            vertices_lower.append((x_down,y_down,z_down))
            
            r+=r_step #5 # And make 1 AU steps

        # Remember how much vertices will be added
        addedVerts = len(vertices_upper + vertices_lower)

        # Reverse vertices on the lower (negative theta) part
        vertices_lower.reverse()
        # And add them to the upper half to make a loop and 
        # add them to the total collection of vertices
        vertices += vertices_upper + vertices_lower 

        # Make edges between points of different R and theta values
        for i in range(prevLenVerts, len(vertices)-1):
            edges.append((i, i+1))
        edges.append((prevLenVerts, len(vertices)-1))
        
        # Make edges between points of this and the previous phi values
        if phi != 0:
            for i in range(addedVerts):
                edges.append((len(vertices)-addedVerts+i, len(vertices)-2*addedVerts+i))

    # Make edges between the first and last phi value to close the disk
    for i in range(addedVerts):
        edges.append((i, len(vertices)-1*addedVerts+i))

    # Make a mesh and an object to add the vertices to
    ob_name = "disk_"+zone_nr
    # Create new mesh and a new object
    mesh = bpy.data.meshes.new(ob_name + "_Mesh")
    ob = bpy.data.objects.new(ob_name, mesh)
    # Add a material and use the radial size of the disk to give it a color:
    material_name = ob_name+"_mat"
    #if material_name in bpy.data.materials:
    #    mesh.materials.append(bpy.data.materials[material_name])
    #else:
    if zone_x != 0 or zone_y != 0 or zone_z != 0:
        opaque = True
    else: 
        opaque = False
        
    mesh.materials.append(create_material(material_name, Rout-Rin, rgb_color, opaque))

    # Make a mesh from a list of vertices/edges/faces
    mesh.from_pydata(vertices, edges, faces)

    # Display name and update the mesh
    ob.show_name = True
    mesh.update()
    bpy.context.collection.objects.link(ob)

    # We have not yet made the faces. Because we have a
    # clean geometry we can let Blender generate them
    bpy.context.view_layer.objects.active = ob
    # Go to edit mode
    bpy.ops.object.editmode_toggle()
    # Fill holes to generate faces
    bpy.ops.mesh.fill_holes()
    bpy.ops.object.editmode_toggle()
    
    # ADDING VERTEX COLORS
    vertex_colors_name = "col"
    if not mesh.vertex_colors:
        mesh.vertex_colors.new(name=vertex_colors_name)

    color_layer = mesh.vertex_colors[vertex_colors_name]

    # INDEXES in a POLYGON
    # poly.vertices: length is the amount of vertices in the polygon
    #                the values of the elements are the indeces to the vertices in the mesh
    # poly.loop_indices:    - length is also the amount of vertices in the polygon
    #                       - the values of the elements is an index that takes every vertex in a polygon as one unit
    #                         This is useful because every vertex can have a different color in each polygon that it is part of.
    #                         Thus color_layer.data can be indexed using the values in loop_index.

    i=0
    #if vert_colors:
    for poly in mesh.polygons:
        for vert_i_poly, vert_i_mesh in enumerate(poly.vertices):#loop_indices:
            #rgb = [random.random(),0,0,0]
            vert_i_loop = poly.loop_indices[vert_i_poly]
            color_layer.data[vert_i_loop].color = rgb_color#vert_colors[vert_i_mesh]#rgb
            i += 1



def create_material(name, radial_size_disk_to_scale_color, rgb_color, opaque=False):

    print("Making material and shaders")

    # Make material
    mat = bpy.data.materials.new(name)
    if opaque:
        mat.blend_method='OPAQUE'
    else:
        mat.blend_method = 'BLEND' # Alpha Blend, Render polygon transparent, depending on alpha channel of the texture.
    mat.use_nodes = True
    mat.show_transparent_back = False
    nodes = mat.node_tree.nodes

    
    # clear all nodes to start clean
    nodes.clear()

    # Make nodes
    # Color input for the Diffuse BSDF shader
    node_attr = nodes.new(type='ShaderNodeRGB')
    node_attr.location = -400, 60
    node_attr.outputs[0].default_value = rgb_color

    # Vertex color Alpha input for transparency
    node_vertex_color_transparency = nodes.new(type='ShaderNodeValue')
    node_vertex_color_transparency.location = -200, 300
    #node_attr.attribute_name = "pipo2"

    # Transparency BSDF shader
    node_BSDF_transparency = nodes.new(type='ShaderNodeBsdfTransparent')
    node_BSDF_transparency.location = -200, 180

    # BSDF SHader Diffuse
    node_BSDF_shader = nodes.new(type='ShaderNodeBsdfDiffuse')
    node_BSDF_shader.location = -200, 60
    
    # Mixer
    node_shader_mixer = nodes.new(type='ShaderNodeMixShader')
    node_shader_mixer.location = 50, 180

    # Output
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = 250, 180

    # link nodes
    links = mat.node_tree.links
    link = links.new(node_attr.outputs[0], node_BSDF_shader.inputs[0])
    link2 = links.new(node_BSDF_shader.outputs[0], node_shader_mixer.inputs[2])
    link3 = links.new(node_BSDF_transparency.outputs[0], node_shader_mixer.inputs[1])
    link4 = links.new(node_vertex_color_transparency.outputs[0], node_shader_mixer.inputs[0])
    link5 = links.new(node_shader_mixer.outputs[0], node_output.inputs[0])
    
    return mat

    
maxR = 0
opac=0.5
i_color = 0
for key,z in zones.items():
    if i_color == 0:
        rgb_color = (1,0,0,opac)
        i_color += 1
    elif i_color == 1:
        rgb_color = (0,1,0,opac)
        i_color += 1
    elif i_color == 2:
        rgb_color = (1,1,0,opac)
        i_color += 1
    else:
        rgb_color = (0,0,1,opac)
        i_color = 0
        
    if z['Rout'] > maxR:
        maxR = z['Rout']
        
    drawZone(key, z['Rin'], z['Rout'], z['shpow'], z['sh'], z['rsh'], 
                z['theta'], z['phi'], z['x'], z['y'], z['z'], rgb_color)
                
                
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(5*maxR, 0, 0), rotation=(0.5*math.pi, 0, 0.5*math.pi))
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0,0, 5*maxR), rotation=(0, 0, 0.5*math.pi))
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-5*maxR, 0, 0), rotation=(0.5*math.pi, 0, -0.5*math.pi))