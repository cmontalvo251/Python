"""
Hi Carlos,

Pandas is amazing!!! Just wanted to share with you the ability to convert an excel table to a .tex file :) Only three lines of  code.
"""

import pandas as pd
df = pd.read_excel(r'Example.xlsx')
df.to_latex('output.tex')


"""
Thanks,
Lisa Schibelius
Pronouns she | her
Graduate Teaching Assistant | PhD Student
Virginia Tech |  Department of Engineering Education
"""
