def cleanDataFrame(df):
    df = cleanColNames(df.copy(), ncol={"CUSTOMER": "customer_id", "ST":"state", "Customer Lifetime Value":"lifetime_value", "Monthly Premium Auto":"monthly_premium_fee", "Number of Open Complaints":"open_complaints"})
    df = cleanInvvalidValues(df.copy())
    df = setDTypes(df.copy())
    df = cleanNullValues(df.copy())
    df = cleanDuplicated(df.copy())

    return df.copy()

def cleanColNames(df, ncol={}):
    df.columns = [ncol[column] if (column in ncol) else (column.lower().replace(" ", "_")) for column in df.columns]

    return df

def cleanInvvalidValues(df):
    df.loc[df["gender"].isin(["Femal", "female"]), "gender"] = "F"
    df.loc[df["gender"]=="Male", "gender"] = "M"
    df["state"] = df["state"].apply(lambda x: abbrev_to_us_state[x] if x in abbrev_to_us_state.keys() else x)
    df.loc[df["education"]=="Bachelors", "education"] = "Bachelor"
    df["lifetime_value"] = df["lifetime_value"].apply(lambda x: float(x.replace('%','')) if isinstance(x, str) else x)
    df.loc[df["vehicle_class"].isin(["Sports Car", "Luxury SUV", "Luxury Car"]), "vehicle_class"] = "Luxury"

    return df
    
def setDTypes(df):
    df["lifetime_value"] = df["lifetime_value"].astype("float64")
    df["open_complaints"] = df["open_complaints"].apply(lambda x: int(x.split("/")[1]) if isinstance(x, str) and "/" in x else x)

    return df

def cleanNullValues(df):
    df = df.dropna(axis=0, how="all")
    df["gender"] = df["gender"].bfill()
    df["lifetime_value"] = df["lifetime_value"].fillna(df["lifetime_value"].mean())

    return df

def cleanDuplicated(df):
    df.drop_duplicates(keep="first", inplace=True)
    df.reset_index(inplace=True)

    return df

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))