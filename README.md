# Simple "OBJ_Texture_Mapper" Texture Adder

<img width="702" height="582" alt="Screenshot (3123)" src="https://github.com/user-attachments/assets/9932163c-f4c6-4e49-b71b-6877c89cb100" />

"OBJ_Texture_Mapper" is a small and simple yet reliable software built on python that let's you easily add/apply textures into your model without needed to go through long process of launching blender, importing model, clicking on shading tab and manually drag and dropping textures and connecting each to corresponding socket

# Usage & Workarounds

Open the program and start drag and dropping .OBJ model anywhere and also different texture maps like diffuse/normal/specular into corresponding white path boxes. 

You can always reset any texture if you missdropped and you can also reset all textures if you want, after all done click on "Apply!" to apply all textures to the .OBJ file.

# Why only three?
Blender's OBJ importer does read specular map (map_Ks) and normal map (bump), but it does not auto-connect them in the material nodes. That’s why your color shows up, but the normal and specular maps are invisible until manually hooked up. 

Blender is limited by the old .mtl format—it doesn’t support PBR workflows out of the box. 

I will still do my work and try fix it for Blender's stuborn node system so it will fully works later.

# Requirepments (Python version)
Python 3 - (https://www.python.org/) - (Don't forget to add it into PATH!!)

tkinter - pip install tkinter

tkinterdnd2 - pip install tkinterdnd2
