"""A dynamic module loader for objects extending an abstract class."""
import glob
import os
import importlib
import inspect
from pathlib import Path


class ObjectSetLoader:

    """A class that can be used to load a set of like objects at runtime.

    Objects loaded by this dynamic loader must satisfy the following
    properties:

    - They must implement the given abstract class
    - They must provide a static params method which returns a Params
      object to describe the parameters for their constructors
    - They must provide a _include_in_factory property. An object will
      only be loaded if this property is set to True.
    """

    def __init__(self, module_dir, package, obj_type):
        """Initialize the object set loader.

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
        """Return the set of loaded objects.

        By default the object set is cached so if this method is called
        multiple times searching and loading does not have to be performed
        again.
        """
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
        """Bind a type cast in object Params to a different method.

        When the factory function is invoked to instantiate an object,
        the function real_case will be used to cast parameters using the
        given cast function to the correct type.
        """
        self.bound_type_casts.append((cast, real_cast))

    def bind_params_type_cast_to_factory(self, cast):
        """Bind a type cast in object Params to the object factory function.

        When the factory function is invoked to instantiate an object, the
        factory function will be used to cast parameters using the given
        cast function to the object type.

        The factory function will accept already constructed instances of
        the object type, or dictionary objects in the following format:

        { "name": object instance name,
          "options": constructor parameters as a dictionary }

        In the latter case, the factory function will be invoked to
        construct the object before passing it as a parameter
        to the object being constructed.
        """
        self.type_casts_bound_to_factory.append(cast)

    def bind_params_type_cast_to_factory_list(self, cast):
        """Bind a type cast in object Params to a list of the object type.

        When the factory function is invoked to instantiate the object,
        the factory function will be used to cast parameters using the
        given cast function to a list of the object type.

        This list can contain a mixture of already constructed instances
        of the object type, or dictionary objects as defined in the
        documentation for bind_params_type_cast_to_factory.
        """
        self.type_casts_bound_to_factory_list.append(cast)

    def make_object_factory(self):
        """Construct a factory function for all loaded objects.

        Invoke the returned factory function by passing the name of the
        object you want to construct, followed by the parameters for
        the constructor as named arguments
        (e.g., factory('MyObject', param1=..., param2=..., ...)).
        """
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
