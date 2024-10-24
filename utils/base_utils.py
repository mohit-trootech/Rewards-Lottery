from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model


def get_model(app_label: str, model_name: str) -> type[Model | None]:
    """This function will return model object
    :param: app_label (name of app label)
    :param: model_name (name of model)
    :returns: Model Object i.e
            <class 'user.models.User'>
    """
    try:
        return apps.get_model(app_label, model_name)
    except ValueError:
        raise ImproperlyConfigured(
            f"Model {model_name} must be in app directory {app_label}"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"App label {app_label} must be defined in project directory"
        )
