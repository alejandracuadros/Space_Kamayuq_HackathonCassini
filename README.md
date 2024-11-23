# Hackathon Cassini
## CMD by:
    - The CAESAR_TRJ_12.xml is an O/O vs US CDM from CAESAR
    - The CSPOC_9.xml is an O/O vs HAC from CSPOC

## Analysis Framework
1. Determine Risk Level :

    Using the TCA from the CDMs and comparing with thresholds:
    - **ALERT Threshold** :
        - Time of Closest Approach <= 7 days.
        - Miss Distance < 5 km and Radial Distance < 500 m, or Probability of Collision > 1E-5.
    - WARNING Threshold :
        - Time of Closest Approach <= 7 days.
        - Miss Distance < 10 km or Probability of Collision > 1E-6.

2. Assess Secondary Object :
    - Identify details about the secondary object from the CDMs (if available).
    - If missing, infer based on context provided in the cheat sheet (eg, object type or behavior).

3. Formulate Recommendations :

    Based on risk levels, suggest:
    - No action (SAFE).
    - Monitor (WARNING).
    - Take action (ALERT).