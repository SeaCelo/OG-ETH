"""
Tests of macro_params.py module
"""

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
    assert "alpha_T" not in test_dict
    assert test_dict["alpha_G"] == [pytest.approx(0.05515691)]
    assert not any("api.imf.org" in url for url in requested_urls)


def test_alpha_g_omitted_when_world_bank_returns_empty(monkeypatch):
    # Simulate the World Bank alpha_G series returning no observations
    # while the GDP-per-capita series is complete. The split fetches keep
    # g_y_annual intact; alpha_T is not sourced from any API for Ethiopia.
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

    assert "alpha_T" not in test_dict
    assert "alpha_G" not in test_dict
    assert test_dict["g_y_annual"] == pytest.approx(0.25)
    assert not any("api.imf.org" in url for url in requested_urls)
