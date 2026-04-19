"""
This module uses World Bank WDI, UN ILO, and documented fiscal-source
values to update OG-ETH macro calibration parameters.
"""

# imports
import pandas as pd
import requests
import datetime
from io import StringIO


def _fetch_wb_data(indicators, country_iso, start_year, end_year, source):
    """
    Fetch a set of World Bank indicators and return a single DataFrame.

    Args:
        indicators (dict): mapping of human-readable labels to indicator codes
        country_iso (str): ISO country code
        start_year (int): first year to request
        end_year (int): last year to request
        source (int): World Bank source ID

    Returns:
        pandas.DataFrame: DataFrame indexed by year/quarter label
    """
    if source == 2:
        date_range = f"{start_year}:{end_year}"
    elif source == 20:
        date_range = f"{start_year}Q1:{end_year}Q4"
    else:
        raise ValueError(f"Unsupported World Bank source: {source}")

    data_frames = []
    for label, indicator_code in indicators.items():
        response = requests.get(
            (
                "https://api.worldbank.org/v2/country/"
                f"{country_iso}/indicator/{indicator_code}"
            ),
            params={
                "date": date_range,
                "source": source,
                "format": "json",
                "per_page": 10000,
            },
        )
        response.raise_for_status()
        try:
            payload = response.json()
        except ValueError as exc:
            raise ValueError(
                f"Malformed World Bank response for {indicator_code}"
            ) from exc

        if (
            not isinstance(payload, list)
            or len(payload) < 2
            or not isinstance(payload[1], list)
            or not payload[1]
        ):
            raise ValueError(
                f"Empty or malformed World Bank response for {indicator_code}"
            )

        series_data = {}
        for row in payload[1]:
            date = row.get("date")
            if date is None:
                continue
            series_data[date] = row.get("value")

        if not series_data:
            raise ValueError(
                f"No dated observations in World Bank response for "
                f"{indicator_code}"
            )

        series = pd.Series(series_data, name=label)
        series = pd.to_numeric(series, errors="coerce")
        data_frames.append(series.to_frame())

    data = pd.concat(data_frames, axis=1)
    data.index.name = "year"
    # Preserve descending time order used by the existing pct_change(-1) logic.
    data = data.sort_index(ascending=False)
    return data


# For Ethiopia, alpha_G is calibrated from general government final
# consumption expenditure because that better matches the OG-ETH concept of
# government spending on goods, services, and public goods than the available
# budgetary central government IMF GFS outlay series.
WB_ALPHA_G_BY_COUNTRY = {
    "ETH": "General government final consumption expenditure (% of GDP)"
}

# Ethiopia's default long-run productivity-growth calibration uses the
# post-2005 growth regime rather than the full World Bank history.
GDP_GROWTH_START_YEAR_BY_COUNTRY = {"ETH": 2006}


def _get_world_bank_alpha_g(wb_data, country_iso, target_year):
    """
    Return a country-specific alpha_G from World Bank data when the spending
    concept aligns better with OG-ETH than the available IMF GFS coverage.
    """
    series_name = WB_ALPHA_G_BY_COUNTRY.get(country_iso.upper())
    if series_name is None or series_name not in wb_data.columns:
        return None

    if isinstance(wb_data.index, pd.MultiIndex):
        years = wb_data.index.get_level_values(-1)
    else:
        years = wb_data.index

    alpha_g_series = pd.Series(
        wb_data[series_name].values,
        index=pd.to_numeric(years, errors="coerce"),
    ).dropna()
    alpha_g_series = alpha_g_series[alpha_g_series.index <= int(target_year)]
    if alpha_g_series.empty:
        raise ValueError(
            "No World Bank government consumption data available for "
            f"{country_iso} up to {target_year}"
        )

    selected_year = (
        int(target_year)
        if int(target_year) in alpha_g_series.index
        else int(alpha_g_series.index.max())
    )
    value = alpha_g_series.loc[selected_year] / 100
    if selected_year != int(target_year):
        print(
            f"No World Bank alpha_G data for {country_iso} in {target_year}. "
            f"Using last available year {selected_year}: alpha_G={value:.4f}"
        )
    return [value]


def _get_world_bank_g_y_annual(wb_data, country_iso, data_start_date):
    """
    Compute average GDP-per-capita growth using the country-specific
    calibration window rather than the full available history.
    """
    series_name = "GDP per capita (constant 2015 US$)"
    if series_name not in wb_data.columns:
        return None

    if isinstance(wb_data.index, pd.MultiIndex):
        years = wb_data.index.get_level_values(-1)
    else:
        years = wb_data.index

    growth_start_year = max(
        int(data_start_date.year),
        GDP_GROWTH_START_YEAR_BY_COUNTRY.get(country_iso.upper(), 0),
    )
    gdp_pc_series = pd.Series(
        wb_data[series_name].values,
        index=pd.to_numeric(years, errors="coerce"),
    ).sort_index(ascending=False)
    gdp_pc_series = gdp_pc_series[gdp_pc_series.index >= growth_start_year]
    g_y_series = gdp_pc_series.pct_change(-1)
    return g_y_series.mean() if not g_y_series.isna().all() else None


def get_macro_params(
    data_start_date=datetime.datetime(1947, 1, 1),
    data_end_date=datetime.datetime(2024, 12, 31),
    country_iso="ETH",
    update_from_api=False,
):
    """
    Compute values of parameters that are derived from macro data

    Args:
        data_start_date (datetime): start date for data
        data_end_date (datetime): end date for data
        country_iso (str): ISO code for country

    Returns:
        macro_parameters (dict): dictionary of parameter values
    """
    # initialize a dictionary of parameters
    macro_parameters = {}

    """
    Retrieve data from the World Bank World Development Indicators.
    """
    # Dictionaries of variables and their corresponding World Bank codes
    # Annual data
    wb_a_variable_dict = {
        "GDP per capita (constant 2015 US$)": "NY.GDP.PCAP.KD",
        "General government final consumption expenditure (% of GDP)": "NE.CON.GOVT.ZS",
        # "Real GDP (constant 2015 US$)": "NY.GDP.MKTP.KD",
        # "Nominal GDP (current US$)": "NY.GDP.MKTP.CD",
        # "General government final consumption expenditure (current US$)": "NE.CON.GOVT.CD",
    }

    wb_alpha_g = None
    if update_from_api:
        try:
            # Pull annual series from the World Bank v2 API
            wb_data_a = _fetch_wb_data(
                wb_a_variable_dict,
                country_iso,
                data_start_date.year,
                data_end_date.year,
                source=2,
            )

            # Compute annual GDP growth safely
            if "GDP per capita (constant 2015 US$)" in wb_data_a.columns:
                macro_parameters["g_y_annual"] = _get_world_bank_g_y_annual(
                    wb_data_a, country_iso, data_start_date
                )
            else:
                print(
                    "Warning: Missing GDP per capita data in World Bank data. Skipping update for g_y_annual."
                )

            print(
                f"g_y_annual updated from World Bank API: {macro_parameters['g_y_annual']}"
            )
            try:
                wb_alpha_g = _get_world_bank_alpha_g(
                    wb_data_a, country_iso, data_end_date.year
                )
            except ValueError:
                wb_alpha_g = None
        except Exception:
            print("Failed to retrieve data from World Bank")
            print("Will not update the following parameters:")
            print(
                "[initial_debt_ratio, initial_foreign_debt_ratio, zeta_D, g_y]"
            )
    else:
        print("Not updating from World Bank API")

    """
    Retrieve labour share data from the United Nations ILOSTAT Data API
    (see https://rplumber-test.ilo.org)
    The series code is SDG_1041_NOC_RT_A (capital share)
    Labor share (gamma) = 1 - capital share
    If this fails we will not update gamma in 'default_parameters.json'
    """
    if update_from_api:
        try:
            target = (
                "https://rplumber.ilo.org/data/indicator/"
                + "?id=SDG_1041_NOC_RT_A"
                + "&ref_area="
                + str(country_iso)
                + "&timefrom="
                + str(data_start_date.year)
                + "&timeto="
                + str(data_end_date.year)
                + "&type=both&format=.csv"
            )
            # Add headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            print("Attempting to update gamma from ILOSTAT")
            response = requests.get(target, headers=headers)
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
            else:
                print("Request successful.")
            csv_content = StringIO(response.text)
            df_temp = pd.read_csv(csv_content)
            ilo_data = df_temp[["time", "obs_value"]]
            # find gamma, capital's share of income
            macro_parameters["gamma"] = [
                1
                - (
                    (
                        ilo_data.loc[
                            ilo_data["time"] == data_end_date.year, "obs_value"
                        ].squeeze()
                    )
                    / 100
                )
            ]
            print(
                f"gamma updated from ILOSTAT API: {macro_parameters['gamma']}"
            )
        except Exception:
            print("Failed to retrieve data from ILOSTAT")
            print("Will not update gamma")
    else:
        print("Not updating from ILOSTAT API")

    """
    Calibrate parameters from documented fiscal sources
    """

    if update_from_api:
        # Ethiopia's alpha_T is calibrated from FY2024/25 government
        # PSNP/UPSNP cash transfers, not from IMF GFS social-benefits
        # series. Source: IMF Country Report 25/188:
        # 51.4 / 14,856 ~= 0.0035, with World Bank DPO P181591 as a
        # consistent ~0.4% of GDP cross-check.
        print("Not updating alpha_T from API for Ethiopia")

        if country_iso.upper() in WB_ALPHA_G_BY_COUNTRY:
            if wb_alpha_g is not None:
                macro_parameters["alpha_G"] = wb_alpha_g
                print(
                    "alpha_G updated from World Bank government consumption "
                    f"data: {macro_parameters['alpha_G']}"
                )
            else:
                print("Will not update alpha_G")
        else:
            print("Will not update alpha_G")

        # initial_debt_ratio, gross general government debt as a fraction of GDP
        # source: from the IMF WEO, Series ETH.GGXWDG_NGDP.A — Gross general government debt (% of GDP).
        # The IMF value annualizes Ethiopia’s fiscal year data (July–June) to the calendar year.
        # 2023/24 (mapped to CY2024) = 32.66% of GDP
        macro_parameters["initial_debt_ratio"] = 0.327

        # initial_foreign_debt_ratio, share of external debt in total public sector debt
        # source: Ministry of Finance, Public Sector Debt Portfolio Analysis No. 25 (2019/20–2023/24)
        # source link: https://www.mofed.gov.et/resources/bulletin/
        # FY2023/24: external debt USD 28.89 billion; total public debt USD 68.86 billion → 42%
        macro_parameters["initial_foreign_debt_ratio"] = 0.42

        # zeta_D, share of new government debt issues purchased by foreign creditors
        # source: Ministry of Finance, Public Sector Debt Portfolio Analysis No. 25 (2019/20–2023/24), Table 1
        # source link: https://www.mofed.gov.et/resources/bulletin/
        # FY2023/24: Δ total debt = +5.53 bn; Δ external debt = +0.64 bn → external share ≈ 11.6%
        # Caution: there is significant annual variatiot: 2020/21 = 49.9, 2021/22 = –152.5, 2022/23 = 5.0, 2023/24 = 11.6
        # We use the latest year.
        macro_parameters["zeta_D"] = [0.12]

    else:
        print("Not updating alpha_T, alpha_G")

    return macro_parameters
