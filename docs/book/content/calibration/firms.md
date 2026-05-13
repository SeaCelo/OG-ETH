(Chap_FirmCalib)=
# Calibration of Firm Parameters

## Aggregate Production Function and Capital Accumulation

The [OG-Core firm theory documentation](https://pslmodels.github.io/OG-Core/content/theory/firms.html) outlines the constant returns to scale, constant elasticity of substitution production function of the representative firm.  This function has two parameters; the elasticity of substitution and capital's share of output.

The production function is given as:

```{math}
:label: EqFirmsCESprodfun
  \begin{split}
    Y_{m,t} &= F(K_{m,t}, K_{g,m,t}, L_{m,t}) \\
    &\equiv Z_{m,t}\biggl[(\gamma_m)^\frac{1}{\varepsilon_m}(K_{m,t})^\frac{\varepsilon_m-1}{\varepsilon_m} + (\gamma_{g,m})^\frac{1}{\varepsilon_m}(K_{g,m,t})^\frac{\varepsilon_m-1}{\varepsilon_m} + \\
    &\quad\quad\quad\quad\quad(1-\gamma_m-\gamma_{g,m})^\frac{1}{\varepsilon_m}(e^{g_y t}L_{m,t})^\frac{\varepsilon_m-1}{\varepsilon_m}\biggr]^\frac{\varepsilon_m}{\varepsilon_m-1} \quad\forall m,t
  \end{split}
```

  This production function has the following parameters:
  * $\varepsilon_m$ is the elasticity of substitution between capital, labor, and infrastructure in sector $m$.
  * $\gamma_m$ is the share of capital in sector $m$.
  * $\gamma_{g,m}$ is the share of government capital in sector $m$.
  * $Z_{m,t}$ is the total factor productivity in sector $m$ at time $t$.

### Elasticity of substitution

`OG-ETH`'s default parameterization has an elasticity of substitution of $\varepsilon=1.0$, which implies a Cobb-Douglas production function.

### Factor shares of output

Labour's share of output for Ethiopia comes from the [UN ILOSTAT database](https://rshiny.ilo.org/dataexplorer41/?lang=en&segment=indicator&id=SDG_1041_NOC_RT_A), SDG indicator 10.4.1 (series code `SDG_1041_NOC_RT_A`).  The most recent value is 0.38209, so total capital's share of output is $1 - 0.38209 = 0.61791$.  We split this between private capital $\gamma_m$ and public capital $\gamma_{g,m}$, with $\gamma_m + \gamma_{g,m} = 0.61791$.

We set $\gamma_{g,m} = 0.10$, within the empirical range of 0.07 to 0.15 reported by {cite}`Buffie:2012`, {cite}`BomLigthart:2014`, and {cite}`Calderon:2015`.  Private capital share is then $\gamma_m = 0.51791$.

### Public-investment efficiency

OG-Core's law of motion for public capital is

```{math}
:label: EqPublicCapitalLOM
K_{g,m,t+1} = (1 - \delta_g)\,K_{g,m,t} + (1 - \phi_g)\,I_{g,m,t}
```

where $\delta_g$ is the depreciation rate of public capital (the `delta_g_annual` parameter) and $\phi_g$ (`infra_investment_leakage_rate`) is the fraction of public investment lost to leakage.  We set $\phi_g = 0.5$, matching the IMF DIG calibration of public-investment efficiency $e = 0.5$ for the average low-income country {cite}`Buffie:2012`.

Public investment flow is set as a share of GDP, $I_{g,t} = \alpha_{I,t}\,Y_t$.  We calibrate `alpha_I` as a five-year linear path from the most recent actual to the IMF ECF program's medium-term target, then hold constant:

| $t$            | 0     | 1     | 2     | 3     | $\geq 4$ |
|:---------------|:-----:|:-----:|:-----:|:-----:|:--------:|
| $\alpha_{I,t}$ | 0.040 | 0.045 | 0.050 | 0.055 | 0.060    |

The $t = 0$ value comes from the [NBE Annual Report 2023/24](https://nbe.gov.et/wp-content/uploads/2025/06/Annual-Report-2023-2024.pdf), Section 3.5: general government capital expenditure was 467,457.6 million Birr against total expenditure of 1,120,077.3 million Birr, where total expenditure was 9.5% of GDP, giving $\alpha_I = (467{,}457.6 / 1{,}120{,}077.3) \times 0.095 = 0.0396$.  The $t \geq 4$ value of 0.060 matches the [IMF ECF program medium-term fiscal framework](https://www.imf.org/en/Publications/CR/Issues/2024/07/29/The-Federal-Democratic-Republic-of-Ethiopia-Request-for-an-Arrangement-Under-the-Extended-552556) and the five-year backward average prior to the recent fiscal consolidation.

### Initial public capital to GDP ratio

The parameter `initial_Kg_ratio` sets the ratio of public capital stock to GDP in the model start year.  We set it to 0.40, matching the steady state implied by the law of motion at our calibrated $\phi_g$, $\delta_g$, $g_y$, and the long-run $\alpha_I = 0.060$:

```{math}
:label: EqInitialKgSS
\bar{K}_g / \bar{Y} = \frac{(1-\phi_g)\,\alpha_I}{\delta_g + g_y} = \frac{0.5 \times 0.06}{0.02 + 0.06} = 0.375
```

Rounded to two decimal places, `initial_Kg_ratio = 0.40`.  Initializing near the model's steady-state $\bar{K}_g/\bar{Y}$ keeps the transition path well-behaved.  This value is also consistent with [IMF Investment and Capital Stock Dataset](https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.FAD:ICSD(1.0.0)) (indicator `CAPSTCK_S13_Q_POGDP_PT`) readings for Ethiopia in the late 2000s, before the GTP infrastructure push raised the ratio to 0.667 by 2019.

### Total factor productivity

In the case of the single production sector, we can normalize $Z_{m,t}=1.0$.
