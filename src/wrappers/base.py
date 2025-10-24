import os
import importlib
import pkgutil

# Dynamically import all modules in the wrappers package
__all__ = []
for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    if name != 'base':  # Skip importing self
        module = importlib.import_module(f'.{name}', package='src.wrappers')
        # Add any classes from the module to __all__
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, type) and item.__module__ == f'src.wrappers.{name}':
                __all__.append(item_name)
                globals()[item_name] = item
print(__all__)
