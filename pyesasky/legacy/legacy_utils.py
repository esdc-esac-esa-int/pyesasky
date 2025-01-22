from IPython.display import display, HTML
import inspect


def deprecated(new_method_name, with_args=False):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Get the deprecated method name
            method_name = func.__name__

            # Get the new method
            new_method = getattr(self, new_method_name)

            display_warning(method_name, new_method_name, with_args)

            # Call the new method
            return new_method(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_super(new_method_name, with_args):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Get the deprecated method name
            method_name = func.__name__

            # Get the corresponding method in the superclass
            super_method = getattr(super(self.__class__, self), new_method_name)

            display_warning(method_name, new_method_name, with_args)

            # Call the corresponding method in the superclass
            return super_method(*args, **kwargs)

        return wrapper

    return decorator


def get_method_args(method):
    sig = inspect.signature(method)
    decorated_args = [
        (
            f"{param.name}={param.default}"
            if param.default != inspect.Parameter.empty
            else param.name
        )
        for param in sig.parameters.values()
    ]

    return decorated_args


def display_warning(old_method_name, new_method_name: str, with_args=False):
    new_method_sig = (
        f"{new_method_name}({', '.join(get_method_args(new_method_name))})"
        if with_args
        else new_method_name
    )
    warning_html = f"""
        <div style="background-color: #fff3cd;
                    color: #856404;
                    border: 1px solid #ffeeba;
                    border-radius: 5px;
                    padding: 12px;
                    margin: 10px 0;
                    font-size: 10px;
                    font-family: Arial, sans-serif;">
            <strong>Warning:</strong> '{old_method_name}' is deprecated.
            Please use '{new_method_sig}' instead.
        </div>
        """
    display(HTML(warning_html))
