"""
Create a mapping from Steam app IDs to game names.
This script processes the steam_games.json.gz file and creates a lightweight JSON mapping.
"""

import gzip
import json
import ast
from pathlib import Path

print("Creating game ID to name mapping...")

game_names = {}
count = 0
errors = 0

try:
    with gzip.open("../data/steam_games.json.gz", "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                # The file contains Python dict representations (not JSON)
                # Use ast.literal_eval to safely parse Python literals
                game = ast.literal_eval(line.strip())
                
                # Extract ID and name
                game_id = game.get('id') or game.get('app_id') or game.get('appid')
                game_name = game.get('app_name') or game.get('name') or game.get('title')
                
                if game_id and game_name:
                    game_names[str(game_id)] = game_name
                    count += 1
                    
                if (i + 1) % 1000 == 0:
                    print(f"  Processed {i + 1} games, found {count} with names...")
                    
            except (ValueError, SyntaxError):
                errors += 1
                if errors < 5:
                    print(f"  Warning: Could not parse line {i+1}")
            except Exception as e:
                errors += 1
                if errors < 5:
                    print(f"  Warning: Error processing line {i+1}: {e}")

except FileNotFoundError:
    print("Error: steam_games.json.gz not found in ../data/")
    print("Creating empty mapping file...")
    game_names = {}

# Save the mapping
output_file = "game_names.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(game_names, f, indent=2, ensure_ascii=False)

print(f"\n✓ Created {output_file}")
print(f"  Total games with names: {count}")
print(f"  Errors: {errors}")
print(f"  File size: {Path(output_file).stat().st_size / 1024:.1f} KB")

# Test with a few IDs
test_ids = ['218230', '205790', '10', '100']
print(f"\nTest lookups:")
for test_id in test_ids:
    name = game_names.get(test_id, f"Unknown (ID: {test_id})")
    print(f"  {test_id}: {name}")
