import streamlit as st
from db_helper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title("Flight Analytics")

user_option = st.sidebar.selectbox('Menu', ['Select One', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1, col2 = st.columns(2)

    city = db.fetch_city_name()

    with col1:
        source = st.selectbox('Source', sorted(city))
    with col2:
        destination = st.selectbox('Destination', sorted(city))
    if st.button('Search'):
        result = db.fetch_all_flights(source, destination)
        st.dataframe(result)

elif user_option == 'Analytics':
        st.title('Analytics')
        airline, frequency = db.fetch_airline_feq()

        fig = go.Figure(
            go.Pie(
                labels=airline,
                values=frequency,
                hoverinfo='label+percent',
                textinfo="value"
            ))

        st.subheader("Airline Frequency Analysis")
        st.plotly_chart(fig)

        city, frequency1 = db.busy_airport()

        fig = px.bar(
                x=city,
                y=frequency1
            )

        st.subheader("Busiest Airport")
        st.plotly_chart(fig)

        date, frequency2 = db.daily_frequency()

        fig = px.line(
            x=date,
            y=frequency2
        )
        st.subheader('Day-wise Airline Frequency')
        st.plotly_chart(fig)

else:
    st.title("Flight Dashboard")
    st.markdown("""The Flight Dashboard is a web-based application built with Streamlit, Python, and SQL. It provides 
    insights into flight data between two airports, including the frequency of airlines, the busiest airport, 
    and day-wise airline frequency. The dashboard uses Plotly charts for data visualization and pymysql for database 
    connectivity.""")
    st.header('Feature')
    st.markdown('- Flight Routes Visualization: Displays flights between two selected airports.')
    st.markdown('- Airline Frequency Analysis: Shows the frequency of airlines in the data.')
    st.markdown('- Busiest Airport Identification: Highlights the airport with the most flights.')
    st.markdown('- Day-wise Airline Frequency: Analyzes and visualizes the frequency of flights for each airline on different days.')

