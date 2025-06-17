import matplotlib.pyplot as plt 
from langchain.tools import tool
import uuid
import ast
import matplotlib.cm as cm
import numpy as np

@tool
def plot_chart(data_dict: str, title: str = "Chart", chart_type: str = "bar") -> str:
    """
    Generates a bar or pie chart from a dictionary input string.
    Parameters:
        data_dict: Dictionary-like string, e.g. "{'Apples': 10, 'Bananas': 20}"
        title: Title of the chart
        chart_type: 'bar' or 'pie'
    Returns the file path of the saved chart image.
    """
    try:
        # Parse and validate input
        data = ast.literal_eval(data_dict)
        if not isinstance(data, dict):
            return "Input must be a dictionary-like string."

        labels = list(data.keys())
        values = list(data.values())

        # Generate color map with enough colors
        cmap = cm.get_cmap('tab20')
        colors = [cmap(i / len(labels)) for i in range(len(labels))]

        plt.figure(figsize=(8, 6))

        if chart_type == "pie":
            plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
            plt.title(title)
        elif chart_type == "bar":
            plt.bar(labels, values, color=colors)
            plt.title(title)
            plt.xlabel("Items")
            plt.ylabel("Values")
        else:
            return "Invalid chart_type. Use 'bar' or 'pie'."

        plt.tight_layout()

        # Save to unique filename
        filename = f"{chart_type}_chart_{uuid.uuid4().hex[:8]}.png"
        plt.savefig(filename)
        plt.close()

        return f"{chart_type.capitalize()} chart saved to: {filename}"
    
    except Exception as e:
        return f"Error generating chart: {e}"


print(plot_chart.invoke({"data_dict": "{'Math': 80, 'Science': 90, 'English': 75}", "title" : "Subject Scores", "chart_type":"bar"}))

print (plot_chart.invoke({
    "data_dict": "{'Chrome': 50, 'Safari': 30, 'Firefox': 20}",
    "title": "Browser Usage",
    "chart_type": "pie"
}))


print(plot_chart.args_schema.model_json_schema())