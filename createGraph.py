import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import numpy as np
from resultsParser import parseHeuristicResults


def createGraph(results_file_name):
    # Create a graph which evaluators found which usability problems in a heuristic evaluation of a banking system.
    # Each row represents one of the evaluators and each column represents one of the usability problems
    # Each square shows whether the evaluator represented by the row found the usability problem represented by the column: The square is black if this is the case and white if the evaluator did not find the problem. The rows have been sorted in such a way that the most successful evaluators are at the bottom and the least successful are at the top. The columns have been sorted in such a way that the usability problems that are the easiest to find are to the right and the usability problems that are the most difficult to find are to the left.

    ordered_evaluators = []
    ordered_problems = []

    for i, evaluation in enumerate(res):
        evaluators_list = list(evaluation[0]) if type(
            evaluation[0]) == tuple else [evaluation[0]]

        for evaluator in evaluators_list:
            if evaluator not in [list(x.keys())[0] for x in ordered_evaluators]:
                ordered_evaluators.append({
                    evaluator: 1
                })
            else:
                for evaluator_dict in ordered_evaluators:
                    if list(evaluator_dict.keys())[0] == evaluator:
                        evaluator_dict[evaluator] += 1
        ordered_problems.append({
            i: len(evaluators_list)
        })

    ordered_evaluators.sort(key=lambda x: list(x.values())[0], reverse=True)
    ordered_problems.sort(key=lambda x: list(x.values())[0])

    num_evaluators = len(ordered_evaluators)
    num_problems = len(ordered_problems)

    matrix = np.zeros((num_evaluators, num_problems))
    for i, evaluator in enumerate(ordered_evaluators):
        for j, problem in enumerate(ordered_problems):
            evaluators_list = list(res[list(problem.keys())[0]][0]) if type(
                res[list(problem.keys())[0]][0]) == tuple else [res[list(problem.keys())[0]][0]]
            if list(evaluator.keys())[0] in evaluators_list:
                matrix[i, j] = 1

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define the size of each square
    square_size = 1

    # Create white squares with padding
    for i in range(num_evaluators):
        for j in range(num_problems):
            problem_index = list(ordered_problems[j].keys())[0]
            if matrix[i, j] == 1:
                rect = plt.Rectangle((j - 0.5, i - 0.5), square_size,
                                     square_size, facecolor='black', edgecolor='white')
                ax.text(j, i, res[problem_index][1][i],
                        va='center', ha='center', color='white')
            else:
                rect = plt.Rectangle((j - 0.5, i - 0.5), square_size,
                                     square_size, facecolor='white', edgecolor='white')
                ax.text(j, i, res[problem_index][1][i],
                        va='center', ha='center', color='black')
            ax.add_patch(rect)
    # Set the x-axis label
    ax.set_xlabel("Usability Problems\n" + r'$Hard \longleftrightarrow Easy$')

    # Set the y-axis label on the right
    ax.set_ylabel("Evaluators\n" +
                  r'$Successful \longleftrightarrow Unsuccesful$')
    ax.yaxis.set_label_position("right")

    # Adjust the axis limits and aspect ratio
    ax.set_xlim(-0.5, num_problems - 0.5)
    ax.set_ylim(num_evaluators - 0.5, -0.5)
    ax.set_aspect('equal')

    # Invert the y-axis to match your desired layout
    ax.yaxis.tick_right()
    ax.invert_yaxis()

    # Set the y-axis tick labels
    ax.set_yticks(np.arange(num_evaluators))
    ax.set_yticklabels([list(evaluator.keys())[0]
                        for evaluator in ordered_evaluators])

    # Remove ticks, tick labels and grid
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)

    # Display the heatmap
    plt.show()

    # Save the graph
    # Get the tight bounding box of the graph
    tight_bbox = ax.get_tightbbox(fig.canvas.get_renderer())

    # Adjust the bounding box to add vertical padding for the labels
    # Unneccessary if the vertical labels are removed or smaller than the graph
    tight_bbox.y0 -= 25
    tight_bbox.y1 += 75
    
    tight_bbox.x0 -= 10
    tight_bbox.x1 += 10
    
    # Save the graph with the adjusted bounding box
    fig.savefig('graph.png', dpi=300, bbox_inches=tight_bbox.transformed(fig.dpi_scale_trans.inverted()))


if __name__ == "__main__":
    res = parseHeuristicResults("example.txt")
    createGraph(res)
