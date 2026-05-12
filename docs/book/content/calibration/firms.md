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

We set $\gamma_{g,m} = 0.15$, the IMF DIG headline output elasticity of installed public capital for the average low-income country {cite}`Buffie:2012`.  This sits within the empirical range of 0.07 to 0.15 reported by {cite}`BomLigthart:2014` and {cite}`Calderon:2015`.  Private capital share is then $\gamma_m = 0.46791$.

### Public-investment efficiency

OG-Core's law of motion for public capital is

```{math}
:label: EqPublicCapitalLOM
K_{g,m,t+1} = (1 - \delta_g)\,K_{g,m,t} + (1 - \phi_g)\,I_{g,m,t}
```

where $\phi_g$ (`infra_investment_leakage_rate`) is the fraction of public investment lost to leakage.  We set $\phi_g = 0.5$, matching the IMF DIG calibration of public-investment efficiency $e = 0.5$ for the average low-income country {cite}`Buffie:2012`.

### Initial public capital to GDP ratio

The parameter `initial_Kg_ratio` sets the ratio of public capital stock to GDP in the model start year.  The most recent direct measurement comes from the [IMF Investment and Capital Stock Dataset](https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.FAD:ICSD(1.0.0)) (indicator `CAPSTCK_S13_Q_POGDP_PT`), which reports 0.667 for Ethiopia in 2019.  Because the ICSD series ends in 2019 and OG-ETH's start year is 2025, we project forward using the standard perpetual-inventory law of motion in stock-to-GDP units:

```{math}
:label: EqInitialKgPIM
\hat{k}_{g,t+1} = \frac{(1-\delta)\hat{k}_{g,t} + i_{g,t}}{1+g_y}
```

where $\hat{k}_{g,t} \equiv K_{g,t}/Y_t$ and $i_{g,t} \equiv I_{g,t}/Y_t$.  We use $\delta = 0.05$ and $g_y = 0.06$, matching `delta_annual` and `g_y_annual`.  The post-2019 public investment path comes from IMF Article IV reports ([IMF Country Report 24/253](https://www.imf.org/-/media/Files/Publications/CR/2024/English/1ethea2024002-print-pdf.ashx) and [IMF Country Report 25/188](https://www.imf.org/-/media/files/publications/cr/2025/english/1ethea2025002-source-pdf.pdf)), reflecting fiscal consolidation under the ECF program.  Applying the recursion year by year:

| Year | $i_{g,t}$ (% of GDP) | $\hat{k}_{g,t}$ |
| ---: | ---: | ---: |
| 2019 | 8.9 (ICSD actual) | 0.667 |
| 2020 | 8.0 | 0.673 |
| 2021 | 7.0 | 0.670 |
| 2022 | 6.5 | 0.661 |
| 2023 | 6.0 | 0.649 |
| 2024 | 6.0 | 0.639 |
| 2025 | 6.0 | 0.634 |

We round to `initial_Kg_ratio = 0.65`.

### Total factor productivity

In the case of the single production sector, we can normalize $Z_{m,t}=1.0$.
