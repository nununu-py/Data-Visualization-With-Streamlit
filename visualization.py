import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.header("Data Visualization")
st.markdown("---")

dataframe = pd.read_csv('d:/Bootcamp/Data Viz Udemy (Gusksra)/tips.csv')
st.caption("Random 10 Sample Data Frame")

button1, button2 = st.columns(2, gap="small")

with st.container():

    with button1:
        show_dataBtn = st.button("Show Data")

    with button2:
        cancel_dataBtn = st.button("Cancel")

    if show_dataBtn:
        sample = dataframe.sample(10)
        st.dataframe(data=sample)

    if cancel_dataBtn:
        show_dataBtn = False

# STATIC
st.markdown("---")
st.header("Static Visualization")
st.write("Make Bar Chart and Pie Chart")

with st.container():

    sex_distribution = dataframe['sex'].value_counts()
    pie_chart, bar_chart = st.columns(2)

    with pie_chart:

        expander = st.expander("PIE CHART VISUALIZATION")

        with expander:

            fig, ax = plt.subplots()
            ax.pie(sex_distribution, autopct="%0.2f%%",
                   labels=["Male", "Female"])
            image = st.pyplot(fig)

    with bar_chart:

        expander = st.expander("BAR CHART VISUALIZATION")

        with expander:

            fig, ax = plt.subplots()
            ax.bar(sex_distribution.index, sex_distribution)
            st.pyplot(fig)


with st.expander("CHECK TABLE INFO"):

    st.write(sex_distribution)


# DYNAMIC
st.markdown("---")
st.header("Dynamic Visualization")
st.write("Make Bar Chart and Pie Chart Using Multiselect Feature")

with st.container():

    feature = dataframe.dtypes

    # Get ONLY Categorical Data
    list_feature = list(feature[feature == "object"].index)

    # st.write(select_feature)

    select_feature = st.selectbox(
        label="Select Feature Do You Want", options=list_feature)

    pie_chart, bar_chart = st.columns(2)

    with pie_chart:

        if select_feature:
            count_values = dataframe[select_feature].value_counts()
            fig, ax = plt.subplots()
            ax.pie(count_values, autopct="%0.2f%%",
                   labels=count_values.index)
            image = st.pyplot(fig)

    with bar_chart:

        if select_feature:
            count_values = dataframe[select_feature].value_counts()
            fig, ax = plt.subplots()
            ax.bar(count_values.index, count_values)
            st.pyplot(fig)

    with st.expander("Feature Selected Count Display"):

        st.write(count_values)

# USING SEABORN

st.markdown("---")
st.header("Sex Distribution 'Static Visualization' with Box plot")

fig, ax = plt.subplots()
sns.boxplot(data=dataframe, x="sex", y="total_bill", ax=ax)

st.pyplot(fig=fig)

st.markdown("---")

with st.container():

    st.header("Select Feature 'Dynamic Visualization'")
    feature = st.selectbox(
        label="Select Feature To Visualization", options=list_feature)

    fig, ax = plt.subplots()
    sns.boxplot(data=dataframe, x=feature, y="total_bill", ax=ax)

    st.pyplot(fig)

st.markdown("---")
st.header("Multi Chart Visualization")

with st.container():

    chart = ("box", "violin", "kdeplot", "histogram")

    col1, col2 = st.columns(2)

    with col1:
        viz = st.selectbox(label="Select Visualization", options=chart)
    with col2:
        feature = st.selectbox(label="Select Feature", options=list_feature)

    if viz == "box":
        fig, ax = plt.subplots()
        sns.boxplot(data=dataframe, x=feature, y="total_bill", ax=ax)

    elif viz == "violin":
        fig, ax = plt.subplots()
        sns.violinplot(data=dataframe, x=feature, y="total_bill", ax=ax)

    elif viz == "kdeplot":
        fig, ax = plt.subplots()
        sns.kdeplot(x=dataframe['total_bill'], hue=dataframe[feature], ax=ax)

    else:
        fig, ax = plt.subplots()
        sns.histplot(data=dataframe, hue=feature,
                     x="total_bill", ax=ax, alpha=0.6, multiple="stack")

    st.pyplot(fig)

# DISTIBUTION OF TOTAL BILL, GROUP BY SEX AND DAYS

st.markdown("---")
st.header("Visualization The Distribution Total Bill, Group by \
    Sex and Day")
feature_to_group = ["day", "sex"]
feature = ["total_bill"]
select_columns = feature_to_group+feature

new_dataframe = dataframe[select_columns].groupby(feature_to_group).mean()

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.write("Dataframe total bill group by day and sex")
        st.dataframe(new_dataframe)

        fig, ax = plt.subplots()
        new_dataframe.plot(kind="bar", ax=ax)
        ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.9))
        st.pyplot(fig)

    with col2:
        st.write("Dataframe total bill group by day and sex 'unstack position'")
        new_dataframe1 = new_dataframe.unstack()
        st.dataframe(new_dataframe1)
        for i in range(5):
            st.write(" ")
        fig, ax = plt.subplots()
        new_dataframe1.plot(kind="bar", ax=ax,
                            stacked=True)  # stacked = False
        ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.9))
        st.pyplot(fig)

# PLOT CONTROL MULTIPLE WIDGET
st.markdown("---")
st.header("Interactive Visualization Using Multi Widget")

with st.container():

    col1, col2, col3 = st.columns(3)

    data = dataframe
    data_col = data.dtypes
    x_axes = list(data_col[data_col == "O"].index)
    y_axes = ['total_bill']

    with col1:

        xaxes_sel = st.multiselect(
            "Select X Axes Features : ", options=x_axes, default=x_axes[0])
        len_xaxes_sel = len(xaxes_sel)

    with col2:

        chart = ["line", "bar", "area"]
        chart_select = st.selectbox("Select Chart You Want", options=chart)

    with col3:

        stacked_pos = st.radio(label="Stacked Position", options=["Yes", "No"])

        if stacked_pos == "Yes":
            stacked_pos = True
        else:
            stacked_pos = False

if len_xaxes_sel < 1:
    st.warning("NO FEATURE SELECTED")

fig, ax = plt.subplots()

grouping_data = data[xaxes_sel+y_axes].groupby(xaxes_sel).mean()

if len_xaxes_sel > 1:
    for i in range(len_xaxes_sel-1):
        grouping_data = grouping_data.unstack()

    fig, ax = plt.subplots()
    grouping_data.plot(kind=chart_select, ax=ax, stacked=stacked_pos)
    grouping_data.fillna(0, inplace=True)

else:

    fig, ax = plt.subplots()
    grouping_data.plot(kind=chart_select, ax=ax)

# Viz

ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.8))
ax.set_ylabel("Avg Total Bills")
st.pyplot(fig)

st.header("Show The Data From Visualization")
with st.expander("This is Your Data"):
    st.dataframe(grouping_data)
