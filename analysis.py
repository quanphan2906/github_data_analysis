import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

data = pd.read_csv("data/repository_data_10k.csv")

# take repos with top 3 licenses
licenses_of_interest = [
    "MIT License",
    "GNU General Public License v3.0",
    "Apache License 2.0",
]
filtered_data = data[data["licence"].isin(licenses_of_interest)]
filtered_data.replace(
    {
        "GNU General Public License v3.0": "GNU GPL v3.0",
        "Apache License 2.0": "Apache 2.0",
    },
    inplace=True,
)
licenses_of_interest = [
    "MIT License",
    "GNU GPL v3.0",
    "Apache 2.0",
]

project_metrics = ["stars_count", "forks_count", "pull_requests", "commit_count", "watchers"]


top_20_percent_data_map = {}
top_20_percent_dfs = []

for license_type in licenses_of_interest:
    license_data = filtered_data[filtered_data["licence"] == license_type]

    percentile_80 = license_data["stars_count"].quantile(0.80)
    top_20_percent = license_data[license_data["stars_count"] >= percentile_80]
    top_20_percent_data_map[license_type] = top_20_percent
    top_20_percent_dfs.append(top_20_percent)

top_20_percent_df = pd.concat(top_20_percent_dfs)


license_counts_percentage = filtered_data["licence"].value_counts(normalize=True) * 100


def license_value_counts():
    fig, ax = plt.subplots()
    sns.barplot(
        x=license_counts_percentage.index,
        y=license_counts_percentage.values,
        palette="deep",
        ax=ax,
    )
    ax.set_title("Percentage Distribution of Projects by License")
    ax.set_xlabel("License")
    ax.set_ylabel("Percentage of Projects (%)")
    plt.xticks(rotation=45)

    st.pyplot(fig)


def generate_grouped_bar_chart(data=top_20_percent_df, title="Average value of metrics by license"):
    grouped_means = data.groupby("licence")[project_metrics].mean().reset_index()

    # Melt the DataFrame to long format for seaborn's barplot
    melted_data = grouped_means.melt(
        id_vars="licence", value_vars=project_metrics, var_name="Metric", value_name="Mean"
    )

    # Create the grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Metric", y="Mean", hue="licence", data=melted_data, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Metric")
    ax.set_ylabel("Mean Value")
    plt.xticks(rotation=45)

    st.pyplot(fig)


def generate_box_plot_and_summary(metric, data):
    if metric not in project_metrics:
        st.error(f"Invalid metric. Please choose from {project_metrics}.")
        return

    # Generate Box Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(y="licence", x=metric, data=data)
    ax.set_xscale("log")
    ax.set_title(f"Box Plot of {metric.capitalize().replace('_', ' ')} by License")
    ax.set_ylabel("License")
    ax.set_xlabel(metric.capitalize().replace("_", " "))
    plt.yticks(rotation=45)
    st.pyplot(fig)

    # Generate Five-Number Summary Table
    summary_df = pd.DataFrame()
    for license_type in licenses_of_interest:
        summary_series = data[data["licence"] == license_type][metric].describe()
        summary_df[license_type] = summary_series

    st.markdown(f"###### Five-Number Summary for {metric.replace('_', ' ').title()}")
    st.table(summary_df)


def generate_overlaid_histograms(data=filtered_data, metric="stars_count"):
    fig, ax = plt.subplots(figsize=(10, 6))

    for license_type in data["licence"].unique():
        # Filter data for each license
        license_data = data[data["licence"] == license_type]

        # Plot histogram
        ax.hist(license_data[metric], bins=30, alpha=0.5, label=license_type)

    ax.set_title(f'Distribution of {metric.capitalize().replace("_", " ")} by License')
    ax.set_xlabel(metric.capitalize().replace("_", " "))
    ax.set_ylabel("Frequency")
    ax.legend()

    st.pyplot(fig)


def generate_overlaid_kde_plots(data=filtered_data, metric="stars_count", use_log_scale=True):
    fig, ax = plt.subplots(figsize=(10, 6))

    for license_type in data["licence"].unique():
        # Filter data for each license
        license_data = data[data["licence"] == license_type][metric]

        # Calculate IQR and determine bounds for outliers
        Q1 = license_data.quantile(0.25)
        Q3 = license_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filter out outliers
        filtered_values = license_data[
            (license_data >= lower_bound) & (license_data <= upper_bound)
        ]

        # Plot KDE
        sns.kdeplot(filtered_values, ax=ax, label=license_type, fill=True)

    ax.set_title(
        f'Distribution of {metric.capitalize().replace("_", " ")} by License (Outliers Removed)'
    )
    ax.set_xlabel(metric.capitalize().replace("_", " "))
    ax.set_ylabel("Density")
    ax.legend()

    st.pyplot(fig)
