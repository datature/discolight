"""A parser for YAML queries used by the Augmentor class."""
import yamale

schema = yamale.make_schema(content="""
input:
  images:
    loader: str()
    options: map()
  annotations:
    loader: str()
    options: map()
output:
  images:
    writer: str()
    options: map()
  annotations:
    writer: str()
    options: map()
augmentations: list(include('augmentation'))
save-original: bool()
save-bbox: bool()
---
augmentation:
  name: str()
  options: map(required=False)
""")


def load_query(filep):
    """Load a YAML query from the open file fp.

    An exception will be raised if the query is invalid.
    """
    content = filep.read()

    query = yamale.make_data(content=content)

    yamale.validate(schema, query)

    return query[0][0]
