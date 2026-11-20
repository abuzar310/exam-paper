# Business Statistics formula notebook (text copy)

Typed from `page-01.jpg` to `page-06.jpg`, sent 19 November 2026. Wording and formulas follow the notebook. Abbreviations: **IS** individual series, **DS** discrete series, **CS** continuous series, **A** assumed mean, **C** class interval (common), **cf** cumulative frequency.

---

## Page 1 — Theory

### Module 1

- Meaning and definition of Statistics
- Nature
- Functions
- Scope
- Limitations

(2-mark certain; 1-mark theory important)

- **1M / 10M** Types of collection of data — primary, secondary
- **2M / 10M** Classification of data

### Module 2

No such theory is important.

- Define graphical representation
- Types of diagram (not important) — just to know. In college 13 Aug 2026
- All graphs (important)
- What is diagram

### Module 3

Define mean, median, mode, quartile.

### Module 4

Measure of dispersion

- Meaning
- Objective
- **1M** Type and methods of range
- Range
- Coefficient

---

## Page 2 — Problems

### Module 1

- Tabulation — 5M
- Blank table — 5M

### Module 2

- Percentage bar diagram with cf — 10M
- **or** subdivided bar diagram
- Ogive curve / histogram

### Module 3

- Mean, median, mode — 10M (continuous series)
- Geometric **or** harmonic mean — 5M (anyone pakka)
- Simple question on mean, median, mode (IS)

### Module 4

- Standard deviation and its coefficient — 10M
- Quartile deviation

### Module 5

- Karl Pearson's coefficient **or** probable error (anyone pakka)
- Regression (2M / 5M / 10M)

Also: properties of mean, mode; any difference between.

---

## Page 3 — Module 4: measure of dispersion

**Range** = L − S  L = largest, S = smallest

**Coefficient of range** = (L − S) / (L + S)

### Quartile deviation

Same as in last module for Q1, Q2, Q3.

**DS**

- QD = (Q3 − Q1) / 2
- Coefficient of QD = (Q3 − Q1) / (Q3 + Q1)

**CS**

- Q1 = L1 + ((N/4 − cf) / f) × C  Q1 = (N + 1) / 4
- Q3 = L1 + ((3(N/4) − cf) / f) × C  Q3 = 3(N + 1) / 4

### Standard deviation and coefficient of standard deviation

**IS, without uniformity**

σ = √[ Σd²/n − (Σd/n)² ]

**IS, with uniformity**

σ = √[ Σd²/n − (Σd/n)² ] × C

**DS and CS, without uniformity**

σ = √[ Σfd²/N − (Σfd/N)² ]

**DS and CS, with uniformity**

σ = √[ Σfd²/N − (Σfd/N)² ] × C

---

## Page 4 — Quartiles (CS), mode, GM, HM

**CS**

- Q1 = N/4
- Q3 = 3(N/4)
- Q1 = L1 + ((L2 − L1) / f) × (q1 − c)
- Q3 = L1 + ((L2 − L1) / f) × (q3 − c)

### Mode

If mean and median is already found:

Z = 3M − 2x̄

- **DS:** which frequency is higher, it is mode
- **CS:** L1 + ((f1 − f0) / (2f1 − f0 − f2)) × (L2 − L1)

### Easy formula for finding mean, median, mode

- Mean: x̄ = A + (Σfd' / N) × C
- Median: M = L1 + ((L2 − L1) / f) × (m − c)  (m = N/2)
- Mode: Z = 3M − 2x̄
- Ogive curve = median
- Histogram = mode

### Geometric mean

GM = Antilog (Σ log x / n)

### Harmonic mean

HM = n / Σ(1/x)

---

## Page 5 — Module 3: all formulas

Note at the top: &lt; 40 = 30–40, &gt; 40 = 40–50.

### Mean

- Individual series: x̄ = Σx / n
- Discrete or continuous series: x̄ = Σfx / N

### Deviation (shortcut method)

- IS: x̄ = A + Σd / n
- DS and CS: x̄ = A + Σfd / N

n = no. of items. N = total frequency.

### Step deviation method (shortcut method for GM or AM)

- IS: x̄ = A + (Σd' / n) × C
- CS and DS: x̄ = A + (Σfd' / N) × C
- d' = (x − A) / C
- A = assumed mean, C = common (class interval)

### Median

- Individual series: M = ((n + 1) / 2)th item
- DS: M = ((N + 1) / 2)th item
- CS, if f is given: M = L1 + ((L2 − L1) / f) × (m − c)

### Quartiles

DS and IS:

- Q1 = ((n + 1) / 4)th item
- Q2 = ((n + 1) / 2)th item
- Q3 = (3(n + 1) / 4)th item

DS also same but had to find cf.

---

## Page 6 — Coefficient of SD, CV, Module 5

**Coefficient of standard deviation** = σ / x̄  x̄ = Σx / n

**Coefficient of variation**

CV = (σ / x̄) × 100  x̄ = Σfx / N

### Module 5 — Correlation and regression analysis

r = Σxy / √(Σx² × Σy²)

- x̄ = Σx / n
- ȳ = Σy / n
- x = X − x̄
- y = Y − ȳ

**Probable error** = 0.6745 × (1 − r²) / √n

### Regression

When σ value not given:

- x on y: bxy = Σdx dy / Σdy²  x − x̄ = bxy (y − ȳ)
- y on x: byx = Σdx dy / Σdx²  (y − ȳ) = byx (x − x̄)

**Regression coefficient**

r = √(bxy × byx)

When σ value given:

- x on y: x − x̄ = r × (σx / σy) (y − ȳ)
- y − ȳ = r × (σy / σx) (x − x̄)
