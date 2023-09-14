# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: styringsinfo-datafortelling-gfZTRbJI-py3.11
#     language: python
#     name: python3
# ---

# %%
import os

# %%
import pandas_gbq
import plotly.express as px
from dotenv import load_dotenv

# %%
load_dotenv()
LOCATION = "europe-north1"
PROJECT = os.environ["GCP_TEAM_PROJECT_ID"]

# %%
QUERY = """--sql
with tidsbruk as (
 select s as soknad_sendt, vfa.vedtak_fattet_tidspunkt as vedtak_fattet,
 JUSTIFY_INTERVAL(vfa.vedtak_fattet_tidspunkt - s.sendt) as tid,
 date_diff(vfa.vedtak_fattet_tidspunkt, s.sendt, day) as dager_brukt,
 date_diff(vfa.vedtak_fattet_tidspunkt, s.sendt, hour) as timer_brukt
from
  `tbd-prod-eacd.spre_styringsinfo_dataset.public_vedtak_fattet` vfa
  left join (
    select * from
    `tbd-prod-eacd.spre_styringsinfo_dataset.public_vedtak_dokument_mapping` vdm inner join 
    `tbd-prod-eacd.spre_styringsinfo_dataset.public_sendt_soknad` sso on vdm.dokument_hendelse_id = sso.hendelse_id
  ) s on vfa.hendelse_id = s.vedtak_hendelse_id
)
select count(1), date(tidsbruk.vedtak_fattet) as vedtak_fattet_dato,
--  extract(YEAR from tid) AS aar,
--  extract(MONTH from tid) AS maaneder,
--  extract(DAY from tid) AS dager,
--  dager_brukt,
--  timer_brukt
from tidsbruk
where extract(year from tid) is null
group by vedtak_fattet_dato
order by vedtak_fattet_dato
"""

# %%
df = pandas_gbq.read_gbq(QUERY, PROJECT, progress_bar_type="None")
px.scatter(df, x="vedtak_fattet_dato", y="f0_").show()
