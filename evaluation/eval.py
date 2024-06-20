# Use this file to evaluate the model responses generated from runs.py, by using metrics.py
# Generate results.csv and html for all model variants
import pandas as pd
from evaluation.metrics import Scorer

results_registry = {
    'results/adapter_prompt1.csv': 'llava_adapter_optimized_prompt',
    'results/adapter_prompt2.csv': 'llava_adapter_gpt_prompt',
    'results/adapter_prompt3.csv': 'llava_adapter_naive_prompt',
    'results/base_prompt1.csv': 'llava_base_optimized_prompt',
    'results/base_prompt2.csv': 'llava_base_gpt_prompt',
    'results/base_prompt3.csv': 'llava_base_naive_prompt',
    'results/random_output.csv': 'random'
}

model_names = []
instance_scores = []
episodic_scores = []
vicinity_3 = []
vicinity_6 = []
success_3 = []
success_6 = []


for result in results_registry.keys():
    llava_scorer = Scorer(result)
    model_names.append(results_registry[result])
    instance_scores.append(llava_scorer.get_instance_score())
    episodic_scores.append(llava_scorer.get_episodic_score())
    vicinity_3.append(llava_scorer.get_vicinity_score(3))
    vicinity_6.append(llava_scorer.get_vicinity_score(6))
    success_3.append(llava_scorer.get_success_score(3))
    success_6.append(llava_scorer.get_success_score(6))

res = {
    'model_names': model_names,
    'instance_scores': instance_scores,
    'episodic_scores': episodic_scores,
    'vicinity_3': vicinity_3,
    'vicinity_6': vicinity_6,
    'success_3': success_3,
    'success_6': success_6
}

res_df = pd.DataFrame(res)
res_df.to_csv('results/result.csv')
res_df.to_html('results/result.html')