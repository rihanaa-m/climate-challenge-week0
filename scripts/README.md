# Climate Data Dashboard

A Streamlit application for visualizing African climate data insights, built for COP32 preparation.

## Overview

This dashboard provides interactive visualizations of climate trends across Ethiopia, Kenya, Nigeria, Sudan, and Tanzania. It allows users to explore temperature trends, precipitation patterns, and other climate variables through an intuitive web interface.

## Features

- **Country Selection**: Multi-select dropdown to filter data by country
- **Year Range Slider**: Interactive slider to focus on specific time periods
- **Variable Selector**: Choose from multiple climate variables (T2M, PRECTOTCORR, RH2M, etc.)
- **Trend Charts**: Monthly average trends for selected variables
- **Distribution Plots**: Boxplots showing precipitation variability
- **Data Preview**: Table view of filtered data

## Installation

1. Ensure you have Python 3.8+ installed
2. Install required packages:
   ```bash
   pip install streamlit pandas numpy matplotlib seaborn
   ```

3. Place cleaned CSV files in a `data/` directory:
   - `data/ethiopia_clean.csv`
   - `data/kenya_clean.csv`
   - `data/nigeria_clean.csv`
   - `data/sudan_clean.csv`
   - `data/tanzania_clean.csv`

## Usage

### Local Development

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

3. Open your browser to `http://localhost:8501`

### Deployment

The app is designed for deployment on Streamlit Community Cloud:

1. Push this repository to GitHub
2. Connect to Streamlit Community Cloud
3. Set the main file path to `app/main.py`
4. Deploy

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py          # Main Streamlit application
│   └── utils.py         # Data processing utilities
├── scripts/
│   ├── __init__.py
│   └── README.md        # This file
├── data/                # Cleaned CSV files (ignored by git)
└── .gitignore
```

## Development Process

### Branch: dashboard-dev

1. **Initial Setup**: Created folder structure and basic file templates
2. **Data Loading**: Implemented CSV concatenation and preprocessing in `utils.py`
3. **UI Components**: Added Streamlit widgets for country selection, year range, and variable selection
4. **Visualizations**: Created trend line charts and boxplots
5. **Styling**: Applied clean, professional design with intuitive navigation
6. **Testing**: Verified functionality with sample data
7. **Documentation**: Added comprehensive README and inline comments

### Key Decisions

- Used Streamlit for rapid web app development
- Implemented caching for data loading performance
- Focused on core climate variables relevant to COP32
- Ensured responsive design for different screen sizes
- Added error handling for missing data files

## KPIs Met

- **Dashboard Usability**: Clear labels, logical layout, helpful tooltips
- **Interactive Elements**: Effective use of multiselect, slider, and dropdown widgets
- **Visual Appeal**: Professional matplotlib/seaborn plots with proper legends and labels
- **Deployment Ready**: Modular code structure suitable for cloud deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is part of the Climate Challenge Week 0 for COP32 preparation.