
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Índice\n",
    "\n",
    "- [Introducción](#introducción)\n",
    "- [Objetivos](#objetivos)\n",
    "- [Fundamento Teórico - Ecuación de calor](#fundamento-teórico---ecuación-de-calor)\n",
    "- [Fundamento Físico - Ecuación de calor en una dimensión](#fundamento-físico---ecuación-de-calor-en-una-dimensión)\n",
    "- [Discretización](#discretización)\n",
    "- [Método de Diferencias Finitas](#método-de-diferencias-finitas)\n",
    "- [Resultados](#resultados)\n",
    "- [Conclusiones](#conclusiones)\n",
    "- [Referencias](#referencias)\n",
    "\n",
    "---\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Introducción\n",
    "\n",
    "Describe el problema físico, la importancia de la ecuación de calor, y por qué es útil simularla numéricamente.\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Objetivos\n",
    "\n",
    "- **Objetivo General**: Desarrollar un programa en C++ que simule la ecuación de calor en una barra unidimensional utilizando el método de diferencias finitas y optimizando su rendimiento mediante la paralelización por medio de OMP.\n",
    "\n",
    "- **Objetivos Específicos**:\n",
    "  - Implementar el método de diferencias finitas para resolver la ecuación de calor.\n",
    "  - Comparar el rendimiento del código en paralelo con el código secuencial.\n",
    "  - Analizar los resultados obtenidos y su relación con la teoría.\n",
    "\n",
    "---"
   ]
  },
