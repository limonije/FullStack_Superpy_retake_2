from main import bought_product, forecast_expired


def test_bought_product():
    assert type(bought_product() is dict)


def test_forecast_expired():
    assert type(forecast_expired() is list)
