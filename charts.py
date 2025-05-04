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
                title='Average price for rent by neighborhood',
                text_auto='.2s',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                xaxis_title="Neighborhood",
                yaxis_title="Average Price ($)",
                title_font_size=18,
                legend=dict(orientation="h", y=-0.3),
                margin=dict(l=40, r=40, t=60, b=60)
            )
            st.plotly_chart(fig)
        else:
            st.info("No data to display.")

    def display_minimum_nights_by_neighbourhood(self, filtered_data):
        if filtered_data is not None and not filtered_data.empty:
            filtered_data['MINIMUM_NIGHTS'] = pd.to_numeric(filtered_data['MINIMUM_NIGHTS'], errors='coerce')
            df_grouped = filtered_data.groupby(['CITY', 'NEIGHBOURHOOD_GROUP'])['MINIMUM_NIGHTS'].mean().reset_index()

            fig = px.bar(
                df_grouped,
                x='NEIGHBOURHOOD_GROUP',
                y='MINIMUM_NIGHTS',
                color='CITY',
                barmode='group',
                title='Average minimum nights by neighbourhood group',
                text_auto='.1f',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                xaxis_title="Neighborhood",
                yaxis_title="Minimum Nights",
                title_font_size=18,
                legend=dict(orientation="h", y=-0.3),
                margin=dict(l=40, r=40, t=60, b=60)
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
            df_grouped = filtered_data.groupby(['NEIGHBOURHOOD_GROUP', 'ROOM_TYPE']).size().reset_index(name='COUNT')

            fig = px.bar(
                df_grouped,
                x='NEIGHBOURHOOD_GROUP',
                y='COUNT',
                color='ROOM_TYPE',
                barmode='group',
                title='Number of listings by room type and neighbourhood group',
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                xaxis_title="Neighborhood",
                yaxis_title="Number of Listings",
                title_font_size=18,
                legend=dict(orientation="h", y=-0.3),
                margin=dict(l=40, r=40, t=60, b=60)
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
                title='Average price by room type',
                labels={'PRICE': 'Average Price ($)', 'ROOM_TYPE': 'Room Type'},
                color='ROOM_TYPE',
                text_auto='.2s',
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            fig.update_layout(
                xaxis_title="Room Type",
                yaxis_title="Average Price ($)",
                title_font_size=18,
                legend=dict(orientation="h", y=-0.3),
                margin=dict(l=40, r=40, t=60, b=60)
            )
            st.plotly_chart(fig)
        else:
            st.info("No data to display.")

    def display_listing_count_by_neighbourhood_group(self, filtered_data):
        if filtered_data is not None and not filtered_data.empty:
            df_grouped = filtered_data.groupby('NEIGHBOURHOOD_GROUP').size().reset_index(name='COUNT')

            fig = px.bar(
                df_grouped,
                x='NEIGHBOURHOOD_GROUP',
                y='COUNT',
                title='Number of listings by neighbourhood group',
                text_auto=True,
                color='NEIGHBOURHOOD_GROUP',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                xaxis_title="Neighborhood Group",
                yaxis_title="Number of Listings",
                title_font_size=18,
                legend=dict(orientation="h", y=-0.3),
                margin=dict(l=40, r=40, t=60, b=60)
            )
            st.plotly_chart(fig)
        else:
            st.info("No data to display.")

    def display_top_listings(self, filtered_data, top_n=10):
        if filtered_data is not None and not filtered_data.empty:
            filtered_data['PRICE'] = pd.to_numeric(filtered_data['PRICE'], errors='coerce')
            filtered_data['REVIEW_RATE_NUMBER'] = pd.to_numeric(filtered_data['REVIEW_RATE_NUMBER'], errors='coerce')

            top_listings = filtered_data.sort_values(
                by=['REVIEW_RATE_NUMBER', 'PRICE'], ascending=[False, False]
            ).head(top_n)

            st.subheader(f"Top {top_n} listings by review score and price")

            st.dataframe(
                top_listings[[
                    'NAME', 'CITY', 'NEIGHBOURHOOD_GROUP', 'ROOM_TYPE',
                    'PRICE', 'REVIEW_RATE_NUMBER', 'MINIMUM_NIGHTS'
                ]].rename(columns={
                    'NAME': 'Listing Title',
                    'CITY': 'City',
                    'NEIGHBOURHOOD_GROUP': 'Neighbourhood',
                    'ROOM_TYPE': 'Room Type',
                    'PRICE': 'Price ($)',
                    'REVIEW_SCORES_RATING': 'Review Score',
                    'MINIMUM_NIGHTS': 'Min Nights'
                }),
                use_container_width=True
            )
        else:
            st.info("No data to display.")
