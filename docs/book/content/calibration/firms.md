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

Labour's share of output for Ethiopia comes from the [UN ILOSTAT database](https://rshiny.ilo.org/dataexplorer41/?lang=en&segment=indicator&id=SDG_1041_NOC_RT_A), SDG indicator 10.4.1 ("Labour income share as a percent of GDP", series code `SDG_1041_NOC_RT_A`). The most recent value is 0.38209, so total capital's share of output is $1 - 0.38209 = 0.61791$. We split this between private capital $\gamma_m$ and public capital $\gamma_{g,m}$:

```{math}
\gamma_m + \gamma_{g,m} = 0.61791
```

We set $\gamma_{g,m} = 0.08$, the efficiency-adjusted output elasticity of public capital for an average low-income country. The headline output elasticity of effective public capital used by the IMF Debt, Investment, and Growth (DIG) model family for LIC analysis is $\alpha_G = 0.15$ {cite}`Buffie:2012`, paired with an assumed public-investment efficiency $e = 0.5$. OG-Core's production function has no separate efficiency parameter, so the comparable quantity in OG-ETH is the elasticity with respect to installed capital, which is $\alpha_G \cdot e = 0.075$. We round to 0.08.

This value is consistent with the broader empirical literature. {cite}`BomLigthart:2014` report a publication-bias-corrected short-run mean of 0.083 across 578 estimates from 68 studies. {cite}`Calderon:2015` report a long-run output elasticity of synthetic infrastructure (transport, power, telecoms) of 0.07-0.10 for developing countries using a dynamic heterogeneous panel, and find that this elasticity "does not seem to vary systematically with countries' level of per capita income." Foster and Briceño-Garmendia (2010), drawing on the Africa Infrastructure Country Diagnostic, attribute 0.6 percentage points per year of Ethiopia's per-capita growth to infrastructure, which under standard growth accounting maps to an output elasticity in the 0.05-0.085 range.

Given $\gamma_{g,m} = 0.08$ and total capital share 0.61791, private capital share is $\gamma_m = 0.61791 - 0.08 = 0.53791$. Labour's share remains at 0.38209.

### Initial public capital to GDP ratio

The parameter `initial_Kg_ratio` sets the ratio of public capital stock to GDP in the model start year. We set it to 0.65, derived from the IMF Investment and Capital Stock Dataset (ICSD) with a forward projection to the 2025 start year.

The most recent direct measurement comes from the [IMF Investment and Capital Stock Dataset](https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.FAD:ICSD(1.0.0)), indicator `CAPSTCK_S13_Q_POGDP_PT` (general government capital stock as a percent of GDP). For Ethiopia in 2019 this value is 0.667. The ICSD series ends in 2019, so we project to 2025 using the standard perpetual-inventory law of motion in stock-to-GDP units:

```{math}
:label: EqInitialKgPIM
\hat{k}_{g,t+1} = \frac{(1-\delta)\hat{k}_{g,t} + i_{g,t}}{1+g_y}
```

where $\hat{k}_{g,t} \equiv K_{g,t}/Y_t$, $i_{g,t} \equiv I_{g,t}/Y_t$, $\delta$ is the depreciation rate, and $g_y$ is the GDP growth rate. We use $\delta = 0.05$ (matches `delta_annual`) and $g_y = 0.06$ (matches `g_y_annual`). The implied $\delta + g_y$ from ICSD year-on-year transitions over 2010-2019 averages 0.11, consistent with these defaults.

For the post-2019 public investment path $i_{g,t}$ we use values drawn from IMF Article IV reports for Ethiopia ([IMF Country Report 24/253](https://www.imf.org/-/media/Files/Publications/CR/2024/English/1ethea2024002-print-pdf.ashx) and [IMF Country Report 25/188](https://www.imf.org/-/media/files/publications/cr/2025/english/1ethea2025002-source-pdf.pdf)), which document fiscal consolidation under the Extended Credit Facility program. Applying the recursion gives:

| Year | $i_{g,t}$ (% of GDP) | $\hat{k}_{g,t}$ |
| ---: | ---: | ---: |
| 2019 | 8.9 (ICSD actual) | 0.667 |
| 2020 | 8.0 | 0.673 |
| 2021 | 7.0 | 0.670 |
| 2022 | 6.5 | 0.661 |
| 2023 | 6.0 | 0.649 |
| 2024 | 6.0 | 0.639 |
| 2025 | 6.0 | 0.634 |

Rounded to two decimal places, `initial_Kg_ratio = 0.65`. The 2025 projection is lower than the 2019 ICSD point because Ethiopia's documented post-2019 fiscal consolidation reduced public investment below the $(\delta + g_y)\,\hat{k}_g$ threshold required to maintain the ratio.

### Total factor productivity

In the case of the single production sector, we can normalize $Z_{m,t}=1.0$.
