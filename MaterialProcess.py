import os.path
from typing import AnyStr
import pathlib
import termcolor
import easygui_qt
materialsFolder = easygui_qt.get_directory_name(title="Select the root folder of Source's VMT materials.")
saveToFolder = easygui_qt.get_directory_name(title="Now, select the Materials folder of Godot game.")

failcounter = []
counter = 0
backslash = "\u005C" # BRUUUUH



def readVMT(fileisVMT: AnyStr | pathlib.PosixPath):
    '''Gets the contents of VMT. Returns a similarly looking VMT structure, but with Python guidelines.'''
    dictionary = {}
    stack = []
    vmttype = ""

    with open(fileisVMT, 'r') as filetoopen:
        for index, line in enumerate(filetoopen, start=0):
            line = line.strip().replace('"', '').split(" ")
            if index == 0: vmttype = line[0]
            else:
                # Skip empty lines
                if not line:
                    continue

                # Skip comments (lines starting with "//")
                if line[0].startswith("//"):
                    continue

                # Handle the start of a block
                if line[0] == '{':
                    if stack:
                        current_block = stack[-1]
                    else:
                        current_block = dictionary
                    stack.append(current_block)

                # Handle key-value pairs
                elif len(line) == 2 and line[0] != '}':
                    key, value = line
                    current_block[key] = value

                # Handle the end of a block
                elif line[0] == '}':
                    stack.pop()

    return dictionary, vmttype

def convertVMT(VMTtype: str, vmt: dict):
    '''Converts VMT into a Godot Material.'''
    global counter
    gdmaterial = '' # Main output
    resources = [] # ext_resouce, mainly textures
    properties = []

    match VMTtype.lower():
        case "lightmappedgeneric":
            color = "1.0, 1.0, 1.0"
            alpha = "1.0"
            for key in vmt:
                match key:
                    # DONT FORGET TO ADD "counter += 1" AT THE END OF CASE IF YOU IMPORT A RESOURCE!!111
                    case "$basetexture":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append(f'albedo_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case "$detail":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append('detail_enabled = true')
                        properties.append(f'detail_albedo = ExtResource("{counter}_hl")')
                        counter += 1
                    case "$envmap":
                        if vmt.get(key) == "env_cubemap": properties.append("metallic_specular = 1")
                    case "$surfaceprop": properties.append(f'resource_name = "{vmt.get(key)}"')
                    case "$color": color = vmt.get(key)
                    case "$alpha": alpha = vmt.get(key)
                    case "$detailblendmode":
                        match vmt.get(key):
                            case 1: properties.append(f'detail_blend_mode = 1')
                            case 8: properties.append(f'detail_blend_mode = 3')
                            case _: properties.append(f'detail_blend_mode = 0')
                    case "$nocull":
                        if vmt.get(key) == 1: properties.append("cull_mode = 2")
                    case "$translucent": properties.append(f"transparency = {vmt.get(key)}")
                    case "$bumpmap":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append('normal_enabled = true')
                        properties.append(f'normal_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case "$nofog":
                        if vmt.get(key) == 1: properties.append('disable_fog = true')
                    case _: print(termcolor.colored(f"Godot might not support {key} - ignoring.", "yellow"))
            properties.append(f'albedo_color = Color({color}, {alpha})')
        case "vertexlitgeneric":
            color = "1.0, 1.0, 1.0"
            alpha = "1.0"
            for key in vmt:
                match key:
                    # DONT FORGET TO ADD "counter += 1" AT THE END OF CASE IF YOU IMPORT A RESOURCE!!111
                    case "$basetexture":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append(f'albedo_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case "$detail":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append('detail_enabled = true')
                        properties.append(f'detail_albedo = ExtResource("{counter}_hl")')
                        counter += 1
                    case "$envmap":
                        if vmt.get(key) == "env_cubemap": properties.append("metallic_specular = 1")
                    case "$color2": color = vmt.get(key)
                    case "$alpha": alpha = vmt.get(key)
                    case "$nocull":
                        if vmt.get(key) == 1: properties.append("cull_mode = 2")
                    case "$translucent": properties.append(f"transparency = {vmt.get(key)}")
                    case "$bumpmap":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append('normal_enabled = true')
                        properties.append(f'normal_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case _: print(termcolor.colored(f"Godot might not support {key} - ignoring.", "yellow"))
            properties.append(f'albedo_color = Color({color}, {alpha})')
        case "unlitgeneric":
            color = "1.0, 1.0, 1.0"
            alpha = "1.0"
            for key in vmt:
                match key:
                    # DONT FORGET TO ADD "counter += 1" AT THE END OF CASE IF YOU IMPORT A RESOURCE!!111
                    case "$basetexture":
                        resources.append(
                            f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append(f'albedo_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case "$color":
                        color = vmt.get(key)
                    case "$translucent": properties.append(f"transparency = {vmt.get(key)}")
                    case "$alpha":
                        alpha = vmt.get(key)
                    case "$surfaceprop": properties.append(f'resource_name = "{vmt.get(key)}"')
                    case _:
                        print(termcolor.colored(f"Godot might not support {key} - ignoring.", "yellow"))
            properties.append(f'albedo_color = Color({color}, {alpha})')
            properties.append('disable_fog = true')
        case "cable":
            for key in vmt:
                match key:
                    # DONT FORGET TO ADD "counter += 1" AT THE END OF CASE IF YOU IMPORT A RESOURCE!!111
                    case "$basetexture":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append(f'albedo_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case "$nocull":
                        if vmt.get(key) == 1: properties.append("cull_mode = 2")
                    case "$bumpmap":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append('normal_enabled = true')
                        properties.append(f'normal_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case _: print(termcolor.colored(f"Godot might not support {key} - ignoring.", "yellow"))
        case "teeth":
            for key in vmt:
                match key:
                    # DONT FORGET TO ADD "counter += 1" AT THE END OF CASE IF YOU IMPORT A RESOURCE!!111
                    case "$basetexture":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append(f'albedo_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case _: print(termcolor.colored(f"Godot might not support {key} - ignoring.", "yellow"))
        case "decalmodulate":
            for key in vmt:
                match key:
                    # DONT FORGET TO ADD "counter += 1" AT THE END OF CASE IF YOU IMPORT A RESOURCE!!111
                    case "$basetexture":
                        resources.append(f'[ext_resource type="Texture2D" path="res://materials/{vmt.get(key).replace(backslash, "/").lower()}.png" id="{counter}_hl"]')
                        properties.append(f'albedo_texture = ExtResource("{counter}_hl")')
                        counter += 1
                    case _: print(termcolor.colored(f"Godot might not support {key} - ignoring.", "yellow"))
        case _:
            print(termcolor.colored("Perhaps you missed something.", "red"))
            failcounter.append(file)

    # Creating the GDMaterial process
    counter += 1
    gdmaterial += f'[gd_resource type="StandardMaterial3D" load_steps=5 format={resources.__len__() + 1} uid="uid://halflifinmaterial{counter}"]'
    gdmaterial += "\n"
    for res in resources:
        gdmaterial += res + "\n"
    gdmaterial += "\n"
    gdmaterial += "[resource]"
    gdmaterial += "\n"
    for prop in properties:
        gdmaterial += prop + "\n"
    return gdmaterial



if materialsFolder is "" or saveToFolder is "":
    easygui_qt.show_text(text="You didn't select one of the folders! You need to select them.", title="Error!")
    print(termcolor.colored("You didn't select one of the folders! You need to select them."), "red")
else:
    for VMT in pathlib.PosixPath(materialsFolder).rglob("*.vmt"):
        print(VMT)
        getVMT = readVMT(VMT)
        print(getVMT[1])
        print()
        file = str(VMT).replace(".vmt", ".tres").replace(materialsFolder, saveToFolder)
        os.makedirs(file.replace(os.path.basename(file), ""), exist_ok=True)
        try:
            vmtfile = open(file, "x")
            vmtfile.write(convertVMT(getVMT[1], getVMT[0]))
            vmtfile.close()
        except FileExistsError:
            print(termcolor.colored("Material already exists in the saving directory! Ignoring i guess.", "red"))
        print("------------------------")

    print("-----------------------")
    print("-----------------------")
    print("-----------------------")
    print(f"Total Errors: {failcounter.__len__()}")
    print("-----------------------")
    print("MAIN SCREEN TURN ON:")
    for err in failcounter:
        print(err)
print("-----------------------")
print("This is it.")