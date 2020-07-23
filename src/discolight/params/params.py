from discolight.result.result import Ok, Error


class Params:
    """
    A description of the parameters for a function that can be used to apply a
    function to the given set of parameters after validating them
    """
    def __init__(self):

        self.params = {}
        self.ensures = []
        self.bound_type_casts = {}

    def add(self, name, description, data_type, default, required=False):
        """
        Adds a new parameter, returing the current Params object to support
        method chaining.

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
        """
        Adds a new validation condition, returning the current Params object to
        support method chaining.

        During validation the check function will be called, and passed a
        dictionary with the current set of parameters. If the parameter set is
        valid, check should return True, and False otherwise. If False is
        returned validation will fail with the string in err as the reason.
        """

        self.ensures.append({"check": check, "err": err})

        return self

    def with_bound_type_cast(self, cast, real_cast):
        self.bound_type_casts[cast.__name__] = real_cast
        return self

    def validate(self, params):
        """Validates the given set of parameters, returning a Result object"""

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

            complete_params[param_name] = param["default"]

        for ensure in self.ensures:
            if not ensure["check"](complete_params):
                return Error(ensure["err"])

        return Ok(complete_params)

    def call_with_params(self, func, params):
        """
        Applies func to the given set of parameters, raising an exception if
        they are invalid
        """

        validation_result = self.validate(params)

        if validation_result.is_error:
            raise ValueError(validation_result.error)

        complete_params = validation_result.value

        return func(**complete_params)
