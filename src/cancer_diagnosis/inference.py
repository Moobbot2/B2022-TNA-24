import pandas as pd
from unidecode import unidecode


try:
    from config.config import (FEATURES, KQ)
    from src.cancer_diagnosis.training import train_evaluate_visualize_decision_tree
except:
    from helpers import add_path_init
    add_path_init()
    from config import (FEATURES, KQ)
    from cancer_diagnosis.training import train_evaluate_visualize_decision_tree
