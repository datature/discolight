"""A CSV annotation writer that reads the bbox in x, y, w, h format."""
from discolight.annotations import BoundingBox
from .types import CSVRow, CSVAnnotationLoader


class WidthHeightCSV(CSVAnnotationLoader):

    """Loads annotations from a CSV file in the following format.

    image_name, x_min, y_min, width, height, label
    """

    def get_csv_row(self, row):
        """Return the image and annotation from a CSV row."""
        x_min = float(row["x_min"])
        y_min = float(row["y_min"])

        width = float(row["width"])
        height = float(row["height"])

        x_max = x_min + width
        y_max = y_min + height

        image_name = row["image_name"]
        class_idx = row["label"]

        return CSVRow(image_name=image_name,
                      bbox=BoundingBox(x_min, y_min, x_max, y_max, class_idx))
