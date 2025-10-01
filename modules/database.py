"""
Database Module
Handles loading and managing mineral data from Excel
"""

import pandas as pd
import json
import os
from datetime import datetime
import uuid


class MineralDatabase:
    """Manage mineral database operations"""
    
    def __init__(self):
        """Initialize database"""
        self.data_dir = 'data'
        self.excel_file = os.path.join(self.data_dir, 'Example of Critical Minerals in Africa.xlsx')
        self.minerals_file = os.path.join(self.data_dir, 'minerals.json')
        self.deposits_file = os.path.join(self.data_dir, 'deposits.json')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load Excel data on initialization
        self.load_excel_data()
    
    def load_excel_data(self):
        """Load data from Excel file and convert to JSON"""
        print("Loading Excel data...")
        
        if not os.path.exists(self.excel_file):
            print(f"Warning: Excel file not found at {self.excel_file}")
            self.create_empty_json_files()
            return
        
        try:
            # Read Excel file
            df = pd.read_excel(self.excel_file, sheet_name='Provide a list of all critical ')
            
            print(f"Loaded {len(df)} minerals from Excel")
            
            # Convert to our format
            minerals_data = []
            
            for index, row in df.iterrows():
                mineral_name = row['Critical Mineral']
                countries_str = row['Primary African Producing Countries']
                uses = row['Key Uses (Criticality)']
                
                # Parse countries (split by comma)
                countries = [c.strip() for c in countries_str.split(',')]
                
                # Create a record for each country
                for country in countries:
                    # Clean country name (remove parenthetical notes)
                    clean_country = country.split('(')[0].strip()
                    
                    mineral_record = {
                        'id': str(uuid.uuid4()),
                        'mineral_name': mineral_name,
                        'country': clean_country,
                        'uses': uses,
                        'year': 2024,  # Current year
                        'production_volume': self.estimate_production(mineral_name, clean_country),
                        'reserves': self.estimate_reserves(mineral_name, clean_country),
                        'price': self.estimate_price(mineral_name),
                        'unit': 'tonnes',
                        'created_at': datetime.now().isoformat()
                    }
                    
                    minerals_data.append(mineral_record)
            
            # Save to JSON
            with open(self.minerals_file, 'w') as f:
                json.dump(minerals_data, f, indent=4)
            
            print(f"✓ Converted to {len(minerals_data)} mineral records")
            
            # Create sample deposits
            self.create_sample_deposits(df)
            
        except Exception as e:
            print(f"Error loading Excel: {e}")
            self.create_empty_json_files()
    
    def estimate_production(self, mineral, country):
        """Estimate production volumes based on mineral and country"""
        # Rough estimates based on known data
        production_data = {
            'Cobalt': {'DRC': 130000, 'Zambia': 5000, 'Morocco': 2000},
            'Manganese': {'South Africa': 6200000, 'Gabon': 7000000, 'Ghana': 500000},
            'Lithium': {'Zimbabwe': 1200, 'DRC': 800, 'Mali': 300},
            'Copper': {'DRC': 1500000, 'Zambia': 800000, 'South Africa': 50000},
            'Graphite (Natural)': {'Mozambique': 30000, 'Madagascar': 50000, 'Tanzania': 15000},
            'Chromium': {'South Africa': 18000000, 'Zimbabwe': 900000},
        }
        
        # Get production or use default
        if mineral in production_data and country in production_data[mineral]:
            return production_data[mineral][country]
        
        # Default values
        return 10000
    
    def estimate_reserves(self, mineral, country):
        """Estimate reserves"""
        # Multiply production by 50-100 years typically
        production = self.estimate_production(mineral, country)
        return production * 75  # 75 years of reserves
    
    def estimate_price(self, mineral):
        """Estimate prices per tonne in USD"""
        prices = {
            'Cobalt': 32000,
            'Platinum-Group Metals (PGMs)': 850000,  # Very expensive
            'Manganese': 1800,
            'Bauxite (for Aluminum)': 50,
            'Graphite (Natural)': 1200,
            'Lithium': 25000,
            'Copper': 8500,
            'Nickel': 18000,
            'Chromium': 450,
            'Uranium': 140000,
            'Rare Earth Elements (REEs)': 75000
        }
        
        return prices.get(mineral, 5000)
    
    def create_sample_deposits(self, df):
        """Create sample deposit locations"""
        deposits = []
        
        # Coordinates for major African countries
        country_coords = {
            'DRC': {'lat': -4.0, 'lon': 23.0},
            'South Africa': {'lat': -29.0, 'lon': 25.0},
            'Zimbabwe': {'lat': -19.0, 'lon': 29.8},
            'Zambia': {'lat': -13.1, 'lon': 27.8},
            'Mozambique': {'lat': -18.6, 'lon': 35.5},
            'Madagascar': {'lat': -19.0, 'lon': 46.3},
            'Tanzania': {'lat': -6.3, 'lon': 34.8},
            'Ghana': {'lat': 7.9, 'lon': -1.0},
            'Guinea': {'lat': 9.9, 'lon': -9.6},
            'Namibia': {'lat': -22.5, 'lon': 17.0},
            'Gabon': {'lat': -0.8, 'lon': 11.6},
            'Niger': {'lat': 17.6, 'lon': 8.0},
            'Morocco': {'lat': 31.7, 'lon': -7.0},
        }
        
        for index, row in df.iterrows():
            mineral = row['Critical Mineral']
            countries_str = row['Primary African Producing Countries']
            
            # Get first country for deposit location
            first_country = countries_str.split(',')[0].split('(')[0].strip()
            
            if first_country in country_coords:
                coords = country_coords[first_country]
                
                deposit = {
                    'id': str(uuid.uuid4()),
                    'mineral': mineral,
                    'location_name': f'{mineral} Deposit - {first_country}',
                    'country': first_country,
                    'latitude': coords['lat'],
                    'longitude': coords['lon'],
                    'reserves': self.estimate_reserves(mineral, first_country),
                    'annual_production': self.estimate_production(mineral, first_country),
                    'status': 'Active'
                }
                
                deposits.append(deposit)
        
        # Save deposits
        with open(self.deposits_file, 'w') as f:
            json.dump(deposits, f, indent=4)
        
        print(f"✓ Created {len(deposits)} deposit locations")
    
    def create_empty_json_files(self):
        """Create empty JSON files if Excel not found"""
        for file_path in [self.minerals_file, self.deposits_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    # ========================================================================
    # QUERY METHODS
    # ========================================================================
    
    def load_json(self, file_path):
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return []
    
    def get_all_minerals(self):
        """Get all mineral records"""
        return self.load_json(self.minerals_file)
    
    def get_unique_mineral_names(self):
        """Get list of unique mineral names"""
        minerals = self.get_all_minerals()
        unique = sorted(list(set(m['mineral_name'] for m in minerals)))
        return unique
    
    def get_unique_countries(self):
        """Get list of unique countries"""
        minerals = self.get_all_minerals()
        unique = sorted(list(set(m['country'] for m in minerals)))
        return unique
    
    def search_minerals(self, filters=None):
        """Search minerals with filters"""
        minerals = self.get_all_minerals()
        
        if not filters:
            return minerals
        
        results = []
        
        for mineral in minerals:
            match = True
            
            # Filter by mineral name
            if 'mineral_name' in filters and filters['mineral_name']:
                if mineral['mineral_name'].lower() != filters['mineral_name'].lower():
                    match = False
            
            # Filter by country
            if 'country' in filters and filters['country']:
                if mineral['country'].lower() != filters['country'].lower():
                    match = False
            
            if match:
                results.append(mineral)
        
        return results
    
    def get_minerals_by_country(self, country):
        """Get all minerals for a specific country"""
        return self.search_minerals({'country': country})
    
    def get_deposits(self, mineral=None, country=None):
        """Get deposits with optional filters"""
        deposits = self.load_json(self.deposits_file)
        
        if not mineral and not country:
            return deposits
        
        results = []
        for deposit in deposits:
            match = True
            
            if mineral and deposit['mineral'].lower() != mineral.lower():
                match = False
            
            if country and deposit['country'].lower() != country.lower():
                match = False
            
            if match:
                results.append(deposit)
        
        return results
    
    def count_minerals(self):
        """Count total mineral records"""
        return len(self.get_all_minerals())
    
    def count_countries(self):
        """Count unique countries"""
        return len(self.get_unique_countries())
    
    def count_deposits(self):
        """Count deposits"""
        return len(self.load_json(self.deposits_file))


# Test the module
if __name__ == '__main__':
    print("Testing Database Module...")
    print("=" * 70)
    
    db = MineralDatabase()
    
    print("\n1. Unique Minerals:")
    minerals = db.get_unique_mineral_names()
    for i, m in enumerate(minerals, 1):
        print(f"   {i}. {m}")
    
    print(f"\n2. Total Records: {db.count_minerals()}")
    print(f"3. Total Countries: {db.count_countries()}")
    print(f"4. Total Deposits: {db.count_deposits()}")
    
    print("\n4. Sample Search - Cobalt:")
    cobalt = db.search_minerals({'mineral_name': 'Cobalt'})
    for record in cobalt[:3]:  # Show first 3
        print(f"   - {record['country']}: {record['production_volume']:,} tonnes")
    
    print("\n5. Deposits in South Africa:")
    sa_deposits = db.get_deposits(country='South Africa')
    print(f"   Found {len(sa_deposits)} deposits")
    
    print("\n✓ Database module working!")