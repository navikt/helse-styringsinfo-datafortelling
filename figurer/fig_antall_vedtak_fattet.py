import datetime

import pandas as pd
import plotly.graph_objects as go


def antall_vedtak_fattet(client):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    QUERY = f"""
        SELECT
            EXTRACT(DATE FROM vedtak_fattet AT TIME ZONE 'Europe/Oslo') AS date,
            DATE_TRUNC(EXTRACT(DATE FROM vedtak_fattet AT TIME ZONE 'Europe/Oslo'), WEEK(MONDAY)) as week,
            DATE_TRUNC(EXTRACT(DATE FROM vedtak_fattet AT TIME ZONE 'Europe/Oslo'), MONTH) AS month,
            COUNT(*) as Totalt
        FROM `styringsinfo_dataset.styringsinfo_vedtak_fattet_view`
        WHERE har_utbetaling=true
          AND vedtak_fattet >= TIMESTAMP("2023-04-01", "Europe/Oslo")
        GROUP BY date, week, month
        ORDER BY date ASC
    """

    query_job = client.query(QUERY)

    df_days: pd.DataFrame = query_job.to_dataframe()
    df_weeks = df_days.groupby(["week"], as_index=False)["Totalt"].sum()
    df_months = df_days.groupby(["month"], as_index=False)["Totalt"].sum()


    # Create a new plotly figure
    fig = go.Figure()

    fig.add_traces(
        data=[
            go.Bar(
                x=df_months.month,
                y=df_months.Totalt,
                name="Totalt",
                visible=True,
                marker_color="#3380A5",
            ),
            go.Bar(
                x=df_weeks.week,
                y=df_weeks.Totalt,
                name="Totalt",
                visible=False,
                marker_color="#3380A5",
            ),
            go.Bar(
                x=df_days.date,
                y=df_days.Totalt,
                name="Totalt",
                visible=False,
                marker_color="#3380A5",
            ),
        ]
    )
    BUTTON_CONFIG = {
        "active": 0,
        "type": "buttons",
        "direction": "right",
        "showactive": True,
        "x": 0,
        "xanchor": "left",
        "y": 1,
        "yanchor": "bottom",
        "font": {"size": 14},
    }

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0,
            )
        )

    fig.update_layout(
        margin=dict(l=50),
        barmode="stack",
        updatemenus=[
            dict(
                buttons=list(
                    [
                        dict(
                            args=[
                                {"visible": [True, False, False]}
                            ],
                            label="Måneder",
                            method="restyle",
                        ),
                        dict(
                            args=[
                                {"visible": [False, True, False]}
                            ],
                            label="Uker",
                            method="restyle",
                        ),
                        dict(
                            args=[
                                {"visible": [False, False, True]}
                            ],
                            label="Dager",
                            method="restyle",
                        ),
                    ]
                ),
                **BUTTON_CONFIG,
            )
        ],
        title=dict(
            text="Antall vedtak",
            x=0,
            y=0.97,
            font=dict(family="Source Sans 3", size=20, color="#23262A"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            gridcolor="#CCCCCC",
        ),
    )
    return fig
