from .types import CSVAnnotationWriter


class FourCornersCSV(CSVAnnotationWriter):
    """
    Writes annotations to a CSV file in the following format:

    image_name, x_min, y_min, x_max, y_max, label
    """
    def get_csv_fieldnames(self):
        return ["image_name", "x_min", "y_min", "x_max", "y_max", "label"]

    def get_csv_row(self, image_name, _image, annotation):

        return {
            "image_name": image_name,
            "x_min": annotation.x_min,
            "y_min": annotation.y_min,
            "x_max": annotation.x_max,
            "y_max": annotation.y_max,
            "label": annotation.class_idx
        }
