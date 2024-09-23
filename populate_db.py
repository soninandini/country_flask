# populate_db.py

import requests
from app import db, create_app
from app.models import Country, CountryNeighbour

app = create_app()
app.app_context().push()

url = "https://restcountries.com/v3.1/all"

def fetch_countries():
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def insert_countries(countries_data):
    country_objs = {}
    for country in countries_data:
        try:
            country_name = country.get("name", {}).get("common")
            cca = country.get("cca3", "")
            currency_code = list(country.get("currencies", {}).keys())[0] if country.get("currencies") else None
            currency_name = list(country.get("currencies", {}).values())[0].get("name") if currency_code else None
            capital = country.get("capital", [None])[0]
            region = country.get("region", "")
            subregion = country.get("subregion", "")
            area = country.get("area", 0)
            population = country.get("population", 0)
            map_url = f"https://www.google.com/maps/search/?api=1&query={country_name}"
            flag_url = country.get("flags", {}).get("png", "")

            country_obj = Country(
                name=country_name,
                cca=cca,
                currency_code=currency_code,
                currency=currency_name,
                capital=capital,
                region=region,
                subregion=subregion,
                area=area,
                map_url=map_url,
                population=population,
                flag_url=flag_url
            )
            db.session.add(country_obj)
            country_objs[cca] = country_obj

        except Exception as e:
            print(f"Error inserting country {country_name}: {e}")

    db.session.commit()

    # Now that all countries are inserted, we can insert neighbours
    for country in countries_data:
        try:
            cca = country.get("cca3", "")
            country_obj = country_objs.get(cca)
            if not country_obj:
                continue

            neighbours = country.get("borders", [])
            for neighbour_cca in neighbours:
                neighbour_country = country_objs.get(neighbour_cca)
                if neighbour_country:
                    neighbour_obj = CountryNeighbour(
                        country_id=country_obj.id,
                        neighbour_country_id=neighbour_country.id
                    )
                    db.session.add(neighbour_obj)
        except Exception as e:
            print(f"Error inserting neighbour for country {cca}: {e}")

    db.session.commit()

if __name__ == "__main__":
    countries_data = fetch_countries()
    insert_countries(countries_data)
