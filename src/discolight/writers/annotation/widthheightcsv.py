"""A CSV annotation writer that writes the bbox in x, y, w, h format."""
from .types import CSVAnnotationWriter


class WidthHeightCSV(CSVAnnotationWriter):

    """Writes annotations to a CSV file in the following format.

    image_name, x_min, y_min, width, height, label
    """

    def get_csv_fieldnames(self):
        """Return the field names for the CSV file."""
        return ["image_name", "x_min", "y_min", "width", "height", "label"]

    def get_csv_row(self, image_name, _image, annotation):
        """Return the CSV row corresponding to the given annotation."""
        return {
            "image_name": image_name,
            "x_min": annotation.x_min,
            "y_min": annotation.y_min,
            "width": annotation.x_max - annotation.x_min,
            "height": annotation.y_max - annotation.y_min,
            "label": annotation.class_idx
        }
