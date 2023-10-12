import datetime

import pandas as pd
import plotly.graph_objects as go


def mottatte_søknader(client):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    QUERY = f"""
        SELECT
            EXTRACT(DATE FROM soknad_mottatt AT TIME ZONE 'Europe/Oslo') AS date,
            DATE_TRUNC(EXTRACT(DATE FROM soknad_mottatt AT TIME ZONE 'Europe/Oslo'), WEEK(MONDAY)) as week,
            DATE_TRUNC(EXTRACT(DATE FROM soknad_mottatt AT TIME ZONE 'Europe/Oslo'), MONTH) as month,
            korrigerende,
            COUNT(*) as Totalt
        FROM `styringsinfo_dataset.styringsinfo_sendt_soknad_view`
        WHERE EXTRACT(YEAR FROM soknad_mottatt AT TIME ZONE 'Europe/Oslo') = {current_year}
            AND EXTRACT(MONTH FROM soknad_mottatt AT TIME ZONE 'Europe/Oslo') <= {current_month}
        GROUP BY date, week, month, korrigerende
        ORDER BY date ASC, korrigerende ASC
    """

    query_job = client.query(QUERY)

    df_days: pd.DataFrame = query_job.to_dataframe()
    df_days_førstegangs = df_days[df_days.korrigerende == False]
    df_days_korrigerende = df_days[df_days.korrigerende == True]

    df_weeks = df_days.groupby(["week", "korrigerende"], as_index=False)["Totalt"].sum()
    df_weeks_førstegang = df_weeks[df_weeks.korrigerende == False]
    df_weeks_korrigerende = df_weeks[df_weeks.korrigerende == True]

    df_months = df_days.groupby(["month", "korrigerende"], as_index=False)[
        "Totalt"
    ].sum()
    df_months_førstegang = df_months[df_months.korrigerende == False]
    df_months_korrigerende = df_months[df_months.korrigerende == True]

    fig = go.Figure()
    fig.add_traces(
        data=[
            go.Bar(
                x=df_months_førstegang.month,
                y=df_months_førstegang.Totalt,
                name="Førstegangs",
                visible=True,
                marker_color="#3380A5",
            ),
            go.Bar(
                x=df_months_korrigerende.month,
                y=df_months_korrigerende.Totalt,
                name="Korrigerende",
                visible=True,
                marker_color="#FF9100",
            ),
            go.Bar(
                x=df_weeks_førstegang.week,
                y=df_weeks_førstegang.Totalt,
                name="Førstegangs",
                visible=False,
                marker_color="#3380A5",
            ),
            go.Bar(
                x=df_weeks_korrigerende.week,
                y=df_weeks_korrigerende.Totalt,
                name="Korrigerende",
                visible=False,
                marker_color="#FF9100",
            ),
            go.Bar(
                x=df_days_førstegangs.date,
                y=df_days_førstegangs.Totalt,
                name="Førstegangs",
                visible=False,
                marker_color="#3380A5",
            ),
            go.Bar(
                x=df_days_korrigerende.date,
                y=df_days_korrigerende.Totalt,
                name="Korrigerende",
                visible=False,
                marker_color="#FF9100",
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
        margin=dict(l=50),
        barmode="stack",
        updatemenus=[
            dict(
                buttons=list(
                    [
                        dict(
                            args=[
                                {"visible": [True, True, False, False, False, False]}
                            ],
                            label="Måneder",
                            method="restyle",
                        ),
                        dict(
                            args=[
                                {"visible": [False, False, True, True, False, False]}
                            ],
                            label="Uker",
                            method="restyle",
                        ),
                        dict(
                            args=[
                                {"visible": [False, False, False, False, True, True]}
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
            text="Antall innsendte førstegangs- og korrigerte søknader",
            x=0,
            y=0.97,
            font=dict(family="Source Sans 3", size=20, color="#23262A"),
        ),
        plot_bgcolor="#FFFFFF",
        yaxis=dict(
            gridcolor="#CCCCCC",
        ),
    )
    return fig
