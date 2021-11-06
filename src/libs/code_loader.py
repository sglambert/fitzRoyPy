from importlib import import_module


def dynamic_import(module, project_root=None, dir_path=None):
    """ Dynamically imports a module using import_module method in importlib module
    """
    module_import_path = '.'.join(filter(None, [project_root, dir_path, module]))
    module = import_module(module_import_path)
    return module


def get_resources():
    """ Helper method to load the resources.py script and instantiate a resourceFactory object.
    """
    resource_module = dynamic_import('resources', project_root='src', dir_path='libs')
    resource = resource_module.Resources()
    return resource
