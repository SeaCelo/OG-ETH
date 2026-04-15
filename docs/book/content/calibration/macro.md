(Chap_MacroCalib)=
# Calibration of Macroeconomic Parameters

## Economic Assumptions

As the default rate of labor augmenting technological change, $g_y$, we use a value of 6%.  The average annual growth rate in GDP per capita in Ethiopia between 2006 and 2024 is 6.0% per year, according to [data from the World Bank](https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG?locations=ET).

## Open Economy Parameters

### Foreign holding of government debt in the initial period

The path of foreign holding of domestic debt is endogenous, but the initial period stock of debt held by foreign investors is exogenous. We set this parameter, `initial_foreign_debt_ratio`, to 0.42 using the Ministry of Finance Public Sector Debt Portfolio Analysis for FY2023/24, where external debt is USD 28.89 billion out of USD 68.86 billion of total public debt.

### Foreign purchases of newly issued debt

We set $\zeta_D = 0.12$ using the same FY2023/24 Ministry of Finance debt portfolio analysis. In that year, the change in total public debt was about USD 5.53 billion while the change in external debt was about USD 0.64 billion, implying that roughly 11.6% of new debt issuance was external.

### Foreign holdings of excess capital

We set $\zeta_K = 0.65$. Note, this parameter is harder to pin down from the data as foreign purchases on "excess" capital demand is not typically directly measured or reported. A value of 0.65 implies a relatively open economy while still allowing for a sizable domestic share of excess capital demand.

## Government Debt, Spending and Transfers

### Government Debt

The path of government debt is endogenous. But the initial value and the steady-state (long-run) value are exogenous. To avoid converting between model units and dollars, we calibrate the initial debt-to-GDP ratio, rather than the dollar value of debt. This is the model parameter $\alpha_D$ and the parameter name in [`ogeth_default_parameters.json`](https://github.com/EAPD-DRB/OG-ETH/blob/main/ogeth/ogeth_default_parameters.json) is `initial_debt_ratio`. We set `initial_debt_ratio = 0.327` using the IMF WEO gross general government debt series for Ethiopia, where FY2023/24 mapped to calendar year 2024 is 32.66% of GDP.


#### Interest rates on government debt

We assume that there is a wedge between the real rate of return on private capital and the real interest rate on government debt.  We model this wedge a scale and level shift.  Specifically, we assume that the real interest rate on government debt, $r_{gov,t}$, is related to the real rate of return on private capital, $r_{t}$, by the following equation:

```{math}
:label: eqn:r_gov
    r_{gov,t} = (1-\tau_{d,t})r_t + \mu_d
```

where $\tau_d$ is the scale parameter and $\mu_d$ is the level shift parameter.  We set the values of these two parameters to 0.245 and -0.034, respectively.  These are found by using the estimated relationship between corporate and sovereign yields in {cite}`LMW2023` (Table 8, Column 2) and simulating a series of corporate yields given a series of sovereign yields between 2% and 12%.  We then estimate the scale and level shift parameters that best fit these simulated data using ordinary least squares.

We use this emerging-markets relationship because a calibration based on readily available US corporate and sovereign yield data would be a poor proxy for Ethiopia. The goal of these parameters is not to capture a country-specific live spread series, but to impose a reasonable wedge between private and government borrowing rates using evidence from a broader sample of emerging markets.

These values are fixed calibrated defaults in [`ogeth_default_parameters.json`](https://github.com/EAPD-DRB/OG-ETH/blob/main/ogeth/ogeth_default_parameters.json); they are not refreshed from live data during calibration updates. The following Python reproduces the one-time calculation used to obtain them:

```python
import numpy as np
import statsmodels.api as sm

sov_y = np.arange(20, 120) / 10
corp_yhat = 8.199 - (2.975 * sov_y) + (0.478 * sov_y**2)
corp_yhat = sm.add_constant(corp_yhat)
res = sm.OLS(sov_y, corp_yhat).fit()

r_gov_shift = -res.params[0] / 100
r_gov_scale = res.params[1]

print(r_gov_shift)  # -0.03376625043803517
print(r_gov_scale)  # 0.24484763593657818
```

### Aggregate transfers

Aggregate (non-Social Security) transfers to households are set as a share of GDP with the parameter $\alpha_T$. We exclude Social Security from transfers since it is modeled specifically. In OG-ETH, the relevant concept is government-financed, non-pension transfers paid to households. For Ethiopia, the IMF GFS `S1311B` social-benefits series (`G27_T` and `G271_T`) do not line up well with that concept in the calibration year because they miss the main FY2024/25 government cash contributions to the rural PSNP and urban UPSNP.

Instead, the default calibration uses the IMF program target for Government Contributions to Productive Safety Net Programme cash transfers in FY2024/25 and scales it by the IMF nominal GDP series for the same fiscal year. The FY2024/25 transfer target is 51.4 billion birr and nominal GDP is 14,856 billion birr, implying $\alpha_T = 51.4 / 14{,}856 \approx 0.00346$, which we round to 0.0035. This choice is also consistent with the World Bank development policy financing documents that place the government contribution to rural and urban safety nets at about 0.4% of GDP in FY2024/25. Using the 2024 calibration year, the default calibration therefore sets $\alpha_T = 0.0035$.

### Government expenditures

Government spending on goods and services are also set as a share of GDP with the parameter $\alpha_G$. We define government spending as:
    <center>Government Spending = Total Outlays - Transfers - Net Interest on Debt - Social Security</center>
For Ethiopia, the concept behind $\alpha_G$ is closer to government consumption and public-goods spending than to a budgetary-central-government outlay residual. Because the IMF GFS data available for Ethiopia are published for `Budgetary central government` (`S1311B`), while the model concept is broader and closer to general government spending on goods and services, the default calibration uses the World Bank indicator `NE.CON.GOVT.ZS` instead of mechanically reusing the IMF construction used elsewhere.

Using the World Bank's 2024 value for general government final consumption expenditure, the default calibration sets $\alpha_G = 0.0552$.


(SecLWI_footnotes)=
## Footnotes
The following are the footnotes for this section.

[^macro_wb_DY]: The macro debt and transfer updates above use FY2023/24 or FY2024/25 sources mapped to the repo's 2024 calibration year when that is the closest official match.
