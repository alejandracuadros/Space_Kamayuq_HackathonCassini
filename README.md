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

2. Assess :
    - Identify details about the secondary object from the CDMs.
    - Who is the secondary object involved in the conjunction? 
    - What is the coordination plan?
    - How is the risk evolving through time until today?
    - Which CDM source seems to be the most reliable?

