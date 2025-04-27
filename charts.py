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


    def display_minimum_nights_by_neighbourhood(self, filtered_data):
        if filtered_data is not None and not filtered_data.empty:
            filtered_data['MINIMUM_NIGHTS'] = pd.to_numeric(filtered_data['MINIMUM_NIGHTS'], errors='coerce')

            # Grupowanie tylko po CITY i NEIGHBOURHOOD_GROUP
            df_grouped = filtered_data.groupby(['CITY', 'NEIGHBOURHOOD_GROUP'])['MINIMUM_NIGHTS'].mean().reset_index()

            # Wykres
            fig = px.bar(
                df_grouped,
                x='NEIGHBOURHOOD_GROUP',
                y='MINIMUM_NIGHTS',
                color='CITY',
                barmode='group',
                title='Average Minimum Nights by Neighbourhood Group'
            )

            st.plotly_chart(fig)
        else:
            st.info("No data to display.")

    def add_room_type_code(self, filtered_data):
        if filtered_data is not None and not filtered_data.empty:
            mapping = {
                'Entire home/apt': 0,
                'Private room': 1,
                'Shared room': 2,
                'No information': 3
            }
            filtered_data['ROOM_TYPE_CODED'] = filtered_data['ROOM_TYPE'].map(mapping)
            return filtered_data
        else:
            st.info("No data to code.")
            return filtered_data
        

    def display_room_type_counts_by_neighbourhood(self, filtered_data):
        if filtered_data is not None and not filtered_data.empty:
            # Grupowanie po NEIGHBOURHOOD_GROUP i ROOM_TYPE
            df_grouped = filtered_data.groupby(['NEIGHBOURHOOD_GROUP', 'ROOM_TYPE']).size().reset_index(name='COUNT')

            # Wykres
            fig = px.bar(
                df_grouped,
                x='NEIGHBOURHOOD_GROUP',
                y='COUNT',
                color='ROOM_TYPE',
                barmode='group',
                title='Number of Listings by Room Type and Neighbourhood Group'
            )

            st.plotly_chart(fig)
        else:
            st.info("No data to display.")

    def display_average_price_by_room_type(self, filtered_data):
        if filtered_data is not None and not filtered_data.empty:

            filtered_data['PRICE'] = pd.to_numeric(filtered_data['PRICE'], errors='coerce')
            
            df_grouped = filtered_data.groupby('ROOM_TYPE')['PRICE'].mean().reset_index()

            fig = px.bar(
                df_grouped,
                x='ROOM_TYPE',
                y='PRICE',
                title='Average Price by Room Type',
                labels={'PRICE': 'Average Price ($)', 'ROOM_TYPE': 'Room Type'},
                color='ROOM_TYPE',
                text_auto='.2s'     
            )
            st.plotly_chart(fig)
        else:
            st.info("No data to display.")
