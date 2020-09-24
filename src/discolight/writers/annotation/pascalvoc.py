"""A Pascal VOC annotation writer."""
import os
import shutil
import xml.etree.cElementTree as ET
import defusedxml
from discolight.params.params import Params
from .types import AnnotationWriter

defusedxml.defuse_stdlib()


class PascalVOC(AnnotationWriter):

    """A Pascal VOC annotation writer."""

    def __init__(self, annotations_folder, database, clean_directory):
        """Construct a new Pascal VOC annotation writer."""
        self.annotations_folder = annotations_folder
        self.database = database
        self.clean_directory = clean_directory

    def __enter__(self):
        """Open the annotation writer for writing."""
        if os.path.isdir(self.annotations_folder) and self.clean_directory:
            shutil.rmtree(self.annotations_folder)

        if not os.path.isdir(self.annotations_folder):
            os.mkdir(self.annotations_folder)

        return self

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_folder",
            "the directory to save annotation files to", str, "", True).add(
                "database", "The name of the source database", str, "").add(
                    "clean_directory",
                    "whether to forcibly ensure the output directory is empty",
                    bool, True)

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotation writer."""

    def write_annotations_for_image(self, image_name, image, annotations):
        """Write the XML annotations file for the given image."""
        root = ET.Element("annotation")

        ET.SubElement(root, "folder").text = ""
        ET.SubElement(root, "filename").text = image_name
        ET.SubElement(root, "path").text = image_name

        source = ET.SubElement(root, "source")
        ET.SubElement(source, "database").text = self.database

        height, width, _ = image.shape
        size = ET.SubElement(root, "size")
        ET.SubElement(size, "width").text = str(width)
        ET.SubElement(size, "height").text = str(height)
        ET.SubElement(size, "depth").text = "3"

        ET.SubElement(root, "segmented").text = "0"

        for annotation in annotations:

            obj = ET.SubElement(root, "object")

            name = annotation.additional_info.get("name",
                                                  str(annotation.class_idx))
            pose = annotation.additional_info.get("pose", "")
            truncated = annotation.additional_info.get("truncated", "0")
            difficult = annotation.additional_info.get("difficult", "0")

            ET.SubElement(obj, "name").text = name
            ET.SubElement(obj, "pose").text = pose
            ET.SubElement(obj, "truncated").text = truncated
            ET.SubElement(obj, "difficult").text = difficult

            bndbox = ET.SubElement(obj, "bndbox")

            ET.SubElement(bndbox, "xmin").text = str(annotation.x_min)
            ET.SubElement(bndbox, "ymin").text = str(annotation.y_min)
            ET.SubElement(bndbox, "xmax").text = str(annotation.x_max)
            ET.SubElement(bndbox, "ymax").text = str(annotation.y_max)

        tree = ET.ElementTree(root)
        tree.write("{}/{}.xml".format(self.annotations_folder, image_name))
