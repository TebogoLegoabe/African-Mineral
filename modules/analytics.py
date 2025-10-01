"""
Analytics Module
Handles data analytics and chart generation using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict


class Analytics:
    """Generate analytics and charts"""
    
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database
    
    def generate_production_by_country(self, mineral):
        """Generate bar chart of production by country for a mineral"""
        # Get data
        minerals = self.db.search_minerals({'mineral_name': mineral})
        
        if not minerals:
            return None
        
        # Aggregate by country
        country_production = defaultdict(int)
        for m in minerals:
            country_production[m['country']] += m['production_volume']
        
        # Sort by production
        sorted_data = sorted(country_production.items(), key=lambda x: x[1], reverse=True)
        countries = [item[0] for item in sorted_data]
        production = [item[1] for item in sorted_data]
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=countries,
                y=production,
                text=[f'{p:,.0f}' for p in production],
                textposition='auto',
                marker=dict(
                    color=production,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Production<br>(tonnes)")
                )
            )
        ])
        
        fig.update_layout(
            title=f'{mineral} Production by Country',
            xaxis_title='Country',
            yaxis_title='Production Volume (tonnes)',
            template='plotly_white',
            height=500,
            hovermode='x'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def generate_reserves_comparison(self, countries):
        """Generate stacked bar chart comparing reserves across countries"""
        if not countries:
            return None
        
        # Collect data
        mineral_data = defaultdict(lambda: defaultdict(int))
        
        for country in countries:
            minerals = self.db.get_minerals_by_country(country)
            for m in minerals:
                mineral_data[m['mineral_name']][country] += m['reserves']
        
        # Create figure
        fig = go.Figure()
        
        for mineral_name, country_reserves in mineral_data.items():
            countries_list = list(country_reserves.keys())
            reserves_list = list(country_reserves.values())
            
            fig.add_trace(go.Bar(
                name=mineral_name,
                x=countries_list,
                y=reserves_list,
                text=[f'{r:,.0f}' for r in reserves_list],
                textposition='auto',
            ))
        
        fig.update_layout(
            title='Mineral Reserves Comparison',
            xaxis_title='Country',
            yaxis_title='Reserves (tonnes)',
            barmode='stack',
            template='plotly_white',
            height=500,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def generate_market_share_pie(self, mineral):
        """Generate pie chart of market share by country"""
        minerals = self.db.search_minerals({'mineral_name': mineral})
        
        if not minerals:
            return None
        
        # Aggregate by country
        country_production = defaultdict(int)
        for m in minerals:
            country_production[m['country']] += m['production_volume']
        
        countries = list(country_production.keys())
        production = list(country_production.values())
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=countries,
            values=production,
            hole=0.3,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(
                colors=px.colors.qualitative.Set3
            )
        )])
        
        fig.update_layout(
            title=f'{mineral} Market Share by Country',
            template='plotly_white',
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def generate_price_comparison(self):
        """Generate bar chart comparing prices of different minerals"""
        all_minerals = self.db.get_all_minerals()
        
        # Get unique minerals with their average prices
        mineral_prices = defaultdict(list)
        for m in all_minerals:
            mineral_prices[m['mineral_name']].append(m['price'])
        
        # Calculate averages
        minerals = []
        avg_prices = []
        for mineral, prices in mineral_prices.items():
            minerals.append(mineral)
            avg_prices.append(sum(prices) / len(prices))
        
        # Sort by price
        sorted_data = sorted(zip(minerals, avg_prices), key=lambda x: x[1], reverse=True)
        minerals = [item[0] for item in sorted_data]
        avg_prices = [item[1] for item in sorted_data]
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=minerals,
                y=avg_prices,
                text=[f'${p:,.0f}' for p in avg_prices],
                textposition='auto',
                marker=dict(
                    color=avg_prices,
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Price<br>(USD/tonne)")
                )
            )
        ])
        
        fig.update_layout(
            title='Average Mineral Prices',
            xaxis_title='Mineral',
            yaxis_title='Price (USD per tonne)',
            template='plotly_white',
            height=500,
            xaxis={'tickangle': -45}
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def generate_top_producers(self, limit=10):
        """Generate chart of top producing countries"""
        all_minerals = self.db.get_all_minerals()
        
        # Aggregate production by country
        country_production = defaultdict(int)
        for m in all_minerals:
            country_production[m['country']] += m['production_volume']
        
        # Sort and limit
        sorted_data = sorted(country_production.items(), key=lambda x: x[1], reverse=True)[:limit]
        countries = [item[0] for item in sorted_data]
        production = [item[1] for item in sorted_data]
        
        # Create horizontal bar chart
        fig = go.Figure(data=[
            go.Bar(
                y=countries,
                x=production,
                orientation='h',
                text=[f'{p:,.0f}' for p in production],
                textposition='auto',
                marker=dict(
                    color=production,
                    colorscale='Blues',
                    showscale=False
                )
            )
        ])
        
        fig.update_layout(
            title=f'Top {limit} Producing Countries',
            xaxis_title='Total Production (tonnes)',
            yaxis_title='Country',
            template='plotly_white',
            height=500,
            yaxis={'autorange': 'reversed'}
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def get_summary_statistics(self):
        """Get summary statistics for dashboard"""
        all_minerals = self.db.get_all_minerals()
        
        total_production = sum(m['production_volume'] for m in all_minerals)
        total_reserves = sum(m['reserves'] for m in all_minerals)
        avg_price = sum(m['price'] for m in all_minerals) / len(all_minerals) if all_minerals else 0
        
        # Top producer
        country_production = defaultdict(int)
        for m in all_minerals:
            country_production[m['country']] += m['production_volume']
        
        top_producer = max(country_production.items(), key=lambda x: x[1]) if country_production else ('N/A', 0)
        
        return {
            'total_production': total_production,
            'total_reserves': total_reserves,
            'avg_price': avg_price,
            'top_producer': top_producer[0],
            'top_producer_volume': top_producer[1]
        }


# Test the module
if __name__ == '__main__':
    from database import MineralDatabase
    
    print("Testing Analytics Module...")
    
    db = MineralDatabase()
    analytics = Analytics(db)
    
    print("\n1. Summary Statistics:")
    stats = analytics.get_summary_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n2. Generating charts...")
    
    # Test production chart
    chart = analytics.generate_production_by_country('Cobalt')
    if chart:
        print("   ✓ Production chart generated")
    
    # Test market share
    chart = analytics.generate_market_share_pie('Lithium')
    if chart:
        print("   ✓ Market share chart generated")
    
    print("\n✓ Analytics module working!")