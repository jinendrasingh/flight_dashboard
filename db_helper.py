import pymysql


class DB:

    def __init__(self):
        # Connection to Database
        try:
            self.conn = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='1234',
                database='indigo'
            )
            self.mycursor = self.conn.cursor()
            print('Connection Establish')

        except:
            print('Connection Error')

    def fetch_city_name(self):

        city = []

        self.mycursor.execute("""select distinct(Destination) from indigo.flights_data
                                  union
                                  select distinct(Source) from indigo.flights_data
                                  """)

        data = self.mycursor.fetchall()

        for i in data:
            city.append(i[0])
        return city

    def fetch_all_flights(self, source, destination):
        self.mycursor.execute("""select Airline, Route, Dep_Time, Price from indigo.flights_data
                                where Source = '{}' and Destination = '{}'""".format(source, destination))

        data = self.mycursor.fetchall()

        return data

    def fetch_airline_feq(self):

        airline = []
        frequency = []
        self.mycursor.execute("select Airline,count(*) from indigo.flights_data group by Airline")
        data = self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            frequency.append(item[1])

        return airline, frequency

    def busy_airport(self):
        city = []
        frequency = []
        self.mycursor.execute("""
                              select Source, count(*) from (select Source from indigo.flights_data
							  union all
							  select Destination from indigo.flights_data) t
                              group by t.Source
                              order by count(*) 
                              """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city, frequency

    def daily_frequency(self):

        date = []
        frequency = []

        self.mycursor.execute("""select Date_of_Journey, count(*) from indigo.flights_data
                                 group by Date_of_Journey;""")

        data = self.mycursor.fetchall()

        for item in data:
            date.append(item[0])
            frequency.append(item[1])

        return date, frequency
