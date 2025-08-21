import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

def assign_texture_type(filename):
    lower = filename.lower()
    if lower.endswith(('_n.png', '_n.jpg', '_n.tga', '_n.dds')):
        return "normal"
    elif lower.endswith(('_s.png', '_s.jpg', '_s.tga', '_s.dds')):
        return "specular"
    elif lower.endswith(('_c.png', '_c.jpg', '_c.tga', '_c.dds')) or lower.endswith(('_d.png', '_d.jpg', '_d.tga', '_d.dds')):
        return "color"
    else:
        return "color"

class TextureAssignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OBJ Texture Assigner")
        self.root.geometry("700x550")
        self.obj_path = None
        self.objects = []
        self.materials = {}
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="Drag and drop the OBJ file anywhere", font=("Arial", 14)).pack(pady=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Apply Textures!", command=self.apply_textures).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Reset All", command=self.reset_all_textures).pack(side=tk.LEFT, padx=10)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_handler)
        self.notebook.drop_target_register(DND_FILES)
        self.notebook.dnd_bind('<<Drop>>', self.drop_handler)

    def drop_handler(self, event):
        for raw_path in self.root.tk.splitlist(event.data):
            path = raw_path.strip('{}')
            ext = os.path.splitext(path)[1].lower()
            if ext == '.obj':
                self.load_obj(path)
            else:
                self.assign_texture(path)

    def load_obj(self, path):
        if not os.path.isfile(path):
            messagebox.showerror("Error", "OBJ file path invalid.")
            return
        self.obj_path = path
        self.objects = []
        self.materials.clear()

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('o '):
                    name = line.strip()[2:].strip()
                    if name:
                        self.objects.append(name)
        if not self.objects:
            self.objects = ['Default']
        
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        for obj in self.objects:
            self.materials[obj] = {"color": None, "normal": None, "specular": None}
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=obj)

            row = 0
            for ttype in ["color", "normal", "specular"]:
                ttk.Label(tab, text=ttype.capitalize() + ":").grid(row=row, column=0, sticky='w', padx=5, pady=5)
                var = tk.StringVar()
                ent = ttk.Entry(tab, textvariable=var, width=50)
                ent.grid(row=row, column=1, padx=5, pady=5)
                ent.drop_target_register(DND_FILES)
                ent.dnd_bind('<<Drop>>', lambda e, o=obj, tt=ttype, v=var: self.texture_drop(e, o, tt, v))
                ttk.Button(tab, text="Reset", command=lambda o=obj, tt=ttype, v=var: self.reset_texture(o, tt, v)).grid(row=row, column=2, padx=5)
                self.materials[obj][ttype + "_var"] = var
                row += 1
            tab.columnconfigure(1, weight=1)

    def texture_drop(self, event, obj, ttype, var):
        path = event.widget.tk.splitlist(event.data)[0].strip('{}')
        if os.path.isfile(path):
            self.materials[obj][ttype] = path
            var.set(path)

    def assign_texture(self, path):
        if not self.objects:
            messagebox.showwarning("Warning", "Load an OBJ first!")
            return
        ttype = assign_texture_type(path)
        idx = self.notebook.index(self.notebook.select())
        obj = self.objects[idx]
        self.materials[obj][ttype] = path
        var = self.materials[obj].get(ttype + "_var")
        if var: var.set(path)

    def reset_texture(self, obj, ttype, var):
        var.set("")
        self.materials[obj][ttype] = None

    def reset_all_textures(self):
        for obj in self.objects:
            for ttype in ["color", "normal", "specular"]:
                var = self.materials[obj].get(ttype + "_var")
                if var:
                    var.set("")
                self.materials[obj][ttype] = None

    def apply_textures(self):
        if not self.obj_path:
            messagebox.showwarning("Warning", "No OBJ loaded.")
            return

        mtl = os.path.splitext(self.obj_path)[0] + ".mtl"
        try:
            with open(mtl, 'w', encoding='utf-8') as f:
                for obj in self.objects:
                    tex = self.materials[obj]
                    f.write(f"newmtl {obj}\n")
                    if tex["color"]:
                        f.write(f"map_Kd ./{os.path.basename(tex['color'])}\n")
                    if tex["specular"]:
                        f.write(f"map_Ks ./{os.path.basename(tex['specular'])}\n")
                    if tex["normal"]:
                        f.write(f"map_Bump ./{os.path.basename(tex['normal'])}\n")
                    f.write("\n")
            messagebox.showinfo("Success", f"MTL saved:\n{mtl}\n(note: Blender may still require manual node setup for bump/specular)")
        except Exception as e:
            messagebox.showerror("Error", f"Could not write MTL:\n{e}")

def main():
    root = TkinterDnD.Tk()
    TextureAssignerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
