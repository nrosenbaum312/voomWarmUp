import React from 'react';
import { NavLink } from 'react-router-dom';
import { Box, Container } from '@mui/material';
import {useState, useEffect} from 'react';
import axios from 'axios';

const flexFormat = { display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-evenly' };

const DashboardPage = () => {
  const[weatherData, setWeatherData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const[countryData, setCountryData] = useState([]);
  const[isLoading2, setIsLoading2] = useState(true);
  const[countryName, setCountryName] = useState('');
  const[jokeData, setJokeData] = useState([]);
  const[isLoading3, setIsLoading3] = useState(true);

  const handleInputChange = (event) => {
    setCountryName(event.target.value);
    console.log(countryName)
  };

  useEffect(() => {
    const fetchJsonData3 = async () =>  {
    try{
      await fetch(`http://localhost:8888/joke`)
      .then(res => res.json())
      .then(resJson => setJokeData(resJson));
      setIsLoading3(false);
      console.log("worked")
    }
    catch(error){
      console.log("error")
    }
  }
  fetchJsonData3();
  }, []);

  useEffect(() => {
    const fetchJsonData = async () =>  {
    try{
      await fetch(`http://localhost:8888/weather`)
      .then(res => res.json())
      .then(resJson => setWeatherData(resJson));
      setIsLoading(false);
      console.log("worked")
    }
    catch(error){
      console.log("error")
    }
  }
  fetchJsonData();
  }, []);


  const onSubmit = () => {
    const fetchJsonData2 = async () => {
      try {
        await fetch(`http://localhost:8888/country?name=${countryName}`)
          .then((res) => res.json())
          .then((resJson) => {
            setCountryData(resJson);
            setIsLoading2(false);
            setCountryName("");
          });
        console.log("Data fetch successful");
      } catch (error) {
        console.log("Error fetching data:", error);
      }
    };
  
    fetchJsonData2();
  };

  console.log("test")
  console.log(weatherData);
  console.log(countryData)


  return (
    <div>
      <div style = {{textAlign: 'center'}}>
      <h1>Dashboard</h1>
      <p>Welcome to your dashboard!</p>
      </div>
    
    <Container style={flexFormat}>
      <Box
        key={1}
        p={3}
        m={2}
        style={{ background: 'white', borderRadius: '16px', border: '2px solid #000' }}
      >
        {
          <div>
          <h2>Tel Aviv Weather</h2>
          {isLoading ? (
        <p>Loading...</p>
      ) : (
        <div>
          <p>Temperature: {weatherData.main.temp}</p>
          <p>Humidity: {weatherData.main.humidity}%</p>
          <p>Conditions: {weatherData.weather[0].description} </p>
          <p>Response Time: {weatherData.response_time}ms </p>
          <p>Time Stamp: {weatherData.time_stamp} </p>
        </div>
      )}
          </div>
        }
      </Box>

      <Box
        key={2}
        p={3}
        m={2}
        style={{ background: 'white', borderRadius: '16px', border: '2px solid #000' }}
      >
        {
          <div>
            <h2> Country Information</h2>
            <div>
            <input
        type="text"
        id="countryInput"
        value={countryName}
        placeholder="Enter country name"
        onChange = {handleInputChange}
        style={{ fontSize: '15px', padding: '10px', marginTop: '10px' }}
      />
      <button  style={{ fontSize: '15px', padding: '10px', marginTop: '10px' }} onClick={onSubmit} > Go</button>

            </div>
            
            {isLoading2 ? (
        <p>Loading...</p>
      ) : (
        <div>
          <p>name: {countryData.name}</p>
          <p>Capital: {countryData.capital}</p>
          <p>Population: {countryData.population} </p>
          <p>Response Time: {countryData.response_time}ms </p>
          <p>Time Stamp: {countryData.time_stamp} </p>
        </div>
      )}

          </div>
          

        }
      </Box>

      <Box
        key={3}
        p={3}
        m={2}
        style={{ background: 'white', borderRadius: '16px', border: '2px solid #000' }}
      >
        {
          <div>
          <h2>Programming Joke</h2>
          {isLoading3 ? (
        <p>Loading...</p>
      ) : (
        <div>
           {jokeData.type == "single" ? (
            <p>{jokeData.joke} </p> ) :( <p> {jokeData.setup}: {jokeData.delivery} </p>) }
          <p>Response Time: {jokeData.response_time}ms </p>
          <p>Time Stamp: {jokeData.time_stamp} </p>
        </div>
      )}
          </div>
        }
      </Box>
      
    
  </Container>
  </div>);
};

export default DashboardPage;