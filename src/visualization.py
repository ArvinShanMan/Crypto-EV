"""
Visualization Module

This module provides visualization tools for EV analysis and simulation results.
Uses Matplotlib for creating charts and plots.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, List, Tuple, Optional
from monte_carlo import SimulationResults, MonteCarloSimulator


class EVVisualizer:
    """
    Visualizer for EV calculations and Monte Carlo results.
    """
    
    def __init__(self, figsize: Tuple[int, int] = (14, 10), style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer.
        
        Args:
            figsize: Figure size (width, height)
            style: Matplotlib style
        """
        self.figsize = figsize
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
    
    def plot_simulation_results(self, results: SimulationResults, num_paths: int = 100) -> Figure:
        """
        Plot comprehensive simulation results.
        
        Args:
            results: SimulationResults object
            num_paths: Number of paths to plot (for clarity)
        
        Returns:
            Matplotlib Figure object
        """
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        fig.suptitle('Monte Carlo Simulation Results', fontsize=16, fontweight='bold')
        
        # 1. Cumulative returns paths
        ax1 = axes[0, 0]
        num_to_plot = min(num_paths, results.cumulative_returns.shape[0])
        for i in range(num_to_plot):
            ax1.plot(results.cumulative_returns[i, :], alpha=0.3, linewidth=0.8)
        
        # Add mean and percentiles
        mean_return = np.mean(results.cumulative_returns, axis=0)
        p5 = np.percentile(results.cumulative_returns, 5, axis=0)
        p95 = np.percentile(results.cumulative_returns, 95, axis=0)
        
        ax1.plot(mean_return, color='darkred', linewidth=2.5, label='Mean')
        ax1.fill_between(range(len(mean_return)), p5, p95, alpha=0.2, color='red', label='5th-95th percentile')
        ax1.set_xlabel('Trade Number')
        ax1.set_ylabel('Cumulative Return')
        ax1.set_title('Cumulative Returns Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Final balance distribution
        ax2 = axes[0, 1]
        ax2.hist(results.final_balances, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        ax2.axvline(np.mean(results.final_balances), color='red', linestyle='--', linewidth=2, label=f"Mean: ${np.mean(results.final_balances):.2f}")
        ax2.axvline(np.median(results.final_balances), color='green', linestyle='--', linewidth=2, label=f"Median: ${np.median(results.final_balances):.2f}")
        ax2.set_xlabel('Final Balance ($)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Final Balances')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Drawdown paths
        ax3 = axes[1, 0]
        for i in range(min(num_paths, results.drawdowns.shape[0])):
            ax3.plot(results.drawdowns[i, :], alpha=0.3, linewidth=0.8)
        
        mean_dd = np.mean(results.drawdowns, axis=0)
        ax3.plot(mean_dd, color='darkred', linewidth=2.5, label='Mean Drawdown')
        ax3.fill_between(range(len(mean_dd)), 0, mean_dd, alpha=0.2, color='red')
        ax3.set_xlabel('Trade Number')
        ax3.set_ylabel('Drawdown (%)')
        ax3.set_title('Drawdown Paths')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Statistics box
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        stats_text = self._format_statistics(results.statistics)
        ax4.text(0.1, 0.95, stats_text, transform=ax4.transAxes,
                fontfamily='monospace', fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        return fig
    
    def plot_return_distribution(self, results: SimulationResults) -> Figure:
        """
        Plot return distribution with metrics.
        
        Args:
            results: SimulationResults object
        
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        returns_pct = ((results.final_balances - np.mean(results.final_balances)) / 
                       np.mean(results.final_balances)) * 100
        
        ax.hist(returns_pct, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        
        # Add statistical lines
        mean_ret = np.mean(returns_pct)
        std_ret = np.std(returns_pct)
        
        ax.axvline(mean_ret, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_ret:.2f}%')
        ax.axvline(mean_ret - std_ret, color='orange', linestyle=':', linewidth=2, label=f'±1 Std Dev')
        ax.axvline(mean_ret + std_ret, color='orange', linestyle=':', linewidth=2)
        ax.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Return (%)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Returns')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def plot_win_rate_analysis(self, win_rate_results: Dict[float, Dict[str, float]]) -> Figure:
        """
        Plot analysis of mean returns across different win rates.
        
        Args:
            win_rate_results: Dictionary from MonteCarloSimulator.win_rate_analysis()
        
        Returns:
            Matplotlib Figure object
        """
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        fig.suptitle('Win Rate Sensitivity Analysis', fontsize=16, fontweight='bold')
        
        win_rates = sorted(win_rate_results.keys())
        
        # Extract metrics
        mean_returns = [win_rate_results[wr]['mean_return_pct'] for wr in win_rates]
        std_returns = [win_rate_results[wr]['std_return_pct'] for wr in win_rates]
        win_sim_pct = [win_rate_results[wr]['winning_simulations_pct'] for wr in win_rates]
        mean_dd = [win_rate_results[wr]['mean_max_drawdown_pct'] for wr in win_rates]
        
        # Plot 1: Mean return vs win rate
        ax1 = axes[0, 0]
        ax1.plot(win_rates, mean_returns, marker='o', linewidth=2, markersize=8, color='steelblue')
        ax1.fill_between(win_rates, np.array(mean_returns) - np.array(std_returns),
                        np.array(mean_returns) + np.array(std_returns), alpha=0.2)
        ax1.axhline(0, color='red', linestyle='--', alpha=0.5)
        ax1.set_xlabel('Win Rate')
        ax1.set_ylabel('Mean Return (%)')
        ax1.set_title('Mean Return vs Win Rate')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Winning simulations percentage
        ax2 = axes[0, 1]
        ax2.plot(win_rates, win_sim_pct, marker='s', linewidth=2, markersize=8, color='green')
        ax2.axhline(50, color='red', linestyle='--', alpha=0.5, label='50%')
        ax2.set_xlabel('Win Rate')
        ax2.set_ylabel('Winning Simulations (%)')
        ax2.set_title('Probability of Profit')
        ax2.set_ylim([0, 100])
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Plot 3: Volatility of returns
        ax3 = axes[1, 0]
        ax3.plot(win_rates, std_returns, marker='^', linewidth=2, markersize=8, color='purple')
        ax3.set_xlabel('Win Rate')
        ax3.set_ylabel('Std Dev of Returns (%)')
        ax3.set_title('Return Volatility vs Win Rate')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Mean drawdown
        ax4 = axes[1, 1]
        ax4.plot(win_rates, mean_dd, marker='d', linewidth=2, markersize=8, color='darkred')
        ax4.set_xlabel('Win Rate')
        ax4.set_ylabel('Mean Max Drawdown (%)')
        ax4.set_title('Drawdown vs Win Rate')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_price_simulation(self, prices: np.ndarray, num_paths: int = 100) -> Figure:
        """
        Plot simulated price paths.
        
        Args:
            prices: 2D array of simulated prices
            num_paths: Number of paths to plot
        
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        num_to_plot = min(num_paths, prices.shape[0])
        for i in range(num_to_plot):
            ax.plot(prices[i, :], alpha=0.3, linewidth=0.8)
        
        # Add mean and percentiles
        mean_price = np.mean(prices, axis=0)
        p5 = np.percentile(prices, 5, axis=0)
        p95 = np.percentile(prices, 95, axis=0)
        
        ax.plot(mean_price, color='darkred', linewidth=2.5, label='Mean')
        ax.fill_between(range(len(mean_price)), p5, p95, alpha=0.2, color='red', label='5th-95th percentile')
        
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Price')
        ax.set_title('Simulated Price Paths')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def _format_statistics(stats: Dict[str, float]) -> str:
        """
        Format statistics dictionary for display.
        
        Args:
            stats: Statistics dictionary
        
        Returns:
            Formatted string
        """
        lines = ["SIMULATION STATISTICS", "=" * 40]
        
        for key, value in stats.items():
            # Format the key
            display_key = key.replace('_', ' ').title()
            
            # Format the value
            if 'pct' in key or 'percentage' in key:
                display_value = f"{value:.2f}%"
            elif 'balance' in key or 'return' in key:
                display_value = f"${value:.2f}"
            else:
                display_value = f"{value:.4f}"
            
            lines.append(f"{display_key:<30} {display_value:>10}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def show():
        """Display all figures."""
        plt.show()
    
    @staticmethod
    def save_figure(fig: Figure, filename: str):
        """
        Save figure to file.
        
        Args:
            fig: Matplotlib Figure object
            filename: Output filename
        """
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {filename}")
