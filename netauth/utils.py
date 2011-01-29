import re

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from django.utils.importlib import import_module

from netauth import settings


def parse_template(template_path, **kwargs):
    """ Load and render template.
        First line of template should contain the subject of email.
        Return tuple with subject and content.
    """
    template = get_template(template_path)
    context = Context(kwargs)
    data = template.render(context).strip()
    subject, content = re.split(r'\r?\n', data, 1)
    return (subject.strip(), content.strip())


def email_template(rcpt, template_path, **kwargs):
    """ Load, render and email template.
        **kwargs may contain variables for template rendering.
    """

    subject, content = parse_template(template_path, **kwargs)
    count = send_mail(subject, content, settings.DEFAULT_FROM_EMAIL,
                      [rcpt], fail_silently=True)
    return bool(count)


def str_to_class(string):
    mod_str, cls_str = string.rsplit('.', 1)
    mod = __import__(mod_str, globals(), locals(), ['foobar'])
    cls = getattr(mod, cls_str)
    return cls


def uri_to_username(uri):
    return re.sub('r[^0-9a-z]', '_', uri)


def get_instance_from_path(path, *args, **kwargs):
    """ Return an instance of a class, given the dotted
        Python import path (as a string) to the backend class.

        If the backend cannot be located (e.g., because no such module
        exists, or because the module does not contain a class of the
        appropriate name), ``django.core.exceptions.ImproperlyConfigured``
        is raised.
    """
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration backend %s: "%s"' % (module, e))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration backend named "%s"' % (module, attr))

    return backend_class(*args, **kwargs)

def get_backend(name):
    return get_instance_from_path(settings.BACKEND_MAPPING[name], name)
