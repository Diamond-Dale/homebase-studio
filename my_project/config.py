from __future__ import annotations

FIELDS = {
    "Science": {
        "niches": {
            "Space & Physics": {
                "concepts": [
                    {"term": "Escape Velocity", "definition": "the minimum speed needed for an object to break free from a planet's gravitational pull without further propulsion.", 
                     "example": "From Earth, escape velocity is about 11.2 km/s; rockets stage their burns to effectively exceed this using sustained thrust rather than a single instantaneous push.",
                     "counter": "Low-thrust ion engines cannot deliver escape velocity instantaneously but still achieve escape via continuous acceleration."},
                    {"term": "Redshift", "definition": "the stretching of light to longer wavelengths due to recession velocity or gravitational effects.", 
                     "example": "Distant galaxies in the Hubble Ultra Deep Field show spectral lines shifted toward red, indicating the universe's expansion.",
                     "counter": "Peculiar velocities can mimic small redshifts locally, so cosmological redshift is confirmed statistically across many sources."},
                    {"term": "Dark Matter", "definition": "an unseen mass component inferred from gravitational effects on galaxies and clusters.", 
                     "example": "Galaxy rotation curves remain flat at large radii, inconsistent with visible mass alone.",
                     "counter": "Modified gravity models attempt to explain rotation curves, but struggle with cluster-scale lensing and CMB observations."}
                ]
            }
        }
    },
    "Finance": {
        "niches": {
            "Personal Finance": {
                "concepts": [
                    {"term": "Dollar-Cost Averaging", "definition": "investing a fixed amount at regular intervals regardless of price to reduce timing risk.", 
                     "example": "Contributing $500 monthly into a broad-market index fund smooths entry points across market cycles.",
                     "counter": "Lump-sum investing often has higher expected returns when markets trend upward, but carries more timing risk."},
                    {"term": "Emergency Fund", "definition": "liquid savings covering 3–6 months of expenses for unexpected events.", 
                     "example": "If monthly expenses are $3,000, target an $9,000–$18,000 reserve in a high-yield savings account.",
                     "counter": "Holding too much cash can erode purchasing power; tiers (cash + short-term T‑bills) balance liquidity and yield."},
                    {"term": "Tax-Advantaged Accounts", "definition": "accounts that defer or reduce taxes to compound wealth more efficiently.", 
                     "example": "Maxing a Roth IRA allows tax-free qualified withdrawals later; an HSA combines health spending with triple tax benefits.",
                     "counter": "Contribution limits and income phase-outs require planning; high-fee funds can negate tax benefits."}
                ]
            }
        }
    }
}

PRICING_PER_1K = {
    "gpt-5": {"input": 5.00, "output": 15.00},
    "gpt-5-mini": {"input": 0.60, "output": 2.40},
    "fallback": {"input": 0.00, "output": 0.00},
}

DEFAULT_IMAGE_SIZE = (1280, 720)
DEFAULT_FPS = 24
