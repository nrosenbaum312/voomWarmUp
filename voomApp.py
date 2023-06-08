import asyncio
import tornado
import tornado.httpclient
import json 
import time
import datetime
import logging
import psycopg2 
import tornado.web

#database connection 
try: 
    connection = psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='voomwarmupdb',
    user='natalie',
    password=''
    )
    print("sucsessful connection")

except psycopg2.Error as e:
    print("Error connecting to database:", e)

#rounding helper function
def round_num(number):
    rounded_number = round(number, 2)
    return rounded_number

#logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

WeatherURL = 'https://api.openweathermap.org/data/2.5/weather?lat=32.08&lon=34.78&appid=d57a296c1ede797ea680ab479573672a'


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        self.write("Hello, world!")
        self.finish()


class JokeHandler(tornado.web.RequestHandler):

    async def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        http_client = tornado.httpclient.AsyncHTTPClient(
        defaults=dict(client_cert=None, client_key=None, validate_cert=False)
        )

        JokeURL = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"

        startTime = time.time()
        joke_response = await http_client.fetch(JokeURL)
        endTime = time.time()

        #timestamp
        timeStamp = datetime.datetime.now()
        formatted_timeStamp= timeStamp.strftime("%Y-%m-%d %H:%M:%S")

        #response time
        response_time = (endTime - startTime) * 1000
        formatted_response_time = round(response_time)


        # Parse the JSON response
        joke_data = json.loads(joke_response.body)
        if joke_data["type"] == "single":
            joke = joke_data["joke"]
        else:
            joke = joke_data["setup"] + ": <br>" + joke_data["delivery"]

        joke_data['response_time'] = formatted_response_time
        joke_data['time_stamp'] = formatted_timeStamp
        updated_joke_data = json.dumps(joke_data)

        #database
        with connection.cursor() as cur:
            query = '''
                INSERT INTO jokeinfo (joke, response_time, time_stamp)
                VALUES (%s, %s, %s)
            '''
            values = (joke, formatted_response_time, formatted_timeStamp)
            try: 
                cur.execute(query, values)
                connection.commit()
                print("written to database")
            except psycopg2.Error as e:
                print("Error creating weather table", e)

        self.write(updated_joke_data)
        self.finish()





class CountryHandler(tornado.web.RequestHandler):

    async def get(self):

        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        http_client = tornado.httpclient.AsyncHTTPClient(
        defaults=dict(client_cert=None, client_key=None, validate_cert=False)
        )

        countryName = self.get_query_argument('name')

        CountryURL = f'https://restcountries.com/v3.1/name/{countryName}'

        startTime = time.time()
        country_response = await http_client.fetch(CountryURL)
        endTime = time.time()

        #timestamp
        timeStamp = datetime.datetime.now()
        formatted_timeStamp= timeStamp.strftime("%Y-%m-%d %H:%M:%S")

        #response time
        response_time = (endTime - startTime) * 1000
        formatted_response_time = round(response_time)


        # Parse the JSON response
        country_data = json.loads(country_response.body)
    
        data = {
        'response_time': formatted_response_time,
        'time_stamp': formatted_timeStamp,
        'capital': capital,
        'name': name,
        'population': population,
        }

        #information for database
        country = country_data[0]
        capital = country.get("capital")
        if isinstance(capital, list):
            capital = capital[0] if capital else None
        population = country.get("population")
        name = country.get("name").get("common")

        #database
        with connection.cursor() as cur:
            query = '''
                INSERT INTO countryinfo (name, capital, population, response_time, time_stamp)
                VALUES (%s, %s, %s, %s, %s)
            '''
            values = (name, capital, population, formatted_response_time, formatted_timeStamp)
            try: 
                cur.execute(query, values)
                connection.commit()
                print("written to database")
            except psycopg2.Error as e:
                print("Error creating weather table", e)

        self.write(data)
        self.finish()






class WeatherHandler(tornado.web.RequestHandler):
    async def get(self):

        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        #Is this okay?
        http_client = tornado.httpclient.AsyncHTTPClient(
    defaults=dict(client_cert=None, client_key=None, validate_cert=False)
        )

        startTime = time.time()
        weather_response = await http_client.fetch(WeatherURL)
        endTime = time.time()
        
        #timestamp
        timeStamp = datetime.datetime.now()
        formatted_timeStamp= timeStamp.strftime("%Y-%m-%d %H:%M:%S")

        #response time
        response_time = (endTime - startTime) * 1000
        # Render the weather information in the response
        
        formatted_response_time = round(response_time)

        # add info to json
        weather_data = json.loads(weather_response.body)
        weather_data['response_time'] = formatted_response_time
        weather_data['time_stamp'] = formatted_timeStamp
        updated_weather_data = json.dumps(weather_data)


        # Extract the weather information for database
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_conditions = weather_data['weather'][0]['description']
        temp = round_num(temperature - 273.15)

        #database
        with connection.cursor() as cur:
            query = '''
                INSERT INTO telavivweather (temp, humidity, conditions, response_time, time_stamp)
                VALUES (%s, %s, %s, %s, %s)
            '''
            values = (temp,humidity, weather_conditions, formatted_response_time, formatted_timeStamp)
            try: 
                cur.execute(query, values)
                connection.commit()
                print("written to database")
            except psycopg2.Error as e:
                print("Error creating weather table", e)

        self.write(updated_weather_data)
        self.finish()

class CorsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def options(self):
        # Handle preflight CORS requests
        self.set_status(204)
        self.finish()

def make_app():
   return tornado.web.Application([
        (r"/", MainHandler),
        (r"/weather", WeatherHandler),
        (r"/country", CountryHandler),
        (r"/joke", JokeHandler),
        (r".*", CorsHandler),
    ])
async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())





# Start logging

