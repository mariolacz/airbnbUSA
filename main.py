import streamlit as st
from application import AIRBNB
from charts import AirbnbCharts

st.set_page_config(page_title="My Streamlit App", layout="wide")
st.title("Rental prices in different US cities")

tab1, tab2 = st.tabs(["Filter options", "Charts"])

# Ścieżki do plików
file_paths = [
    '/Users/mariolaczajkowska/anaconda_projects/python/project_mcz2/downloads/cleaned_airbnb_data.csv',
    '/Users/mariolaczajkowska/anaconda_projects/python/project_mcz2/downloads/cleaned_data_USA.csv'
]

# Inicjalizacja aplikacji
airbnb_app = AIRBNB(file_paths)

# Inicjalizacja domyślnych filtrów
if 'filters' not in st.session_state:
    st.session_state.filters = {
        'city': airbnb_app.data['CITY'].unique().tolist(),
        'host': airbnb_app.data['HOST_IDENTITY_VERIFIED'].unique().tolist(),
        'instant_bookable': airbnb_app.data['INSTANT_BOOKABLE'].unique().tolist(),
        'neighborhood': airbnb_app.data['NEIGHBOURHOOD_GROUP'].unique().tolist(),
        'cancellation_policy': airbnb_app.data['CANCELLATION_POLICY'].unique().tolist(),
        'room_type': airbnb_app.data['ROOM_TYPE'].unique().tolist(),
        'price': (0, 1500),
        'minimum_nights': (0, 365),
        'review_rate_number': (0.0, 5.0)
    }

with tab1:
    st.session_state["current_tab"] = "Filters"
    col1, col2 = st.columns([10, 15])

    with col1:
        city_options = airbnb_app.data['CITY'].unique().tolist()
        host_options = airbnb_app.data['HOST_IDENTITY_VERIFIED'].unique().tolist()
        neighborhood_options = airbnb_app.data['NEIGHBOURHOOD_GROUP'].unique().tolist()
        cancellation_policy_options = airbnb_app.data['CANCELLATION_POLICY'].unique().tolist()
        room_type_options = airbnb_app.data['ROOM_TYPE'].unique().tolist()
        instant_bookable_options = airbnb_app.data['INSTANT_BOOKABLE'].unique().tolist()

        # Filtry z ustawień sesji
        o_city = st.multiselect("City", city_options, default=st.session_state.filters['city'])

        if o_city:
            neighborhood_options = airbnb_app.data[airbnb_app.data['CITY'].isin(o_city)]['NEIGHBOURHOOD_GROUP'].dropna().unique().tolist()

        o_host = st.multiselect("Host verification", host_options, default=st.session_state.filters['host'])
        o_instant_bookable = st.multiselect("Instant bookable", instant_bookable_options, default=st.session_state.filters['instant_bookable'])
        o_neighborhood = st.multiselect("Neighborhood", neighborhood_options, default=[n for n in st.session_state.filters['neighborhood'] if n in neighborhood_options])
        o_cancellation_policy = st.multiselect("Cancellation policy", cancellation_policy_options, default=st.session_state.filters['cancellation_policy'])
        o_room_type = st.multiselect('Room type', room_type_options, default=st.session_state.filters['room_type'])
        o_price = st.slider("Choose your price range", min_value=0, max_value=1500, step=10, value=st.session_state.filters['price'])
        o_minimum_nights = st.slider('Minimum nights', min_value=0, max_value=365, step=1, value=st.session_state.filters['minimum_nights'])
        o_review_rate_number = st.slider('Rate number', min_value=0.0, max_value=5.0, step=0.1, value=st.session_state.filters['review_rate_number'])

    # Zapisz filtry do session state
    st.session_state.filters.update({
        'city': o_city,
        'host': o_host,
        'instant_bookable': o_instant_bookable,
        'neighborhood': o_neighborhood,
        'cancellation_policy': o_cancellation_policy,
        'room_type': o_room_type,
        'price': o_price,
        'minimum_nights': o_minimum_nights,
        'review_rate_number': o_review_rate_number
    })

    if st.button("Filter"):
        filtered_data = airbnb_app.filter_data(
            o_city, o_host, o_neighborhood, o_instant_bookable, o_cancellation_policy,
            o_room_type, o_minimum_nights, o_review_rate_number, o_price
        )
        if filtered_data is not None:
            st.session_state["filtered_data"] = filtered_data

        with col2:
            if filtered_data is not None and not filtered_data.empty:
                airbnb_app.display_map(filtered_data)
            else:
                st.warning("No results match your filters. Try changing the criteria")

        airbnb_app.display_data(filtered_data)

    if st.button("Reset filters"):
        st.session_state.filters = {
            'city': city_options,
            'host': host_options,
            'instant_bookable': instant_bookable_options,
            'neighborhood': neighborhood_options,
            'cancellation_policy': cancellation_policy_options,
            'room_type': room_type_options,
            'price': (0, 1500),
            'minimum_nights': (0, 365),
            'review_rate_number': (0.0, 5.0)
        }
        st.session_state["filtered_data"] = airbnb_app.data
        st.rerun()

with tab2:
    st.session_state["current_tab"] = "Charts"

    charts = AirbnbCharts()  # teraz bez argumentów
    filtered_data = st.session_state.get("filtered_data", airbnb_app.data)

    charts.display_price_chart_by_city(filtered_data)
    charts.display_minimum_nights_by_neighbourhood(filtered_data)
    charts.display_room_type_counts_by_neighbourhood(filtered_data)