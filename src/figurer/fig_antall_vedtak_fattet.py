import datetime

import pandas as pd
import plotly.graph_objects as go


def antall_vedtak_fattet(client):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    QUERY = f"""
        SELECT
            EXTRACT(YEAR FROM vedtak_fattet AT TIME ZONE 'Europe/Oslo') AS year,
            EXTRACT(MONTH FROM vedtak_fattet AT TIME ZONE 'Europe/Oslo') AS month,
            COUNT(*) as Totalt
        FROM `styringsinfo_dataset.styringsinfo_vedtak_fattet_view`
        WHERE har_utbetaling=true
        AND EXTRACT(YEAR FROM vedtak_fattet AT TIME ZONE 'Europe/Oslo') = {current_year}
        AND EXTRACT(MONTH FROM vedtak_fattet AT TIME ZONE 'Europe/Oslo') <= {current_month}
        GROUP BY year, month
        ORDER BY year DESC, month DESC
    """

    query_job = client.query(QUERY)

    df_months: pd.DataFrame = query_job.to_dataframe()

    # Create a new plotly figure
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[f"{row['year']}-{row['month']:02}" for _, row in df_months.iterrows()],
            y=df_months["Totalt"],
            text=df_months["Totalt"],
            textposition="auto",
            marker_color="#3380A5",
            marker_line_width=1,
            opacity=1,
        )
    )

    fig.update_layout(
        title=dict(
            text="Antall vedtak per måned",
            x=0,
            y=0.95,
            font=dict(family="Source Sans 3", size=20, color="#23262A"),
        ),
        xaxis_tickangle=-45,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            gridcolor="#CCCCCC",
        ),
    )
    return fig
