# Employee Data Analysis

Prepared for: Sriyog Consulting | Date: July, 2026

## About
This project analyzes data for 1,474 employees, covering department, salary, performance rating, attendance, tenure and promotion status. The goal is to understand how these different aspects of the workforce relate to each other, such as whether higher performance leads to higher pay or promotion, and whether staying longer at the company makes a real difference.

## Files
| File | Description |
|---|---|
| finalanalyze_with_tenure_1.csv | Raw dataset |
| Employee_Data_Analysis.ipynb | Jupyter notebook with the full analysis and charts |
| Employee_Data_Analysis.html | HTML export of the notebook |
| Employee_Data_Analysis.pdf | Final analysis report with charts and insights |

## Key Findings
- 43 rows have "Unknown" values spread across Department, Gender, Job Role, Promotion Status and Work Location.
- A few salary entries look like data errors, as low as Rs 100 and as high as Rs 50 lakh.
- Operations and Logistics pay the highest on average once outliers are set aside; Customer Support and HR pay the least.
- Salary does not move together with performance rating or employee value score.
- Tenure has almost no relationship with employee value score.
- Promotion rate stays around 33-37% regardless of value rating, department or gender.

## Tools Used
Python, pandas, matplotlib, seaborn, Jupyter Notebook