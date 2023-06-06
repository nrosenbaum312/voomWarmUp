import asyncio
import tornado
import tornado.httpclient
import requests
import json 
import time
import datetime
import logging
import psycopg2 

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

        self.write("Programming Joke: <br>" f'{joke} <br>')
        self.write(f"Response Time: {formatted_response_time} ms<br>")
        self.write(f"Time Stamp: {formatted_timeStamp} <br>")
        self.finish()





class CountryHandler(tornado.web.RequestHandler):

    async def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient(
        defaults=dict(client_cert=None, client_key=None, validate_cert=False)
        )


        CountryURL = f'https://restcountries.com/v3.1/name/Israel'

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
        

        self.write(f"{name} information:<br>")
        self.write(f"capital: {capital}<br>")
        self.write(f"population: {population}<br>")
        self.write(f"Response Time: {formatted_response_time} ms<br>")
        self.write(f"Time Stamp: {formatted_timeStamp} <br>")
        self.finish()






class WeatherHandler(tornado.web.RequestHandler):
    async def get(self):

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

        # Parse the JSON response
        weather_data = json.loads(weather_response.body)

        # Extract the weather information
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_conditions = weather_data['weather'][0]['description']

        # Render the weather information in the response
        temp = round_num(temperature - 273.15)
        formatted_response_time = round(response_time)

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

        #printing 
        self.write("Tel Aviv Weather <br>")
        self.write(f"Temperature: {temp} C<br>")
        self.write(f"Humidity: {humidity}%<br>")
        self.write(f"Weather Conditions: {weather_conditions}<br>")
        self.write(f"Response Time: {formatted_response_time} ms<br>")
        self.write(f"Time Stamp: {formatted_timeStamp} <br>")
        self.finish()

       

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/weather", WeatherHandler),
        (r"/country", CountryHandler),
        (r"/joke", JokeHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())





# Start logging

