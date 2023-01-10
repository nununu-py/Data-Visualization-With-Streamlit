import random
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

df = pd.DataFrame(data=np.random.randint(
    low=10, high=20, size=(10, 3)), columns=['A', "B", "C"])

st.bar_chart(data=df)
st.area_chart(data=df)
st.line_chart(data=df)

new_df = pd.read_csv('tips.csv')

# PLOTLY
st.header("Visualization With Plotly")
st.markdown("---")

fig = px.histogram(data_frame=new_df, x='total_bill')
st.plotly_chart(fig)

fig = px.histogram(data_frame=new_df, x='total_bill', color="sex")
st.plotly_chart(fig)

# FEATURE
feature = ['sex', 'day', 'smoker', 'time']

feature_selected = st.selectbox(label="select feature", options=feature)
fig = px.histogram(data_frame=new_df, x="total_bill", y='tip',
                   color=feature_selected)
st.plotly_chart(fig)

feature_selected2 = st.selectbox(label="select feature ", options=feature)
fig = px.scatter(data_frame=new_df, x="total_bill", y='tip',
                 color=feature_selected2, size="tip")
st.plotly_chart(fig)

feature_selected3 = st.multiselect(label='select feature', options=feature)
fig = px.sunburst(data_frame=new_df, path=feature_selected3)
st.plotly_chart(fig)

# BOKEH
st.markdown('---')
st.header('Visualization With Bokeh')

x = [1, 2, 3, 4, 5, 6]
y = [random.randint(1, 10) for x in range(1, 7)]

p = figure(title="Line Chart", x_axis_label="x", y_axis_label="Y")
p.line(x, y, line_width=2)
p.circle(x, y, size=5)
st.bokeh_chart(p)

p = figure(title='Scatter plot and coloring by categories')

select = st.selectbox('select the categories',
                      ('sex', 'smoker', 'day', 'time'))

color_palette = ['blue', 'red', 'green', '#D35400', 'black']

unique_cats = new_df[select].unique()

index_cmap = factor_cmap(select, palette=color_palette[:len(unique_cats)],
                         factors=sorted(unique_cats))

p.circle('total_bill', 'tip', source=new_df,
         fill_color=index_cmap, size=12, legend=select)

st.bokeh_chart(p)
