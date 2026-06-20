import pkgutil
if not hasattr(pkgutil, 'ImpImporter'):
    class ImpImporter:
        pass
    pkgutil.ImpImporter = ImpImporter

import numpy as np
# We subclass the original C implementation of RandomState (numpy.random.mtrand.RandomState)
# and use a custom metaclass to ensure that isinstance(x, np.random.RandomState) returns True
# for instances of both the wrapper and the original mtrand.RandomState. This avoids breaking SciPy.
mtrand_RS = np.random.mtrand.RandomState
class RandomStateWrapperMeta(type(mtrand_RS)):
    def __instancecheck__(cls, instance):
        return isinstance(instance, mtrand_RS)

class RandomStateWrapper(mtrand_RS, metaclass=RandomStateWrapperMeta):
    def integers(self, low, high=None, size=None, dtype=int, endpoint=False):
        return self.randint(low, high, size, dtype)
np.random.RandomState = RandomStateWrapper

from recbole.trainer import HyperTuning
from recbole.quick_start import objective_function as recbole_objective_function

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

def objective_function(config_dict=None, config_file_list=None, saved=True):
    fixed_config = {
        'checkpoint_dir': '3_Evaluation/Saved/',
        'state': 'INFO'
    }
    if config_dict is None:
        config_dict = {}
    config_dict.update(fixed_config)
    return recbole_objective_function(
        config_dict=config_dict, 
        config_file_list=config_file_list,
        saved=saved
    )

if __name__ == '__main__':
    model_name = 'NeuMF'
    config_file_list = ['2_Experiments/Configs/ncf.yaml']
    params_file = '2_Experiments/Hyperparams/ncf.hyper'
    output_file = f'3_Evaluation/Reports/hyper_results_ncf.result'

    hp = HyperTuning(
        objective_function, 
        params_file=params_file,
        fixed_config_file_list=config_file_list
    )

    print(f"Rozpoczynam optymalizację parametrów dla modelu: {model_name}")
    hp.run()
    hp.export_result(output_file)
    
    print(f"\nOptymalizacja zakończona!")
    print(f"Najlepsze parametry: {hp.best_params}")
    print(f"Wyniki zapisano w: {output_file}")
