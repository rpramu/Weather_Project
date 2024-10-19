# OpenWeatherMap API Project

This project leverages FastAPI to communicate with the OpenWeatherMap API, providing insightful weather data.

## Installation

To install the dependencies locally, use the following command:
```sh
pip install -r requirements.txt
```
Also create a .env file in the same directory, and add these parameters:


```sh
OPEN_WEATHERMAP_API_KEY="your_openweathermap_api_key"
OPEN_WEATHERMAP_URL=http://api.openweathermap.org/data/2.5/weather
```



## Running the Application

You can run the application using Docker or Podman with the following commands:
```sh
docker build -t openweathermapproject .
docker run -p 8000:8000 openweathermapproject
```

This will spawn a container bound to the port [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Example Usage

To fetch weather data from the OpenWeatherMap API for a given city, use the following endpoint:
```
http://0.0.0.0:8000/weather/{cityname}
```

### Example:
```
http://0.0.0.0:8000/weather/delhi
```

## License



## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or inquiries, please contact [@gmail.com](mailto:@gmail.com).