
import streamlit as st
import pandas as pd
import plotly.express as px

class AirbnbCharts:

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.data = self.load_data()

    def load_data(self):
        try:
            dataframes = [pd.read_csv(file, dtype=str) for file in self.file_paths]
            data = pd.concat(dataframes, ignore_index=True)
        # przekonwertowanie na wlasciwy typ
            num_cols = ['MINIMUM_NIGHTS', 'REVIEW_RATE_NUMBER', 'PRICE', 'LAT', 'LONG']
            for col in num_cols:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
                    data[col] = data[col].fillna(0)
        
            return data
    
        except Exception as e:
            
            print(f"Error: {e}")
            return None
        
    def display_data(self, filtered_data=None):

        if filtered_data is not None:
            st.write(filtered_data)
        elif self.data is not None:
            st.write(self.data)
        else:
            st.write("No data loaded")

    def filter_data(self, city, host_identity_verified, neighbourhood_group, instant_bookable, cancellation_policy, room_type, minimum_nights_range, review_rate_number_range, price_range):
    
        if self.data is not None:

        # sprawdzenie, czy kolumna istnieje
            required_columns = ['CITY','HOST_IDENTITY_VERIFIED', 'NEIGHBOURHOOD_GROUP', 'INSTANT_BOOKABLE', 'CANCELLATION_POLICY', 'ROOM_TYPE', 'MINIMUM_NIGHTS', 'REVIEW_RATE_NUMBER', 'PRICE']
            for col in required_columns:
                if col not in self.data.columns:
                    st.error(f"Column {col} does not exist.")
                    return None
                
        self.data = self.data.astype(str)
        filtered_data = self.data

        if city:
            filtered_data = filtered_data[filtered_data['CITY'].isin(city)]
        if host_identity_verified:
            filtered_data = filtered_data[filtered_data['HOST_IDENTITY_VERIFIED'].isin(host_identity_verified)]
        if neighbourhood_group:
            filtered_data = filtered_data[filtered_data['NEIGHBOURHOOD_GROUP'].isin(neighbourhood_group)]
        if instant_bookable:
            filtered_data = filtered_data[filtered_data['INSTANT_BOOKABLE'].isin(instant_bookable)]
        if cancellation_policy:
            filtered_data = filtered_data[filtered_data['CANCELLATION_POLICY'].isin(cancellation_policy)]
        if room_type:
            filtered_data = filtered_data[filtered_data['ROOM_TYPE'].isin(room_type)]

        if minimum_nights_range != (0, 365):
            min_nights, max_nights = minimum_nights_range
            filtered_data = filtered_data[(pd.to_numeric(filtered_data['MINIMUM_NIGHTS'], errors='coerce') >= min_nights) & (pd.to_numeric(filtered_data['MINIMUM_NIGHTS'], errors='coerce') <= max_nights)]
        if review_rate_number_range != (1.0, 5.0):
            min_rate, max_rate = review_rate_number_range
            filtered_data = filtered_data[(pd.to_numeric(filtered_data['REVIEW_RATE_NUMBER'], errors='coerce') >= min_rate) & (pd.to_numeric(filtered_data['REVIEW_RATE_NUMBER'], errors='coerce') <= max_rate)]
        if price_range != (0, 2000):
            min_price, max_price = price_range
            filtered_data = filtered_data[(pd.to_numeric(filtered_data['PRICE'], errors='coerce') >= min_price) & (pd.to_numeric(filtered_data['PRICE'], errors='coerce') <= max_price)]
        return filtered_data
    
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
                title='Avarage price for rent'
            )

            st.plotly_chart(fig)
        else:
            st.info("Lack of data.")