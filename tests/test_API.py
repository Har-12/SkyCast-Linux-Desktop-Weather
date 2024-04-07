import json
from unittest import TestCase, mock, main

from halo.API import OpenWeatherMap, NotFound, APIError, RateLimitReached

current = json.loads("""
{"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":300,"main":"Drizzle","description":"light intensity drizzle","icon":"09d"}],"base":"stations","main":{"temp":280.32,"pressure":1012,"humidity":81,"temp_min":279.15,"temp_max":281.15},"visibility":10000,"wind":{"speed":4.1,"deg":80},"clouds":{"all":90},"dt":1485789600,"sys":{"type":1,"id":5091,"message":0.0103,"country":"GB","sunrise":1485762037,"sunset":1485794875},"id":2643743,"name":"London","cod":200}
""")
forecast_data = json.loads("""
{"cod":"200","message":0,"cnt":40,"list":[{"dt":1573992000,"main":{"temp":33.1,"temp_min":28.57,"temp_max":33.1,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":78,"temp_kf":4.53},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":57},"wind":{"speed":4.09,"deg":321},"rain":{"3h":1.44},"sys":{"pod":"d"},"dt_txt":"2019-11-17 12:00:00"},{"dt":1574002800,"main":{"temp":31.2,"temp_min":27.8,"temp_max":31.2,"pressure":1012,"sea_level":1012,"grnd_level":1011,"humidity":79,"temp_kf":3.4},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":100},"wind":{"speed":4.41,"deg":355},"rain":{"3h":1.69},"sys":{"pod":"n"},"dt_txt":"2019-11-17 15:00:00"},{"dt":1574013600,"main":{"temp":29.13,"temp_min":26.87,"temp_max":29.13,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":83,"temp_kf":2.26},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":78},"wind":{"speed":4.24,"deg":38},"rain":{"3h":1.19},"sys":{"pod":"n"},"dt_txt":"2019-11-17 18:00:00"},{"dt":1574024400,"main":{"temp":27.59,"temp_min":26.46,"temp_max":27.59,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":80,"temp_kf":1.13},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":4.07,"deg":43},"sys":{"pod":"n"},"dt_txt":"2019-11-17 21:00:00"},{"dt":1574035200,"main":{"temp":25.6,"temp_min":25.6,"temp_max":25.6,"pressure":1010,"sea_level":1010,"grnd_level":1010,"humidity":80,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":4.89,"deg":60},"sys":{"pod":"n"},"dt_txt":"2019-11-18 00:00:00"},{"dt":1574046000,"main":{"temp":26.06,"temp_min":26.06,"temp_max":26.06,"pressure":1013,"sea_level":1013,"grnd_level":1012,"humidity":79,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":3.8,"deg":85},"sys":{"pod":"d"},"dt_txt":"2019-11-18 03:00:00"},{"dt":1574056800,"main":{"temp":28.68,"temp_min":28.68,"temp_max":28.68,"pressure":1011,"sea_level":1011,"grnd_level":1011,"humidity":67,"temp_kf":0},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":{"all":13},"wind":{"speed":1.17,"deg":217},"sys":{"pod":"d"},"dt_txt":"2019-11-18 06:00:00"},{"dt":1574067600,"main":{"temp":28.03,"temp_min":28.03,"temp_max":28.03,"pressure":1009,"sea_level":1009,"grnd_level":1008,"humidity":74,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":67},"wind":{"speed":3.53,"deg":234},"sys":{"pod":"d"},"dt_txt":"2019-11-18 09:00:00"},{"dt":1574078400,"main":{"temp":27.85,"temp_min":27.85,"temp_max":27.85,"pressure":1009,"sea_level":1009,"grnd_level":1008,"humidity":78,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":78},"wind":{"speed":3.51,"deg":259},"sys":{"pod":"d"},"dt_txt":"2019-11-18 12:00:00"},{"dt":1574089200,"main":{"temp":28.03,"temp_min":28.03,"temp_max":28.03,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":79,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"clouds":{"all":80},"wind":{"speed":1.85,"deg":326},"sys":{"pod":"n"},"dt_txt":"2019-11-18 15:00:00"},{"dt":1574100000,"main":{"temp":26.68,"temp_min":26.68,"temp_max":26.68,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":84,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"clouds":{"all":57},"wind":{"speed":2.52,"deg":57},"sys":{"pod":"n"},"dt_txt":"2019-11-18 18:00:00"},{"dt":1574110800,"main":{"temp":25.9,"temp_min":25.9,"temp_max":25.9,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":87,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":45},"wind":{"speed":3.02,"deg":83},"rain":{"3h":0.13},"sys":{"pod":"n"},"dt_txt":"2019-11-18 21:00:00"},{"dt":1574121600,"main":{"temp":26.34,"temp_min":26.34,"temp_max":26.34,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":81,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":73},"wind":{"speed":4.72,"deg":53},"rain":{"3h":0.75},"sys":{"pod":"n"},"dt_txt":"2019-11-19 00:00:00"},{"dt":1574132400,"main":{"temp":27.42,"temp_min":27.42,"temp_max":27.42,"pressure":1013,"sea_level":1013,"grnd_level":1012,"humidity":77,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":{"all":100},"wind":{"speed":5.34,"deg":53},"sys":{"pod":"d"},"dt_txt":"2019-11-19 03:00:00"},{"dt":1574143200,"main":{"temp":29.15,"temp_min":29.15,"temp_max":29.15,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":68,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":{"all":100},"wind":{"speed":2,"deg":177},"sys":{"pod":"d"},"dt_txt":"2019-11-19 06:00:00"},{"dt":1574154000,"main":{"temp":28.01,"temp_min":28.01,"temp_max":28.01,"pressure":1008,"sea_level":1008,"grnd_level":1007,"humidity":76,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":{"all":91},"wind":{"speed":5.15,"deg":236},"sys":{"pod":"d"},"dt_txt":"2019-11-19 09:00:00"},{"dt":1574164800,"main":{"temp":28.58,"temp_min":28.58,"temp_max":28.58,"pressure":1008,"sea_level":1008,"grnd_level":1007,"humidity":74,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":82},"wind":{"speed":3.35,"deg":289},"sys":{"pod":"d"},"dt_txt":"2019-11-19 12:00:00"},{"dt":1574175600,"main":{"temp":28.17,"temp_min":28.17,"temp_max":28.17,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":79,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":100},"wind":{"speed":3.16,"deg":323},"rain":{"3h":0.19},"sys":{"pod":"n"},"dt_txt":"2019-11-19 15:00:00"},{"dt":1574186400,"main":{"temp":27.34,"temp_min":27.34,"temp_max":27.34,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":80,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":98},"wind":{"speed":3.7,"deg":2},"rain":{"3h":2.31},"sys":{"pod":"n"},"dt_txt":"2019-11-19 18:00:00"},{"dt":1574197200,"main":{"temp":26.25,"temp_min":26.25,"temp_max":26.25,"pressure":1008,"sea_level":1008,"grnd_level":1007,"humidity":84,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":17},"wind":{"speed":3.11,"deg":54},"rain":{"3h":1.06},"sys":{"pod":"n"},"dt_txt":"2019-11-19 21:00:00"},{"dt":1574208000,"main":{"temp":25.98,"temp_min":25.98,"temp_max":25.98,"pressure":1009,"sea_level":1009,"grnd_level":1008,"humidity":83,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":30},"wind":{"speed":3.87,"deg":65},"rain":{"3h":0.19},"sys":{"pod":"n"},"dt_txt":"2019-11-20 00:00:00"},{"dt":1574218800,"main":{"temp":27.23,"temp_min":27.23,"temp_max":27.23,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":77,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":4.63,"deg":73},"sys":{"pod":"d"},"dt_txt":"2019-11-20 03:00:00"},{"dt":1574229600,"main":{"temp":29.44,"temp_min":29.44,"temp_max":29.44,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":66,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":1.71,"deg":141},"sys":{"pod":"d"},"dt_txt":"2019-11-20 06:00:00"},{"dt":1574240400,"main":{"temp":28.39,"temp_min":28.39,"temp_max":28.39,"pressure":1007,"sea_level":1007,"grnd_level":1006,"humidity":75,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":20},"wind":{"speed":4.22,"deg":226},"rain":{"3h":0.06},"sys":{"pod":"d"},"dt_txt":"2019-11-20 09:00:00"},{"dt":1574251200,"main":{"temp":28.1,"temp_min":28.1,"temp_max":28.1,"pressure":1008,"sea_level":1008,"grnd_level":1007,"humidity":75,"temp_kf":0},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":{"all":16},"wind":{"speed":2.82,"deg":288},"sys":{"pod":"d"},"dt_txt":"2019-11-20 12:00:00"},{"dt":1574262000,"main":{"temp":28.33,"temp_min":28.33,"temp_max":28.33,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":74,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"clouds":{"all":72},"wind":{"speed":1.16,"deg":301},"sys":{"pod":"n"},"dt_txt":"2019-11-20 15:00:00"},{"dt":1574272800,"main":{"temp":26.89,"temp_min":26.89,"temp_max":26.89,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":83,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"clouds":{"all":86},"wind":{"speed":3.32,"deg":74},"sys":{"pod":"n"},"dt_txt":"2019-11-20 18:00:00"},{"dt":1574283600,"main":{"temp":26.89,"temp_min":26.89,"temp_max":26.89,"pressure":1009,"sea_level":1009,"grnd_level":1008,"humidity":74,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"clouds":{"all":97},"wind":{"speed":6.99,"deg":57},"rain":{"3h":0.88},"sys":{"pod":"n"},"dt_txt":"2019-11-20 21:00:00"},{"dt":1574294400,"main":{"temp":26.68,"temp_min":26.68,"temp_max":26.68,"pressure":1009,"sea_level":1009,"grnd_level":1008,"humidity":76,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"clouds":{"all":73},"wind":{"speed":5.56,"deg":62},"sys":{"pod":"n"},"dt_txt":"2019-11-21 00:00:00"},{"dt":1574305200,"main":{"temp":27.38,"temp_min":27.38,"temp_max":27.38,"pressure":1012,"sea_level":1012,"grnd_level":1011,"humidity":74,"temp_kf":0},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":{"all":41},"wind":{"speed":5.27,"deg":74},"sys":{"pod":"d"},"dt_txt":"2019-11-21 03:00:00"},{"dt":1574316000,"main":{"temp":29.69,"temp_min":29.69,"temp_max":29.69,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":68,"temp_kf":0},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":{"all":21},"wind":{"speed":1.94,"deg":124},"sys":{"pod":"d"},"dt_txt":"2019-11-21 06:00:00"},{"dt":1574326800,"main":{"temp":27.92,"temp_min":27.92,"temp_max":27.92,"pressure":1008,"sea_level":1008,"grnd_level":1007,"humidity":76,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":27},"wind":{"speed":4.94,"deg":222},"rain":{"3h":1},"sys":{"pod":"d"},"dt_txt":"2019-11-21 09:00:00"},{"dt":1574337600,"main":{"temp":28.39,"temp_min":28.39,"temp_max":28.39,"pressure":1009,"sea_level":1009,"grnd_level":1008,"humidity":73,"temp_kf":0},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":{"all":43},"wind":{"speed":2.3,"deg":277},"rain":{"3h":1.56},"sys":{"pod":"d"},"dt_txt":"2019-11-21 12:00:00"},{"dt":1574348400,"main":{"temp":27.79,"temp_min":27.79,"temp_max":27.79,"pressure":1011,"sea_level":1011,"grnd_level":1010,"humidity":77,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"clouds":{"all":100},"wind":{"speed":3.51,"deg":43},"sys":{"pod":"n"},"dt_txt":"2019-11-21 15:00:00"},{"dt":1574359200,"main":{"temp":26.56,"temp_min":26.56,"temp_max":26.56,"pressure":1012,"sea_level":1012,"grnd_level":1010,"humidity":79,"temp_kf":0},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"clouds":{"all":94},"wind":{"speed":7.41,"deg":60},"sys":{"pod":"n"},"dt_txt":"2019-11-21 18:00:00"},{"dt":1574370000,"main":{"temp":26.1,"temp_min":26.1,"temp_max":26.1,"pressure":1010,"sea_level":1010,"grnd_level":1009,"humidity":79,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":4.79,"deg":72},"sys":{"pod":"n"},"dt_txt":"2019-11-21 21:00:00"},{"dt":1574380800,"main":{"temp":26.76,"temp_min":26.76,"temp_max":26.76,"pressure":1011,"sea_level":1011,"grnd_level":1009,"humidity":74,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":1},"wind":{"speed":6.55,"deg":60},"sys":{"pod":"n"},"dt_txt":"2019-11-22 00:00:00"},{"dt":1574391600,"main":{"temp":26.46,"temp_min":26.46,"temp_max":26.46,"pressure":1013,"sea_level":1013,"grnd_level":1011,"humidity":71,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":77},"wind":{"speed":7.54,"deg":66},"sys":{"pod":"d"},"dt_txt":"2019-11-22 03:00:00"},{"dt":1574402400,"main":{"temp":29,"temp_min":29,"temp_max":29,"pressure":1012,"sea_level":1012,"grnd_level":1011,"humidity":63,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":59},"wind":{"speed":4.66,"deg":59},"sys":{"pod":"d"},"dt_txt":"2019-11-22 06:00:00"},{"dt":1574413200,"main":{"temp":30.02,"temp_min":30.02,"temp_max":30.02,"pressure":1009,"sea_level":1009,"grnd_level":1008,"humidity":67,"temp_kf":0},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"clouds":{"all":65},"wind":{"speed":1.81,"deg":117},"sys":{"pod":"d"},"dt_txt":"2019-11-22 09:00:00"}],"city":{"id":1254187,"name":"Thrissur","coord":{"lat":10.5257,"lon":76.2131},"country":"IN","population":325110,"timezone":19800,"sunrise":1573951866,"sunset":1573993749}}
""")
history_daily_data = json.loads("""
{"message":"","cod":"200","city_id":2885679,"calctime":0.0823,"cnt":3,"list":[{"main":{"temp":266.052,"temp_min":266.052,"temp_max":266.052,"pressure":957.86,"sea_level":1039.34,"grnd_level":957.86,"humidity":90},"wind":{"speed":1.16,"deg":139.502},"clouds":{"all":0},"weather":[{"id":800,"main":"Clear","description":"Sky is Clear","icon":"01n"}],"dt":1485722804},{"main":{"temp":263.847,"temp_min":263.847,"temp_max":263.847,"pressure":955.78,"sea_level":1037.43,"grnd_level":955.78,"humidity":91},"wind":{"speed":1.49,"deg":159},"clouds":{"all":0},"weather":[{"id":800,"main":"Clear","description":"Sky is Clear","icon":"01n"}],"dt":1485749608},{"main":{"temp":274.9,"pressure":1019,"temp_min":274.15,"temp_max":275.15,"humidity":88},"wind":{"speed":1,"deg":0},"clouds":{"all":76},"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"dt":1485773778}]}
""")

MOCK_DATA = None


def mock_request(*args, **kwargs):
    class FakeResponse:
        def __init__(self, status, response):
            self.status_code = status
            self.response = response

        def json(self):
            return self.response

    if "ip=0.0.0.1" in args[0]:
        return FakeResponse(204, MOCK_DATA)
    elif "ip=0.0.0.2" in args[0]:
        return FakeResponse(500, MOCK_DATA)
    elif "ip=0.0.0.3" in args[0]:
        return FakeResponse(429, MOCK_DATA)
    return FakeResponse(200, MOCK_DATA)


class TestAPI(TestCase):
    """
    Tests each and every :class:`API` methods.
    """
    def setUp(self):
        TestCase.setUp(self)
        self.api = OpenWeatherMap()

    def errors_check(self, fn, *args):
        """Just a wrapper to be reused for error checking."""
        with self.assertRaises(NotFound):
            fn("ip=0.0.0.1", *args)
        with self.assertRaises(APIError):
            fn("ip=0.0.0.2", *args)
        with self.assertRaises(RateLimitReached):
            fn("ip=0.0.0.3", *args)

    @mock.patch('requests.get', side_effect=mock_request)
    def test_get_current_weather(self, mock_get):
        global MOCK_DATA
        MOCK_DATA = current
        self.errors_check(self.api.get_current_weather)

        city, city_tz, current_weather = self.api.get_current_weather("ip=auto")
        self.assertIsNotNone(city, "Invalid city.")
        self.assertIsNotNone(city_tz, "Invalid timezone.")
        self.assertDictEqual({
            'status': 'Drizzle', 'code': 300, 'temp': 280.32
        }, current_weather, "Invalid current weather data.")

    @mock.patch('requests.get', side_effect=mock_request)
    def test_get_forecast_weather(self, mock_get):
        global MOCK_DATA
        MOCK_DATA = forecast_data
        self.errors_check(self.api.get_forecast_weather)

        forecast_weather = self.api.get_forecast_weather("ip=auto")
        self.assertIsNotNone(forecast_weather, "Invalid forecast data.")

    @mock.patch('requests.get', side_effect=mock_request)
    def test_get_weather_history(self, mock_get):
        global MOCK_DATA
        MOCK_DATA = history_daily_data
        self.errors_check(self.api.get_weather_history, "America/New_York")

        history_weather = self.api.get_weather_history("ip=auto", "America/New_York")
        self.assertIsNotNone(history_weather, "Invalid history data.")


if __name__ == '__main__':
    main()