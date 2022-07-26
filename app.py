import streamlit as st
import requests
from datetime import date, time, timezone, timedelta
from datetime import datetime
from plotly import graph_objs as go
import pandas as pd
import numpy as np
#from get_data import load_data
import trainer_advanced
from PIL import Image
#from turtle import width
import altair as alt

# import final_python_file
# from final_python_file import load_data
# df_all_data = load_data
# Title st.title('Cryptocurrencies Prediction App')

# Page layout
## page expands to full width
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# Add image
image = Image.open('logo.png')
st.image(image, width = 90)

st.title('Chain Oracle App')

# Data for Graph

crypto_currencies=('ethereum', 'bitcoin', 'tether')

#selected_currency=st.selectbox('Select dataset for prediction', crypto_currencies)

# today = datetime.date.today()
# yesterday = today - datetime.timedelta(days = 1)
# tomorrow = today + datetime.timedelta(days = 1)
# print('Yesterday : ',yesterday)
# print('Today : ',today)
# print('Tomorrow : ',tomorrow)

# All the data from different sources in one DataFrame
#df = load_data()
data = pd.read_csv('raw_data/data_advanced_v2.csv')
trainer = trainer_advanced.Trainer(data)
trainer.preproc_data()

#my_expander = st.expander(#)
#my_expander.write(df.head(n=10))
#clicked = my_expander.button('Show raw data')

# Plot Graph
def plot_raw_data():
    fig = go.Figure()
    #fig.set_size(800, 400)
    fig.add_trace(go.Scatter(x=trainer.original_data.index,
                             y=trainer.original_data['price_usd']))
    fig.update_layout(title_text='Ethereum usd price',
                      xaxis_title="Time (days)",
                      yaxis_title="ETH (usd)",
                      xaxis_rangeslider_visible=True,
                      width=1400,
                      height=600,
                      template="plotly_dark",
                      font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="White"))
    st.plotly_chart(fig)

# #####
# import plotly.graph_objects as go

# fig = go.Figure()

# fig.add_trace(go.Scatter(
#     x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
#     y=[0, 1, 2, 3, 4, 5, 6, 7, 8],
#     name="Name of Trace 1"       # this sets its legend entry
# ))


# fig.add_trace(go.Scatter(
#     x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
#     y=[1, 0, 3, 2, 5, 4, 7, 6, 8],
#     name="Name of Trace 2"
# ))

# fig.update_layout(
#     title="Plot Title",
#     xaxis_title="X Axis Title",
#     yaxis_title="Y Axis Title",
#     legend_title="Legend Title",
#     font=dict(
#         family="Courier New, monospace",
#         size=18,
#         color="RebeccaPurple"
#     )
# )

# fig.show()
######


# Compute the prediction and extraxt next three days in pred list
trainer.extract_xy_tr_te()
trainer.padding_seq()
# pred = trainer.get_prediction()

pred = np.array([[1284.8817],
                 [1518.0892],
                 [1480.2537]])

last_known_days = trainer.target_scaler.inverse_transform(trainer.y_test)

last_date = trainer.original_data.tail(1).index[0]
last_date = datetime.strptime(last_date, "%Y-%m-%d")
pred_day_1 = last_date + timedelta(days = 1)
pred_day_2 = last_date + timedelta(days = 2)
pred_day_3 = last_date + timedelta(days = 3)
pred_day_1 = str(pred_day_1)[0:10]
pred_day_2 = str(pred_day_2)[0:10]
pred_day_3 = str(pred_day_3)[0:10]

# Under the Graph show Metric of our prediction for the next three days compared to the value t -1

#st.metric(label="Ethereum", value="$1.109,67", delta="+ 0.01")
col1, col2, col3 = st.columns(3)

pred_d1_fromatted = "{:.2f}".format(pred[0,0].item())
pred_d2_fromatted = "{:.2f}".format(pred[1,0].item())
pred_d3_fromatted = "{:.2f}".format(pred[2,0].item())

pred_d1_fromatted = pred_d1_fromatted[:1] + ',' + pred_d1_fromatted[1:]
pred_d2_fromatted = pred_d1_fromatted[:1] + ',' + pred_d2_fromatted[1:]
pred_d3_fromatted = pred_d1_fromatted[:1] + ',' + pred_d3_fromatted[1:]

col1.metric(label=pred_day_1, value=f'${pred_d1_fromatted}',
            delta="{:.2f}".format(pred[0,0].item() - last_known_days[2,0].item()))

col2.metric(label=pred_day_2, value=f'${pred_d2_fromatted}',
            delta="{:.2f}".format(pred[1,0].item() - pred[0,0].item()))

col3.metric(label=pred_day_3, value=f'${pred_d3_fromatted}',
            delta="{:.2f}".format(pred[2,0].item() - pred[1,0].item()), delta_color="normal")

# today = datetime.date.today()
#st.subheader('Raw data')
#st.write(trainer.original_data.tail())

#if __name__ == "__main__":
    #data = load_data()
    #print(data.shape)


plot_raw_data()
