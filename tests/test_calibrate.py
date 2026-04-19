"""
Tests of calibrate.py module
"""

import warnings
from unittest.mock import MagicMock, patch

import numpy as np

from ogeth.calibrate import Calibration


def _make_mock_p(I=1, M=1):
    """
    Create a minimal mock Specifications object.
    """
    p = MagicMock()
    p.I = I
    p.M = M
    p.E = 20
    p.S = 80
    p.J = 7
    p.T = 160
    p.start_year = 2025
    p.lambdas = np.array([0.25, 0.25, 0.2, 0.1, 0.1, 0.09, 0.01])
    return p


class TestOfflineMode:
    """
    Tests for update_from_api=False.
    """

    def test_single_sector_returns_identity_values(self):
        p = _make_mock_p(I=1, M=1)
        c = Calibration(p, update_from_api=False)

        d = c.get_dict()
        assert "alpha_c" in d
        assert "io_matrix" in d
        np.testing.assert_array_equal(d["alpha_c"], np.array([1.0]))
        np.testing.assert_array_equal(d["io_matrix"], np.array([[1.0]]))

    def test_single_sector_omits_macro_and_demographics(self):
        p = _make_mock_p(I=1, M=1)
        c = Calibration(p, update_from_api=False)

        d = c.get_dict()
        assert "g_y_annual" not in d
        assert "initial_debt_ratio" not in d
        assert "e" not in d
        assert "omega_SS" not in d

    def test_multisector_offline_returns_empty_dict(self):
        p = _make_mock_p(I=5, M=4)
        c = Calibration(p, update_from_api=False)

        assert c.alpha_c is None
        assert c.io_matrix is None
        assert c.get_dict() == {}

    @patch("ogeth.calibrate.macro_params")
    @patch("ogeth.calibrate.io")
    @patch("ogeth.calibrate.demographics")
    @patch("ogeth.calibrate.income")
    def test_offline_mode_makes_no_refresh_calls(
        self, mock_income, mock_demog, mock_io, mock_macro
    ):
        p = _make_mock_p(I=5, M=4)
        Calibration(p, update_from_api=False)

        mock_macro.get_macro_params.assert_not_called()
        mock_io.get_alpha_c.assert_not_called()
        mock_io.get_io_matrix.assert_not_called()
        mock_demog.get_pop_objs.assert_not_called()
        mock_income.get_e_interp.assert_not_called()


class TestOnlinePartialFailure:
    """
    Tests for update_from_api=True with partial failures.
    """

    @patch("ogeth.calibrate.macro_params")
    @patch("ogeth.calibrate.demographics")
    def test_macro_failure_warns_and_omits(self, mock_demog, mock_macro):
        mock_macro.get_macro_params.side_effect = RuntimeError("API down")
        mock_demog.get_pop_objs.side_effect = RuntimeError("skip")

        p = _make_mock_p(I=1, M=1)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            c = Calibration(p, update_from_api=True)

        assert any(
            "Macro params update failed" in str(w.message) for w in caught
        )
        d = c.get_dict()
        assert "g_y_annual" not in d
        assert "initial_debt_ratio" not in d
        assert "alpha_c" in d
        assert "io_matrix" in d

    @patch("ogeth.calibrate.io")
    @patch("ogeth.calibrate.macro_params")
    @patch("ogeth.calibrate.demographics")
    def test_sam_failure_warns_and_omits(
        self, mock_demog, mock_macro, mock_io
    ):
        mock_macro.get_macro_params.return_value = {"g_y_annual": 0.01}
        mock_io.get_alpha_c.side_effect = RuntimeError("SAM unavailable")
        mock_io.get_io_matrix.side_effect = RuntimeError("SAM unavailable")
        mock_demog.get_pop_objs.side_effect = RuntimeError("skip")

        p = _make_mock_p(I=5, M=4)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            c = Calibration(p, update_from_api=True)

        assert any("alpha_c update failed" in str(w.message) for w in caught)
        assert any("io_matrix update failed" in str(w.message) for w in caught)
        d = c.get_dict()
        assert d["g_y_annual"] == 0.01
        assert "alpha_c" not in d
        assert "io_matrix" not in d

    @patch("ogeth.calibrate.income")
    @patch("ogeth.calibrate.macro_params")
    @patch("ogeth.calibrate.demographics")
    def test_demographics_failure_warns_and_omits(
        self, mock_demog, mock_macro, mock_income
    ):
        mock_macro.get_macro_params.return_value = {"g_y_annual": 0.01}
        mock_demog.get_pop_objs.side_effect = RuntimeError("UN API down")
        mock_income.get_e_interp.return_value = np.ones((80, 7))

        p = _make_mock_p(I=1, M=1)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            c = Calibration(p, update_from_api=True)

        assert any(
            "Demographics/income update failed" in str(w.message)
            for w in caught
        )
        d = c.get_dict()
        assert d["g_y_annual"] == 0.01
        assert "e" not in d
        assert "omega_SS" not in d
        assert "alpha_c" in d
        assert "io_matrix" in d
