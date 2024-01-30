import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("survey_results_public.csv")

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    # Apply notnull checks for each column as you did in your notebook
    df = df[df["Country"].notnull()]

    df = df[df["EdLevel"].notnull()]

    df = df[df["YearsCodePro"].notnull()]

    df = df[df["Employment"].notnull()]

    df = df[df["ConvertedCompYearly"].notnull()]

    

    # Apply your existing category shortening and cleaning functions
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    
    # Filter based on salary
    df = df[df["ConvertedCompYearly"] <= 200000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    # Clean experience and education levels
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    
    # Rename salary column for consistency
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("### Stack Overflow Developer Survey 2022")

    data = df["Country"].value_counts()
    top_n = 10
    top_categories = data.nlargest(top_n)
    other_sum = data.iloc[top_n:].sum()
    top_categories['Other'] = other_sum

    # Create explode data
    explode_vals = [0.1 if i < top_n else 0 for i in range(top_n + 1)]

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.pie(top_categories, labels=top_categories.index, autopct="%1.1f%%", startangle=90, explode=explode_vals)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.

    # Set the facecolor of the figure to transparent
    fig.patch.set_facecolor('none')
    # Set the facecolor of the axis to transparent
    ax.patch.set_facecolor('none')

    # Save the figure with a transparent background
    plt.savefig('pie_chart.png', transparent=True)

    for text in ax.texts:
        text.set_color('white')

    st.pyplot(fig)  # Display the plot in Streamlit
   
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)