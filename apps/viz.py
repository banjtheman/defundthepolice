from enum import Enum

import altair as alt
import streamlit as st

from plotly import graph_objects


class ChartTypes(Enum):
    BAR_CHART = "Bar Chart"
    PIE_CHART = "Pie Chart"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ChartDisplay:
    def __init__(self, data, chart=ChartTypes.BAR_CHART):
        self.chart = chart
        st.info(
            "Select which columns to display on the bar chart below which displays percent of budget"
        )
        selected_cols = st.multiselect(
            "Select columns", list(data.get("item", "")), list(data.get("item", ""))
        )
        self.data = data.loc[data.get("item", "").isin(selected_cols)]
        self.CHART_DICT = {
            ChartTypes.BAR_CHART.value: self.bar_chart,
            ChartTypes.PIE_CHART.value: self.pie_chart,
        }

    def bar_chart(self):
        # x_col = st.selectbox("Select x axis for bar chart", df.columns)
        # xcol_string=x_col+":O"
        # if st.checkbox("Show as continuous?",key="bar_chart_x_is_cont"):
        x_col = "percent"
        xcol_string = x_col + ":Q"
        y_col = "item"
        z_col = "percent"
        # y_col = st.selectbox("Select y axis for bar chart", df.columns)
        # z_col = st.selectbox("Select z axis for bar chart", df.columns)

        chart = (
            alt.Chart(self.data)
            .mark_bar()
            .encode(
                x=xcol_string,
                y=alt.Y(y_col, sort="-x"),
                color=z_col,
                tooltip=list(self.data.columns),
            )
            # .interactive()
            # .properties(title="Defund The Police")
            .configure_title(
                fontSize=20,
            )
            .configure_axis(labelFontSize=10, titleFontSize=10)
            .configure_legend(labelFontSize=10, titleFontSize=10)
        )
        # TODO figure out saving images
        # chart.save('chart.png')
        return st.altair_chart(chart, use_container_width=True)

    def pie_chart(self):
        labels = list(self.data.get("item", []))
        values = list(self.data.get("percent", []))
        fig = graph_objects.Figure(
            data=[graph_objects.Pie(labels=labels, values=values)]
        )
        return st.plotly_chart(fig, use_container_width=True)

    def get_chart(self):
        return self.CHART_DICT.get(self.chart)()
