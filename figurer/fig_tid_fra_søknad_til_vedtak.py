import datetime

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def tid_fra_søknad_til_vedtak(client):
    QUERY = """
    SELECT COUNT(*) AS antall_vedtak, dager_brukt, DATE_TRUNC(vedtak_fattet_dato, WEEK(MONDAY)) as week
        FROM `styringsinfo_dataset.styringsinfo_vedtak_tidsbruk`
        WHERE vedtak_fattet_dato >= CURRENT_DATE() - 21
        AND har_utbetaling = true
        GROUP BY dager_brukt, week
        ORDER BY dager_brukt desc
    """

    query_job = client.query(QUERY)

    df: pd.DataFrame = query_job.to_dataframe()
    uker = sorted(df["week"].unique(), reverse=True)
    i_dag = datetime.date.today()
    inneværende_uke = uker[0] if len(uker) > 0 else i_dag
    forrige_uke = uker[1] if len(uker) > 1 else inneværende_uke
    to_uker_siden = uker[2] if len(uker) > 2 else forrige_uke

    df_inneværende_uke = df[df.week == inneværende_uke]
    df_forrige_uke = df[df.week == forrige_uke]
    df_to_uker_siden = df[df.week == to_uker_siden]
    beholder = [df_inneværende_uke, df_forrige_uke, df_to_uker_siden]

    fig = make_subplots(
        rows=2,
        cols=3,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
            [{"colspan": 3}, None, None],
        ],
    )

    for df, visible in zip(beholder, [True, False, False]):
        totalt = df["antall_vedtak"].values.sum()
        under_en_dag = df.query("dager_brukt == 0")["antall_vedtak"].values.sum()
        mer_enn_90_dager = df.query("dager_brukt > 90")["antall_vedtak"].values.sum()

        bar = go.Bar(
            x=df.query("dager_brukt > 0 & dager_brukt <= 90")["dager_brukt"],
            y=df.query("dager_brukt > 0 & dager_brukt <= 90")["antall_vedtak"],
            visible=visible,
        )

        fig.add_trace(bar, row=2, col=1)

        fig.add_trace(
            go.Indicator(
                title="Totalt",
                mode="number",
                value=totalt,
                number={"font": {"size": 48}},
                visible=visible,
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Indicator(
                title="Under en dag",
                mode="number",
                value=under_en_dag,
                number={"font": {"size": 48}},
                visible=visible,
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Indicator(
                title="Mer enn 90 dager",
                mode="number",
                number={"font": {"size": 48}},
                value=mer_enn_90_dager,
                visible=visible,
            ),
            row=1,
            col=3,
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
        xaxis_title="Dager gått til vedtaket ble fattet",
        xaxis_tick0=1,
        yaxis_title="Antall søknader",
        xaxis_tickangle=-45,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        updatemenus=[
            dict(
                buttons=list(
                    [
                        dict(
                            args=[{"visible": [True] * 4 + [False] * 8}],
                            label="Inneværende uke",
                            method="restyle",
                        ),
                        dict(
                            args=[{"visible": [False] * 4 + [True] * 4 + [False] * 4}],
                            label="Forrige uke",
                            method="restyle",
                        ),
                        dict(
                            args=[{"visible": [False] * 8 + [True] * 4}],
                            label="To uker siden",
                            method="restyle",
                        ),
                    ]
                ),
                **BUTTON_CONFIG,
            )
        ],
    )
    return fig
