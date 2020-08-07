"""A runtime function parameter type checker."""
from discolight.result.result import Ok, Error


class Params:

    """A function parameter type checker that gives detailed error messages.

    Function parameters can be specified with types and default values, and
    additional validation checks can also be added using the ensure method.
    """

    def __init__(self):
        """Constuct a new Params object."""
        self.params = {}
        self.ensures = []
        self.bound_type_casts = {}

    def add(self, name, description, data_type, default, required=False):
        """Add a new parameter.

        The current Params object is returned to support method chaining.

        Keyword arguments:
        name: The name of the parameter
        description: The description of the parameter
        data_type: The type of the parameter
        default: The default value of the parameter
        required: Whether the parameter must be specified
        """
        self.params[name] = {
            "name": name,
            "description": description,
            "data_type": data_type,
            "default": default,
            "required": required
        }

        return self

    def ensure(self, check, err):
        """Add a new validation condition.

        The current Params object is returned to support method chaining.

        During validation the check function will be called, and passed a
        dictionary with the current set of parameters. If the parameter set is
        valid, check should return True, and False otherwise. If False is
        returned validation will fail with the string in err as the reason.
        """
        self.ensures.append({"check": check, "err": err})

        return self

    def with_bound_type_cast(self, cast, real_cast):
        """Designate a different type cast to be applied.

        The current Params object is returned to support method chaining.

        During validation the type casts specified when parameters are
        added are used to cast the specified parameters to the correct
        type. Invoking this method will invoke real_cast to do this
        instead of cast, wherever cast would normally be used.
        """
        self.bound_type_casts[cast.__name__] = real_cast
        return self

    def validate(self, params):
        """Validate the given set of parameters, returning a Result object.

        If the parameters are valid, an OK result will be returned containing
        the complete parameter set (including default values for
        non-required parameters left unspecified).

        If the parameters are invalid, an Error result will be returned
        containing a description of the error as a string.
        """
        complete_params = {}
        for param, value in params.items():

            if param not in self.params:

                return Error("Parameter {} is not accepted".format(param))

            typecast = self.params[param]["data_type"]

            if typecast.__name__ in self.bound_type_casts:
                typecast = self.bound_type_casts[typecast.__name__]

            try:
                complete_params[param] = typecast(value)
            except ValueError as e:
                print(repr(e))
                return Error(
                    "Value for parameter {} cannot be converted to {}".format(
                        param, self.params[param]["data_type"].__name__))

        for param_name, param in self.params.items():

            if param_name in complete_params:
                continue

            if param["required"] and param_name not in params:
                return Error(
                    "The parameter {} must be specified".format(param_name))

            typecast = param["data_type"]

            if typecast.__name__ in self.bound_type_casts:
                typecast = self.bound_type_casts[typecast.__name__]

            complete_params[param_name] = typecast(param["default"])

        for ensure in self.ensures:
            if not ensure["check"](complete_params):
                return Error(ensure["err"])

        return Ok(complete_params)

    def call_with_params(self, func, params):
        """Apply func to the given set of parameters as a dictionary.

        An exception will be raised if the given set of parameters is invalid.
        """
        validation_result = self.validate(params)

        if validation_result.is_error:
            raise ValueError(validation_result.error)

        complete_params = validation_result.value

        return func(**complete_params)
