"""
Visualization Module
Handles interactive map generation using Folium
"""

import folium
from folium import plugins


class MapVisualization:
    """Generate interactive maps"""
    
    def __init__(self):
        """Initialize visualization"""
        self.mineral_colors = {
            'Cobalt': 'blue',
            'Platinum-Group Metals (PGMs)': 'purple',
            'Manganese': 'darkpurple',
            'Bauxite (for Aluminum)': 'lightgray',
            'Graphite (Natural)': 'gray',
            'Lithium': 'lightblue',
            'Copper': 'orange',
            'Nickel': 'green',
            'Chromium': 'darkgreen',
            'Uranium': 'red',
            'Rare Earth Elements (REEs)': 'pink'
        }
    
    def get_mineral_color(self, mineral):
        """Get color for mineral type"""
        return self.mineral_colors.get(mineral, 'gray')
    
    def generate_map(self, deposits):
        """Generate interactive Folium map with deposits"""
        
        # Create base map centered on Africa
        africa_map = folium.Map(
            location=[0.0, 20.0],  # Center of Africa
            zoom_start=3,
            tiles='OpenStreetMap',
            control_scale=True
        )
        
        # Add fullscreen button
        plugins.Fullscreen(
            position='topright',
            title='Enter Fullscreen',
            title_cancel='Exit Fullscreen',
            force_separate_button=True
        ).add_to(africa_map)
        
        # Add markers for each deposit
        for deposit in deposits:
            # Create popup content with styling
            popup_html = f"""
            <div style="width: 280px; font-family: Arial, sans-serif;">
                <h4 style="margin: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;">
                    <i class="fas fa-gem"></i> {deposit['mineral']}
                </h4>
                <table style="width: 100%; margin-top: 10px; font-size: 13px;">
                    <tr>
                        <td style="padding: 5px; font-weight: bold; width: 45%;">Location:</td>
                        <td style="padding: 5px;">{deposit['location_name']}</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 5px; font-weight: bold;">Country:</td>
                        <td style="padding: 5px;">{deposit['country']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; font-weight: bold;">Reserves:</td>
                        <td style="padding: 5px;">{deposit['reserves']:,} tonnes</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 5px; font-weight: bold;">Production:</td>
                        <td style="padding: 5px;">{deposit['annual_production']:,} tonnes/year</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; font-weight: bold;">Status:</td>
                        <td style="padding: 5px;">
                            <span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">
                                {deposit['status']}
                            </span>
                        </td>
                    </tr>
                </table>
            </div>
            """
            
            popup = folium.Popup(popup_html, max_width=300)
            
            # Get marker color based on mineral
            color = self.get_mineral_color(deposit['mineral'])
            
            # Add marker with custom icon
            folium.Marker(
                location=[deposit['latitude'], deposit['longitude']],
                popup=popup,
                tooltip=f"<b>{deposit['mineral']}</b><br>{deposit['location_name']}",
                icon=folium.Icon(
                    color=color,
                    icon='gem',
                    prefix='fa'
                )
            ).add_to(africa_map)
        
        # Add legend
        legend_html = self._create_legend()
        africa_map.get_root().html.add_child(folium.Element(legend_html))
        
        # Add mini map
        plugins.MiniMap(toggle_display=True).add_to(africa_map)
        
        # Add measurement tool
        plugins.MeasureControl(
            position='topleft',
            primary_length_unit='kilometers',
            secondary_length_unit='miles',
            primary_area_unit='sqkilometers',
            secondary_area_unit='acres'
        ).add_to(africa_map)
        
        # Convert to HTML
        map_html = africa_map._repr_html_()
        
        return map_html
    
    def _create_legend(self):
        """Create map legend for minerals"""
        legend_items = []
        for mineral, color in self.mineral_colors.items():
            # Shorten long names
            display_name = mineral.replace(' (for Aluminum)', '').replace(' (Natural)', '')
            legend_items.append(f'''
                <div style="margin-bottom: 5px;">
                    <i class="fa fa-map-marker" style="color: {self._get_folium_color(color)}; font-size: 18px;"></i>
                    <span style="margin-left: 8px; font-size: 12px;">{display_name}</span>
                </div>
            ''')
        
        legend_html = f'''
        <div style="
            position: fixed; 
            bottom: 50px; 
            left: 50px; 
            width: 220px; 
            background-color: white; 
            z-index: 9999; 
            font-size: 14px;
            border: 2px solid #ccc; 
            border-radius: 8px; 
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h4 style="margin-top: 0; margin-bottom: 12px; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;">
                <i class="fa fa-list"></i> Mineral Legend
            </h4>
            {''.join(legend_items)}
        </div>
        '''
        return legend_html
    
    def _get_folium_color(self, color_name):
        """Convert Folium color names to hex colors for legend"""
        color_map = {
            'blue': '#3186cc',
            'purple': '#8e44ad',
            'darkpurple': '#5b2c6f',
            'lightgray': '#a0a0a0',
            'gray': '#7f8c8d',
            'lightblue': '#5dade2',
            'orange': '#e67e22',
            'green': '#27ae60',
            'darkgreen': '#196f3d',
            'red': '#e74c3c',
            'pink': '#f1948a'
        }
        return color_map.get(color_name, '#95a5a6')


# Test the module
if __name__ == '__main__':
    print("Testing Visualization Module...")
    
    # Sample deposit
    test_deposits = [
        {
            'mineral': 'Cobalt',
            'location_name': 'Test Mine',
            'country': 'DRC',
            'latitude': -4.0,
            'longitude': 23.0,
            'reserves': 1000000,
            'annual_production': 50000,
            'status': 'Active'
        }
    ]
    
    viz = MapVisualization()
    map_html = viz.generate_map(test_deposits)
    
    # Save to test file
    with open('test_map.html', 'w', encoding='utf-8') as f:
        f.write(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Map</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        </head>
        <body>
            {map_html}
        </body>
        </html>
        ''')
    
    print("✓ Map generated successfully!")
    print("✓ Saved to test_map.html")