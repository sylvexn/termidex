from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static

try:
    import httpx
except ImportError:
    raise ImportError("!!! 'pip install httpx' !!!")


class Pokedex(App):
    """
    Test App
    """

    CSS_PATH = "dex.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a Pokemon")
        with VerticalScroll(id="pokemon-con"):
            yield Static(id="pokemon")

    async def on_input_submitted(self, message: Input.Changed) -> None:
        self.update_dex(message.value)

    @work(exclusive=True)
    async def update_dex(self, pokemon: str) -> None:
        pokemon_info = self.query_one("#pokemon", Static)
        if pokemon:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                data = response.json()

                # get pokemon name
                name = data.get("name")

                # get type or types
                pTypes = [t["type"]["name"] for t in data.get("types", [])]
                if len(pTypes) == 1:
                    types = pTypes[0]
                else:
                    types = " / ".join(pTypes)

                # get abilities     TODO: hidden
                pAbilities = [a["ability"]["name"] for a in data.get("abilities", [])]
                if len(pAbilities) == 1:
                    abs = pAbilities[0]
                else:
                    abs = " & ".join(pAbilities)

                info = f"name: {name}\ntypes: {types}\nabilities: {abs}"
                pokemon_info.update(info)
        else:
            pokemon_info.update("")


if __name__ == "__main__":
    app = Pokedex()
    app.run()
