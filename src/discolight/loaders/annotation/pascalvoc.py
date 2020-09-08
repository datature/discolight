"""A Pascal VOC annnotation loader."""
import glob
import defusedxml.ElementTree as ET
from discolight.params.params import Params
from discolight.annotations import BoundingBox, ImageWithAnnotations
from .types import AnnotationLoader


class PascalVOC(AnnotationLoader):

    """A Pascal VOC annotation loader."""

    def __init__(self, annotations_folder):
        """Construct a new Pascal VOC annotation loader."""
        self.annotations_folder = annotations_folder
        self.name_to_class_idx = {}
        self.next_class_idx = 0

    def __enter__(self):
        """Open the annotation loader."""
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotation loader."""

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add("annotations_folder",
                            "The folder where the annotations are stored", str,
                            "", True)

    def parse_xml_bounding_box(self, bndbox):
        """Parse a bounding box from an XML <bndbox> tag."""
        xmin = None
        ymin = None
        xmax = None
        ymax = None

        for bndbox_tag in bndbox:

            if bndbox_tag.tag == "xmin":
                xmin = float(bndbox_tag.text)
                continue

            if bndbox_tag.tag == "ymin":
                ymin = float(bndbox_tag.text)
                continue

            if bndbox_tag.tag == "xmax":
                xmax = float(bndbox_tag.text)
                continue

            if bndbox_tag.tag == "ymax":
                ymax = float(bndbox_tag.text)
                continue

        if xmin is None or ymin is None or xmax is None or ymax is None:
            raise ValueError("Annotation missing complete bounding box")

        return xmin, ymin, xmax, ymax

    def parse_xml_object(self, obj):
        """Parse an annotation from an XML <object> tag."""
        name = ""
        pose = ""
        truncated = ""
        difficult = ""
        xmin = None
        ymin = None
        xmax = None
        ymax = None

        for obj_tag in obj:

            if obj_tag.tag == "name":
                name = obj_tag.text
                continue

            if obj_tag.tag == "pose":
                pose = obj_tag.text
                continue

            if obj_tag.tag == "truncated":
                truncated = obj_tag.text
                continue

            if obj_tag.tag == "difficult":
                difficult = obj_tag.text
                continue

            if obj_tag.tag != "bndbox":
                continue

            xmin, ymin, xmax, ymax = self.parse_xml_bounding_box(obj_tag)

        additional_info = {
            "name": name,
            "pose": pose,
            "truncated": truncated,
            "difficult": difficult
        }

        try:
            class_idx = int(name)
            self.next_class_idx = class_idx + 1
        except ValueError:
            class_idx = self.name_to_class_idx.get(name, self.next_class_idx)

            if class_idx == self.next_class_idx:
                self.name_to_class_idx[name] = self.next_class_idx
                self.next_class_idx += 1

        annotation = BoundingBox(xmin, ymin, xmax, ymax, class_idx,
                                 additional_info)

        return annotation

    def load_annotations_from_xml(self, filename):
        """Load an image and annotations from a Pascal VOC-format XML file."""
        tree = ET.parse(filename)
        root = tree.getroot()

        image_filename = None
        annotations = []

        for tag in root:

            if tag.tag == "filename":
                image_filename = tag.text

            if tag.tag != "object":
                continue

            annotations.append(self.parse_xml_object(tag))

        if image_filename is None:
            raise ValueError("Image filename not specified")

        return image_filename, annotations

    def load_annotated_images(self, image_loader):
        """Load annotations, images from a directory in Pascal VOC format."""
        images = {}

        for annotation_file in glob.glob("{}/{}".format(
                self.annotations_folder, "*.xml")):

            image_name, annotations = self.load_annotations_from_xml(
                annotation_file)

            images[image_name] = ImageWithAnnotations(
                image=image_loader.load_image(image_name), bboxes=annotations)

        return images
