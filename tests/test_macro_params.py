"""
Tests of macro_params.py module
"""

import datetime

import pandas as pd
import pytest
import requests

from ogeth import macro_params


class MockResponse:
    """
    Minimal mock response for requests.get().
    """

    def __init__(self, *, json_data=None, text="", status_code=200):
        self._json_data = json_data
        self.text = text
        self.status_code = status_code

    def json(self):
        if isinstance(self._json_data, Exception):
            raise self._json_data
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(
                f"HTTP {self.status_code} returned from mocked request"
            )


def _imf_payload(indicator_year_values, country="ETH", sector="S1311B"):
    years = sorted(
        {
            int(year)
            for observations in indicator_year_values.values()
            for year in observations.keys()
        }
    )
    indicators = list(indicator_year_values.keys())
    return {
        "meta": {},
        "data": {
            "dataSets": [
                {
                    "structure": 0,
                    "action": "Replace",
                    "series": {
                        f"0:0:0:{indicator_idx}:0:0": {
                            "attributes": [0, None, 0],
                            "observations": {
                                str(years.index(int(year))): [value]
                                for year, value in observations.items()
                            },
                        }
                        for indicator_idx, observations in enumerate(
                            indicator_year_values.values()
                        )
                    },
                }
            ],
            "structures": [
                {
                    "dimensions": {
                        "series": [
                            {"id": "COUNTRY", "values": [{"id": country}]},
                            {"id": "SECTOR", "values": [{"id": sector}]},
                            {"id": "GFS_GRP", "values": [{"id": "G2M"}]},
                            {
                                "id": "INDICATOR",
                                "values": [
                                    {"id": indicator}
                                    for indicator in indicators
                                ],
                            },
                            {
                                "id": "TYPE_OF_TRANSFORMATION",
                                "values": [{"id": "POGDP_PT"}],
                            },
                            {"id": "FREQUENCY", "values": [{"id": "A"}]},
                        ],
                        "observation": [
                            {
                                "id": "TIME_PERIOD",
                                "values": [
                                    {"value": str(year)} for year in years
                                ],
                            }
                        ],
                    },
                    "attributes": {
                        "series": [
                            {
                                "id": "SCALE",
                                "values": [{"id": "0"}],
                            },
                            {"id": "DECIMALS_DISPLAYED", "values": []},
                            {"id": "OVERLAP", "values": [{"id": "OL"}]},
                        ],
                        "observation": [
                            {"id": "PRECISION", "values": []},
                            {
                                "id": "DERIVATION_TYPE",
                                "values": [{"id": "O"}],
                            },
                            {"id": "STATUS", "values": []},
                            {"id": "NATURE_OF_DATA", "values": []},
                            {
                                "id": "BASES_OF_RECORDING_CASH_NON_CASH",
                                "values": [],
                            },
                            {
                                "id": "BASES_OF_RECORDING_GROSS_NET",
                                "values": [{"id": "NP"}],
                            },
                            {"id": "VALUATION", "values": [{"id": "_Z"}]},
                        ],
                    },
                }
            ],
        },
    }


def _wb_payload(observations):
    return [
        {
            "page": 1,
            "pages": 1,
            "per_page": "10000",
            "total": len(observations),
        },
        [
            {
                "date": date,
                "value": value,
                "indicator": {"id": "mock-indicator"},
            }
            for date, value in observations
        ],
    ]


_DEFAULT_WB_PAYLOADS = {
    "NY.GDP.PCAP.KD": _wb_payload(
        [("2024", 100.0), ("2023", 80.0), ("2022", 64.0)]
    ),
    "NE.CON.GOVT.ZS": _wb_payload(
        [("2024", 5.515691), ("2023", 6.317772), ("2022", 7.361735)]
    ),
}


def _mock_requests_get(
    monkeypatch,
    requested_urls,
    *,
    ilo_text=None,
    imf_json=None,
    wb_payloads=None,
):
    payloads = _DEFAULT_WB_PAYLOADS if wb_payloads is None else wb_payloads

    def fake_get(url, params=None, headers=None, timeout=None):
        requested_urls.append(url)
        if "worldbank.org" in url:
            indicator_code = url.rstrip("/").split("/")[-1]
            return MockResponse(json_data=payloads[indicator_code])
        if "rplumber.ilo.org" in url:
            return MockResponse(
                text=ilo_text or "time,obs_value\n2024,38.209\n2023,38.0\n"
            )
        if "api.imf.org" in url:
            return MockResponse(
                json_data=imf_json
                or _imf_payload(
                    {
                        "G2_T": {
                            2023: 6.121621434173129,
                            2024: 5.117707506327274,
                        },
                        "G24_T": {
                            2023: 0.5526694185117545,
                            2024: 0.5920776865725198,
                        },
                        "G27_T": {2023: 0.0, 2024: 0.0},
                        "G271_T": {2023: 0.0, 2024: 0.0},
                    }
                )
            )
        raise AssertionError(f"Unexpected URL requested in test: {url}")

    monkeypatch.setattr(macro_params.requests, "get", fake_get)


def test_get_macro_params_update_from_api_false_returns_empty_dict():
    test_dict = macro_params.get_macro_params(update_from_api=False)

    assert isinstance(test_dict, dict)
    assert test_dict == {}


def test_get_macro_params_update_from_api_true(monkeypatch):
    requested_urls = []
    _mock_requests_get(monkeypatch, requested_urls)

    test_dict = macro_params.get_macro_params(update_from_api=True)

    assert isinstance(test_dict, dict)
    assert sorted(test_dict.keys()) == sorted(
        [
            "alpha_T",
            "alpha_G",
            "initial_debt_ratio",
            "g_y_annual",
            "gamma",
            "zeta_D",
            "initial_foreign_debt_ratio",
        ]
    )
    assert test_dict["initial_debt_ratio"] == 0.327
    assert test_dict["initial_foreign_debt_ratio"] == 0.42
    assert test_dict["zeta_D"] == [0.12]
    assert test_dict["g_y_annual"] == pytest.approx(0.25)
    assert test_dict["gamma"] == [pytest.approx(0.61791)]
    assert test_dict["alpha_T"] == [pytest.approx(0.0)]
    assert test_dict["alpha_G"] == [pytest.approx(0.05515691)]
    assert any(
        ".ETH.S1311B.G2M." in url or "/ETH.S1311B.G2M." in url
        for url in requested_urls
    )


def test_get_imf_macro_params_uses_eth_budgetary_sector(monkeypatch):
    requested_urls = []
    _mock_requests_get(monkeypatch, requested_urls)

    result = macro_params._get_imf_macro_params("ETH", 2024)

    assert result["alpha_T"] == [pytest.approx(0.0)]
    assert result["alpha_G"] == [pytest.approx(0.04525629819754754)]
    assert any("/ETH.S1311B.G2M.*.POGDP_PT.A" in url for url in requested_urls)


def test_get_imf_macro_params_overwrites_saved_file(monkeypatch, tmp_path):
    requested_urls = []
    _mock_requests_get(monkeypatch, requested_urls)

    data_file = tmp_path / "imf_gfs_soo_eth_s1311b_g2m_pogdp_pt_a.csv"
    result = macro_params._get_imf_macro_params(
        "ETH", 2024, data_path=data_file
    )

    assert result["alpha_G"] == [pytest.approx(0.04525629819754754)]
    assert data_file.exists()

    requested_urls.clear()
    _mock_requests_get(
        monkeypatch,
        requested_urls,
        imf_json=_imf_payload(
            {
                "G2_T": {2024: 5.0},
                "G24_T": {2024: 0.5},
                "G27_T": {2024: 0.0},
                "G271_T": {2024: 0.0},
            }
        ),
    )

    refreshed = macro_params._get_imf_macro_params(
        "ETH", 2024, data_path=data_file
    )

    assert refreshed != result
    saved_data = pd.read_csv(data_file)
    saved_2024 = saved_data[saved_data["year"] == 2024].set_index("indicator")
    assert saved_2024.loc["G2_T", "value"] == pytest.approx(5.0)
    assert saved_2024.loc["G24_T", "value"] == pytest.approx(0.5)


def test_get_imf_macro_params_falls_back_to_last_available_year(monkeypatch):
    requested_urls = []
    _mock_requests_get(
        monkeypatch,
        requested_urls,
        imf_json=_imf_payload(
            {
                "G2_T": {2024: 5.117707506327274},
                "G24_T": {2024: 0.5920776865725198},
                "G27_T": {2024: 0.0},
                "G271_T": {2024: 0.0},
            }
        ),
    )

    result = macro_params._get_imf_macro_params("ETH", 2025)

    assert result["alpha_T"] == [pytest.approx(0.0)]
    assert result["alpha_G"] == [pytest.approx(0.04525629819754754)]


def test_get_macro_params_passes_imf_year_override(monkeypatch):
    requested_urls = []
    _mock_requests_get(
        monkeypatch,
        requested_urls,
        imf_json=_imf_payload(
            {
                "G2_T": {2023: 6.121621434173129},
                "G24_T": {2023: 0.5526694185117545},
                "G27_T": {2023: 0.0},
                "G271_T": {2023: 0.0},
            }
        ),
    )

    test_dict = macro_params.get_macro_params(
        update_from_api=True,
        imf_data_year=2023,
        data_end_date=datetime.datetime(2024, 12, 31),
    )

    assert test_dict["alpha_G"] == [pytest.approx(0.05515691)]


def test_eth_alpha_g_updates_when_imf_fails(monkeypatch):
    requested_urls = []

    def fake_get(url, params=None, headers=None, timeout=None):
        requested_urls.append(url)
        if "worldbank.org" in url:
            indicator_code = url.rstrip("/").split("/")[-1]
            return MockResponse(json_data=_DEFAULT_WB_PAYLOADS[indicator_code])
        if "rplumber.ilo.org" in url:
            return MockResponse(
                text="time,obs_value\n2024,38.209\n2023,38.0\n"
            )
        if "api.imf.org" in url:
            raise requests.HTTPError("mock IMF failure")
        raise AssertionError(f"Unexpected URL requested in test: {url}")

    monkeypatch.setattr(macro_params.requests, "get", fake_get)

    test_dict = macro_params.get_macro_params(update_from_api=True)

    assert "alpha_T" not in test_dict
    assert test_dict["alpha_G"] == [pytest.approx(0.05515691)]


def test_eth_alpha_t_updates_without_world_bank_alpha_g(monkeypatch):
    # Simulate the World Bank alpha_G series returning no observations
    # while the GDP-per-capita series is complete. The outer try/except
    # in get_macro_params swallows the resulting fetch error, so alpha_T
    # still updates from IMF but alpha_G is not set.
    requested_urls = []
    _mock_requests_get(
        monkeypatch,
        requested_urls,
        wb_payloads={
            "NY.GDP.PCAP.KD": _wb_payload(
                [("2024", 100.0), ("2023", 80.0), ("2022", 64.0)]
            ),
            "NE.CON.GOVT.ZS": [
                {"page": 1, "pages": 1, "per_page": "10000", "total": 0},
                [],
            ],
        },
    )

    test_dict = macro_params.get_macro_params(update_from_api=True)

    assert test_dict["alpha_T"] == [pytest.approx(0.0)]
    assert "alpha_G" not in test_dict
