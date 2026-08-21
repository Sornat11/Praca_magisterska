"""
Moduł zawierający łatki (monkey-patching) dla biblioteki RecBole.
W nowszych wersjach NumPy/SciPy usunięto starsze interfejsy z `numpy.random`,
co powoduje błędy przy inicjalizacji modeli. Ten skrypt zapewnia kompatybilność.
Używać ostrożnie i pamiętać przy ewentualnej aktualizacji środowiska.
"""
import pkgutil
import importlib.machinery
import numpy as np

# We subclass the original C implementation of RandomState (numpy.random.mtrand.RandomState)
# and use a custom metaclass to ensure that isinstance(x, np.random.RandomState) returns True
# for instances of both the wrapper and the original mtrand.RandomState. This avoids breaking SciPy.
mtrand_RS = np.random.mtrand.RandomState
class RandomStateWrapperMeta(type(mtrand_RS)):
    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, mtrand_RS)

class RandomStateWrapper(mtrand_RS, metaclass=RandomStateWrapperMeta):
    def integers(self, low, high=None, size=None, dtype=int, endpoint=False):
        return self.randint(low, high, size, dtype)

def apply_patches() -> None:
    # NumPy 2.0+ Compatibility for RecBole Colab
    if not hasattr(np, 'float_'): np.float_ = np.float64
    if not hasattr(np, 'float'): np.float = np.float64
    if not hasattr(np, 'int_'): np.int_ = np.int64
    if not hasattr(np, 'int'): np.int = np.int64
    if not hasattr(np, 'bool_'): np.bool_ = bool
    if not hasattr(np, 'bool'): np.bool = bool
    if not hasattr(np, 'object'): np.object = object
    if not hasattr(np, 'complex_'): np.complex_ = np.complex128
    if not hasattr(np, 'complex'): np.complex = complex

    if not hasattr(pkgutil, 'ImpImporter'):
        class ImpImporter:
            pass
        pkgutil.ImpImporter = ImpImporter

    # PyTorch 2.6+ Compatibility (Colab)
    import torch
    original_torch_load = torch.load
    def patched_torch_load(*args, **kwargs):
        kwargs.setdefault('weights_only', False)
        return original_torch_load(*args, **kwargs)
    torch.load = patched_torch_load

    if hasattr(importlib.machinery, 'FileFinder') and not hasattr(importlib.machinery.FileFinder, 'find_module'):
        def find_module(self, fullname, path=None):
            return None
        importlib.machinery.FileFinder.find_module = find_module

    np.random.RandomState = RandomStateWrapper

    from recbole.trainer import Trainer
    original_fit = Trainer.fit
    def patched_fit(self, *args, **kwargs):
        args_list = list(args)
        if len(args_list) > 2:
            args_list[2] = True  # verbose
        else:
            kwargs['verbose'] = True
        if len(args_list) > 4:
            args_list[4] = True  # show_progress
        else:
            kwargs['show_progress'] = True
        return original_fit(self, *args_list, **kwargs)
    Trainer.fit = patched_fit

# Aby zastosować łatki, należy wywołać utils.recbole_patch.apply_patches() jawnie w głównym skrypcie.
