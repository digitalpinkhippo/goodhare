"""
Compatibility shim for pkgutil.get_loader on Python 3.12+
This fixes the AttributeError: module 'pkgutil' has no attribute 'get_loader'
"""

import sys
import pkgutil

# Check if get_loader exists (it was removed in Python 3.12+)
if not hasattr(pkgutil, 'get_loader'):
    import importlib.util
    
    def get_loader(fullname):
        """
        Compatibility shim for pkgutil.get_loader.
        Returns the loader for the given module name.
        """
        try:
            spec = importlib.util.find_spec(fullname)
            if spec is not None:
                return spec.loader
        except (ImportError, AttributeError, ValueError):
            pass
        return None
    
    # Add the function to pkgutil module
    pkgutil.get_loader = get_loader

