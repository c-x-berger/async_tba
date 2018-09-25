class Team():
    def __init__(self, team_number: int, key: str = None, nickname: str = None,
                 name: str = None, city: str = None, state_prov: str = None,
                 country: str = None, address: str = None, postal_code: str = None,
                 gmaps_place_id: str = None, gmaps_url: str = None, lat: int = 0, lng: int = 0,
                 location_name: str = None, website: str = None, rookie_year: int = 0,
                 motto: str = None, home_championship: dict = {}):
        self.team_number = team_number
        
        self.nickname = nickname
        self.name = name

        self.city, self.state_prov, self.country, self.address, self.postal_code = city, state_prov, country, address, postal_code
        self.gmaps_place_id, self.gmaps_url = gmaps_place_id, gmaps_url
        self.lat, self.lng = lat, lng
        self.location_name = location_name
        
        self.website = website
        
        self.rookie_year = rookie_year

        self.motto = motto

        self.home_championship = home_championship
