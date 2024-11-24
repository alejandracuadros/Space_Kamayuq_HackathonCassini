# Space Kamayuq: Satellite Collision Risk Assessment and Maneuver Planning

## Overview

**Space Kamayuq** is a cutting-edge solution designed to address the growing risk of satellite collisions with space debris. By leveraging Conjunction Data Messages (CDMs), our platform empowers satellite operators with actionable insights to enhance satellite safety, mission continuity, and orbital sustainability.

Through the integration of European Space technologies, Space Kamayuq not only identifies collision risks but also refines trajectory predictions and optimizes maneuver strategies, ensuring uninterrupted satellite operations.

---

## 💡 Idea

Space Kamayuq addresses the escalating risk of satellite collisions with space debris. Leveraging Conjunction Data Messages (CDMs), our system analyzes collision risks, predicts potential impacts, and provides operators with actionable insights for maneuver planning. This empowers satellite operators to make data-driven decisions, ensuring satellite safety, mission continuity, and orbital sustainability.

---

## 🛰️ EU Space Technologies

We integrate CDM data with Copernicus Earth Observation data and Galileo positioning signals to enhance collision prevention.

- **CDM ESA Data**: Identifies conjunction risks and calculates collision probabilities.
- **Copernicus**: Provides environmental context, such as atmospheric drag, to improve trajectory predictions (for future analysis once launched the project).
- **Galileo**: Delivers high-precision positioning for accurate satellite maneuvers (for future analysis once launched the project).

Together, these technologies optimize risk assessments, refine maneuver strategies, and minimize operational disruptions caused by space debris.

---

## 🚀 EU Space for Defence and Security

Space Kamayuq directly addresses the **Orbital Security – Navigating the Collision Frontier** challenge by improving Space Situational Awareness (SSA). Our solution ensures uninterrupted satellite operations, protects critical orbital infrastructure, and strengthens the EU’s Defence and Security ecosystem by mitigating risks from space debris and traffic congestion.

---

## 👽 Team

- **Alejandra Cuadros** (Coordinator): Industrial Engineer pursuing an MSc in Computer Science, Data Science, AI, and Quantum Computing at BME. She brings expertise in data processing, analysis, and visualization, combined with a strong understanding of business strategy and project management.  
  Email: [acuadrosr18@gmail.com](mailto:acuadrosr18@gmail.com)

- **Matheo Gómez**: Mechatronic Engineer currently pursuing an MSc in Autonomous Vehicles Control Engineering at BME. He contributes expertise in control systems and optimization for satellite maneuver planning and innovative solutions for satellite operations.  
  Email: [gomezcornejo.98@gmail.com](mailto:gomezcornejo.98@gmail.com)

- **Altynjemal Taganova**: Computer Science Bachelor student at BME with strong skills in software development and technical implementation, ensuring a seamless and functional platform.  
  Email: [taganovaaltynjemal@gmail.com](mailto:taganovaaltynjemal@gmail.com)

---

## 🔍 Features

1. **Collision Risk Analysis**:
   - Parses CDM data to calculate collision risks based on proximity and probability of collision.

2. **Risk Level Categorization**:
   - Classifies risks into `ALERT`, `WARNING`, or `SAFE` categories using configurable thresholds.

3. **Data Integration**:
   - Combines data from CSPOC, CAESAR_TRJ, and CAESAR_ALM CDMs for comprehensive analysis.

4. **Visualization**:
   - Generates visual reports for satellite operators to make informed decisions.

---

## 🧑‍💻 Code Features

### 1. **Data Parsing and Cleaning**:
The system parses XML and CSV data from multiple CDM sources:
- Extracts key metrics such as `TCA`, `Miss Distance`, and `Radial Distance`.
- Normalizes and cleans data for consistency.

### 2. **Reliability Assessment**:
- Assigns a `Reliability Score` to CDM entries based on normalized `Miss Distance`, `Relative Speed`, and creation date.

### 3. **Risk Level Determination**:
Classifies risks using thresholds:
- **ALERT**:
  - `TCA ≤ 7 days`
  - `Miss Distance < 5 km` and `Radial Distance < 500 m` or `PoC > 1E-5`.
- **WARNING**:
  - `TCA ≤ 7 days`
  - `Miss Distance < 10 km` or `PoC > 1E-6`.

### 4. **File Outputs**:
- Saves results for:
  - Most reliable entries.
  - Risk levels for each entry.
  - Comprehensive analysis.

---

## 📂 File Structure

```plaintext
/
|-- data/                        # Folder containing the raw CDM data files
|-- scripts/                     # Python scripts for parsing, analysis, and risk assessment
|-- outputs/                     # Results and CSV exports
|-- README.md                    # Project documentation (this file)
|-- requirements.txt             # Python dependencies

