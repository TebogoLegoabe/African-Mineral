"""
African Critical Minerals Application
Main Flask Application

Author: Mining Engineering Team
Version: 1.0.0
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import timedelta
from modules.visualization import MapVisualization
import os

# Import our modules
from modules.auth import Authentication
from modules.database import MineralDatabase
from modules.analytics import Analytics

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Initialize modules
auth = Authentication()
db = MineralDatabase()
viz = MapVisualization()
analytics = Analytics(db)

print("=" * 70)
print("African Critical Minerals Application")
print("Chrono Minerals - 2025")
print("=" * 70)
print(f"✓ Loaded {db.count_minerals()} mineral records")
print(f"✓ Loaded {db.count_countries()} countries")
print(f"✓ Loaded {db.count_deposits()} deposits")
print("=" * 70)


# ============================================================================
# DECORATORS
# ============================================================================

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# ROUTES - PUBLIC
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        result = auth.login(username, password)
        
        if result['success']:
            # Set session data
            session['user_id'] = result['user']['id']
            session['username'] = result['user']['username']
            session['role'] = result['user']['role']
            
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        role = request.form.get('role', 'Researcher')
        
        result = auth.register(username, password, email, role)
        
        if result['success']:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('index'))


# ============================================================================
# ROUTES - PROTECTED
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    stats = {
        'total_minerals': db.count_minerals(),
        'total_countries': db.count_countries(),
        'total_deposits': db.count_deposits(),
        'unique_minerals': len(db.get_unique_mineral_names()),
        'user_role': session.get('role'),
        'username': session.get('username')
    }
    
    return render_template('dashboard.html', stats=stats)


@app.route('/minerals')
@login_required
def minerals():
    """View mineral database"""
    # Get filter parameters
    mineral_filter = request.args.get('mineral')
    country_filter = request.args.get('country')
    
    # Build filters
    filters = {}
    if mineral_filter:
        filters['mineral_name'] = mineral_filter
    if country_filter:
        filters['country'] = country_filter
    
    # Search minerals
    mineral_data = db.search_minerals(filters)
    
    # Get unique values for dropdowns
    all_minerals = db.get_unique_mineral_names()
    all_countries = db.get_unique_countries()
    
    return render_template('minerals.html',
                         minerals=mineral_data,
                         all_minerals=all_minerals,
                         all_countries=all_countries,
                         selected_mineral=mineral_filter,
                         selected_country=country_filter)


@app.route('/countries')
@login_required
def countries():
    """List all countries"""
    all_countries = db.get_unique_countries()
    
    # Get mineral count for each country
    country_data = []
    for country in all_countries:
        minerals = db.get_minerals_by_country(country)
        unique_minerals = set(m['mineral_name'] for m in minerals)
        
        country_data.append({
            'name': country,
            'mineral_count': len(unique_minerals),
            'total_records': len(minerals)
        })
    
    return render_template('countries.html', countries=country_data)


@app.route('/country/<country_name>')
@login_required
def country_profile(country_name):
    """View country profile"""
    minerals = db.get_minerals_by_country(country_name)
    deposits = db.get_deposits(country=country_name)
    
    if not minerals:
        flash(f'No data found for {country_name}', 'warning')
        return redirect(url_for('countries'))
    
    # Calculate statistics
    unique_minerals = list(set(m['mineral_name'] for m in minerals))
    total_production = sum(m['production_volume'] for m in minerals)
    total_reserves = sum(m['reserves'] for m in minerals)
    
    profile = {
        'name': country_name,
        'minerals': minerals,
        'deposits': deposits,
        'unique_minerals': unique_minerals,
        'total_production': total_production,
        'total_reserves': total_reserves,
        'mineral_count': len(unique_minerals)
    }
    
    return render_template('country_profile.html', profile=profile)


@app.route('/map')
@login_required
def map_view():
    """Interactive map view"""
    # Get filters
    mineral_filter = request.args.get('mineral')
    country_filter = request.args.get('country')
    
    # Get deposits
    deposits = db.get_deposits(mineral_filter, country_filter)
    
    # Generate map
    map_html = viz.generate_map(deposits)
    
    # Get filter options
    all_minerals = db.get_unique_mineral_names()
    all_countries = db.get_unique_countries()
    
    return render_template('map.html',
                         map_html=map_html,
                         deposits=deposits,
                         all_minerals=all_minerals,
                         all_countries=all_countries,
                         selected_mineral=mineral_filter,
                         selected_country=country_filter)

@app.route('/analytics')
@login_required
def analytics_dashboard():
    """Analytics dashboard"""
    stats = analytics.get_summary_statistics()
    
    return render_template('analytics.html', stats=stats)


@app.route('/analytics/production/<mineral>')
@login_required
def production_chart(mineral):
    """Production chart for a specific mineral"""
    chart_html = analytics.generate_production_by_country(mineral)
    all_minerals = db.get_unique_mineral_names()
    
    return render_template('production_chart.html',
                         chart_html=chart_html,
                         mineral=mineral,
                         all_minerals=all_minerals)


@app.route('/analytics/market-share/<mineral>')
@login_required
def market_share_chart(mineral):
    """Market share chart"""
    chart_html = analytics.generate_market_share_pie(mineral)
    all_minerals = db.get_unique_mineral_names()
    
    return render_template('market_share.html',
                         chart_html=chart_html,
                         mineral=mineral,
                         all_minerals=all_minerals)


@app.route('/analytics/prices')
@login_required
def price_comparison():
    """Price comparison chart"""
    chart_html = analytics.generate_price_comparison()
    
    return render_template('price_comparison.html',
                         chart_html=chart_html)


@app.route('/analytics/top-producers')
@login_required
def top_producers():
    """Top producers chart"""
    chart_html = analytics.generate_top_producers(limit=10)
    
    return render_template('top_producers.html',
                         chart_html=chart_html)

# ============================================================================
# CONTEXT PROCESSOR
# ============================================================================

@app.context_processor
def inject_user():
    """Inject user data into all templates"""
    return {
        'current_user': {
            'username': session.get('username'),
            'role': session.get('role'),
            'is_authenticated': 'user_id' in session
        },
        'app_name': 'Chrono Minerals'
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\nServer starting on http://localhost:5000")
    print("Press CTRL+C to quit\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)