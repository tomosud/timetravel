#!/usr/bin/env python3
"""
Buy Balance Visualization Tool for Timetravel Game

This script visualizes the balance and efficiency of the buying mechanism
with three parameters: years, distance, and UFO size.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import os

class BuyAnalyzer:
    def __init__(self):
        # Constants from game logic
        self.FAILURE_RATE = 0.1
        self.SELLING_EFFICIENCY = 0.8  # 80% of base value when selling
        self.INITIAL_MONEY = 1000
        
        # Item condition multipliers
        self.CONDITION_MULTIPLIERS = {
            'A': 1.0,  # New
            'B': 0.8,  # Good
            'C': 0.6   # Worn
        }
    
    def calculate_cost(self, years, distance, ufo_size):
        """Calculate travel cost based on parameters"""
        return (years * distance) * ufo_size
    
    def calculate_rarity_multiplier(self, years, distance):
        """Calculate rarity multiplier from years and distance"""
        base_multiplier = 1.0
        year_bonus = min(years * 0.02, 2.0)
        distance_bonus = min(distance * 0.001, 1.5)
        combo_bonus = min((years * distance) * 0.00001, 1.0)
        return base_multiplier + year_bonus + distance_bonus + combo_bonus
    
    def calculate_item_count(self, ufo_size):
        """Calculate number of items obtained"""
        return max(1, min(8, int(ufo_size)))
    
    def calculate_condition_probability(self, years):
        """Calculate condition distribution based on years"""
        # Based on game logic: older items have higher degradation
        prob_new = max(0.1, 1.0 - years * 0.01)
        prob_worn = min(0.9, years * 0.01)
        prob_good = 1.0 - prob_new - prob_worn
        
        # Normalize to ensure sum = 1.0
        total = prob_new + prob_good + prob_worn
        return {
            'A': prob_new / total,
            'B': prob_good / total,
            'C': prob_worn / total
        }
    
    def calculate_expected_value(self, years, distance, ufo_size):
        """Calculate expected value of purchase"""
        cost = self.calculate_cost(years, distance, ufo_size)
        rarity_mult = self.calculate_rarity_multiplier(years, distance)
        item_count = self.calculate_item_count(ufo_size)
        condition_probs = self.calculate_condition_probability(years)
        
        # Calculate expected item value
        base_value_range = (100, 1000)
        avg_base_value = (base_value_range[0] + base_value_range[1]) / 2
        
        # Expected condition multiplier
        expected_condition_mult = sum(
            prob * self.CONDITION_MULTIPLIERS[condition]
            for condition, prob in condition_probs.items()
        )
        
        # Expected value per item
        expected_item_value = avg_base_value * expected_condition_mult * rarity_mult
        
        # Total expected value (before failure rate)
        total_expected_value = expected_item_value * item_count
        
        # Account for failure rate
        expected_value_with_failure = total_expected_value * (1 - self.FAILURE_RATE)
        
        # Account for selling efficiency
        expected_selling_value = expected_value_with_failure * self.SELLING_EFFICIENCY
        
        return {
            'cost': cost,
            'expected_revenue': expected_selling_value,
            'expected_profit': expected_selling_value - cost,
            'roi': (expected_selling_value - cost) / cost if cost > 0 else 0,
            'item_count': item_count,
            'rarity_multiplier': rarity_mult
        }

def create_visualizations():
    """Create comprehensive visualizations of buying mechanics"""
    analyzer = BuyAnalyzer()
    
    # Create output directory
    output_dir = './plots'
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Cost Visualization (Years vs Distance)
    print("Generating cost visualization...")
    years_range = np.linspace(1, 1000, 50)
    distance_range = np.linspace(100, 50000, 50)
    Y, D = np.meshgrid(years_range, distance_range)
    
    costs = np.zeros_like(Y)
    for i in range(len(distance_range)):
        for j in range(len(years_range)):
            costs[i, j] = analyzer.calculate_cost(Y[i, j], D[i, j], 1.0)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(Y, D, costs, cmap='viridis', alpha=0.8)
    ax.set_xlabel('Years')
    ax.set_ylabel('Distance (km)')
    ax.set_zlabel('Cost (¥)')
    ax.set_title('Travel Cost vs Years and Distance (UFO Size = 1.0)')
    fig.colorbar(surf)
    plt.savefig(f'{output_dir}/cost_3d.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. ROI Heatmap
    print("Generating ROI heatmap...")
    years_sample = np.linspace(10, 500, 20)
    distance_sample = np.linspace(1000, 30000, 20)
    roi_matrix = np.zeros((len(distance_sample), len(years_sample)))
    
    for i, distance in enumerate(distance_sample):
        for j, years in enumerate(years_sample):
            result = analyzer.calculate_expected_value(years, distance, 2.0)
            roi_matrix[i, j] = result['roi']
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(roi_matrix, 
                xticklabels=[f'{int(y)}' for y in years_sample[::2]], 
                yticklabels=[f'{int(d)}' for d in distance_sample[::2]],
                annot=False, cmap='RdYlGn', center=0, fmt='.2f')
    plt.title('ROI Heatmap (UFO Size = 2.0)')
    plt.xlabel('Years')
    plt.ylabel('Distance (km)')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/roi_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. UFO Size Efficiency
    print("Generating UFO size analysis...")
    ufo_sizes = np.linspace(1.0, 10.0, 50)
    profits = []
    item_counts = []
    costs = []
    
    # Fixed years=100, distance=5000 for comparison
    base_years, base_distance = 100, 5000
    
    for ufo_size in ufo_sizes:
        result = analyzer.calculate_expected_value(base_years, base_distance, ufo_size)
        profits.append(result['expected_profit'])
        item_counts.append(result['item_count'])
        costs.append(result['cost'])
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Profit vs UFO Size
    ax1.plot(ufo_sizes, profits, 'b-', linewidth=2)
    ax1.set_xlabel('UFO Size')
    ax1.set_ylabel('Expected Profit (¥)')
    ax1.set_title(f'Expected Profit vs UFO Size (Years={base_years}, Distance={base_distance}km)')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    # Item Count vs UFO Size
    ax2.plot(ufo_sizes, item_counts, 'g-', linewidth=2)
    ax2.set_xlabel('UFO Size')
    ax2.set_ylabel('Item Count')
    ax2.set_title('Item Count vs UFO Size')
    ax2.grid(True, alpha=0.3)
    
    # Cost vs UFO Size
    ax3.plot(ufo_sizes, costs, 'r-', linewidth=2)
    ax3.set_xlabel('UFO Size')
    ax3.set_ylabel('Cost (¥)')
    ax3.set_title('Cost vs UFO Size')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ufo_size_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Rarity Bonus Visualization
    print("Generating rarity bonus analysis...")
    years_range = np.linspace(1, 1000, 100)
    distance_range = np.linspace(0, 50000, 100)
    
    rarity_by_years = [analyzer.calculate_rarity_multiplier(y, 1000) for y in years_range]
    rarity_by_distance = [analyzer.calculate_rarity_multiplier(100, d) for d in distance_range]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    ax1.plot(years_range, rarity_by_years, 'b-', linewidth=2)
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Rarity Multiplier')
    ax1.set_title('Rarity Multiplier vs Years (Distance=1000km)')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=2.0, color='r', linestyle='--', alpha=0.5, label='Year Bonus Cap')
    ax1.legend()
    
    ax2.plot(distance_range, rarity_by_distance, 'g-', linewidth=2)
    ax2.set_xlabel('Distance (km)')
    ax2.set_ylabel('Rarity Multiplier')
    ax2.set_title('Rarity Multiplier vs Distance (Years=100)')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=2.5, color='r', linestyle='--', alpha=0.5, label='Distance Bonus Cap')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/rarity_bonus.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Budget-constrained optimization
    print("Generating budget optimization analysis...")
    budgets = [1000, 5000, 10000, 50000, 100000]
    optimal_strategies = []
    
    # Sample parameter space
    param_combinations = []
    for years in [10, 50, 100, 200, 500]:
        for distance in [1000, 5000, 10000, 20000]:
            for ufo_size in [1.0, 2.0, 3.0, 5.0]:
                param_combinations.append((years, distance, ufo_size))
    
    for budget in budgets:
        best_roi = -float('inf')
        best_params = None
        
        for years, distance, ufo_size in param_combinations:
            result = analyzer.calculate_expected_value(years, distance, ufo_size)
            if result['cost'] <= budget and result['roi'] > best_roi:
                best_roi = result['roi']
                best_params = (years, distance, ufo_size, result['expected_profit'])
        
        optimal_strategies.append((budget, best_params, best_roi))
    
    # Create budget strategy table
    strategy_data = []
    for budget, params, roi in optimal_strategies:
        if params:
            years, distance, ufo_size, profit = params
            strategy_data.append({
                'Budget': f'¥{budget:,}',
                'Years': int(years),
                'Distance': f'{distance:,}km',
                'UFO Size': f'{ufo_size:.1f}',
                'Expected Profit': f'¥{profit:,.0f}',
                'ROI': f'{roi:.2%}'
            })
    
    df = pd.DataFrame(strategy_data)
    
    # Save strategy table
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, 
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)
    plt.title('Optimal Strategies by Budget', pad=20, fontsize=14, fontweight='bold')
    plt.savefig(f'{output_dir}/optimal_strategies.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"All visualizations saved to {output_dir}/")
    print("Generated files:")
    print("- cost_3d.png: 3D surface plot of costs")
    print("- roi_heatmap.png: ROI heatmap for parameter combinations") 
    print("- ufo_size_analysis.png: UFO size efficiency analysis")
    print("- rarity_bonus.png: Rarity bonus curves")
    print("- optimal_strategies.png: Budget-constrained optimal strategies")

if __name__ == "__main__":
    create_visualizations()