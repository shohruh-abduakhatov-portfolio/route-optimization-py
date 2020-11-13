class Config(object):
    @property
    def test_config(self):
        return "test_config"

    @property
    def osrm_host_dev(self):
        return "34.245.180.18"

    @property
    def osrm_host(self):
        return '34.254.124.76'#'34.243.76.238:5000'#"34.254.124.76"


config = Config()
