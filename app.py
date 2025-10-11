from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper, GoogleSerperAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun, YouTubeSearchTool
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langgraph.graph import MessagesState, StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for sessions

# Custom Tools
@tool
def addition(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

@tool
def division(a: int, b: int) -> float:
    """Divide two integers."""
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b

@tool
def substraction(a: int, b: int) -> float:
    """Subtract two integers."""
    return a - b

@tool
def get_weather(city: str) -> str:
    """Fetches the current weather of the city from OpenWeatherMap."""
    try:
        weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if weather_api_key:
            os.environ["OPENWEATHERMAP_API_KEY"] = weather_api_key
            weather = OpenWeatherMapAPIWrapper()
            return weather.run(city)
        else:
            return f"Weather API key not available. Cannot get weather for {city}."
    except Exception as e:
        return f"Weather data unavailable for {city}. Error: {str(e)}"

@tool
def search_google(query: str) -> str:
    """Fetches details about attractions, restaurants, hotels, etc. from Google Serper API."""
    try:
        serper_api_key = os.getenv("SERPER_API_KEY")
        if serper_api_key:
            os.environ["SERPER_API_KEY"] = serper_api_key
            search_serper = GoogleSerperAPIWrapper()
            return search_serper.run(query)
        else:
            # Fallback to duck search if serper not available
            return search_duck(query)
    except Exception as e:
        return f"Google search unavailable, trying alternative search. Error: {str(e)}"

@tool
def search_duck(query: str) -> str:
    """Fetches details using DuckDuckGo search."""
    try:
        search_d = DuckDuckGoSearchRun()
        return search_d.invoke(query)
    except Exception as e:
        return f"Search unavailable. Error: {str(e)}"

@tool
def youtube_search(query: str) -> str:
    """Fetches YouTube videos about travel destinations."""
    try:
        youtubetool = YouTubeSearchTool()
        return youtubetool.run(query)
    except Exception as e:
        return f"YouTube search unavailable. Error: {str(e)}"

# Advanced calculation tool
python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="A Python shell for complex calculations. Input should be a valid python command.",
    func=python_repl.run,
)

def initialize_travel_agent():
    """Initialize the travel agent with all tools and configurations."""
    try:
        # Get OpenAI API key from environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            return None
        
        # Initialize OpenAI model
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=2000,
            api_key=openai_api_key
        )
        
        # System prompt
        system_prompt = SystemMessage("""
        You are a professional AI Travel Agent. You MUST follow this EXACT process for every travel query:

        STEP 1: ALWAYS call get_weather tool first for the destination city

        STEP 2: ALWAYS call search_google or search_duck to find:
           - Hotels with specific prices per night
           - Top attractions with entry fees
           - Restaurants with price ranges
           - Transportation options with costs
           - CURRENCY CONVERSION: If user needs different currency, search for:
             "current exchange rate [from_currency] to [to_currency] today"

        STEP 3: ALWAYS use arithmetic tools (addition, multiply) to calculate:
           - Hotel cost = daily_rate × number_of_days
           - Total food cost = daily_food_budget × number_of_days
           - Total attraction costs = sum of all entry fees
           - Currency conversion = amount × exchange_rate (from search)
           - Grand total = hotel + food + attractions + transport

        STEP 4: ALWAYS call youtube_search for relevant travel videos

        STEP 5: Create detailed day-by-day itinerary with REAL costs from your searches

        MANDATORY RULES:
        - For currency conversion: SEARCH for current exchange rates, don't guess
        - Use ACTUAL data from tool calls, never make up prices
        - Show detailed cost breakdown with calculations
        - Include weather information from the weather tool
        - Provide YouTube video links from your search

        FORMAT your response as:
        ## 🌤️ Weather Information
        ## 💱 Currency Conversion  
        ## 🏛️ Attractions & Activities
        ## 🏨 Hotels & Accommodation
        ## 📅 Daily Itinerary
        ## 💰 Cost Breakdown
        ## 🎥 YouTube Resources
        ## 📋 Summary
        """)
        
        # Create tools list
        tools = [addition, multiply, division, substraction, get_weather, 
                search_google, search_duck, repl_tool, youtube_search]
        
        # Bind tools to LLM
        llm_with_tools = llm.bind_tools(tools)
        
        # Create graph function
        def function_1(state: MessagesState):
            user_question = state["messages"]
            input_question = [system_prompt] + user_question
            response = llm_with_tools.invoke(input_question)
            return {"messages": [response]}
        
        # Build the graph
        builder = StateGraph(MessagesState)
        builder.add_node("llm_decision_step", function_1)
        builder.add_node("tools", ToolNode(tools))
        builder.add_edge(START, "llm_decision_step")
        builder.add_conditional_edges("llm_decision_step", tools_condition)
        builder.add_edge("tools", "llm_decision_step")
        
        # Compile the graph
        react_graph = builder.compile()
        return react_graph
        
    except Exception as e:
        print(f"Error initializing travel agent: {str(e)}")
        return None

# Global variable to store the travel agent
travel_agent = None

def get_travel_agent():
    """Get or initialize the travel agent."""
    global travel_agent
    if travel_agent is None:
        travel_agent = initialize_travel_agent()
    return travel_agent

def generate_demo_response(query):
    """Generate demo response based on query."""
    query_lower = query.lower()
    
    # Check for specific destinations
    if 'دبي' in query_lower or 'dubai' in query_lower:
        return """## Weather Information
Temperature: 28°C - Sunny
Humidity: 65%
Wind: 15 km/h

## Hotel Recommendations
- Burj Khalifa Hotel: 450 AED/night
- Atlantis Hotel: 380 AED/night  
- Jumeirah Hotel: 320 AED/night

## Tourist Attractions
- Burj Khalifa: 150 AED
- Dubai Mall: Free
- Dubai Fountain: Free
- Palm Island: 200 AED

## Daily Itinerary
Day 1:
- Morning: Visit Burj Khalifa
- Afternoon: Dubai Mall shopping
- Evening: Dubai Fountain

Day 2:
- Morning: Palm Island
- Afternoon: Jumeirah Beach
- Evening: Dinner at Dubai Marina

Day 3:
- Morning: Dubai Museum
- Afternoon: Gold Souk
- Evening: Dubai Airport

## Cost Calculation
- Hotels: 450 × 3 = 1,350 AED
- Food: 200 × 3 = 600 AED
- Attractions: 350 AED
- Transportation: 300 AED
- Total: 2,600 AED

## YouTube Resources
- Dubai Travel Guide
- Best Places in Dubai
- Dubai Travel Tips"""
    else:
        return """## Travel Plan

### Accommodation
- 4-star hotel: 300-500 AED/night
- 5-star hotel: 500-800 AED/night

### Food
- Regular meal: 50-100 AED
- Fine dining: 100-200 AED

### Transportation
- Taxi: 20-50 AED
- Metro: 5-15 AED
- Bus: 3-10 AED

### Important Tips
- Book hotels in advance
- Pack light clothes
- Use Dubai Metro app
- Try local cuisine

Note: This is a demo version. For accurate information, you need a valid OpenAI API key."""

@app.route('/')
def index():
    """Main page route."""
    # Check API keys status
    openai_key = os.getenv("OPENAI_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    weather_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    api_status = {
        'openai': bool(openai_key and openai_key != "your_openai_api_key_here"),
        'serper': bool(serper_key and serper_key != "your_serper_api_key_here"),
        'weather': bool(weather_key and weather_key != "your_openweathermap_api_key_here")
    }
    
    return render_template('index.html', api_status=api_status)

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat functionality."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter your travel query!'}), 400
        
        # Check if OpenAI API key is properly configured
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key or openai_key == "your_openai_api_key_here":
            # Return demo response instead of error
            demo_response = generate_demo_response(query)
            return jsonify({'response': demo_response})
        
        # Get travel agent
        agent = get_travel_agent()
        if agent is None:
            # Return demo response instead of error
            demo_response = generate_demo_response(query)
            return jsonify({'response': demo_response})
        
        # Process the query
        response = agent.invoke({
            "messages": [HumanMessage(query)]
        })
        
        if response and "messages" in response:
            final_response = response["messages"][-1].content
            return jsonify({'response': final_response})
        else:
            # Return demo response instead of error
            demo_response = generate_demo_response(query)
            return jsonify({'response': demo_response})
            
    except Exception as e:
        # Return demo response instead of error
        demo_response = generate_demo_response(query)
        return jsonify({'response': demo_response})

@app.route('/api/status')
def status():
    """API endpoint to check API keys status."""
    openai_key = os.getenv("OPENAI_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    weather_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    return jsonify({
        'openai': bool(openai_key and openai_key != "your_openai_api_key_here"),
        'serper': bool(serper_key and serper_key != "your_serper_api_key_here"),
        'weather': bool(weather_key and weather_key != "your_openweathermap_api_key_here")
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
