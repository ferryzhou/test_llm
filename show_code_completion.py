import inspect
from typing import Optional, List, Dict

def generate_code_prompt(
    existing_code: str,
    task_description: str,
    function_name: Optional[str] = None,
    context_lines: int = 5
) -> str:
    """
    Generates a structured prompt for AI code generation based on existing code context
    and task description.
    
    Args:
        existing_code: The current content of the Python file
        task_description: Description of what needs to be implemented
        function_name: Optional name of the function to be generated
        context_lines: Number of context lines to include before/after relevant sections
    
    Returns:
        A formatted prompt string for the AI model
    """
    # Extract imports and context
    imports = []
    relevant_context = []
    
    for line in existing_code.split('\n'):
        if line.startswith('import ') or line.startswith('from '):
            imports.append(line)
        # Add relevant context based on function name if provided
        if function_name and function_name.lower() in line.lower():
            start_idx = max(0, existing_code.split('\n').index(line) - context_lines)
            end_idx = min(len(existing_code.split('\n')), 
                         existing_code.split('\n').index(line) + context_lines)
            relevant_context = existing_code.split('\n')[start_idx:end_idx]

    # Build the structured prompt
    prompt_parts = [
        "# Task: Generate Python code based on the following requirements",
        "\n## Context",
        "Existing imports:",
        "\n".join(imports) if imports else "No existing imports",
        "\nRelevant code context:",
        "\n".join(relevant_context) if relevant_context else "No relevant context found",
        "\n## Requirements",
        f"Task description: {task_description}",
    ]
    
    if function_name:
        prompt_parts.extend([
            f"\nFunction name to implement: {function_name}",
            "\nPlease implement this function following Python best practices:",
            "- Include type hints",
            "- Add comprehensive docstring",
            "- Follow PEP 8 style guidelines",
            "- Include error handling where appropriate",
            "- Add comments for complex logic"
        ])
    
    prompt_parts.append("\n## Generated Code")
    prompt_parts.append("Please provide the implementation below:")
    
    return "\n\n".join(prompt_parts)

# Example usage
def example_prompt_generation():
    # Sample existing code
    existing_code = """
import pandas as pd
from typing import List, Dict

def process_data(data: pd.DataFrame) -> Dict:
    # Process the data
    return {"result": "processed"}
    
def validate_input(data: pd.DataFrame) -> bool:
    return len(data) > 0
"""
    
    task = "Create a function to aggregate data by category and calculate statistics"
    function_name = "aggregate_by_category"
    
    prompt = generate_code_prompt(
        existing_code=existing_code,
        task_description=task,
        function_name=function_name
    )
    return prompt

if __name__ == "__main__":
    # Generate and print an example prompt
    example_prompt = example_prompt_generation()
    print(example_prompt)