from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
from sqlalchemy import create_engine
import oracledb


@dataclass
class PokemonScraping:
    """
    A scraper that extracts Pokémon data from pokemondb.net
    and stores the results in a pandas DataFrame.
    """

    url_path: Optional[str] = None
    pokemon_url_suffixes: List[str] = field(default_factory=list)

    soup: Optional[BeautifulSoup] = None

    pokemon_dict_data: Dict[str, str] = field(default_factory=dict)
    dataframe: Optional[pd.DataFrame] = None


    def fetch_soup(self, path: str) -> None:
        """
        Fetch an HTML page and parse it into BeautifulSoup.

        Parameters
        ----------
        path : str
            The URL of the page to fetch.
        """
        response = requests.get(path)
        html = response.text
        self.soup = BeautifulSoup(html, "html.parser")

    def get_urls(self) -> None:
        """
        Scrape the national Pokédex page and extract
        the URL suffix of each Pokémon listed.
        """
        
        print("Fetching pokemons url suffixes...")
        self.fetch_soup(path=self.url_path)

        selector: str = "div.infocard > span.infocard-lg-img > a"
        tags: List[Tag] = self.soup.select(selector)

        self.pokemon_url_suffixes = [tag["href"] for tag in tags]

    @staticmethod
    def build_pokemon_url(pokemon_suffix: str) -> str:
        """
        Construct a full Pokémon URL from a suffix.

        Parameters
        ----------
        pokemon_suffix : str
            The relative URL extracted from the national Pokédex list.

        Returns
        -------
        str
            The complete URL for the Pokémon page.
        """
        return "https://pokemondb.net" + pokemon_suffix

    @staticmethod
    def get_table_dict(table: Tag) -> Dict[str, str]:
        """
        Convert an HTML table into a dictionary of key-value pairs.

        Parameters
        ----------
        table : Tag
            A BeautifulSoup table tag containing Pokémon data.

        Returns
        -------
        dict
            A dictionary mapping table headers (th) to data values (td).
        """
        data: Dict[str, str] = {}

        for tr in table.select("tr"):
            th = tr.find("th")
            td = tr.find("td")

            if th and td:
                key = th.get_text(strip=True)
                value = td.get_text(" ", strip=True)
                data[key] = value

        return data

    def get_pokemon_data(self, url: str) -> None:
        """
        Scrape all basic Pokémon data from a Pokémon detail page.

        Parameters
        ----------
        url : str
            The full URL of the Pokémon page.
        """
        
        print("\nFetching pokemon page...")
        self.fetch_soup(url)
        
        selector_name: str = "#main > h1"
        pokemon_name: Tag = self.soup.select_one(selector_name)
        self.pokemon_dict_data["Pokemon Name"] = pokemon_name.get_text(strip=True)
        
        print(f"Getting {self.pokemon_dict_data['Pokemon Name']} data")
        tables: List[Tag] = self.soup.select('[id^="tab-basic-"] table')

        for table in tables:
            self.pokemon_dict_data.update(self.get_table_dict(table))

    def build_database(self) -> None:
        """
        Add the current Pokémon dictionary to the global DataFrame.
        Creates a new DataFrame on first run.
        """
        
        print("Updating master dataframe...")
        row = pd.DataFrame([self.pokemon_dict_data])
    
        if self.dataframe is None:
            self.dataframe = row
        else:
            self.dataframe = pd.concat(
                [self.dataframe, row],
                ignore_index=True,
            )
    
    def save_dataframe_to_oracle(self, conn: Dict[str, str]) -> None:
        
        """
        Save the internal pandas DataFrame to an Oracle table.
        """
        if self.dataframe is None:
            raise ValueError("DataFrame is empty. Run scraping first.")
    
        user = conn["user"]
        password = conn["password"]
        host = conn["host"]
        port = conn["port"]
        service = conn["service"]
        table_name = conn["table_name"]
    
        dsn = f"{host}:{port}/{service}"
    
        engine = create_engine(
            "oracle+oracledb://",
            creator=lambda: oracledb.connect(
                user=user,
                password=password,
                dsn=dsn
            )
        )
    
        self.dataframe.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )



    def run_scraping(self) -> None:
        """
        Execute the complete scraping process:
        - Retrieve Pokémon URLs
        - Extract data for each Pokémon
        - Build the global DataFrame
        """
        self.get_urls()

        for pokemon_url_suffix in self.pokemon_url_suffixes:
            pokemon_full_url = self.build_pokemon_url(pokemon_url_suffix)
            self.get_pokemon_data(pokemon_full_url)
            self.build_database()



if __name__ == "__main__":
    
    instancia = PokemonScraping(url_path="https://pokemondb.net/pokedex/national")
    instancia.run_scraping()

    # Your connection data here
    connection = {
        "user": "",
        "password": "",
        "host": "",
        "port": ,
        "service": "",
        "table_name": "master_pokemon"
    }
    
    instancia.save_dataframe_to_oracle(connection)





