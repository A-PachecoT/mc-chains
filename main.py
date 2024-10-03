import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.base import Chain
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List
from pydantic import Field
from prompts import (
    DESCRIPTION_PROMPT,
    INTUITION_PROMPT,
    ALGORITHM_PROMPT,
    STEP_BY_STEP_EXAMPLE_PROMPT,
    PYTHON_CODE_PROMPT,
    LANGUAGE_INSTRUCTIONS,
    ONE_SHOT_EXAMPLE,
)
import datetime

# Load environment variables
load_dotenv()

# Initialize the ChatOpenAI LLM
llm = ChatOpenAI(temperature=0.3)


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
        return ["latex_content"]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        course = inputs["course"]
        method = inputs["method"]

        # Create the sequential chain using LCEL
        chain = RunnableSequence(
            RunnablePassthrough(),
            {
                "description": PromptTemplate(
                    input_variables=[
                        "language",
                        "course",
                        "method",
                        "one_shot_example",
                    ],
                    template=DESCRIPTION_PROMPT,
                )
                | llm
                | StrOutputParser(),
            },
            {
                "intuition": lambda x: (
                    PromptTemplate(
                        input_variables=[
                            "language",
                            "course",
                            "method",
                            "description",
                            "one_shot_example",
                        ],
                        template=INTUITION_PROMPT,
                    )
                    | llm
                    | StrOutputParser()
                ).invoke({**x, "description": x["description"]}),
                "description": lambda x: x["description"],
            },
            {
                "algorithm": lambda x: (
                    PromptTemplate(
                        input_variables=[
                            "language",
                            "course",
                            "method",
                            "description",
                            "intuition",
                            "one_shot_example",
                        ],
                        template=ALGORITHM_PROMPT,
                    )
                    | llm
                    | StrOutputParser()
                ).invoke(
                    {**x, "description": x["description"], "intuition": x["intuition"]}
                ),
                "description": lambda x: x["description"],
                "intuition": lambda x: x["intuition"],
            },
            {
                "step_by_step": lambda x: (
                    PromptTemplate(
                        input_variables=[
                            "language",
                            "course",
                            "method",
                            "algorithm",
                            "one_shot_example",
                        ],
                        template=STEP_BY_STEP_EXAMPLE_PROMPT,
                    )
                    | llm
                    | StrOutputParser()
                ).invoke({**x, "algorithm": x["algorithm"]}),
                "algorithm": lambda x: x["algorithm"],
                "description": lambda x: x["description"],
                "intuition": lambda x: x["intuition"],
            },
            {
                "python_code": lambda x: (
                    PromptTemplate(
                        input_variables=[
                            "language",
                            "course",
                            "method",
                            "algorithm",
                            "step_by_step",
                            "one_shot_example",
                        ],
                        template=PYTHON_CODE_PROMPT,
                    )
                    | llm
                    | StrOutputParser()
                ).invoke(
                    {
                        **x,
                        "algorithm": x["algorithm"],
                        "step_by_step": x["step_by_step"],
                    }
                ),
                "step_by_step": lambda x: x["step_by_step"],
                "algorithm": lambda x: x["algorithm"],
                "description": lambda x: x["description"],
                "intuition": lambda x: x["intuition"],
            },
        )
        # Execute the sequential chain
        results = chain.invoke(
            {
                "language": self.language_instruction,
                "course": course,
                "method": method,
                "one_shot_example": self.one_shot_example,
            }
        )

        # Combine all sections into a single LaTeX document
        latex_content = f"""
\\section{{{method}}}
{results["description"]}
{results["intuition"]}
{results["algorithm"]}
{results["step_by_step"]}
{results["python_code"]}
"""

        return {"latex_content": latex_content}


def generate_latex_file(latex_content: str, filename: str):
    with open(filename, "w") as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage{amsmath}" + "\n")
        f.write(r"\usepackage{algorithm}" + "\n")
        f.write(r"\usepackage{algpseudocode}" + "\n")
        f.write(r"\usepackage{minted}" + "\n")
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

    course = "Matemática Computacional - Optimización con Restricciones"
    method = "Método del Punto Interior"

    results = explainer.invoke({"course": course, "method": method})

    print("\nContenido LaTeX generado:")
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
