import streamlit as st
import pandas as pd
import plotly.express as px

class AirbnbCharts:

    def display_price_chart_by_city(self, filtered_data):
        if filtered_data is not None and not filtered_data.empty:
            filtered_data['PRICE'] = pd.to_numeric(filtered_data['PRICE'], errors='coerce')
            df_grouped = filtered_data.groupby(['CITY', 'NEIGHBOURHOOD_GROUP'])['PRICE'].mean().reset_index()

            fig = px.bar(
                df_grouped,
                x='NEIGHBOURHOOD_GROUP',
                y='PRICE',
                color='CITY',
                barmode='group',
                title='Average Price for Rent by Neighborhood'
            )

            st.plotly_chart(fig)
        else:
            st.info("No data to display.")