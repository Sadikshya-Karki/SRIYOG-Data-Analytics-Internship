# GardenSewa Yearly Services Analysis

**Prepared for:** Sriyog Consulting | **Date:** August 2026

## About
Analysis of the yearly demand pattern for GardenSewa's 20 gardening and landscaping services, rating each service's monthly demand as Low, Medium, or High based on Nepal's climate cycle (pre-monsoon, monsoon, post-monsoon, winter) and major festivals such as Dashain and Tihar.

## Files
| File | Description |
|------|-------------|
| `Yearly_Services.xlsx` | Raw dataset |
| `Yearly_Services.ipynb` | Full report with introduction, analysis, visualizations, and key findings |
| `Yearly_Services_Report.html` | HTML export of .ipynb file |

## Key Findings
- April is the busiest month, with 15 of the 20 services (75%) rated High demand, followed by March and October, tied at 12 each
- January, August, and December have zero services rated High demand, marking the quietest stretches of the year
- Medium demand is the most common rating overall at 39.6% of all monthly ratings, followed by Low at 33.8% and High at 26.7%
- Garden Care has the longest average High demand window at 5 months per service, driven mainly by Flower Maintenance
- Seasonal Services and Landscape Lighting break from the weather driven pattern, peaking instead around Dashain and Tihar between September and November
- Design and Consultation, Planting Services, and Tree Services have the shortest average High demand window at 2.5 months each, pointing to sharper, more concentrated seasonal spikes

## Tools Used
- Python (pandas, matplotlib, seaborn)
- Jupyter Notebook
- Microsoft Excel
