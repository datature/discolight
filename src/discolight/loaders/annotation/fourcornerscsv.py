from discolight.annotations import BoundingBox
from .types import CSVRow, CSVAnnotationLoader


class FourCornersCSV(CSVAnnotationLoader):
    """
    Loads annotations from a CSV file in the following format:

    image_name, x_min, y_min, x_max, y_max, label
    """
    def get_csv_row(self, row):

        x_min = float(row["x_min"])
        y_min = float(row["y_min"])

        x_max = float(row["x_max"])
        y_max = float(row["y_max"])

        image_name = row["image_name"]
        class_idx = row["label"]

        return CSVRow(image_name=image_name,
                      bbox=BoundingBox(x_min, y_min, x_max, y_max, class_idx))
