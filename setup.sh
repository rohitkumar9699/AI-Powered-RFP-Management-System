#!/bin/bash
# Setup and run the RFP Management System locally

set -e

echo "🚀 AI-Powered RFP Management System - Setup Script"
echo "=================================================="
echo ""

# Check prerequisites
echo "✓ Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is required but not installed."; exit 1; }

echo "✓ Python: $(python3 --version)"
echo "✓ Node: $(node --version)"
echo "✓ npm: $(npm --version)"
echo ""

# Backend Setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "  Installing Python dependencies..."
pip install -q -r requirements.txt

# Setup environment variables
if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    cp .env.example .env
    echo "  ⚠️  Please update .env with your credentials:"
    echo "     - OPENAI_API_KEY"
    echo "     - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD"
    echo "     - MONGODB_URI (if not local)"
fi

cd ..
echo "✓ Backend setup complete"
echo ""

# Frontend Setup
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
echo "  Installing npm dependencies..."
npm install -q

cd ..
echo "✓ Frontend setup complete"
echo ""

# Database check
echo "🗄️  Checking database..."
if command -v mongod >/dev/null 2>&1; then
    echo "✓ MongoDB is installed"
    if ! pgrep -x "mongod" > /dev/null; then
        echo "  Note: MongoDB is not running. Start it with: mongod"
    else
        echo "✓ MongoDB is running"
    fi
else
    echo "⚠️  MongoDB not found. Use MongoDB Atlas (cloud) or install locally:"
    echo "   macOS: brew install mongodb-community"
    echo "   Linux: sudo apt-get install mongodb"
    echo "   Windows: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/"
fi
echo ""

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Configure credentials:"
echo "   Edit backend/.env with your:"
echo "   - OPENAI_API_KEY (from https://platform.openai.com/api-keys)"
echo "   - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD"
echo "   - MONGODB_URI (if using MongoDB Atlas)"
echo ""
echo "2. Start services (in separate terminals):"
echo ""
echo "   Terminal 1 - Backend:"
echo "   cd backend && source venv/bin/activate && python manage.py runserver"
echo ""
echo "   Terminal 2 - Frontend:"
echo "   cd frontend && npm start"
echo ""
echo "   Terminal 3 - Database (if local MongoDB):"
echo "   mongod"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:4200"
echo "   Backend API: http://localhost:8000/api/"
echo ""
echo "4. (Optional) Seed sample vendors:"
echo "   cd backend && python manage.py seed_vendors"
echo ""
echo "📚 Documentation:"
echo "   - QUICKSTART.md - 5-minute setup guide"
echo "   - README.md - Complete documentation"
echo "   - API_EXAMPLES.md - API usage examples"
echo "   - ARCHITECTURE.md - System design"
echo ""
