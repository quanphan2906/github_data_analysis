import streamlit as st
import analysis
import seaborn as sns

sns.set_theme()
data = analysis.Analysis()

st.title("⌨️ Choice of license in open-sourced Github repositories ⌨️")

st.markdown("Author: [Quan Phan](https://github.com/quanphan2906)")

st.header("👋 Introduction")

"In software engineering, especially in the open-source world, a license of a project provides important information on how people other than the authors can use, distribute, and modify the project."

"In this analysis, I want to understand how the choice of license changes across different open-sourced projects and communities. More specifically, I want to answer three questions..."

st.markdown(
    """
    1. What is the most popular license in the open-sourced world?
    2. How does the choice of license differs for a popular, well-known project, compared to a regular-size open-source repo?
    3. How does the choice of license differs across open-source communities (by programming language)?
    """
)

"This analysis was inspired by my recent research and choice of license for a new open-source project."

st.header("🍌 Data")
st.markdown(
    """
The dataset is a sample of 10,000 data points, taken from the version 2 of the [Github Dataset](https://www.kaggle.com/datasets/nikhil25803/github-dataset/data) on Kaggle. Readers can find the description of the data in the Kaggle link.
"""
)

st.header("🏆 Top choice licenses")

data.plot_top_licenses(7)

"It is impressive to see 50% of the projects use the MIT license. The runner-ups are Apache License 2.0 and GNU GPL v3.0."

"To better understand this distribution, here is a brief overview of these three licenses' features:"

st.markdown(
    """
__MIT license__ is known for its simplicity and permissive nature. It allows users to do almost anything they want with the code, even distributing, sublicensing, and selling copies of the software. The only major requirement is to include the original copyright and license notice in any copy of the software/source code.
"""
)

st.markdown(
    """
    __Apache License 2.0__ is as permissive as MIT license, and users can do almost anything they want with the code. However, a distinctive feature of the Apache License is its explicit grant of patent rights from contributors to users, protecting users from patent litigation. In addition, it requires modifications to be documented, making it easier for subsequent users to understand what was altered.
    """
)

st.markdown(
    """
    A key feature of __GNU GPL v3.0__ is its strong copyleft requirement. If you distribute modified versions of GPLv3-licensed software, you must also distribute the entire source code under GPLv3. This ensures that all modified versions of the software remain free and open.
    """
)

"With this understanding, we can hypothesize the reasons behind the distribution we saw earlier. The MIT license, due to its simplicity and minimal requirements, becomes the most widely adopted license across the open-sourced community. The runner-ups, Apache  2.0 and GNU GPL v3.0, are also famous because they are as permissive as the MIT license, but are less appealing as the champion due to their additional requirements, including the modifications documentation requirement of Apache 2.0 and the strong copyleft of GNU GPL v3.0."

st.header("🍉 Prefered license types in popular vs. regular repositories")

st.subheader("Hypothesis")
"One hypothesis that might spring off from our understanding of the licenses is this. MIT license might be more appealing to a typical, small-scale project due to its simplicity. Conversely, the Apache 2.0 License offers more protection against patent infringement claims and has explicit grants of patent rights. This might make it more appealing for larger and commercially-oriented projects, which could be more prevalent in the popular group."

st.subheader("Popular vs. regular repositories")

st.markdown(
    """To examine this hypothesis, I first define what a popular repository is versus a typically small-scale one, and separate them into two groups: A popular (and mature) project is any project with the __weighted average number of stars, watchers, forks, and pull requests larger than the upper interquartile range of this metric__. The rest, I call regular projects. 
    """
)

data.compute_composite_score()
composite_outlier_category_counts = data.split_typical_popular()
typical = composite_outlier_category_counts.values[0]
popu = composite_outlier_category_counts.values[1]

f"By this definition, we have {typical} typical repositories ({typical / (typical + popu) * 100}%), and {popu} popular repositories ({popu / (typical + popu) * 100}%)."

st.markdown(
    """
    In defining my proxy metric, I intentionally leave out the number of commits. My _assumption_ is that the number of commits does not necessarily correlate with the maturity of a project. A high number of commits might just mean a high number of bug fixes. Alternatively, beginner developers can push many commits without good reasons. I also use the upperquartile range of this proxy metric as a cutoff point because as a norm in the Stats community, anything beyond the upperquartile range is considered outliers.
    """
)

st.subheader("Result")

"While MIT license dominates in both the popular and regular-size project groups, the percentage is considerably higher in the latter (10 percentage unit difference). Among the three, only Apache 2.0 has a higher usage rate in the popular project group compared to the typical group."

license_distribution_outliers, license_distribution_typical = data.get_license_distribution()
data.plot_license_dist(license_distribution_outliers, license_distribution_typical)

"This result confirms the direction of my initial hypothesis, that a small-scale project is more likely to use the MIT license and the popular, mature projects are more likely to use Apache 2.0. However, the magnitude of difference is not as significant as I expected."

st.header("⌨️ Prefered license types across different open-sourced communities")

"Here, I have no hypothesis to start out with, so let's begin by getting to know the largest programming communities:"

top_10_languages = data.get_and_plot_top_10_languages()

"This is a well-expected list. Let's see how the choice of license differs across the communities."

data.plot_lang_and_license(top_10_languages)

"Notice the high usage proportion of MIT license in Javascript and Typescript projects. This pattern well aligns with the strong culture of sharing and building upon others' work in the web development world (which heavily uses Javascript and Typescript). In addition, many large and influential projects in these languages (like Angular, React, Express.js) use the MIT License, setting a precedent for others in the community."

data.plot_lang_and_license(top_10_languages, "Apache License 2.0")

"Apache License 2.0 is significantly more popular in the Java community than the rest. The connection between these two are more subtle. One hypothesis is that since both Java and Apache 2.0 (with its explicit grants of patent rights) are widely used in the enterprise environments, there are more Java projects with Apache 2.0 than other languages."

data.plot_lang_and_license(top_10_languages, "GNU General Public License v3.0")

"Finally, we see GNU GPL v3.0 is more widely used in the C++ and Python communities than the rest, although the difference is not that significant."

st.header("🍊 Conclusion")

"In this analysis, I have explored and answered all the questions in the Introduction related to the choice of licenses. Here are some highlights..."

st.markdown(
    """
    1. The most popular license in the open-sourced world is MIT license, followed by Apache 2.0 and GNU GPL v3.0.
    2. Compared to large, well-known project, a small-scale project is more likely to use the MIT license. Conversely, Apache 2.0 is more popular for large projects than small ones.
    3. MIT license has the highest usage proportion in the web development community, while Apache 2.0 is the most popular in the Java community.
    """
)

"I hope you had fun following this analysis and it is somehow helpful for your choice of license in your next open-source project. Thanks for following along and will see you in an interview 😉"
