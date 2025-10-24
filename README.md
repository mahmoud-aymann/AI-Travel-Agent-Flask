# 🌍 AI Travel Agent - Flask Version

A powerful AI-powered travel planning application built with Flask that helps you plan your perfect trip with real-time data and detailed cost calculations.

## ✨ Features ##

- **AI-Powered Travel Planning**: Uses OpenAI GPT-4 for intelligent travel recommendations
- **Real-Time Weather Data**: Get current weather information for your destination
- **Cost Calculations**: Detailed expense breakdown with currency conversion
- **Search Integration**: Google Search and DuckDuckGo for finding hotels, attractions, and restaurants
- **YouTube Integration**: Find relevant travel videos for your destination
- **Interactive Web Interface**: Modern, responsive design with Bootstrap
- **Chat History**: Keep track of your previous queries and responses

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - OpenAI (required)
  - Serper API (optional, falls back to DuckDuckGo)
  - OpenWeatherMap (optional, for weather features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_Travel_agent_Streamlit-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
   ```

4. **Run the application**
   ```bash
   python run_script.py
   ```
   
   Or directly:
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
AI_Travel_agent_Streamlit-main/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── run_script.py         # Quick start script
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Custom CSS styles
│   └── script.js         # JavaScript functionality
└── README.md             # This file
```

## 🔧 Configuration

### API Keys Setup

1. **OpenAI API Key** (Required)
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Add it to your `.env` file

2. **Serper API Key** (Optional)
   - Get your API key from [Serper.dev](https://serper.dev/)
   - Add it to your `.env` file
   - If not provided, the app will use DuckDuckGo as fallback

3. **OpenWeatherMap API Key** (Optional)
   - Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Add it to your `.env` file
   - If not provided, weather features won't work

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=sk-your-openai-key-here

# Optional
SERPER_API_KEY=your-serper-key-here
OPENWEATHERMAP_API_KEY=your-weather-key-here
```

## 🎯 Usage

1. **Open the application** in your browser at `http://localhost:5000`

2. **Check API status** in the sidebar to ensure all required APIs are configured

3. **Enter your travel query** or select from example queries:
   - Beach vacation planning
   - International trip planning
   - Custom queries

4. **Click "Plan My Trip"** and wait for the AI to process your request

5. **View your personalized travel plan** with:
   - Weather information
   - Currency conversion
   - Attractions and activities
   - Hotel recommendations
   - Daily itinerary
   - Cost breakdown
   - YouTube resources

## 🔄 API Endpoints

- `GET /` - Main application page
- `POST /api/chat` - Send travel queries and get AI responses
- `GET /api/status` - Check API keys status

## 🛠️ Development

### Running in Development Mode

```bash
python app.py
```

The app will run in debug mode with auto-reload enabled.

### Production Deployment

For production deployment, consider using:

- **Gunicorn** for WSGI server
- **Nginx** for reverse proxy
- **Environment variables** for configuration

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Make sure your `.env` file exists and contains a valid OpenAI API key
   - Check that the key doesn't have extra spaces or quotes

2. **"Module not found" errors**
   - Run `pip install -r requirements.txt` to install all dependencies

3. **Port already in use**
   - Change the port in `app.py` (line with `app.run()`)
   - Or kill the process using port 5000

4. **API rate limits**
   - Check your OpenAI API usage and billing
   - Consider adding delays between requests for large queries

### Debug Mode

To enable debug mode, set `debug=True` in the `app.run()` call in `app.py`.

## 📝 Migration from Streamlit

This project was converted from Streamlit to Flask. Key differences:

- **Web Framework**: Flask instead of Streamlit
- **UI**: HTML/CSS/JavaScript instead of Streamlit components
- **Session Management**: Flask sessions instead of Streamlit session state
- **Deployment**: More flexible deployment options
- **Customization**: Easier to customize UI and add new features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your API keys are correct
3. Check the console for error messages
4. Open an issue on the repository

---

**Happy Travel Planning! ✈️🌍**#
