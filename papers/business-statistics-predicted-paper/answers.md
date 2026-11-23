<!--
  Business Statistics (B.Com. 3), a full predicted paper in the last university paper's blueprint (code 54322), with answers.
  Made 23-11-2026. Methods follow the solved 54322 (step-deviation, (N+1)/4 quartiles, GM by logs, Karl Pearson actual-mean, PE).
  Every figure was computed and cross-checked in a script.
-->

# SECTION A – 2 MARKS

## Q1.
**Statistics** is the science of collecting, classifying, presenting, analysing and interpreting numerical data to help in decision-making.

## Q2.
**Primary data** are data collected originally by the investigator for the first time, for a specific purpose, directly from the source.

## Q3.
**Classification** is the process of arranging data into groups or classes according to their common characteristics.

## Q4.
**Tabulation** is the systematic presentation of classified data in rows and columns with suitable headings.

## Q5.
The **arithmetic mean** is the sum of all the values divided by the number of values. Mean = Σx / N.

## Q6.
The **median** is the middle value of a series arranged in ascending or descending order; it divides the series into two equal halves.

## Q7.
The **mode** is the value that occurs most frequently in a series.

## Q8.
**Standard deviation** is the square root of the arithmetic mean of the squares of the deviations of the values from their mean. It is the most reliable measure of dispersion.

## Q9.
The **coefficient of variation** = (Standard deviation ÷ Mean) × 100. It compares the variability of two or more series.

## Q10.
**Correlation** is the statistical relationship between two variables, in which a change in one variable is associated with a change in the other.

## Q11.
**Regression** is the statistical method of estimating or predicting the value of one variable from the known value of another related variable.

## Q12.
The **probable error** of the coefficient of correlation = 0.6745 × (1 − r²) ÷ √N. It tests the reliability of the value of r.

# SECTION B – 5 MARKS

## Q2.
Classification is done on four main bases:
1. **Geographical classification:** data grouped by place or region (for example sales by state).
2. **Chronological classification:** data grouped by time (for example production year by year).
3. **Qualitative classification:** data grouped by an attribute or quality (for example sex, literacy).
4. **Quantitative classification:** data grouped by a measurable characteristic (for example height, income).

## Q3.
The main methods of collecting primary data are:
1. **Direct personal investigation:** the investigator collects data personally from the informants.
2. **Indirect oral investigation:** information is taken from third parties who know the facts.
3. **Information through local agents or correspondents:** agents in the field send the data regularly.
4. **Mailed questionnaire:** a questionnaire is mailed to informants, who fill and return it.
5. **Schedule sent through enumerators:** trained enumerators visit informants and fill the schedule.

## Q4.
| x | f | cf |
|---|---|---|
| 10 | 5 | 5 |
| 20 | 8 | 13 |
| 30 | 12 | 25 |
| 40 | 20 | 45 |
| 50 | 22 | 67 |
| 60 | 12 | 79 |
| | **Σf = N = 79** | |

Q1 = size of (N+1)/4 th item = 80/4 = 20th item → falls in cf, so **Q1 = 30**.

Q3 = size of 3(N+1)/4 th item = 60th item → falls in cf, so **Q3 = 50**.

Quartile deviation = (Q3 − Q1) / 2 = (50 − 30) / 2 = **10**

Coefficient of QD = (Q3 − Q1)/(Q3 + Q1) = 20/80 = **0.25**

## Q5.
| x | log x |
|---|---|
| 2 | 0.3010 |
| 4 | 0.6021 |
| 8 | 0.9031 |
| 16 | 1.2041 |
| 32 | 1.5051 |
| **n = 5** | **Σ log x = 4.5154** |

GM = Antilog(Σ log x / n) = Antilog(4.5154 / 5) = Antilog 0.9031 = **8.00**

## Q6.
Data: 25, 60, 33, 20, 47, 38.

Range = L − S = 60 − 20 = **40**

Coefficient of range = (L − S)/(L + S) = 40/80 = **0.5**

## Q7.
N = 10, x̄ = 20, ȳ = 15, Σdx² = 200, Σdy² = 50, Σdxdy = 80

byx = Σdxdy/Σdx² = 80/200 = **0.4**;  bxy = Σdxdy/Σdy² = 80/50 = **1.6**

**y on x:** y − 15 = 0.4(x − 20) → **y = 0.4x + 7**

**x on y:** x − 20 = 1.6(y − 15) → **x = 1.6y − 4**

When x = 25: y = 0.4(25) + 7 = **17**

## Q8.
| x | x − x̄ | (x − x̄)² |
|---|---|---|
| 10 | -20 | 400 |
| 20 | -10 | 100 |
| 30 | 0 | 0 |
| 40 | 10 | 100 |
| 50 | 20 | 400 |
| **Σx = 150** | | **Σ(x−x̄)² = 1000** |

Mean x̄ = Σx/n = 150/5 = **30**

σ = √(Σ(x−x̄)²/n) = √(1000/5) = √200 = **14.14**

## Q9.
**Frequency distribution of the given data**

| Class | Frequency |
|---|---|
| 0 – 10 | 4 |
| 10 – 20 | 9 |
| 20 – 30 | 10 |
| 30 – 40 | 6 |
| 40 – 50 | 1 |
| **Total** | **30** |

# SECTION C – 10 MARKS

## Q10.
A = 25, c = 10, d' = (x − A)/c

| CI | f | x | d' | fd' | cf |
|---|---|---|---|---|---|
| 0–10 | 5 | 5 | -2 | -10 | 5 |
| 10–20 | 8 | 15 | -1 | -8 | 13 |
| 20–30 | 15 | 25 | 0 | 0 | 28 |
| 30–40 | 12 | 35 | 1 | 12 | 40 |
| 40–50 | 7 | 45 | 2 | 14 | 47 |
| 50–60 | 3 | 55 | 3 | 9 | 50 |
| | **N = 50** | | | **Σfd' = 17** | |

**Mean** = A + (Σfd'/N)×c = 25 + (17/50)×10 = **28.40**

**Median:** N/2 = 25th item → class 20–30. Median = 20 + (25 − 13)/15 × 10 = **28.00**

**Mode:** modal class 20–30. Mode = 20 + (15−8)/(2×15−8−12) × 10 = **27.00**

**Mean = 28.40, Median = 28.00, Mode = 27.00**

## Q11.
A = 25, c = 10, d' = (x − A)/c

| CI | f | x | d' | fd' | fd'² |
|---|---|---|---|---|---|
| 0–10 | 4 | 5 | -2 | -8 | 16 |
| 10–20 | 10 | 15 | -1 | -10 | 10 |
| 20–30 | 16 | 25 | 0 | 0 | 0 |
| 30–40 | 12 | 35 | 1 | 12 | 12 |
| 40–50 | 8 | 45 | 2 | 16 | 32 |
| | **N = 50** | | | **Σfd' = 10** | **Σfd'² = 70** |

**σ** = √(Σfd'²/N − (Σfd'/N)²) × c = √(70/50 − (10/50)²) × 10 = **11.66**

**Mean** = 25 + (10/50)×10 = **27.00**

**CV** = (σ/x̄)×100 = (11.66/27.00)×100 = **43.19%**

## Q12.
x̄ = 90/6 = 15, ȳ = 161/6 = 26.8333; x = X−x̄, y = Y−ȳ

| X | Y | x | y | xy | x² | y² |
|---|---|---|---|---|---|---|
| 10 | 18 | -5 | -8.83333 | 44.17 | 25.00 | 78.03 |
| 12 | 24 | -3 | -2.83333 | 8.50 | 9.00 | 8.03 |
| 14 | 25 | -1 | -1.83333 | 1.83 | 1.00 | 3.36 |
| 16 | 30 | 1 | 3.16667 | 3.17 | 1.00 | 10.03 |
| 18 | 28 | 3 | 1.16667 | 3.50 | 9.00 | 1.36 |
| 20 | 36 | 5 | 9.16667 | 45.83 | 25.00 | 84.03 |
| **90** | **161** | | | **Σxy = 107.00** | **Σx² = 70.00** | **Σy² = 184.83** |

**r** = Σxy/√(Σx²·Σy²) = 107.00/√(70.00×184.83) = **0.941**

**PE** = 0.6745×(1 − r²)/√n = 0.6745×(1 − 0.885)/√6 = **0.0317**

r = 0.941 (high positive). r > 6 PE (0.1902), so it is significant.

## Q13.
x̄ = 6, ȳ = 8

| X | Y | x=X−x̄ | y=Y−ȳ | xy | x² | y² |
|---|---|---|---|---|---|---|
| 2 | 5 | -4 | -3 | 12 | 16 | 9 |
| 4 | 7 | -2 | -1 | 2 | 4 | 1 |
| 6 | 9 | 0 | 1 | 0 | 0 | 1 |
| 8 | 8 | 2 | 0 | 0 | 4 | 0 |
| 10 | 11 | 4 | 3 | 12 | 16 | 9 |
| **30** | **40** | | | **Σxy = 26** | **Σx² = 40** | **Σy² = 20** |

byx = Σxy/Σx² = 26/40 = **0.65**;  bxy = Σxy/Σy² = 26/20 = **1.30**

**y on x:** y − 8 = 0.65(x − 6) → **y = 0.65x + 4.10**

**x on y:** x − 6 = 1.30(y − 8) → **x = 1.30y − 4.40**

Estimate of y when x = 12: y = 0.65(12) + 4.10 = **11.90**

## Q14.
| CI | f | cf |
|---|---|---|
| 0–10 | 6 | 6 |
| 10–20 | 10 | 16 |
| 20–30 | 18 | 34 |
| 30–40 | 14 | 48 |
| 40–50 | 8 | 56 |
| 50–60 | 4 | 60 |
| | **N = 60** | |

**Q1:** N/4 = 15th item → class 10–20. Q1 = 10 + (15 − 6)/10 × 10 = **19.00**

**Q3:** 3N/4 = 45th item → class 30–40. Q3 = 30 + (45 − 34)/14 × 10 = **37.86**

Quartile deviation = (Q3 − Q1)/2 = (37.86 − 19.00)/2 = **9.43**

Coefficient of QD = (Q3 − Q1)/(Q3 + Q1) = **0.332**

