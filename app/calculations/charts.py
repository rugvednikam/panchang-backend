def get_north_indian_chart(planets):
    # North Indian diamond chart
    # planets dict: {house: [planet list]}
    svg = '''
    <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#FFF8E1" stroke="#B71C1C" stroke-width="3"/>
    <!-- Diamond lines North Indian -->
    <line x1="0" y1="0" x2="400" y2="400" stroke="#B71C1C" stroke-width="2"/>
    <line x1="400" y1="0" x2="0" y2="400" stroke="#B71C1C" stroke-width="2"/>
    <line x1="200" y1="0" x2="200" y2="400" stroke="#B71C1C" stroke-width="2"/>
    <line x1="0" y1="200" x2="400" y2="200" stroke="#B71C1C" stroke-width="2"/>
    <text x="180" y="60" font-size="12">12</text><text x="280" y="110" font-size="12">1</text><text x="330" y="190" font-size="12">2</text>
    <text x="280" y="310" font-size="12">3</text><text x="180" y="350" font-size="12">4</text><text x="80" y="310" font-size="12">5</text>
    <text x="30" y="190" font-size="12">6</text><text x="80" y="110" font-size="12">7</text><text x="100" y="100" font-size="10">North Indian</text>
    </svg>
    '''
    return svg

def get_south_indian_chart(planets):
    # South Indian square 4x3 grid
    svg = '''
    <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#FFF8E1" stroke="#B71C1C" stroke-width="3"/>
    <!-- 4x3 grid South -->
    <line x1="100" y1="0" x2="100" y2="400" stroke="#B71C1C"/><line x1="200" y1="0" x2="200" y2="400" stroke="#B71C1C"/><line x1="300" y1="0" x2="300" y2="400" stroke="#B71C1C"/>
    <line x1="0" y1="100" x2="400" y2="100" stroke="#B71C1C"/><line x1="0" y1="200" x2="400" y2="200" stroke="#B71C1C"/><line x1="0" y1="300" x2="400" y2="300" stroke="#B71C1C"/>
    <text x="30" y="50" font-size="10">11 Meena</text><text x="130" y="50" font-size="10">12 Mesha</text><text x="230" y="50" font-size="10">1 Vrishabha</text><text x="330" y="50" font-size="10">2 Mithuna</text>
    <text x="50" y="150" font-size="10">South Indian</text>
    </svg>
    '''
    return svg

def get_east_indian_chart(planets):
    # East Indian (Bengali) chart
    svg = '''
    <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#FFF8E1" stroke="#B71C1C" stroke-width="3"/>
    <circle cx="200" cy="200" r="150" fill="none" stroke="#B71C1C" stroke-width="2"/>
    <line x1="200" y1="50" x2="200" y2="350" stroke="#B71C1C"/><line x1="50" y1="200" x2="350" y2="200" stroke="#B71C1C"/>
    <text x="180" y="80" font-size="12">1</text><text x="280" y="130" font-size="12">2</text><text x="320" y="210" font-size="12">3</text>
    <text x="180" y="220" font-size="10">East Indian (Bengali)</text>
    </svg>
    '''
    return svg

def get_west_indian_chart(planets):
    # West Indian chart (Gujarati style)
    svg = '''
    <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="400" fill="#FFF8E1" stroke="#B71C1C" stroke-width="3"/>
    <!-- West style similar to North but with different house numbering -->
    <line x1="0" y1="0" x2="400" y2="400" stroke="#B71C1C" stroke-width="1.5"/>
    <line x1="400" y1="0" x2="0" y2="400" stroke="#B71C1C" stroke-width="1.5"/>
    <rect x="100" y="100" width="200" height="200" fill="none" stroke="#B71C1C" stroke-width="2"/>
    <text x="180" y="120" font-size="12">1 Lagna</text><text x="180" y="200" font-size="10">West Indian</text>
    </svg>
    '''
    return svg

def generate_all_charts(planets=None):
    if planets is None:
        planets = {}
    return {
      "north_indian": get_north_indian_chart(planets),
      "south_indian": get_south_indian_chart(planets),
      "east_indian_bengali": get_east_indian_chart(planets),
      "west_indian": get_west_indian_chart(planets),
      "note": "North Indian Diamond - Most popular North, South 4x3 grid - Tamil/Kerala, East Bengali circular, West Gujarati - All compatible with 20 languages"
    }
