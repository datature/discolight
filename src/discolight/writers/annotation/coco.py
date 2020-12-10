"""A COCO annotation writer."""
import datetime
import json
from discolight.params.params import Params
from .types import AnnotationWriter


class COCO(AnnotationWriter):

    """A COCO annotation writer."""

    def __init__(self, annotations_file):
        """Construct a COCO annotation writer."""
        self.annotations_file = annotations_file

        self.coco_json = {
            "info": {
                "year":
                datetime.datetime.now().year,
                "version":
                1,
                "description":
                "Discolight augmented images",
                "contributor":
                "",
                "url":
                "",
                "date_created":
                datetime.datetime.utcnow().replace(
                    tzinfo=datetime.timezone.utc).isoformat(),
            },
            "categories": [],
            "images": [],
            "annotations": [],
            "licenses": [],
        }

        self.image_counter = 0
        self.annotation_counter = 0
        self.category_counter = 0
        self.license_counter = 0

        self.unknown_license_id = None

        self.old_license_id_to_new = {}
        self.old_category_id_to_new = {}
        self.class_idx_category_id = {}

    def __enter__(self):
        """Open the annotation writer for writing."""
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Close the annotation writer for writing."""
        with open(self.annotations_file, "w") as annotations_fp:
            json.dump(self.coco_json, annotations_fp)

    @staticmethod
    def params():
        """Return a Params object describing constructor parameters."""
        return Params().add(
            "annotations_file",
            "The path to the JSON file to write the annotations to", str, "",
            True)

    def get_image_license_id(self, annotations):
        """Retrieve the license ID of an image based on its annotations."""
        licens = None

        if len(annotations) > 1:
            licens = annotations[0].additional_info[
                "image_license"] if "image_license" in annotations[
                    0].additional_info else None

        if licens is None and self.unknown_license_id is None:

            self.unknown_license_id = self.license_counter
            self.license_counter += 1

            self.coco_json["licenses"].append({
                "id": self.unknown_license_id,
                "url": "",
                "name": "Unknown"
            })

            return self.unknown_license_id

        if licens is None and self.unknown_license_id is not None:

            return self.unknown_license_id

        new_license_id = self.old_license_id_to_new.get(
            str(licens["id"]), None)

        if new_license_id is None:
            new_license_id = self.license_counter
            self.license_counter += 1

            self.old_license_id_to_new[str(licens["id"])] = new_license_id

            self.coco_json["licenses"].append({
                "id": new_license_id,
                "url": licens["url"],
                "name": licens["name"]
            })

            return new_license_id

        return new_license_id

    def get_annotation_category_id(self, annotation):
        """Retrieve the category ID of an annotation."""
        if "category" in annotation.additional_info:

            category = annotation.additional_info["category"]

            new_category_id = self.old_category_id_to_new.get(
                str(category["id"]), None)

            if new_category_id is None:

                new_category_id = self.category_counter
                self.category_counter += 1

                self.old_category_id_to_new[str(
                    category["id"])] = new_category_id

                self.coco_json["categories"].append({
                    "id":
                    new_category_id,
                    "name":
                    category["name"],
                    "supercategory":
                    category["supercategory"]
                })

                return new_category_id

            return new_category_id

        category_id = self.class_idx_category_id.get(str(annotation.class_idx),
                                                     None)

        if category_id is None:

            category_id = self.category_counter
            self.category_counter += 1

            self.class_idx_category_id[str(annotation.class_idx)] = category_id

            self.coco_json["categories"].append({
                "id":
                category_id,
                "name":
                "class{}".format(annotation.class_idx),
                "supercategory":
                "none"
            })

            return category_id

        return category_id

    def write_annotations_for_image(self, image_name, image, annotations):
        """Write annotations for the given image."""
        height, width, _ = image.shape

        image_id = self.image_counter
        self.image_counter += 1

        self.coco_json["images"].append({
            "id":
            image_id,
            "license":
            self.get_image_license_id(annotations),
            "file_name":
            image_name,
            "height":
            height,
            "width":
            width,
            "date_captured":
            datetime.datetime.utcnow().replace(
                tzinfo=datetime.timezone.utc).isoformat()
        })

        for annotation in annotations:

            annotation_id = self.annotation_counter
            self.annotation_counter += 1

            self.coco_json["annotations"].append({
                "id":
                annotation_id,
                "image_id":
                image_id,
                "category_id":
                self.get_annotation_category_id(annotation),
                "bbox": [
                    annotation.x_min, annotation.y_min,
                    annotation.x_max - annotation.x_min,
                    annotation.y_max - annotation.y_min
                ],
                "area": (annotation.x_max - annotation.x_min) *
                (annotation.y_max - annotation.y_max),
                "segmentation": [],
                "iscrowd":
                0
            })
