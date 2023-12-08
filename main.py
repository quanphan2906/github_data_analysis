"""
Find and highlight an interesting insight or pattern 
in the GitHub projects data and develop visualizations to showcase this.
"""

import streamlit as st
import analysis

st.title("Impact of License Types on Open Source Project Metrics")

st.header("Introduction")

st.markdown(
    "The goal of this analysis is to provide insights into how the **choice of license** might influence **project engagement and contribution** in the *open source* community."
)

st.markdown(
    """
To that end, I examine the correlations between open source project licenses and key project metrics, including 
- star counts
- fork counts
- pull requests
- commit counts.
"""
)

"I focus on three popular licenses – the MIT License, GNU General Public License v3.0 (GPL 3.0), and Apache License 2.0. These licenses were chosen due to their popularity and distinct characteristics, offering a broad view of different open source licensing approaches."

st.header("Data source")

st.markdown(
    """
The dataset is a sample of 10,000 data points, taken from the version 2 of the [Github Dataset](https://www.kaggle.com/datasets/nikhil25803/github-dataset/data) on Kaggle.
"""
)

st.header("Preliminary")

f"""The majority of the repositories ({analysis.license_counts_percentage["MIT License"].round()}%) are licensed under the MIT license, which is well expected. The MIT license is known for its permissiveness, simplicity and compatibility with many other types of licenses, which makes it a popular choice among developers and organizations, all-size alike. While Apache 2.0 ({analysis.license_counts_percentage["Apache 2.0"].round()}%) and GNU GPL 3.0 ({analysis.license_counts_percentage["GNU GPL v3.0"].round()}%) are all popular options, their popularity is nowhere near the MIT license."""

analysis.license_value_counts()

"Maybe we also do the distribution of the engagement metrics"

st.header("License type correlates with popularity of repo")

"""
To start off our correlation analysis, let us focus on the average values of the engagement metrics across different license types. Consistently across all metrics, Apache 2.0 takes the lead, followed by GNU GPL 3.0 and MIT License, in that order.
"""

analysis.generate_grouped_bar_chart(analysis.filtered_data)
analysis.generate_grouped_bar_chart(
    analysis.top_20_percent_df,
    title="Average value of metrics by license (top 20% most popular repos)",
)

analysis.generate_box_plot_and_summary("stars_count", analysis.top_20_percent_df)

analysis.generate_overlaid_histograms()
analysis.generate_overlaid_kde_plots()
