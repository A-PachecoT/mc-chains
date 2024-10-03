ONE_SHOT_EXAMPLE = r"""
Curso: Matemática Computacional
Método: Método de Bisección para Optimización
Contenido FINAL:

\section{Método de Bisección para Optimización}
\subsection{Descripción}
El método de bisección para optimización es un algoritmo que busca el mínimo \textbf{de una función unimodal en un intervalo cerrado}. Funciona dividiendo repetidamente el intervalo y seleccionando el subintervalo donde se encuentra el mínimo. Es un método simple y robusto, aunque puede ser relativamente lento en comparación con otros métodos más avanzados.


\textit{Observación}: Es análogo al algoritmo de Búsqueda binaria, pero en lugar de buscar un valor específico, buscamos el punto donde la función alcanza su valor mínimo.

\subsubsection{Intuición del Algoritmo}
La intuición detrás del método de bisección para optimización se basa en la naturaleza de las funciones unimodales. En una función unimodal, existe un único mínimo global en el intervalo dado. El método aprovecha esta propiedad de la siguiente manera:

\begin{itemize}
    \item Dividimos el intervalo en tres partes usando dos puntos internos.
    \item Evaluamos la función en estos puntos y en el punto medio.
    \item Comparando estos valores, podemos determinar en qué tercio del intervalo \textit{no} se encuentra el mínimo.
    \item Descartamos ese tercio y repetimos el proceso con el intervalo reducido.
\end{itemize}

En cada iteración, estamos seguros de que el mínimo se encuentra en el intervalo que conservamos. A medida que el intervalo se reduce, nos acercamos cada vez más al punto mínimo. Esta estrategia de "dividir y conquistar" nos permite converger al mínimo de manera sistemática y confiable, sin necesidad de calcular derivadas o usar información sobre la pendiente de la función.


\subsection{Algoritmo}
\begin{algorithm}
\caption{Método de Bisección para Optimización}
\begin{algorithmic}
\Procedure{BiseccionOptimizacion}{$f, a, b, \epsilon$}
    \While{$b - a > \epsilon$}
        \State $m \gets (a + b) / 2$
        \State $x_1 \gets (a + m) / 2$
        \State $x_2 \gets (m + b) / 2$
        \If{$f(x_1) < f(m)$}
            \State $b \gets m$
        \ElsIf{$f(x_2) < f(m)$}
            \State $a \gets m$
        \Else
            \State $a \gets x_1$
            \State $b \gets x_2$
        \EndIf
    \EndWhile
    \State \Return $(a + b) / 2$
\EndProcedure
\end{algorithmic}
\end{algorithm}


\subsubsection{Ejemplo paso a paso}
Supongamos que queremos encontrar el mínimo de la función
$$f(x) = (x - 2)^2 + 1$$
utilizando el método de bisección para optimización.
\begin{enumerate}
    \item \textbf{Inicialización}:
    \begin{itemize}
        \item Elegimos $a = 0$ y $b = 3$ como intervalo inicial.
    \end{itemize}
    \item \textbf{Primera Iteración}:
    \begin{itemize}
        \item Calculamos $m = (0 + 3) / 2 = 1.5$, $x_1 = (0 + 1.5) / 2 = 0.75$, $x_2 = (1.5 + 3) / 2 = 2.25$.
        \item Evaluamos $f(x_1) = 2.5625$, $f(m) = 1.25$, $f(x_2) = 1.0625$.
        \item Como $f(x_2) < f(m) < f(x_1)$, actualizamos $a = 1.5$ y $b = 3$.
    \end{itemize}
    \item \textbf{Segunda Iteración}:
    \begin{itemize}
        \item Calculamos $m = (1.5 + 3) / 2 = 2.25$, $x_1 = (1.5 + 2.25) / 2 = 1.875$, $x_2 = (2.25 + 3) / 2 = 2.625$.
        \item Evaluamos $f(x_1) = 1.015625$, $f(m) = 1.0625$, $f(x_2) = 1.390625$.
        \item Como $f(x_1) < f(m) < f(x_2)$, actualizamos $a = 1.5$ y $b = 2.25$.
    \end{itemize}
    \item \textbf{Tercera Iteración}:
    \begin{itemize}
        \item Calculamos $m = (1.5 + 2.25) / 2 = 1.875$, $x_1 = (1.5 + 1.875) / 2 = 1.6875$, $x_2 = (1.875 + 2.25) / 2 = 2.0625$.
        \item Evaluamos $f(x_1) = 1.099609375$, $f(m) = 1.015625$, $f(x_2) = 1.00390625$.
        \item Como $f(x_2) < f(m) < f(x_1)$, actualizamos $a = 1.875$ y $b = 2.25$.
    \end{itemize}
\end{enumerate}
El proceso continúa hasta que se alcance la precisión deseada o se llegue al número máximo de iteraciones permitidas.
\subsection{Código en Python}
\begin{mintedbox}{python}
def biseccion_optimizacion(f, a, b, epsilon):
    while b - a > epsilon:
        m = (a + b) / 2
        x1 = (a + m) / 2
        x2 = (m + b) / 2
        if f(x1) < f(m):
            b = m
        elif f(x2) < f(m):
            a = m
        else:
            a, b = x1, x2
    return (a + b) / 2

# Ejemplo de uso
def f(x):
    return (x - 2)**2 + 1

a = 0
b = 3
epsilon = 0.001
minimo = biseccion_optimizacion(f, a, b, epsilon)
print("El punto mínimo aproximado es:", minimo)
print("El valor mínimo aproximado es:", f(minimo))
\end{mintedbox}
\textbf{Resultado:}
\begin{lstlisting}
El punto minimo aproximado es: 1.9998779296875
El valor minimo aproximado es: 1.0000000149011612
\end{lstlisting}
"""

EXPLAIN_METHOD_PROMPT = """
{language}
Given the course "{course}" and the method "{method}", please provide a detailed explanation in LaTeX format, following the structure and style of the example below. Include the following sections:

1. Method Description
2. Algorithm Intuition
3. Algorithm in pseudocode
4. Step-by-step example
5. Python implementation

Here's an example of the expected format and level of detail:

{one_shot_example}

Now, please provide a similar explanation for the given course and method.
"""

PSEUDOCODE_PROMPT = """
{language}
Based on the explanation of the method "{method}" in the course "{course}", please provide a pseudocode representation of the method using LaTeX and the algorithm environment. Use clear and concise steps that outline the algorithm or process. Follow the style and format of the example below:

{one_shot_example}

Now, please provide the pseudocode for the given method.
"""

STEP_BY_STEP_EXAMPLE_PROMPT = """
{language}
Using the pseudocode for the method "{method}" in the course "{course}", please provide a step-by-step example of how this method would be applied to a specific problem. Use a realistic scenario and show each step of the process. Format your response in LaTeX, following the style and detail level of the example below:

{one_shot_example}

Now, please provide a step-by-step example for the given method.
"""

PYTHON_CODE_PROMPT = """
{language}
Based on the pseudocode and step-by-step example for the method "{method}" in the course "{course}", please provide a Python implementation of this method. Include comments to explain key parts of the code. Format your response using the LaTeX mintedbox environment, following the style of the example below:

{one_shot_example}

Now, please provide the Python implementation for the given method.
"""

PARSE_MARKDOWN_TO_LATEX_PROMPT = """
{language}
Given the following content that includes an explanation and pseudocode for the method "{method}" in the course "{course}", please ensure it is properly formatted in LaTeX. Make any necessary adjustments to match the style and structure of the example below:

{one_shot_example}

Here's the content to format:

{markdown_content}

Please provide the fully formatted LaTeX content for the given method.
"""

# Dictionary to store language instructions
LANGUAGE_INSTRUCTIONS = {
    "en": "Please provide the response in English.",
    "es": "Por favor, proporcione la respuesta en español.",
    # Add more languages as needed
}
