import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import chi2_contingency
import streamlit as st


class Analysis:
    def __init__(self) -> None:
        self.data = pd.read_csv("data/repository_data_10k.csv")
        self.numerical_columns = ["stars_count", "forks_count", "watchers", "pull_requests"]
        self.license_types = [
            "MIT License",
            "GNU General Public License v3.0",
            "Apache License 2.0",
        ]

    def compute_composite_score(self):
        data = self.data
        numerical_columns = self.numerical_columns

        data[numerical_columns] = data[numerical_columns].fillna(data[numerical_columns].median())

        scaler = MinMaxScaler()
        data_normalized = scaler.fit_transform(data[numerical_columns])
        weights = np.ones(len(numerical_columns)) / len(numerical_columns)
        composite_scores = np.dot(data_normalized, weights)
        data["Composite_Score"] = composite_scores

    def split_typical_popular(self):
        data = self.data

        # Determining the upper interquartile range for the composite score
        Q3_composite = data["Composite_Score"].quantile(0.75)
        IQR_composite = Q3_composite - data["Composite_Score"].quantile(0.25)
        upper_bound_composite = Q3_composite + 1.5 * IQR_composite

        # Classifying repositories as 'popular' if their composite score is beyond the upper interquartile range
        data["is_popular"] = data["Composite_Score"] > upper_bound_composite

        composite_outlier_category_counts = data["is_popular"].value_counts()
        return composite_outlier_category_counts

    def plot_top_licenses(self, top_count=5):
        license_counts = self.data["licence"].value_counts(normalize=True) * 100
        top_10_licenses = license_counts.round(1).head(top_count)

        # Plot setup
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = top_10_licenses.plot(kind="bar", ax=ax)

        # Setting labels and title
        ax.set_title(f"Top {top_count}  Most Used Licenses (by percentage)")
        ax.set_xlabel("License")
        ax.set_ylabel("Percentage of Projects")

        plt.xticks(rotation=45)
        ax.bar_label(bars.containers[0])
        plt.tight_layout()

        st.pyplot(fig)

    def get_license_distribution(self):
        data = self.data

        popular = data[data["is_popular"]]
        typical = data[data["is_popular"] == False]
        license_distribution_outliers = (
            popular["licence"].value_counts(normalize=True)[self.license_types] * 100
        )
        license_distribution_typical = (
            typical["licence"].value_counts(normalize=True)[self.license_types] * 100
        )

        return license_distribution_outliers, license_distribution_typical

    def plot_license_dist(self, license_distribution_outliers, license_distribution_typical):
        # Ensure that both series have the same index in the correct order
        index = self.license_types
        license_distribution_outliers = license_distribution_outliers.reindex(index).fillna(0)
        license_distribution_typical = license_distribution_typical.reindex(index).fillna(0)

        fig, ax = plt.subplots()
        grouped_data = pd.DataFrame(
            {
                "Popular Repositories": license_distribution_outliers,
                "Typical Repositories": license_distribution_typical,
            }
        ).T

        # Creating a grouped bar chart
        grouped_data.plot(kind="bar", ax=ax, figsize=(10, 6))
        ax.set_title("License Distribution Comparison")
        ax.set_ylabel("Percentage")
        ax.set_xlabel("Repository Type")

        # Annotate the bars with the percentage values
        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f%%", padding=3)

        plt.xticks(rotation=0)

        plt.tight_layout()
        st.pyplot(fig)

    def test_significance(self):
        data = self.data

        popular = data[data["is_popular"]]
        typical = data[data["is_popular"] == False]

        # MIT license
        mit_popular = popular["licence"].value_counts().get("MIT License", 0)
        mit_typical = typical["licence"].value_counts().get("MIT License", 0)
        non_mit_popular = popular.shape[0] - mit_popular
        non_mit_typical = typical.shape[0] - mit_typical

        contingency_table = np.array(
            [[mit_popular, non_mit_popular], [mit_typical, non_mit_typical]]
        )

        chi2, p, _, _ = chi2_contingency(contingency_table)

        # Apache License 2.0
        apache_popular = popular["licence"].value_counts().get("Apache License 2.0", 0)
        apache_typical = typical["licence"].value_counts().get("Apache License 2.0", 0)
        non_apache_popular = popular.shape[0] - apache_popular
        non_apache_typical = typical.shape[0] - apache_typical

        contingency_table_apache = np.array(
            [[apache_popular, non_apache_popular], [apache_typical, non_apache_typical]]
        )

        chi2_apache, p_apache, _, _ = chi2_contingency(contingency_table_apache)

        # Visualize the result
        test_results = pd.DataFrame(
            {
                "License": ["MIT License", "Apache 2.0"],
                "Chi-Squared": [chi2, chi2_apache],
                "p-value": [p, p_apache],
            }
        )

        return test_results

    def get_and_plot_top_10_languages(self):
        language_popularity = self.data["primary_language"].value_counts()
        top_10_languages = language_popularity.head(10)
        total_count = language_popularity.sum()
        top_10_languages_percentage = (top_10_languages / total_count) * 100

        # Plot setup
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = top_10_languages_percentage.plot(kind="bar", ax=ax)

        # Setting labels and title
        ax.set_title("Top 10 Programming Languages by Percentage")
        ax.set_xlabel("Programming Language")
        ax.set_ylabel("Percentage")

        # Add values on top of the bars
        for bar in bars.patches:
            ax.annotate(
                f"{bar.get_height():.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        return top_10_languages

    def plot_lang_and_license(self, top_10_languages, license="MIT License"):
        data = self.data

        top_10_languages_list = top_10_languages.index.tolist()
        filtered_data = data[data["primary_language"].isin(top_10_languages_list)]
        license_distribution = (
            filtered_data.groupby(["primary_language", "licence"]).size().unstack().fillna(0)
        )
        license_distribution_percentage = (
            license_distribution.div(license_distribution.sum(axis=1), axis=0) * 100
        )
        license_distribution_percentage = license_distribution_percentage.round(1)
        sorted_values = license_distribution_percentage[license].sort_values(ascending=False)

        # Plot setup
        fig, ax = plt.subplots(figsize=(8, 5))  # Adjust the figure size as needed

        # Plotting for the specified license
        bars = sorted_values.plot(kind="bar", ax=ax)
        ax.set_xticklabels(sorted_values.index, rotation=45, fontsize=12)
        ax.set_title(f"{license} Proportion by Programming Language", fontsize=14)
        ax.set_ylabel("Proportion (%)", fontsize=12)
        ax.set_xlabel("")

        for bar in bars.patches:
            ax.annotate(
                f"{bar.get_height():.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

        plt.tight_layout()
        st.pyplot(fig)
