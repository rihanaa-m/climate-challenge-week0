import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

try:
    from app.utils import filter_data, get_country_options, get_monthly_trends, load_data
except ImportError:
    from utils import filter_data, get_country_options, get_monthly_trends, load_data

st.set_page_config(page_title="Climate Insights Dashboard", page_icon="🌍", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    """Load dashboard data once per session."""
    return load_data()


def main():
    st.title("🌍 Climate Insights Dashboard")
    st.caption("Interactive climate exploration by country, year, and variable")

    df = get_data()
    if df.empty:
        st.error(
            "No valid CSV data found. Add climate CSV files in `data/` "
            "or the project root, then refresh."
        )
        st.stop()

    countries = get_country_options(df)
    min_year = int(df["YEAR_INT"].min())
    max_year = int(df["YEAR_INT"].max())

    st.sidebar.header("Filters")
    selected_countries = st.sidebar.multiselect(
        "Country selector",
        options=countries,
        default=countries,
        help="Choose one or more countries to compare",
    )
    selected_year_range = st.sidebar.slider(
        "Year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        help="Zoom into a specific period",
    )
    variable_options = [var for var in ["T2M", "PRECTOTCORR", "RH2M"] if var in df.columns]
    selected_variable = st.sidebar.selectbox(
        "Variable selector",
        options=variable_options,
        index=0,
        help="Choose a variable to inspect monthly trends",
    )

    filtered = filter_data(df, selected_countries, selected_year_range)
    if filtered.empty:
        st.warning("No data matches your filters. Adjust country or year range.")
        st.stop()

    k1, k2, k3 = st.columns(3)
    k1.metric("Records", f"{len(filtered):,}")
    k2.metric("Countries", filtered["COUNTRY"].nunique())
    k3.metric("Period", f"{selected_year_range[0]}-{selected_year_range[1]}")

    st.subheader(f"Monthly {selected_variable} Trend")
    monthly = get_monthly_trends(filtered, selected_variable)

    fig1, ax1 = plt.subplots(figsize=(12, 5))
    for country in monthly["COUNTRY"].unique():
        country_data = monthly[monthly["COUNTRY"] == country]
        ax1.plot(
            country_data["PLOT_DATE"],
            country_data[selected_variable],
            label=country,
            linewidth=2,
        )
    ax1.set_xlabel("Date")
    ax1.set_ylabel(selected_variable)
    ax1.set_title(f"{selected_variable} monthly means by country")
    ax1.legend(loc="best")
    plt.xticks(rotation=45)
    st.pyplot(fig1, use_container_width=True)

    st.subheader("Precipitation Distribution")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered, x="COUNTRY", y="PRECTOTCORR", ax=ax2)
    ax2.set_xlabel("Country")
    ax2.set_ylabel("PRECTOTCORR")
    ax2.set_title("PRECTOTCORR distribution across selected countries")
    plt.xticks(rotation=25)
    st.pyplot(fig2, use_container_width=True)

    with st.expander("Filtered data preview"):
        st.dataframe(filtered.head(200), use_container_width=True)


if __name__ == "__main__":
    main()