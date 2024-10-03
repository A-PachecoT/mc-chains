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

DESCRIPTION_PROMPT = """
{language}
Proporcione una descripción detallada del método "{method}" en el curso "{course}" en formato LaTeX. Incluya una explicación general del método, su propósito y sus características principales. Use notación matemática cuando sea apropiado.

Ejemplo de formato y nivel de detalle:

{one_shot_example}

Genere solo la subsección de Descripción, siguiendo el estilo y formato del ejemplo.
"""

INTUITION_PROMPT = """
{language}
Basándose en la descripción proporcionada, explique la intuición detrás del algoritmo "{method}" en el curso "{course}" en formato LaTeX. Incluya una explicación de cómo funciona el método conceptualmente y por qué es efectivo.

Descripción previa:
{description}

Ejemplo de formato y nivel de detalle:

{one_shot_example}

Genere solo la subsección de Intuición del Algoritmo, siguiendo el estilo y formato del ejemplo.
"""

ALGORITHM_PROMPT = """
{language}
Proporcione el algoritmo formal para el método "{method}" en el curso "{course}" en formato LaTeX, utilizando el entorno 'algorithm' y 'algorithmic'. Asegúrese de que el algoritmo sea preciso y refleje la descripción e intuición proporcionadas.

Descripción e intuición previas:
{description}
{intuition}

Ejemplo de formato y nivel de detalle:

{one_shot_example}

Genere solo la subsección del Algoritmo, siguiendo el estilo y formato del ejemplo.
"""

STEP_BY_STEP_EXAMPLE_PROMPT = """
{language}
Proporcione un ejemplo paso a paso detallado de cómo se aplica el método "{method}" en el curso "{course}" a un problema específico. Use notación matemática y explique cada paso claramente.

Algoritmo:
{algorithm}

Ejemplo de formato y nivel de detalle:

{one_shot_example}

Genere solo la subsección de Ejemplo paso a paso, siguiendo el estilo y formato del ejemplo.
"""

PYTHON_CODE_PROMPT = """
{language}
Basándose en el algoritmo y el ejemplo paso a paso, proporcione una implementación en Python del método "{method}" para el curso "{course}". Incluya comentarios explicativos y use el entorno 'mintedbox' de LaTeX para el código.

Algoritmo y ejemplo paso a paso:
{algorithm}
{step_by_step}

Ejemplo de formato y nivel de detalle:

{one_shot_example}

Genere solo la subsección de Código en Python, siguiendo el estilo y formato del ejemplo.
"""

LANGUAGE_INSTRUCTIONS = {
    "en": "Please provide the response in English.",
    "es": "Por favor, proporcione la respuesta en español.",
}
