import textwrap

from apps.utils import create_budget_json, draw_image
from viz import ChartDisplay


class CountyInfo:
    def __init__(self, county, state, bg_color, text_color, font, chart):
        self.county = county
        self.state = state
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font
        self.chart = chart

    def get_data(self):
        return create_budget_json(self.state, self.county)

    def get_budget_for_year(self):
        police_data, budget_df = self.get_data()
        money = "$" + f'{police_data.get("budget", ""):,}'
        header_string = (
            # "For "
            # + str(police_data["year"])
            # + " "
            str(self.county)
            + " County, "
            + str(self.state)
            + " has a police budget of "
            + str(money)
        )
        wrapped_string = textwrap.wrap(header_string, width=30)
        return draw_image(wrapped_string, self.bg_color, self.text_color, self.font)

    def chart_display(self):
        _, budget_df = self.get_data()
        ChartDisplay(data=budget_df, chart=self.chart).get_chart()
