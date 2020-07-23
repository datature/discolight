import glob
import os
import importlib
import inspect
from pathlib import Path


class ObjectSetLoader:
    """
    A class that can be used to load a set of like objects at runtime by
    searching through all of the modules in a given folder

    Objects loaded by this dynamic loader must satisfy the following
    properties:
    """
    def __init__(self, module_dir, package, obj_type):
        """
        Initializes the object set loader

        Keyword arguments:

        module_dir - The path to the directory whose modules should be loaded
        package - The package the modules should be loaded into. Usually this
                  is __file__.
        obj_type - The type of objects to search for in the loaded modules.
        """

        self.module_dir = module_dir
        self.package = package
        self.obj_type = obj_type

        self.cached_object_set = None

        self.bound_type_casts = []
        self.type_casts_bound_to_factory = []
        self.type_casts_bound_to_factory_list = []

    def get_object_set(self, use_cache=True):

        if use_cache and self.cached_object_set is not None:
            return self.cached_object_set

        modules = glob.glob(os.path.join(self.module_dir, "*.py"))
        objects = {}

        for module_path in modules:
            module_name = Path(module_path).stem
            module = importlib.import_module("..{}".format(module_name),
                                             package=self.package)

            for _name, obj in inspect.getmembers(module):

                if not inspect.isclass(obj):
                    continue

                if inspect.isabstract(obj):
                    continue

                if not issubclass(obj, self.obj_type):
                    continue

                # pylint: disable=protected-access
                if not obj._include_in_factory:
                    continue

                objects[obj.__name__] = obj

        self.cached_object_set = objects

        return objects

    def bind_params_type_cast(self, cast, real_cast):
        self.bound_type_casts.append((cast, real_cast))

    def bind_params_type_cast_to_factory(self, cast):
        self.type_casts_bound_to_factory.append(cast)

    def bind_params_type_cast_to_factory_list(self, cast):
        self.type_casts_bound_to_factory_list.append(cast)

    def make_object_factory(self):

        objects = self.get_object_set()

        def object_factory(name, **params):

            if name not in objects:
                raise NameError("The {} {} does not exist.".format(
                    self.obj_type.__name__, name))

            def object_factory_type_cast(obj):

                if isinstance(obj, self.obj_type):
                    return obj

                try:
                    obj_type = obj["name"]
                    obj_opts = obj.get("options", {})

                    return object_factory(obj_type, **obj_opts)
                except (KeyError, TypeError, ValueError):
                    raise ValueError("Unable to coerce {} to {}".format(
                        repr(obj), self.obj_type))

            def object_factory_list_type_cast(objs):

                return [object_factory_type_cast(obj) for obj in objs]

            obj = objects[name]

            obj_params = obj.params()

            for cast, real_cast in self.bound_type_casts:
                obj_params = obj_params.with_bound_type_cast(cast, real_cast)

            for cast in self.type_casts_bound_to_factory:
                obj_params = obj_params.with_bound_type_cast(
                    cast, object_factory_type_cast)

            for cast in self.type_casts_bound_to_factory_list:
                obj_params = obj_params.with_bound_type_cast(
                    cast, object_factory_list_type_cast)

            return obj_params.call_with_params(obj, params)

        return object_factory
