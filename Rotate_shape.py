import os
import vtk

# Function to create a textured face for a cube
def create_textured_face(image_path, origin, point1, point2):
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return None

    reader = vtk.vtkJPEGReader()
    reader.SetFileName(image_path)

    texture = vtk.vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())
    texture.InterpolateOn()

    plane = vtk.vtkPlaneSource()
    plane.SetOrigin(*origin)
    plane.SetPoint1(*point1)
    plane.SetPoint2(*point2)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)

    return actor


# Define cube face coordinates and initial images
cube_faces = [
    {"image": "", "origin": [-0.5, -0.5, -0.5], "point1": [0.5, -0.5, -0.5], "point2": [-0.5, 0.5, -0.5]},
    {"image": "", "origin": [-0.5, -0.5, 0.5], "point1": [0.5, -0.5, 0.5], "point2": [-0.5, 0.5, 0.5]},
    {"image": "", "origin": [-0.5, -0.5, -0.5], "point1": [-0.5, 0.5, -0.5], "point2": [-0.5, -0.5, 0.5]},
    {"image": "", "origin": [0.5, -0.5, -0.5], "point1": [0.5, 0.5, -0.5], "point2": [0.5, -0.5, 0.5]},
    {"image": "", "origin": [-0.5, 0.5, -0.5], "point1": [0.5, 0.5, -0.5], "point2": [-0.5, 0.5, 0.5]},
    {"image": "", "origin": [-0.5, -0.5, -0.5], "point1": [0.5, -0.5, -0.5], "point2": [-0.5, -0.5, 0.5]},
]

# List of images to cycle through
images_to_cycle = ["harambee_logo2.jpg", "amentum.jpg"]
current_image_index = 0  # Start with the first image

# Translation parameters
translation = [0.0, 0.0, 0.0]  # Initial translation values

# Set up the rendering environment
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)  # Background color: dark blue

# Create a list of actors for the cube faces
actors = []
for face in cube_faces:
    face["image"] = images_to_cycle[current_image_index]
    actor = create_textured_face(face["image"], face["origin"], face["point1"], face["point2"])
    if actor:
        actors.append(actor)
        renderer.AddActor(actor)

# Set up the camera to focus on the center of the cube
camera = vtk.vtkCamera()
camera.SetPosition(2, 2, 2)  # Set a position that views the cube from a diagonal angle
camera.SetFocalPoint(0, 0, 0)  # Focus on the cube's center
camera.SetViewUp(0, 0, 1)  # Ensure the camera's up direction is consistent
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Transform for rotating and translating the cube
transform = vtk.vtkTransform()
angle_x = 0
angle_y = 0
angle_z = 0

# Function to update textures
def update_textures():
    global current_image_index

    current_image_index = (current_image_index + 1) % len(images_to_cycle)
    new_image = images_to_cycle[current_image_index]

    for i, actor in enumerate(actors):
        reader = vtk.vtkJPEGReader()
        if not os.path.exists(new_image):
            print(f"Image not found: {new_image}")
            continue

        reader.SetFileName(new_image)
        texture = vtk.vtkTexture()
        texture.SetInputConnection(reader.GetOutputPort())
        texture.InterpolateOn()
        texture.Update()

        actor.SetTexture(texture)

    print(f"Updated cube textures to image: {new_image}")

# Function to rotate the cube
def rotate_cube():
    global angle_x, angle_y, angle_z

    # Increment rotation angles
    angle_x = (angle_x + 1) % 360
    angle_y = (angle_y + 1) % 360
    angle_z = (angle_z + 1) % 360

    transform.Identity()
    transform.Translate(*translation)  # Apply translation to the cube
    transform.RotateX(angle_x)
    transform.RotateY(angle_y)
    transform.RotateZ(angle_z)

    for actor in actors:
        actor.SetUserTransform(transform)

# Function to handle key press events for translation
def keypress_callback(obj, event):
    global translation
    key = obj.GetKeySym()

    if key == "Left":
        translation[0] -= 0.1
    elif key == "Right":
        translation[0] += 0.1
    elif key == "Up":
        translation[1] += 0.1
    elif key == "Down":
        translation[1] -= 0.1
    elif key == "w":
        translation[2] += 0.1
    elif key == "s":
        translation[2] -= 0.1

    print(f"Translation updated to: {translation}")

# Timer callback for both rotation and texture update
def timer_callback(obj, event):
    rotate_cube()
    if angle_x % 360 == 0:  # Change texture every full rotation
        update_textures()
    render_window.Render()

# Start the rendering loop
def start_render_loop():
    render_window.Render()

    render_window_interactor.Initialize()
    render_window_interactor.CreateRepeatingTimer(10)  # Timer interval in ms
    render_window_interactor.AddObserver("TimerEvent", timer_callback)
    render_window_interactor.AddObserver("KeyPressEvent", keypress_callback)  # Add keypress event
    render_window_interactor.Start()


# Run the render loop
start_render_loop()




### GOOD ATTEMPT 5 ###
# import os
# import vtk
#
# # Function to create a textured face for a cube
# def create_textured_face(image_path, origin, point1, point2):
#     if not os.path.exists(image_path):
#         print(f"Image not found: {image_path}")
#         return None
#
#     reader = vtk.vtkJPEGReader()
#     reader.SetFileName(image_path)
#
#     texture = vtk.vtkTexture()
#     texture.SetInputConnection(reader.GetOutputPort())
#     texture.InterpolateOn()
#
#     plane = vtk.vtkPlaneSource()
#     plane.SetOrigin(*origin)
#     plane.SetPoint1(*point1)
#     plane.SetPoint2(*point2)
#
#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection(plane.GetOutputPort())
#
#     actor = vtk.vtkActor()
#     actor.SetMapper(mapper)
#     actor.SetTexture(texture)
#
#     return actor
#
# # Define cube face coordinates and initial images
# cube_faces = [
#     {"image": "", "origin": [0, 0, 0.5], "point1": [1, 0, 0.5], "point2": [0, 1, 0.5]},
#     {"image": "", "origin": [1, 0, -0.5], "point1": [0, 0, -0.5], "point2": [1, 1, -0.5]},
#     {"image": "", "origin": [0, 1, -0.5], "point1": [1, 1, -0.5], "point2": [0, 1, 0.5]},
#     {"image": "", "origin": [0, 0, -0.5], "point1": [1, 0, -0.5], "point2": [0, 0, 0.5]},
#     {"image": "", "origin": [0, 0, -0.5], "point1": [0, 1, -0.5], "point2": [0, 0, 0.5]},
#     {"image": "", "origin": [1, 0, 0.5], "point1": [1, 1, 0.5], "point2": [1, 0, -0.5]},
# ]
#
# # List of images to cycle through
# images_to_cycle = ["harambee_logo2.jpg", "craig.jpg", "cody.jpg", "jordyn.jpg"]
# current_image_index = 0  # Start with the first image
#
# # Set up the rendering environment
# renderer = vtk.vtkRenderer()
# renderer.SetBackground(0.1, 0.2, 0.4)  # Background color: dark blue
#
# # Create a list of actors for the cube faces
# actors = []
# for face in cube_faces:
#     face["image"] = images_to_cycle[current_image_index]
#     actor = create_textured_face(face["image"], face["origin"], face["point1"], face["point2"])
#     if actor:
#         actors.append(actor)
#         renderer.AddActor(actor)
#
# # Set up the camera to ensure the cube remains in view
# camera = vtk.vtkCamera()
# camera.SetPosition(2, 2, 2)  # Set a position that views the cube from a diagonal angle
# camera.SetFocalPoint(0, 0, 0)  # Focus on the cube's center
# camera.SetViewUp(0, 0, 1)  # Ensure the camera's up direction is consistent
# renderer.SetActiveCamera(camera)
# renderer.ResetCamera()
#
# render_window = vtk.vtkRenderWindow()
# render_window.AddRenderer(renderer)
# render_window.SetSize(800, 600)
#
# render_window_interactor = vtk.vtkRenderWindowInteractor()
# render_window_interactor.SetRenderWindow(render_window)
#
# # Transform for rotating the cube
# transform = vtk.vtkTransform()
# angle_x = 0
# angle_y = 0
# angle_z = 0
#
# # Function to update textures
# def update_textures():
#     global current_image_index
#
#     current_image_index = (current_image_index + 1) % len(images_to_cycle)
#     new_image = images_to_cycle[current_image_index]
#
#     for i, actor in enumerate(actors):
#         reader = vtk.vtkJPEGReader()
#         if not os.path.exists(new_image):
#             print(f"Image not found: {new_image}")
#             continue
#
#         reader.SetFileName(new_image)
#         texture = vtk.vtkTexture()
#         texture.SetInputConnection(reader.GetOutputPort())
#         texture.InterpolateOn()
#         texture.Update()
#
#         actor.SetTexture(texture)
#
#     print(f"Updated cube textures to image: {new_image}")
#
# # Function to rotate the cube
# def rotate_cube():
#     global angle_x, angle_y, angle_z
#
#     # Increment rotation angles
#     angle_x = (angle_x + 1) % 360
#     angle_y = (angle_y + 1) % 360
#     angle_z = (angle_z + 1) % 360
#
#     transform.Identity()
#     transform.Translate(0,0,0)  # Set the rotation point at the cube's center
#     transform.RotateX(angle_x)
#     transform.RotateY(angle_y)
#     transform.RotateZ(angle_z)
#
#     for actor in actors:
#         actor.SetUserTransform(transform)
#
# # Timer callback for both rotation and texture update
# def timer_callback(obj, event):
#     rotate_cube()
#     if angle_x % 360 == 0:  # Change texture every full rotation
#         update_textures()
#     render_window.Render()
#
# # Start the rendering loop
# def start_render_loop():
#     render_window.Render()
#
#     render_window_interactor.Initialize()
#     render_window_interactor.CreateRepeatingTimer(10)  # Timer interval in ms
#     render_window_interactor.AddObserver("TimerEvent", timer_callback)
#     render_window_interactor.Start()
#
#
# # Run the render loop
# start_render_loop()
#




### rotates slightly offscreen
# import os
# import vtk
#
# # Function to create a textured face for a cube
# def create_textured_face(image_path, origin, point1, point2):
#     if not os.path.exists(image_path):
#         print(f"Image not found: {image_path}")
#         return None
#
#     reader = vtk.vtkJPEGReader()
#     reader.SetFileName(image_path)
#
#     texture = vtk.vtkTexture()
#     texture.SetInputConnection(reader.GetOutputPort())
#     texture.InterpolateOn()
#
#     plane = vtk.vtkPlaneSource()
#     plane.SetOrigin(*origin)
#     plane.SetPoint1(*point1)
#     plane.SetPoint2(*point2)
#
#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection(plane.GetOutputPort())
#
#     actor = vtk.vtkActor()
#     actor.SetMapper(mapper)
#     actor.SetTexture(texture)
#
#     return actor
#
#
# # Define cube face coordinates and initial images
# cube_faces = [
#     {"image": "", "origin": [0, 0, 0.5], "point1": [1, 0, 0.5], "point2": [0, 1, 0.5]},
#     {"image": "", "origin": [1, 0, -0.5], "point1": [0, 0, -0.5], "point2": [1, 1, -0.5]},
#     {"image": "", "origin": [0, 1, -0.5], "point1": [1, 1, -0.5], "point2": [0, 1, 0.5]},
#     {"image": "", "origin": [0, 0, -0.5], "point1": [1, 0, -0.5], "point2": [0, 0, 0.5]},
#     {"image": "", "origin": [0, 0, -0.5], "point1": [0, 1, -0.5], "point2": [0, 0, 0.5]},
#     {"image": "", "origin": [1, 0, 0.5], "point1": [1, 1, 0.5], "point2": [1, 0, -0.5]},
# ]
#
# # List of images to cycle through
# images_to_cycle = ["harambee_logo2.jpg", "craig.jpg", "cody.jpg", "jordyn.jpg"]
# current_image_index = 0  # Start with the first image
#
# # Set up the rendering environment
# renderer = vtk.vtkRenderer()
# renderer.SetBackground(0.1, 0.2, 0.4)  # Background color: dark blue
#
# # Create a list of actors for the cube faces
# actors = []
# for face in cube_faces:
#     face["image"] = images_to_cycle[current_image_index]
#     actor = create_textured_face(face["image"], face["origin"], face["point1"], face["point2"])
#     if actor:
#         actors.append(actor)
#         renderer.AddActor(actor)
#
# render_window = vtk.vtkRenderWindow()
# render_window.AddRenderer(renderer)
# render_window.SetSize(800, 600)
#
# render_window_interactor = vtk.vtkRenderWindowInteractor()
# render_window_interactor.SetRenderWindow(render_window)
#
# # Transform for rotating the cube
# # Transform for rotating the cube
# transform = vtk.vtkTransform()
# angle_x = 0
# angle_y = 0
# angle_z = 0
#
#
# # Function to update textures
# def update_textures():
#     global current_image_index
#
#     current_image_index = (current_image_index + 1) % len(images_to_cycle)
#     new_image = images_to_cycle[current_image_index]
#
#     for i, actor in enumerate(actors):
#         reader = vtk.vtkJPEGReader()
#         if not os.path.exists(new_image):
#             print(f"Image not found: {new_image}")
#             continue
#
#         reader.SetFileName(new_image)
#         texture = vtk.vtkTexture()
#         texture.SetInputConnection(reader.GetOutputPort())
#         texture.InterpolateOn()
#         texture.Update()
#
#         actor.SetTexture(texture)
#
#     print(f"Updated cube textures to image: {new_image}")
#
# # Function to rotate the cube
#
# def rotate_cube():
#     global angle_x, angle_y, angle_z
#
#     # Increment rotation angles
#     angle_x = (angle_x + 1) % 360
#     angle_y = (angle_y) % 360
#     angle_z = (angle_z + 1) % 360
#
#     transform.Identity()
#     transform.RotateX(angle_x)
#     transform.RotateY(angle_y)
#     transform.RotateZ(angle_z)
#
#     for actor in actors:
#         actor.SetUserTransform(transform)
#
# # Timer callback for both rotation and texture update
# def timer_callback(obj, event):
#     rotate_cube()
#     if angle_x % 360 == 0:  # Change texture every full rotation
#         update_textures()
#     render_window.Render()
#
# # Start the rendering loop
# def start_render_loop():
#     render_window.Render()
#
#     render_window_interactor.Initialize()
#     render_window_interactor.CreateRepeatingTimer(10)  # Timer interval in ms
#     render_window_interactor.AddObserver("TimerEvent", timer_callback)
#     render_window_interactor.Start()
#
#
# # Run the render loop
# start_render_loop()
#

### att  4 - texture error when rotation is applied
# import os
# import vtk
# import random
#
# # Function to create a textured face for a cube
# def create_textured_face(image_path, origin, point1, point2):
#     reader = vtk.vtkJPEGReader()
#     if not os.path.exists(image_path):
#         print(f"Image not found: {image_path}")
#         return None
#
#     reader.SetFileName(image_path)
#
#     texture = vtk.vtkTexture()
#     texture.SetInputConnection(reader.GetOutputPort())
#     texture.InterpolateOn()
#
#     plane = vtk.vtkPlaneSource()
#     plane.SetOrigin(*origin)
#     plane.SetPoint1(*point1)
#     plane.SetPoint2(*point2)
#
#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection(plane.GetOutputPort())
#
#     actor = vtk.vtkActor()
#     actor.SetMapper(mapper)
#     actor.SetTexture(texture)
#
#     return actor
#
# # Define cube face coordinates and initial images
# cube_faces = [
#     {"image": "", "origin": [0, 0, 0.5], "point1": [1, 0, 0.5], "point2": [0, 1, 0.5]},
#     {"image": "", "origin": [1, 0, -0.5], "point1": [0, 0, -0.5], "point2": [1, 1, -0.5]},
#     {"image": "", "origin": [0, 1, -0.5], "point1": [1, 1, -0.5], "point2": [0, 1, 0.5]},
#     {"image": "", "origin": [0, 0, -0.5], "point1": [1, 0, -0.5], "point2": [0, 0, 0.5]},
#     {"image": "", "origin": [0, 0, -0.5], "point1": [0, 1, -0.5], "point2": [0, 0, 0.5]},
#     {"image": "", "origin": [1, 0, 0.5], "point1": [1, 1, 0.5], "point2": [1, 0, -0.5]},
# ]
#
# # List of images to cycle through
# images_to_cycle = ["harambee_logo2.jpg", "craig.jpg", "cody.jpg", "jordyn.jpg"]
# current_image_index = 0  # Start with the first image
#
# # Set up the rendering environment
# renderer = vtk.vtkRenderer()
# renderer.SetBackground(0.1, 0.2, 0.4)  # Background color: dark blue
#
# # Create a list of actors for the cube faces
# actors = []
# for face in cube_faces:
#     face["image"] = images_to_cycle[current_image_index]
#     actor = create_textured_face(face["image"], face["origin"], face["point1"], face["point2"])
#     if actor:
#         actors.append(actor)
#         renderer.AddActor(actor)
#
# render_window = vtk.vtkRenderWindow()
# render_window.AddRenderer(renderer)
# render_window.SetSize(800, 600)
#
# render_window_interactor = vtk.vtkRenderWindowInteractor()
# render_window_interactor.SetRenderWindow(render_window)
#
# # Transform for rotating the cube
# transform = vtk.vtkTransform()
#
# # Define a vertex as the rotation pivot point
# pivot_point = [0, 0, 0]  # One vertex of the cube
#
# # Function to update textures
# def update_textures():
#     global current_image_index
#
#     current_image_index = (current_image_index + 1) % len(images_to_cycle)
#     new_image = images_to_cycle[current_image_index]
#     print(f"Updating cube faces to use image: {new_image}")
#
#     for i, face in enumerate(cube_faces):
#         reader = vtk.vtkJPEGReader()
#         if not os.path.exists(new_image):
#             print(f"Image not found: {new_image}")
#             continue
#
#         reader.SetFileName(new_image)
#         texture = vtk.vtkTexture()
#         texture.SetInputConnection(reader.GetOutputPort())
#         texture.InterpolateOn()
#
#         actors[i].SetTexture(texture)
#
#     render_window.Render()
#
# # Function to rotate the cube
# def rotate_cube():
#     angle = 1  # Incremental rotation angle in degrees
#
#     # Move to pivot point
#     transform.Translate(-pivot_point[0], -pivot_point[1], -pivot_point[2])
#
#     # Rotate around the axes
#     transform.RotateX(angle)
#     transform.RotateY(angle)
#     # transform.RotateZ(angle)
#
#     # Move back to original position
#     transform.Translate(pivot_point[0], pivot_point[1], pivot_point[2])
#
#     for actor in actors:
#         actor.SetUserTransform(transform)
#
#     render_window.Render()
#
# # Timer callback for rotation
# def rotation_timer_callback(obj, event):
#     rotate_cube()
#
# # Function to start rendering loop
# def start_render_loop():
#     render_window_interactor.Initialize()
#     render_window.Render()
#
#     # Timer for rotation updates every 10 ms
#     render_window_interactor.CreateRepeatingTimer(10)
#     render_window_interactor.AddObserver("TimerEvent", rotation_timer_callback)
#
#     render_window_interactor.Start()
#
#
# def timer_callback(obj, event):
#     update_textures()  # Only update textures when the timer event triggers
#
# # Function to start rendering loop
# def start_texture_loop():
#     # Initialize the render window interactor and the render window
#     render_window_interactor.Initialize()
#     render_window.Render()
#
#     # Create a repeating timer for texture updates every 5 seconds (5000 ms)
#     render_window_interactor.CreateRepeatingTimer(5000)  # 5000 ms = 5 seconds
#
#     # Bind the timer callback to the timer event
#     render_window_interactor.AddObserver("TimerEvent", timer_callback)
#
#     # Start the render window interaction loop (this will handle events like mouse and keyboard inputs)
#     render_window_interactor.Start()
#
#
# start_texture_loop()
# # Run the render loop
# start_render_loop()






#### att 2. - this works with picture replacement for image uploading on to the cube ##
import os
import vtk
import time
import threading

# Function to create a textured face for a cube
def create_textured_face(image_path, origin, point1, point2):
    reader = vtk.vtkJPEGReader()
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return None

    reader.SetFileName(image_path)

    texture = vtk.vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())
    texture.InterpolateOn()

    plane = vtk.vtkPlaneSource()
    plane.SetOrigin(*origin)
    plane.SetPoint1(*point1)
    plane.SetPoint2(*point2)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)

    return actor

# Define cube face coordinates and initial images (placeholders)
cube_faces = [
    {"image": "", "origin": [0, 0, 0.5], "point1": [1, 0, 0.5], "point2": [0, 1, 0.5]},
    {"image": "", "origin": [1, 0, -0.5], "point1": [0, 0, -0.5], "point2": [1, 1, -0.5]},
    {"image": "", "origin": [0, 1, -0.5], "point1": [1, 1, -0.5], "point2": [0, 1, 0.5]},
    {"image": "", "origin": [0, 0, -0.5], "point1": [1, 0, -0.5], "point2": [0, 0, 0.5]},
    {"image": "", "origin": [0, 0, -0.5], "point1": [0, 1, -0.5], "point2": [0, 0, 0.5]},
    {"image": "", "origin": [1, 0, 0.5], "point1": [1, 1, 0.5], "point2": [1, 0, -0.5]},
]

# List of images to cycle through
images_to_cycle = ["harambee_logo2.jpg", "craig.jpg", "cody.jpg", "jordyn.jpg"]
current_image_index = 0  # Start with the first image

# Set up the rendering environment
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)  # Background color: dark blue

# Create a list of actors for the cube faces
actors = []
for face in cube_faces:
    # Temporarily use the first image
    face["image"] = images_to_cycle[current_image_index]
    actor = create_textured_face(face["image"], face["origin"], face["point1"], face["point2"])
    if actor:
        actors.append(actor)
        renderer.AddActor(actor)

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Function to update textures when spacebar is pressed
def update_textures():
    global current_image_index

    # Cycle to the next image
    current_image_index = (current_image_index + 1) % len(images_to_cycle)

    # Update all cube face textures
    new_image = images_to_cycle[current_image_index]
    print(f"Updating cube faces to use image: {new_image}")

    for i, face in enumerate(cube_faces):
        # Update the actor's texture
        reader = vtk.vtkJPEGReader()
        if not os.path.exists(new_image):
            print(f"Image not found: {new_image}")
            continue

        print(f"Loading image: {new_image}")
        reader.SetFileName(new_image)

        texture = vtk.vtkTexture()
        texture.SetInputConnection(reader.GetOutputPort())
        texture.InterpolateOn()
        texture.Update()  # Make sure the texture is fully loaded

        # Check if the texture is loaded properly
        if texture.GetInput() is None:
            print(f"Texture loading failed for image: {new_image}")
            continue

        # Set the texture on the actor
        actors[i].SetTexture(texture)

    # Re-render the scene to apply changes
    render_window.Render()

# Timer callback function
def timer_callback(obj, event):
    update_textures()  # Only update textures when the timer event triggers

# Function to start rendering loop
def start_render_loop():
    # Initialize the render window interactor and the render window
    render_window_interactor.Initialize()
    render_window.Render()

    # Create a repeating timer for texture updates every 5 seconds (5000 ms)
    render_window_interactor.CreateRepeatingTimer(5000)  # 5000 ms = 5 seconds

    # Bind the timer callback to the timer event
    render_window_interactor.AddObserver("TimerEvent", timer_callback)

    # Start the render window interaction loop (this will handle events like mouse and keyboard inputs)
    render_window_interactor.Start()

# # Function to start rendering loop


# Run the render loop
start_render_loop()



# Spacebar event to trigger texture update
# def keypress_callback(obj, event):
#     key = obj.GetKeySym()
#     if key == "space":
#         update_textures()
#
# # Bind the spacebar event
# render_window_interactor.AddObserver("KeyPressEvent", keypress_callback)

# Start the rendering loop
# render_window_interactor.Initialize()
# render_window.Render()
# render_window_interactor.Start()

# while True:
#     update_textures()
#     render_window_interactor.CreateRepeatingTimer(5000)  # Re-trigger every 5 seconds



#### this one is original and good ##########
# import vtk
# import os
#
#
# def create_textured_face(image_path, origin, point1, point2):
#     # Load the image as a texture
#     reader = vtk.vtkJPEGReader()
#     reader.SetFileName(image_path)
#
#     texture = vtk.vtkTexture()
#     texture.SetInputConnection(reader.GetOutputPort())
#     texture.InterpolateOn()
#
#     # Create a plane for the cube face
#     plane = vtk.vtkPlaneSource()
#     plane.SetOrigin(*origin)
#     plane.SetPoint1(*point1)
#     plane.SetPoint2(*point2)
#
#     # Create a mapper and actor for the face
#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection(plane.GetOutputPort())
#
#     actor = vtk.vtkActor()
#     actor.SetMapper(mapper)
#     actor.SetTexture(texture)
#
#     return actor
#
#
# # Define cube face coordinates
# cube_faces = [
#     # Front face
#     {"image": "harambee_logo2.jpg", "origin": [0, 0, 0.5], "point1": [1, 0, 0.5], "point2": [0, 1, 0.5]},
#     # Back face
#     {"image": "harambee_logo2.jpg", "origin": [1, 0, -0.5], "point1": [0, 0, -0.5], "point2": [1, 1, -0.5]},
#     # Top face
#     {"image": "harambee_logo2.jpg", "origin": [0, 1, -0.5], "point1": [1, 1, -0.5], "point2": [0, 1, 0.5]},
#     # Bottom face
#     {"image": "harambee_logo2.jpg", "origin": [0, 0, -0.5], "point1": [1, 0, -0.5], "point2": [0, 0, 0.5]},
#     # Left face
#     {"image": "harambee_logo2.jpg", "origin": [0, 0, -0.5], "point1": [0, 1, -0.5], "point2": [0, 0, 0.5]},
#     # Right face
#     {"image": "harambee_logo2.jpg", "origin": [1, 0, 0.5], "point1": [1, 1, 0.5], "point2": [1, 0, -0.5]},
# ]
#
#
# # Set up the rendering environment
# renderer = vtk.vtkRenderer()
# renderer.SetBackground(0.1, 0.2, 0.4)  # Background color: dark blue
#
# # Add each textured face to the renderer
# for face in cube_faces:
#     actor = create_textured_face(face["image"], face["origin"], face["point1"], face["point2"])
#     renderer.AddActor(actor)
#
# render_window = vtk.vtkRenderWindow()
# render_window.AddRenderer(renderer)
# render_window.SetSize(800, 600)  # Window size in pixels
#
# render_window_interactor = vtk.vtkRenderWindowInteractor()
# render_window_interactor.SetRenderWindow(render_window)
#
# # Start the visualization
# render_window.Render()
# render_window_interactor.Start()
#



# import vtk
#
# # Create a cube
# cube = vtk.vtkCubeSource()
#
# # Set the position and size of the cube (optional)
# cube.SetXLength(1.0)  # Length along the X-axis
# cube.SetYLength(1.0)  # Length along the Y-axis
# cube.SetZLength(1.0)  # Length along the Z-axis
#
# # Create a mapper and actor
# mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputConnection(cube.GetOutputPort())
#
# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
#
# # Set up the rendering environment
# renderer = vtk.vtkRenderer()
# renderer.AddActor(actor)
# renderer.SetBackground(0.1, 0.2, 0.4)  # Background color: dark blue
#
# render_window = vtk.vtkRenderWindow()
# render_window.AddRenderer(renderer)
# render_window.SetSize(800, 600)  # Window size in pixels
#
# render_window_interactor = vtk.vtkRenderWindowInteractor()
# render_window_interactor.SetRenderWindow(render_window)
#
# # Start the visualization
# render_window.Render()
# render_window_interactor.Start()



# import cv2
# import numpy as np
# from scipy.ndimage import affine_transform
# import random
#
#
# def get_random_rotation_matrix():
#     # Generate random rotation angles for each axis
#     x_angle = np.radians(random.uniform(-90, 90))
#     y_angle = np.radians(random.uniform(-90, 90))
#     z_angle = np.radians(random.uniform(-90, 90))
#
#     # Rotation matrix around the X-axis
#     Rx = np.array([[1, 0, 0],
#                    [0, np.cos(x_angle), -np.sin(x_angle)],
#                    [0, np.sin(x_angle), np.cos(x_angle)]])
#
#     # Rotation matrix around the Y-axis
#     Ry = np.array([[np.cos(y_angle), 0, np.sin(y_angle)],
#                    [0, 1, 0],
#                    [-np.sin(y_angle), 0, np.cos(y_angle)]])
#
#     # Rotation matrix around the Z-axis
#     Rz = np.array([[np.cos(z_angle), -np.sin(z_angle), 0],
#                    [np.sin(z_angle), np.cos(z_angle), 0],
#                    [0, 0, 1]])
#
#     # Combine the rotations
#     R = Rz @ Ry @ Rx
#     return R
#
#
# def rotate_image_3d(image, rotation_matrix):
#     # Get image dimensions
#     h, w = image.shape[:2]
#     depth = max(h, w)
#
#     # Create a 3D grid for the image
#     coords = np.array(np.meshgrid(np.arange(w), np.arange(h), [0]))
#     coords = np.vstack((coords[0].ravel(), coords[1].ravel(), coords[2].ravel(), np.ones((w * h,))))
#
#     # Apply rotation matrix to coordinates
#     rotated_coords = rotation_matrix @ coords[:3]
#     rotated_coords = rotated_coords[:2] / rotated_coords[2]  # Perspective division
#
#     # Transform the image using affine transform
#     rotated_image = affine_transform(image, rotation_matrix[:2, :2], offset=rotation_matrix[:2, 2])
#     return rotated_image
#
#
# def main():
#     # Load an image
#     image_path = "your_image.jpg"  # Replace with your image path
#     image = cv2.imread(image_path)
#     if image is None:
#         print("Error loading image.")
#         return
#
#     # Generate a random 3D rotation matrix
#     rotation_matrix = get_random_rotation_matrix()
#
#     # Apply the rotation
#     rotated_image = rotate_image_3d(image, rotation_matrix)
#
#     # Show the result
#     cv2.imshow("Original Image", image)
#     cv2.imshow("Rotated Image", rotated_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     main()
