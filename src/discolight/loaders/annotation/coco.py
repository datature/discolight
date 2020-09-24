"""A COCO annotation loader."""
import json
from discolight.params.params import Params
from discolight.annotations import BoundingBox, ImageWithAnnotations
from .types import AnnotationLoader


class COCO(AnnotationLoader):

    """A COCO annotation loader."""

    def __init__(self, annotations_file):
        """Construct a new COCO annotation loader."""
        self.annotations_file = annotations_file

        self.annotations_fp = None
        self.coco_json = None

    def __enter__(self):
        """Open the annotations_file for reading."""
        self.annotations_fp = open(self.annotations_file, "r")
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotations_file."""
        self.annotations_fp.close()

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_file",
            "The path to the JSON file containing the annotations", str, "",
            True)

    def load_annotated_images(self, image_loader):
        """Load annotations and images from a COCO JSON file."""
        coco_json = json.load(self.annotations_fp)

        licenses = {}
        categories = {}
        images_json = {}

        for licens in coco_json["licenses"]:
            licenses[str(licens["id"])] = licens

        for category in coco_json["categories"]:
            categories[str(category["id"])] = category

        for image in coco_json["images"]:
            images_json[str(image["id"])] = image

        images = {}

        for annotation in coco_json["annotations"]:

            image_name = images_json[str(annotation["image_id"])]["file_name"]
            image_license_id = images_json[str(
                annotation["image_id"])]["license"]

            if image_name not in images:

                image = image_loader.load_image(image_name)
                images[image_name] = ImageWithAnnotations(image, [])

            images[image_name].bboxes.append(
                BoundingBox(
                    annotation["bbox"][0], annotation["bbox"][1],
                    annotation["bbox"][0] + annotation["bbox"][2],
                    annotation["bbox"][1] + annotation["bbox"][3],
                    annotation["category_id"], {
                        "category": categories[str(annotation["category_id"])],
                        "image_license": licenses[str(image_license_id)]
                    }))

        return images
