from pgmpy.readwrite import BIFReader
from pgmpy.sampling import BayesianModelSampling
import pandas as pd

# Load the .bif file
network_name = 'earthquake'
reader = BIFReader(f'./data/networks/{network_name}.bif')
sample_size = 1000

model = reader.get_model()

# Generate samples
sampler = BayesianModelSampling(model)
samples = sampler.forward_sample(size=sample_size)

# Create mapping from category names to indices
mapping = {var: {state: i for i, state in enumerate(model.get_cpds(var).state_names[var])}
           for var in model.nodes()}

# Convert category names to indices
samples = samples.replace(mapping)

# Save samples to .dat file
with open(f'{network_name}-{sample_size}.dat', 'w') as f:
    # Write variable names (0 to n)
    f.write(' '.join(map(str, range(len(model.nodes())))) + '\n')
    
    # Write the number of categories
    categories = [len(model.get_cpds(var).state_names[var]) for var in model.nodes()]
    f.write(' '.join(map(str, categories)) + '\n')
    
    # Write the samples
    for _, row in samples.iterrows():
        f.write(' '.join(map(str, row.values.tolist())) + '\n')
