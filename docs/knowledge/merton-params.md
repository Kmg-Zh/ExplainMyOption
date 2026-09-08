# Merton (1976) default jump parameters

## Takeaway

When a vol surface fit is skipped or fails, LSM-Merton and the European Merton series use frozen typical-equity defaults from Merton (1976), flagged `merton_params_defaulted`.

## Details

```text
λ  (jump_intensity) = 0.5   jumps per year
μ_J (jump_mean)      = −0.10  mean of log jump size
δ  (jump_vol)        = 0.15   jump-size standard deviation
```

Compensation: `k = exp(μ_J + ½ δ²) − 1`. The diffusion drift uses `r − q − λk`.

Cheap calibration (when a surface exists): 1-parameter λ grid vs the contract's European BS price; revert to defaults if the error is large.

American Merton is **numpy LSM**, not QuantLib `MCAmericanEngine` (that engine is BS-only). There is **no** in-repo American Merton PIDE.

## Source

- Merton, R. C. (1976), *Option pricing when underlying stock returns are discontinuous*.
- `src/pricing/config.py` · `src/pricing/engines/lsm.py` · `src/pricing/engines/merton.py`
