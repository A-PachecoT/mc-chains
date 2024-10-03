import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.base import Chain
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from typing import Dict, List
from pydantic import Field
from prompts import (
    EXPLAIN_METHOD_PROMPT,
    PSEUDOCODE_PROMPT,
    STEP_BY_STEP_EXAMPLE_PROMPT,
    PYTHON_CODE_PROMPT,
    PARSE_MARKDOWN_TO_LATEX_PROMPT,
    LANGUAGE_INSTRUCTIONS,
    ONE_SHOT_EXAMPLE,
)
import datetime

# Load environment variables
load_dotenv()

# Initialize the ChatOpenAI LLM
llm = ChatOpenAI(temperature=0.7)


class MethodExplainer(Chain):
    language: str = Field(default="en")
    language_instruction: str = Field(
        default_factory=lambda: LANGUAGE_INSTRUCTIONS["en"]
    )
    one_shot_example: str = Field(default=ONE_SHOT_EXAMPLE)

    @property
    def input_keys(self) -> List[str]:
        return ["course", "method"]

    @property
    def output_keys(self) -> List[str]:
        return ["explanation", "pseudocode", "example", "python_code", "latex_content"]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        course = inputs["course"]
        method = inputs["method"]

        # Create individual chains using the pipe syntax
        explain_chain = (
            PromptTemplate(
                input_variables=["language", "course", "method", "one_shot_example"],
                template=EXPLAIN_METHOD_PROMPT,
            )
            | llm
        )

        pseudocode_chain = (
            PromptTemplate(
                input_variables=["language", "course", "method", "one_shot_example"],
                template=PSEUDOCODE_PROMPT,
            )
            | llm
        )

        example_chain = (
            PromptTemplate(
                input_variables=["language", "course", "method", "one_shot_example"],
                template=STEP_BY_STEP_EXAMPLE_PROMPT,
            )
            | llm
        )

        python_code_chain = (
            PromptTemplate(
                input_variables=["language", "course", "method", "one_shot_example"],
                template=PYTHON_CODE_PROMPT,
            )
            | llm
        )

        parse_to_latex_chain = (
            PromptTemplate(
                input_variables=[
                    "language",
                    "course",
                    "method",
                    "markdown_content",
                    "one_shot_example",
                ],
                template=PARSE_MARKDOWN_TO_LATEX_PROMPT,
            )
            | llm
        )

        # Create the parallel chain
        overall_chain = RunnableParallel(
            explanation=explain_chain,
            pseudocode=pseudocode_chain,
            example=example_chain,
            python_code=python_code_chain,
        )

        # Execute the parallel chain
        results = overall_chain.invoke(
            {
                "language": self.language_instruction,
                "course": course,
                "method": method,
                "one_shot_example": self.one_shot_example,
            }
        )

        # Parse the markdown to LaTeX
        latex_results = parse_to_latex_chain.invoke(
            {
                "language": self.language_instruction,
                "course": course,
                "method": method,
                "markdown_content": results["explanation"]
                + "\n\n"
                + results["pseudocode"],
                "one_shot_example": self.one_shot_example,
            }
        )

        results["latex_content"] = latex_results

        return results


def generate_latex_file(latex_content: str, filename: str):
    with open(filename, "w") as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage{amsmath}" + "\n")
        f.write(r"\usepackage{algorithm}" + "\n")
        f.write(r"\usepackage{algpseudocode}" + "\n")
        f.write(r"\begin{document}" + "\n\n")
        f.write(latex_content)
        f.write(r"\end{document}")


def main():
    language = "es"  # Set to Spanish
    explainer = MethodExplainer(
        language=language,
        language_instruction=LANGUAGE_INSTRUCTIONS[language],
        one_shot_example=ONE_SHOT_EXAMPLE,
    )

    course = "Computational Mathematics"
    method = "Interior Point Method"

    results = explainer.invoke({"course": course, "method": method})

    print("\nExplicación:")
    print(results["explanation"])

    print("\nPseudocódigo:")
    print(results["pseudocode"])

    print("\nEjemplo paso a paso:")
    print(results["example"])

    print("\nCódigo Python:")
    print(results["python_code"])

    print("\nContenido LaTeX:")
    print(results["latex_content"])

    # Create a log folder if it doesn't exist
    log_folder = "log"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Generate LaTeX file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    latex_filename = f"{course}_{method}_{timestamp}.tex".replace(" ", "_").lower()
    latex_filepath = os.path.join(log_folder, latex_filename)
    generate_latex_file(results["latex_content"], latex_filepath)
    print(f"\nArchivo LaTeX generado: {latex_filepath}")


if __name__ == "__main__":
    main()
