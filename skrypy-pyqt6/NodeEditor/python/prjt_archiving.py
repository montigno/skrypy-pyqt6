import re
import os
import ast
import shutil
import struct
import zipfile

from pathlib import Path


class project_archive():
    def __init__(self, diagram_src, skrypy_src, remove_src_dgr):
        # diagram_src = "/home/olivier/tmp/test_archive_skrypy/demo_OM.dgr"
        # skrypy_src = "/home/olivier/Documents/eclipse-workspace/skrypy/NodeEditor/"

        list_blocks, list_submod = self.get_blocks_submod_from_dgr(diagram_src, skrypy_src)

        archive_tmp = os.path.join(os.path.dirname(diagram_src), Path(diagram_src).stem)

        for k_class, v_class in list_blocks.items():
            class_src = self.get_class_source(v_class, k_class)
            file_py = os.path.join(archive_tmp, os.path.basename(v_class))
            self.write_class_source(file_py, class_src, k_class)

        for list_sub in list_submod:
            self.copy_submod(list_sub, archive_tmp)

        shutil.copy(diagram_src, archive_tmp)

        fold = os.path.dirname(diagram_src)
        archive_path = Path(diagram_src).with_suffix(".sky")
        self.create_archive(archive_tmp)

        if remove_src_dgr:
            os.remove(diagram_src)

    def create_archive(self, archive_root):
        shutil.make_archive(
            base_name=archive_root,
            format="zip",
            root_dir=os.path.dirname(archive_root),
            base_dir=os.path.basename(archive_root)
        )
        os.rename(archive_root + ".zip", archive_root + ".sky")

        shutil.rmtree(archive_root)

    ##########################################################################################

    def read_archive(self, archive_file, folder_destination):
        with zipfile.ZipFile(archive_file, "r") as archive:
            archive.extractall(folder_destination)

    ##########################################################################################

    def get_blocks_submod_from_dgr(self, dgr_file, skrypy_src):
        with open(dgr_file, 'r') as sm:
            lines = sm.readlines()
        list_blocks = {}
        list_submod = []
        for line in lines:
            if "block=" in line:
                # Cherche tout ce qui est entre crochets
                valeurs = re.findall(r"\[([^\]]*)\]", line)
                list_blocks[valeurs[2]] = os.path.join(skrypy_src, "modules", valeurs[1].replace(".", "/") + ".py")
            if "submod=" in line:
                valeurs = re.findall(r"\[([^\]]*)\]", line)
                submod_path = os.path.join(skrypy_src, "submodules", valeurs[2], valeurs[1] + ".mod")
                list_submod.append(submod_path)
                list_blocks_elem, list_submod_elem = self.get_blocks_submod_from_dgr(submod_path, skrypy_src)
                list_blocks |= list_blocks_elem
                list_submod.extend(list_submod_elem)

        return list_blocks, list_submod

    ##########################################################################################

    def get_class_source(self, file_path, class_name):
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                start_line = node.lineno - 1
                end_line = node.end_lineno
                return "\n".join(source.splitlines()[start_line:end_line])

        raise ValueError(f"Class '{class_name}' not found")

    ##########################################################################################

    def write_class_source(self, file_py, class_src, class_name):
        path = Path(file_py)
        path.parent.mkdir(parents=True, exist_ok=True)
        if os.path.exists(file_py):
            content = path.read_text(encoding="utf-8")
            tree_cl = ast.parse(content)
            for noeud in ast.walk(tree_cl):
                if isinstance(noeud, ast.ClassDef) and noeud.name == class_name:
                    return
        with path.open("a", encoding="utf-8") as f:
            f.write("{}\n{}\n\n".format(class_src, "#" * 79))

    ##########################################################################################

    def copy_submod(self, file_mod, folder_dest):
        source = Path(file_mod)
        dest = Path(folder_dest)
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)

    ##########################################################################################
