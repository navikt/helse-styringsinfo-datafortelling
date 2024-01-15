import pandas as pd
import plotly.graph_objects as go


def antall_med_glidende_gjennomsnitt(
    tittel, timestamp_felt, tabell, client, predikat=""
):
    # SQL query to count number of rows per day and calculate moving averages
    QUERY = f"""
    WITH PreprocessedData AS (
        SELECT
            EXTRACT(DATE FROM {timestamp_felt} AT TIME ZONE 'Europe/Oslo') AS date,
            korrigerende,
            COUNT(*) as Totalt
        FROM `{tabell}`
        WHERE {timestamp_felt} >= TIMESTAMP("2023-03-01", "Europe/Oslo")
          {predikat}
        GROUP BY date, korrigerende
    ),
    AveragedData AS (
        SELECT
            date,
            korrigerende,
            Totalt,
            AVG(Totalt) OVER(
                PARTITION BY korrigerende
                ORDER BY date
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ) as MovingAverage7Days,
            AVG(Totalt) OVER(
                PARTITION BY korrigerende
                ORDER BY date
                ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
            ) as MovingAverage28Days
        FROM PreprocessedData
    )
    SELECT *
    FROM AveragedData
    WHERE date >= "2023-04-01"
    ORDER BY date ASC, korrigerende ASC
    """

    query_job = client.query(QUERY)

    df: pd.DataFrame = query_job.to_dataframe()

    fig = go.Figure()

    # Add bar chart for daily counts
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["count"],
            name="Antall per dag",
            marker_color="#3380A5",
        )
    )

    # Add lines for moving averages
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["moving_7_day_avg"],
            name="Snitt over 7 dager",
            line=dict(color="#FF9100"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["moving_28_day_avg"],
            name="Snitt over 28 dager",
            line=dict(color="#C30000"),
        )
    )

    # Set x and y axis labels
    fig.update_layout(
        title=dict(
            text="7- og 28 dagers glidende gjennomsnitt",
            x=0,
            y=0.95,
            font=dict(family="Source Sans 3", size=20, color="#23262A"),
        ),
        plot_bgcolor="#FFFFFF",
        yaxis=dict(
            gridcolor="#CCCCCC",
        ),
    )

    return fig
