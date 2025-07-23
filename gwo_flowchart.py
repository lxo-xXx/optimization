import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_gwo_flowchart():
    """Create a flowchart for the Multi-Objective Grey Wolf Optimization algorithm"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 16))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 20)
    ax.axis('off')
    
    # Define box style
    box_style = "round,pad=0.1"
    
    # Helper function to create boxes
    def create_box(x, y, width, height, text, color='lightblue'):
        box = FancyBboxPatch((x-width/2, y-height/2), width, height,
                           boxstyle=box_style, facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, weight='bold', wrap=True)
    
    # Helper function to create diamond (decision)
    def create_diamond(x, y, width, height, text, color='yellow'):
        diamond = patches.RegularPolygon((x, y), 4, radius=width/2, 
                                       orientation=np.pi/4, facecolor=color, 
                                       edgecolor='black', linewidth=1.5)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, weight='bold')
    
    # Helper function to create arrows
    def create_arrow(x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        if text:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=8, weight='bold')
    
    # Title
    ax.text(5, 19.5, 'Multi-Objective Grey Wolf Optimization (MOGWO) Flowchart', 
            ha='center', va='center', fontsize=14, weight='bold')
    
    # Flowchart elements
    y_pos = 18.5
    
    # Start
    create_box(5, y_pos, 2, 0.6, 'START', 'lightgreen')
    y_pos -= 1
    create_arrow(5, 18.2, 5, 17.8)
    
    # Initialize parameters
    create_box(5, y_pos, 3.5, 0.8, 'Initialize Parameters:\nn_wolves, max_iterations,\narchive_size, bounds', 'lightblue')
    y_pos -= 1.2
    create_arrow(5, 17.1, 5, 16.5)
    
    # Initialize population
    create_box(5, y_pos, 3, 0.8, 'Initialize Wolf Population\nRandomly', 'lightblue')
    y_pos -= 1.2
    create_arrow(5, 15.9, 5, 15.3)
    
    # Evaluate initial population
    create_box(5, y_pos, 3, 0.8, 'Evaluate Fitness for\nEach Wolf', 'lightblue')
    y_pos -= 1.2
    create_arrow(5, 14.7, 5, 14.1)
    
    # Initialize archive
    create_box(5, y_pos, 3, 0.8, 'Initialize Archive with\nNon-dominated Solutions', 'lightblue')
    y_pos -= 1.2
    create_arrow(5, 13.5, 5, 12.9)
    
    # Set iteration counter
    create_box(5, y_pos, 2.5, 0.6, 'Set t = 0', 'lightblue')
    y_pos -= 1
    create_arrow(5, 12.6, 5, 12.1)
    
    # Main loop condition
    create_diamond(5, y_pos, 1.8, 0.8, 't < max_iter?', 'yellow')
    y_pos -= 1.5
    create_arrow(5, 11.6, 5, 10.6, 'Yes')
    create_arrow(6.2, 11.5, 8.5, 11.5)
    create_arrow(8.5, 11.5, 8.5, 2)
    create_arrow(8.5, 2, 5, 2, 'No')
    
    # Select leaders from archive
    create_box(5, y_pos, 3.5, 0.8, 'Select α, β, δ Leaders\nfrom Archive', 'lightcoral')
    y_pos -= 1.2
    create_arrow(5, 10, 5, 9.4)
    
    # Update wolf positions
    create_box(5, y_pos, 3.5, 1, 'Update Position of Each Wolf\nBased on α, β, δ:\nX(t+1) = (X₁ + X₂ + X₃)/3', 'lightcoral')
    y_pos -= 1.4
    create_arrow(5, 8.6, 5, 7.8)
    
    # Evaluate new positions
    create_box(5, y_pos, 3, 0.8, 'Evaluate Fitness of\nNew Positions', 'lightcoral')
    y_pos -= 1.2
    create_arrow(5, 7.2, 5, 6.6)
    
    # Update archive
    create_box(5, y_pos, 3.5, 1, 'Update Archive:\n- Remove dominated solutions\n- Add non-dominated solutions\n- Apply crowding distance', 'lightcoral')
    y_pos -= 1.4
    create_arrow(5, 5.8, 5, 5.2)
    
    # Update iteration
    create_box(5, y_pos, 2, 0.6, 't = t + 1', 'lightcoral')
    y_pos -= 1
    create_arrow(5, 4.6, 5, 4.2)
    
    # Loop back arrow
    create_arrow(5, 4.2, 2, 4.2)
    create_arrow(2, 4.2, 2, 11.5)
    create_arrow(2, 11.5, 4.1, 11.5)
    
    # Output results
    create_box(5, 1.5, 3, 0.8, 'Output Pareto Front\n(Archive Solutions)', 'lightgreen')
    create_arrow(5, 2.3, 5, 1.9)
    
    # End
    create_box(5, 0.5, 1.5, 0.6, 'END', 'lightgreen')
    create_arrow(5, 1.1, 5, 0.8)
    
    # Add legend
    legend_x = 0.5
    legend_y = 3
    ax.text(legend_x, legend_y + 0.5, 'Legend:', fontsize=10, weight='bold')
    
    create_box(legend_x + 0.3, legend_y, 0.4, 0.3, '', 'lightblue')
    ax.text(legend_x + 0.8, legend_y, 'Process', fontsize=8)
    
    create_diamond(legend_x + 0.3, legend_y - 0.5, 0.6, 0.3, '', 'yellow')
    ax.text(legend_x + 0.8, legend_y - 0.5, 'Decision', fontsize=8)
    
    create_box(legend_x + 0.3, legend_y - 1, 0.4, 0.3, '', 'lightcoral')
    ax.text(legend_x + 0.8, legend_y - 1, 'Main Loop', fontsize=8)
    
    create_box(legend_x + 0.3, legend_y - 1.5, 0.4, 0.3, '', 'lightgreen')
    ax.text(legend_x + 0.8, legend_y - 1.5, 'Start/End', fontsize=8)
    
    plt.title('Multi-Objective Grey Wolf Optimization Algorithm Flowchart', 
              fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('MOGWO_Flowchart.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_modification_flowchart():
    """Create a flowchart showing the modifications made to the standard GWO"""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Define box style
    box_style = "round,pad=0.1"
    
    def create_box(x, y, width, height, text, color='lightblue'):
        box = FancyBboxPatch((x-width/2, y-height/2), width, height,
                           boxstyle=box_style, facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, weight='bold', wrap=True)
    
    # Title
    ax.text(5, 13.5, 'Modifications to Standard GWO for Multi-Objective Optimization', 
            ha='center', va='center', fontsize=14, weight='bold')
    
    y_pos = 12.5
    
    # Standard GWO
    create_box(2.5, y_pos, 4, 1.2, 'Standard GWO:\n- Single objective\n- Three best solutions (α, β, δ)\n- Direct fitness comparison', 'lightcyan')
    
    # Arrow
    ax.annotate('', xy=(7.5, y_pos), xytext=(4.5, y_pos),
               arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax.text(6, y_pos + 0.3, 'Modifications', ha='center', fontsize=10, weight='bold', color='red')
    
    # Modified MOGWO
    create_box(7.5, y_pos, 4, 1.2, 'Multi-Objective GWO:\n- Multiple objectives\n- Pareto dominance\n- External archive', 'lightgreen')
    
    y_pos -= 2
    
    # Modification 1: Pareto Dominance
    create_box(5, y_pos, 8, 1, 'Modification 1: Pareto Dominance Concept\nReplace single fitness comparison with Pareto dominance\nSolution A dominates B if A is better in all objectives', 'lightyellow')
    
    y_pos -= 1.8
    
    # Modification 2: External Archive
    create_box(5, y_pos, 8, 1, 'Modification 2: External Archive\nMaintain archive of non-dominated solutions\nUse crowding distance to maintain diversity', 'lightyellow')
    
    y_pos -= 1.8
    
    # Modification 3: Leader Selection
    create_box(5, y_pos, 8, 1, 'Modification 3: Leader Selection Strategy\nSelect α, β, δ from archive (Pareto optimal solutions)\nRandom selection to maintain diversity', 'lightyellow')
    
    y_pos -= 1.8
    
    # Modification 4: Archive Management
    create_box(5, y_pos, 8, 1.2, 'Modification 4: Archive Management\n- Remove dominated solutions\n- Add non-dominated solutions\n- Apply crowding distance for size control', 'lightyellow')
    
    y_pos -= 2
    
    # Result
    create_box(5, y_pos, 6, 0.8, 'Result: Pareto Front of Optimal Solutions', 'lightgreen')
    
    plt.tight_layout()
    plt.savefig('MOGWO_Modifications.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Creating Multi-Objective GWO Flowcharts...")
    create_gwo_flowchart()
    create_modification_flowchart()
    print("Flowcharts saved as MOGWO_Flowchart.png and MOGWO_Modifications.png")