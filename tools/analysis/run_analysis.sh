#!/bin/bash

echo "Starting Buy Balance Analysis Visualization..."

# Navigate to project root
cd ..

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment venv..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install/update requirements
echo "Installing requirements..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install packages."
    exit 1
fi

# Navigate back to analysis directory
cd analysis

# Create plots directory
if [ ! -d "plots" ]; then
    echo "Creating plots directory..."
    mkdir plots
fi

# Run visualization
echo "Running buy balance analysis..."
python buy_visualizer.py
if [ $? -ne 0 ]; then
    echo "Visualization failed."
    exit 1
fi

echo ""
echo "Analysis completed successfully!"
echo "Check the analysis/plots directory for generated visualizations:"
echo "- cost_3d.png: 3D surface plot of costs"
echo "- roi_heatmap.png: ROI heatmap for parameter combinations" 
echo "- ufo_size_analysis.png: UFO size efficiency analysis"
echo "- rarity_bonus.png: Rarity bonus curves"
echo "- optimal_strategies.png: Budget-constrained optimal strategies"