import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define vehicle data
companies = ['Honda', 'Tata', 'Maruti', 'Hyundai', 'Toyota']
honda_models = ['Amaze', 'City', 'Civic', 'Jazz', 'WR-V', 'CR-V', 'Accord']
tata_models = ['Tiago', 'Nexon', 'Harrier', 'Safari', 'Altroz']
maruti_models = ['Swift', 'Baleno', 'Alto', 'WagonR', 'Dzire', 'Vitara Brezza']
hyundai_models = ['i10', 'i20', 'Creta', 'Venue', 'Verna', 'Tucson']
toyota_models = ['Innova', 'Fortuner', 'Glanza', 'Urban Cruiser', 'Camry']

model_mapping = {
    'Honda': honda_models,
    'Tata': tata_models,
    'Maruti': maruti_models,
    'Hyundai': hyundai_models,
    'Toyota': toyota_models
}

# Define service issues with realistic patterns
service_issues = [
    'Engine Oil Change',
    'Brake Pad Replacement',
    'Battery Replacement',
    'AC Gas Refill',
    'Tire Rotation',
    'Wheel Alignment',
    'Suspension Check',
    'Transmission Fluid Change',
    'Air Filter Replacement',
    'Fuel Filter Replacement',
    'Spark Plug Replacement',
    'Coolant Flush',
    'Power Steering Fluid Change',
    'Brake Fluid Change',
    'Timing Belt Replacement',
    'Clutch Replacement',
    'Shock Absorber Replacement',
    'Headlight Bulb Replacement',
    'Wiper Blade Replacement',
    'Exhaust System Repair'
]

def generate_service_record():
    """Generate a single service record with realistic patterns"""
    
    # Select company and model
    company = random.choice(companies)
    model = random.choice(model_mapping[company])
    
    # Generate year (2010-2023)
    year = random.randint(2010, 2023)
    current_year = 2024
    vehicle_age = current_year - year
    
    # Generate mileage based on age (realistic patterns)
    # Average 10,000-15,000 km per year
    avg_km_per_year = random.randint(8000, 18000)
    mileage = vehicle_age * avg_km_per_year + random.randint(-5000, 5000)
    mileage = max(0, mileage)  # Ensure non-negative
    
    # Determine service issues based on realistic patterns
    issues = []
    
    # Age-based issues
    if vehicle_age >= 5:
        if random.random() < 0.7:
            issues.append('Timing Belt Replacement')
        if random.random() < 0.5:
            issues.append('Clutch Replacement')
    
    if vehicle_age >= 3:
        if random.random() < 0.6:
            issues.append('Battery Replacement')
        if random.random() < 0.4:
            issues.append('Suspension Check')
    
    # Mileage-based issues
    if mileage > 80000:
        if random.random() < 0.8:
            issues.append('Transmission Fluid Change')
        if random.random() < 0.7:
            issues.append('Brake Pad Replacement')
    
    if mileage > 50000:
        if random.random() < 0.6:
            issues.append('Spark Plug Replacement')
        if random.random() < 0.5:
            issues.append('Coolant Flush')
    
    if mileage > 30000:
        if random.random() < 0.7:
            issues.append('Air Filter Replacement')
    
    # Common issues for all vehicles
    if random.random() < 0.8:
        issues.append('Engine Oil Change')
    
    if random.random() < 0.3:
        issues.append('Tire Rotation')
    
    if random.random() < 0.25:
        issues.append('Wheel Alignment')
    
    if random.random() < 0.2:
        issues.append('AC Gas Refill')
    
    if random.random() < 0.15:
        issues.append('Wiper Blade Replacement')
    
    # Company-specific patterns
    if company == 'Tata':
        if random.random() < 0.3:
            issues.append('Exhaust System Repair')
    
    if company == 'Maruti':
        if random.random() < 0.25:
            issues.append('Fuel Filter Replacement')
    
    # Ensure at least one issue
    if not issues:
        issues.append(random.choice(['Engine Oil Change', 'Air Filter Replacement', 'Tire Rotation']))
    
    # Remove duplicates and join
    issues = list(set(issues))
    issue_string = ', '.join(issues)
    
    return {
        'company': company,
        'model': model,
        'year': year,
        'vehicle_age': vehicle_age,
        'mileage': mileage,
        'service_issues': issue_string
    }

# Generate 1000 records
print("Generating 1000 service records...")
records = [generate_service_record() for _ in range(1000)]

# Create DataFrame
df = pd.DataFrame(records)

# Add some variety and edge cases
# Add some very old vehicles
for i in range(20):
    idx = random.randint(0, 999)
    df.loc[idx, 'year'] = random.randint(2005, 2009)
    df.loc[idx, 'vehicle_age'] = 2024 - df.loc[idx, 'year']
    df.loc[idx, 'mileage'] = df.loc[idx, 'vehicle_age'] * random.randint(12000, 20000)

# Add some brand new vehicles
for i in range(20):
    idx = random.randint(0, 999)
    df.loc[idx, 'year'] = random.randint(2023, 2024)
    df.loc[idx, 'vehicle_age'] = 2024 - df.loc[idx, 'year']
    df.loc[idx, 'mileage'] = random.randint(500, 15000)
    df.loc[idx, 'service_issues'] = 'Engine Oil Change'

# Save to CSV
df.to_csv('vehicle_service_history.csv', index=False)

print(f"\n✅ Dataset created successfully!")
print(f"Total records: {len(df)}")
print(f"\nDataset statistics:")
print(f"- Companies: {df['company'].unique()}")
print(f"- Year range: {df['year'].min()} - {df['year'].max()}")
print(f"- Age range: {df['vehicle_age'].min()} - {df['vehicle_age'].max()} years")
print(f"- Mileage range: {df['mileage'].min():.0f} - {df['mileage'].max():.0f} km")
print(f"- Unique service issues found: {len(set([issue.strip() for issues in df['service_issues'] for issue in issues.split(',')]))}")
print(f"\nFirst few records:")
print(df.head())
print(f"\nDataset saved as 'vehicle_service_history.csv'")