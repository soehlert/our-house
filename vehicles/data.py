# vehicles/data.py

# A mapping of makes to models. In a real-world application, this data would
# likely come from a database or a more robust external API.
MAKE_MODELS = {
    "Acura": sorted(["Integra", "MDX", "RDX", "TLX"]),
    "Audi": sorted(["A3", "A4", "A5", "A6", "A7", "A8", "Q3", "Q5", "Q7", "Q8", "e-tron"]),
    "BMW": sorted(["2 Series", "3 Series", "4 Series", "5 Series", "7 Series", "8 Series", "i4", "iX", "X1", "X3", "X5", "X7", "Z4"]),
    "Buick": sorted(["Encore", "Encore GX", "Envision", "Enclave", "Regal", "LaCrosse"]),
    "Cadillac": sorted(["CT4", "CT5", "Escalade", "Lyriq", "XT4", "XT5", "XT6"]),
    "Chevrolet": sorted([
        "Astro", "Avalanche", "Aveo", "Beretta", "Blazer", "Bolt EV", "C1500", "Camaro", "Caprice",
        "Cavalier", "Celebrity", "Chevelle", "Citation", "Cobalt", "Colorado", "Corsica", "Corvette",
        "Cruze", "El Camino", "Equinox", "Express", "HHR", "Impala", "Lumina", "Malibu", "Monte Carlo",
        "Nova", "S-10", "Silverado", "Silverado 1500", "Silverado 2500HD", "Sonic", "Spark", "Suburban",
        "Tahoe", "Trailblazer", "Traverse", "Trax", "Vega", "Volt"
    ]),
    "Chrysler": sorted(["300", "Aspen", "Concorde", "Crossfire", "LeBaron", "LHS", "New Yorker", "Pacifica", "PT Cruiser", "Sebring", "Town & Country", "Voyager"]),
    "Dodge": sorted(["Avenger", "Caliber", "Caravan", "Challenger", "Charger", "Dakota", "Dart", "Durango", "Grand Caravan", "Hornet", "Intrepid", "Journey", "Magnum", "Neon", "Nitro", "Ram 1500", "Ram 2500", "Spirit", "Stratus", "Viper"]),
    "FIAT": sorted(["124 Spider", "500", "500L", "500X"]),
    "Ford": sorted([
        "Aerostar", "Bronco", "Bronco II", "C-Max", "Contour", "Crown Victoria", "E-Series", "EcoSport",
        "Edge", "Escape", "Escort", "Excursion", "Expedition", "Explorer", "F-150", "F-250", "F-350",
        "Fairmont", "Festiva", "Fiesta", "Five Hundred", "Flex", "Focus", "Freestar", "Freestyle",
        "Fusion", "Granada", "LTD", "Maverick", "Mustang", "Mustang Mach-E", "Pinto", "Probe", "Ranger",
        "Taurus", "Taurus X", "Tempo", "Thunderbird", "Transit", "Windstar"
    ]),
    "GMC": sorted(["Acadia", "Canyon", "Envoy", "Hummer EV", "Jimmy", "Safari", "Sierra 1500", "Sierra 2500HD", "Sonoma", "Syclone", "Terrain", "Typhoon", "Yukon"]),
    "Genesis": sorted(["G70", "G80", "G90", "GV60", "GV70", "GV80"]),
    "Honda": sorted(["Accord", "Civic", "CR-V", "CR-Z", "Clarity", "Crosstour", "Del Sol", "Element", "Fit", "HR-V", "Insight", "Odyssey", "Passport", "Pilot", "Prelude", "Ridgeline", "S2000"]),
    "Hyundai": sorted(["Accent", "Azera", "Elantra", "Entourage", "Equus", "Genesis", "Ioniq", "Kona", "Nexo", "Palisade", "Santa Cruz", "Santa Fe", "Sonata", "Tiburon", "Tucson", "Veloster", "Venue", "Veracruz", "XG350"]),
    "Infiniti": sorted(["EX35", "FX35", "G35", "G37", "I30", "I35", "M35", "M45", "Q45", "Q50", "QX4", "QX50", "QX55", "QX60", "QX70", "QX80"]),
    "Jaguar": sorted(["E-Pace", "F-Pace", "F-Type", "I-Pace", "S-Type", "X-Type", "XF", "XJ", "XK"]),
    "Jeep": sorted(["Cherokee", "Commander", "Compass", "Gladiator", "Grand Cherokee", "Liberty", "Patriot", "Renegade", "Wagoneer", "Wrangler"]),
    "Kia": sorted(["Amanti", "Borrego", "Cadenza", "Carnival", "EV6", "Forte", "K5", "K900", "Niro", "Optima", "Rio", "Rondo", "Sedona", "Seltos", "Sorento", "Soul", "Spectra", "Sportage", "Stinger", "Telluride"]),
    "Land Rover": sorted(["Defender", "Discovery", "Discovery Sport", "LR2", "LR3", "LR4", "Range Rover", "Range Rover Evoque", "Range Rover Sport", "Range Rover Velar"]),
    "Lexus": sorted(["CT", "ES", "GS", "GX", "HS", "IS", "LC", "LFA", "LS", "LX", "NX", "RC", "RX", "RZ", "SC", "UX"]),
    "Lincoln": sorted(["Aviator", "Blackwood", "Continental", "Corsair", "LS", "Mark LT", "Mark VII", "Mark VIII", "MKC", "MKS", "MKT", "MKX", "MKZ", "Nautilus", "Navigator", "Town Car", "Zephyr"]),
    "Mazda": sorted(["3", "5", "6", "626", "929", "B-Series", "CX-3", "CX-30", "CX-5", "CX-50", "CX-7", "CX-9", "MX-3", "MX-5 Miata", "MX-6", "Millenia", "MPV", "Protege", "RX-7", "RX-8", "Tribute"]),
    "Mercedes-Benz": sorted([
        "A-Class", "C-Class", "CL-Class", "CLA-Class", "CLK-Class", "CLS-Class", "E-Class", "G-Class",
        "GL-Class", "GLA-Class", "GLB-Class", "GLC-Class", "GLE-Class", "GLK-Class", "GLS-Class",
        "ML-Class", "R-Class", "S-Class", "SL-Class", "SLK-Class", "EQB", "EQE", "EQS", "Metris", "Sprinter"
    ]),
    "Mitsubishi": sorted(["3000GT", "Diamante", "Eclipse", "Eclipse Cross", "Endeavor", "Galant", "i-MiEV", "Lancer", "Lancer Evolution", "Mirage", "Montero", "Montero Sport", "Outlander", "Outlander Sport", "Raider"]),
    "Nissan": sorted(["240SX", "300ZX", "350Z", "370Z", "Altima", "Ariya", "Armada", "Cube", "Frontier", "GT-R", "Juke", "Kicks", "Leaf", "Maxima", "Murano", "NV200", "Pathfinder", "Quest", "Rogue", "Rogue Sport", "Sentra", "Titan", "Versa", "Xterra", "Z"]),
    "Porsche": sorted(["718 Boxster", "718 Cayman", "911", "928", "944", "968", "Boxster", "Carrera GT", "Cayenne", "Cayman", "Macan", "Panamera", "Taycan"]),
    "Ram": sorted(["1500", "2500", "3500", "ProMaster", "ProMaster City"]),
    "Rivian": sorted(["R1S", "R1T"]),
    "Rolls-Royce": sorted(["Cullinan", "Dawn", "Ghost", "Phantom", "Wraith"]),
    "Subaru": sorted(["Ascent", "B9 Tribeca", "Baja", "Brat", "BRZ", "Crosstrek", "Forester", "Impreza", "Justy", "Legacy", "Loyale", "Outback", "SVX", "Tribeca", "WRX", "XT"]),
    "Smart": sorted(["EQ Fortwo", "Fortwo"]),
    "Tesla": sorted(["Model 3", "Model S", "Model X", "Model Y", "Roadster"]),
    "Toyota": sorted([
        "4Runner", "86", "Avalon", "C-HR", "Camry", "Celica", "Corolla", "Corolla Cross", "Cressida", "Echo",
        "FJ Cruiser", "GR86", "Grand Highlander", "Highlander", "Land Cruiser", "Matrix", "Mirai", "MR2",
        "Paseo", "Previa", "Prius", "RAV4", "Sequoia", "Sienna", "Solara", "Supra", "T100", "Tacoma",
        "Tercel", "Tundra", "Venza", "Yaris"
    ]),
    "Volkswagen": sorted(["Arteon", "Atlas", "Atlas Cross Sport", "Beetle", "Cabrio", "CC", "Corrado", "Eos", "EuroVan", "Fox", "GLI", "Golf", "Golf R", "GTI", "ID.4", "Jetta", "Passat", "Phaeton", "Quantum", "Rabbit", "Routan", "Scirocco", "Taos", "Tiguan", "Touareg"]),
    "Volvo": sorted(["C30", "C40 Recharge", "C70", "EX30", "EX90", "S40", "S60", "S70", "S80", "S90", "V40", "V50", "V60", "V70", "V90", "XC40", "XC60", "XC70", "XC90"]),
}