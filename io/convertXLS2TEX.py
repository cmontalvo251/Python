import pandas as pd
df = pd.read_excel(r'Example.xlsx')
df.to_latex('output.tex')
