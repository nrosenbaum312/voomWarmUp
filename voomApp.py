import asyncio
import tornado
import tornado.httpclient
import requests
import json 

#WeatherURL =  'https://api.openweathermap.org/data/2.5/weather?q=Tel%20Aviv,is&APPID=d57a296c1ede797ea680ab479573672a'
WeatherURL = 'https://api.openweathermap.org/data/2.5/weather?lat=32.08&lon=34.78&appid=d57a296c1ede797ea680ab479573672a'

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        self.write("Hello, world!")
        self.finish()


        

class WeatherHandler(tornado.web.RequestHandler):
    async def get(self):

        #Is this okay?
        http_client = tornado.httpclient.AsyncHTTPClient(
    defaults=dict(client_cert=None, client_key=None, validate_cert=False)
)
        weather_response = await http_client.fetch(WeatherURL)
        
        # Parse the JSON response
        weather_data = json.loads(weather_response.body)
        # Extract the weather information
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_conditions = weather_data['weather'][0]['description']
        self.write("Tel Aviv Weather \n")
        
        # Render the weather information in the response
        self.write(f"Temperature: {temperature - 273.15} C\n")
        self.write("\n")
        self.write(f"Humidity: {humidity}%\n")
        self.write(f"Weather Conditions: {weather_conditions}\n")
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/weather", WeatherHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())


