import pandas as pd

# Load data
route_legs = pd.read_csv("data/raw/routes_legs.csv")
vessels = pd.read_csv("data/raw/vessel_profiles.csv")

results = []

for _, leg in route_legs.iterrows():
    for _, vessel in vessels.iterrows():

        speed_knots = vessel["speed_knots"]
        consumption_mt_day = vessel["consumption_mt_day"]
        safety_reserve_pct = vessel["safety_reserve_pct"]

        # 1 knot = 1 nautical mile per hour
        daily_distance_nm = speed_knots * 24

        # Days needed for this leg
        voyage_days = leg["distance_nm"] / daily_distance_nm

        # Fuel needed without reserve
        fuel_needed_mt = voyage_days * consumption_mt_day

        # Fuel needed with safety reserve
        fuel_required_with_reserve_mt = fuel_needed_mt * (1 + safety_reserve_pct)

        results.append({
            "route_id": leg["route_id"],
            "leg_order": leg["leg_order"],
            "from_port": leg["from_port"],
            "to_port": leg["to_port"],
            "distance_nm": leg["distance_nm"],
            "vessel_type": vessel["vessel_type"],
            "speed_knots": speed_knots,
            "voyage_days": round(voyage_days, 2),
            "fuel_needed_mt": round(fuel_needed_mt, 2),
            "fuel_required_with_reserve_mt": round(fuel_required_with_reserve_mt, 2),
        })

fuel_needs = pd.DataFrame(results)

# Save output
fuel_needs.to_csv("data/raw/fuel_needs_by_leg.csv", index=False)

print(fuel_needs.head(20))
print("\nSaved file: data/raw/fuel_needs_by_leg.csv")