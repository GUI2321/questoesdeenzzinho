from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import random
import hashlib


class Difficulty(Enum):
    FACIL = "facil"
    MEDIO = "medio"
    DIFICIL = "dificil"


@dataclass
class Topic:
    id: str
    name: str
    description: str
    subtopics: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)


@dataclass
class Volume:
    id: int
    name: str
    description: str
    topics: List[Topic] = field(default_factory=list)


CURRICULUM = {
    1: Volume(
        id=1,
        name="Conjuntos, Lógica e Funções Básicas",
        description="Fundamentos da teoria dos conjuntos, lógica matemática e introdução ao estudo de funções",
        topics=[
            Topic(
                id="1.1",
                name="Noções de Lógica",
                description="Proposições, conectivos lógicos, tabelas-verdade, equivalências e quantificadores",
                subtopics=["Proposições", "Negação", "Conjunção e Disjunção", "Condicionais", "Bicondicional", "Tautologias", "Quantificadores"],
                concepts=["proposição", "valor lógico", "conectivo", "tabela-verdade", "implicação", "equivalência", "quantificador universal", "quantificador existencial"]
            ),
            Topic(
                id="1.2",
                name="Teoria dos Conjuntos",
                description="Definições, operações e propriedades de conjuntos",
                subtopics=["Definições de Conjuntos", "Subconjuntos", "União e Interseção", "Diferença e Complementar", "Propriedades"],
                concepts=["conjunto", "elemento", "pertinência", "inclusão", "conjunto vazio", "conjunto universo", "união", "interseção", "diferença", "complementar", "diagrama de Venn"]
            ),
            Topic(
                id="1.3",
                name="Conjuntos Numéricos",
                description="Naturais, inteiros, racionais, irracionais e reais",
                subtopics=["Números Naturais", "Números Inteiros", "Números Racionais", "Números Irracionais", "Números Reais", "Intervalos"],
                concepts=["número natural", "número inteiro", "número racional", "número irracional", "número real", "reta numérica", "intervalo aberto", "intervalo fechado"]
            ),
            Topic(
                id="1.4",
                name="Relações e Funções",
                description="Conceito de função, domínio, imagem e gráficos",
                subtopics=["Par Ordenado", "Produto Cartesiano", "Relações", "Definição de Função", "Domínio e Imagem", "Gráficos"],
                concepts=["par ordenado", "produto cartesiano", "relação binária", "função", "domínio", "contradomínio", "imagem", "gráfico de função"]
            ),
            Topic(
                id="1.5",
                name="Função Afim",
                description="Função do primeiro grau, crescimento, decrescimento e aplicações",
                subtopics=["Definição", "Coeficientes", "Gráfico", "Zero da Função", "Crescimento e Decrescimento", "Inequações"],
                concepts=["função afim", "coeficiente angular", "coeficiente linear", "reta", "zero da função", "função crescente", "função decrescente"]
            ),
            Topic(
                id="1.6",
                name="Função Quadrática",
                description="Função do segundo grau, parábola, vértice e aplicações",
                subtopics=["Definição", "Gráfico e Parábola", "Raízes", "Vértice", "Estudo do Sinal", "Inequações"],
                concepts=["função quadrática", "parábola", "concavidade", "vértice", "discriminante", "raízes", "forma fatorada", "forma canônica"]
            ),
            Topic(
                id="1.7",
                name="Função Modular",
                description="Módulo de um número real e função modular",
                subtopics=["Definição de Módulo", "Propriedades", "Função Modular", "Equações Modulares", "Inequações Modulares"],
                concepts=["valor absoluto", "módulo", "distância", "equação modular", "inequação modular"]
            ),
            Topic(
                id="1.8",
                name="Composição e Inversão",
                description="Composição de funções, função inversa e bijeções",
                subtopics=["Composição", "Função Injetora", "Função Sobrejetora", "Função Bijetora", "Função Inversa"],
                concepts=["composição de funções", "função injetora", "função sobrejetora", "função bijetora", "função inversa"]
            ),
        ]
    ),
    2: Volume(
        id=2,
        name="Potências, Raízes, Logaritmos e Exponenciais",
        description="Estudo aprofundado de potenciação, radiciação, funções exponenciais e logarítmicas",
        topics=[
            Topic(
                id="2.1",
                name="Potenciação",
                description="Potências com expoentes naturais, inteiros, racionais e reais",
                subtopics=["Expoente Natural", "Expoente Inteiro", "Expoente Racional", "Expoente Real", "Propriedades"],
                concepts=["potência", "base", "expoente", "potência de expoente negativo", "raiz enésima", "potência de expoente fracionário"]
            ),
            Topic(
                id="2.2",
                name="Radiciação",
                description="Raízes e suas propriedades",
                subtopics=["Raiz Quadrada", "Raiz Cúbica", "Raiz Enésima", "Propriedades", "Racionalização"],
                concepts=["radical", "índice", "radicando", "radical aritmético", "racionalização"]
            ),
            Topic(
                id="2.3",
                name="Função Exponencial",
                description="Definição, propriedades, gráfico e equações exponenciais",
                subtopics=["Definição", "Gráfico", "Propriedades", "Equações Exponenciais", "Inequações Exponenciais"],
                concepts=["função exponencial", "base", "crescimento exponencial", "decaimento exponencial", "equação exponencial"]
            ),
            Topic(
                id="2.4",
                name="Logaritmos",
                description="Definição, propriedades e cálculo com logaritmos",
                subtopics=["Definição", "Consequências da Definição", "Propriedades Operatórias", "Mudança de Base"],
                concepts=["logaritmo", "logaritmando", "base do logaritmo", "logaritmo decimal", "logaritmo natural", "propriedades dos logaritmos"]
            ),
            Topic(
                id="2.5",
                name="Função Logarítmica",
                description="Definição, gráfico e aplicações",
                subtopics=["Definição", "Gráfico", "Propriedades", "Equações Logarítmicas", "Inequações Logarítmicas"],
                concepts=["função logarítmica", "gráfico logarítmico", "equação logarítmica", "inequação logarítmica"]
            ),
        ]
    ),
    3: Volume(
        id=3,
        name="Trigonometria",
        description="Trigonometria no triângulo retângulo, no ciclo e funções trigonométricas",
        topics=[
            Topic(
                id="3.1",
                name="Trigonometria no Triângulo Retângulo",
                description="Razões trigonométricas básicas no triângulo retângulo",
                subtopics=["Seno", "Cosseno", "Tangente", "Relações Fundamentais", "Ângulos Notáveis"],
                concepts=["seno", "cosseno", "tangente", "cateto oposto", "cateto adjacente", "hipotenusa", "ângulos notáveis"]
            ),
            Topic(
                id="3.2",
                name="Arcos e Ângulos",
                description="Medidas de arcos, conversões e ciclo trigonométrico",
                subtopics=["Graus", "Radianos", "Conversões", "Ciclo Trigonométrico", "Arcos Côngruos"],
                concepts=["arco", "ângulo", "grau", "radiano", "ciclo trigonométrico", "arco côngruo"]
            ),
            Topic(
                id="3.3",
                name="Funções Trigonométricas",
                description="Seno, cosseno, tangente e suas propriedades como funções",
                subtopics=["Função Seno", "Função Cosseno", "Função Tangente", "Gráficos", "Período e Amplitude"],
                concepts=["função seno", "função cosseno", "função tangente", "período", "amplitude", "fase"]
            ),
            Topic(
                id="3.4",
                name="Identidades Trigonométricas",
                description="Fórmulas de adição, subtração, duplicação e transformações",
                subtopics=["Fórmulas de Adição", "Fórmulas de Subtração", "Arco Duplo", "Arco Metade", "Transformações em Produto"],
                concepts=["identidade trigonométrica", "fórmula de adição", "arco duplo", "arco metade"]
            ),
            Topic(
                id="3.5",
                name="Equações Trigonométricas",
                description="Resolução de equações envolvendo funções trigonométricas",
                subtopics=["Equações Fundamentais", "Equações Redutíveis", "Sistemas Trigonométricos"],
                concepts=["equação trigonométrica", "solução geral", "conjunto solução"]
            ),
            Topic(
                id="3.6",
                name="Lei dos Senos e Cossenos",
                description="Resolução de triângulos quaisquer",
                subtopics=["Lei dos Senos", "Lei dos Cossenos", "Resolução de Triângulos", "Área do Triângulo"],
                concepts=["lei dos senos", "lei dos cossenos", "circunraio", "área por seno"]
            ),
        ]
    ),
    4: Volume(
        id=4,
        name="Sequências, Matrizes e Sistemas Lineares",
        description="Progressões aritméticas e geométricas, matrizes e sistemas",
        topics=[
            Topic(
                id="4.1",
                name="Sequências Numéricas",
                description="Conceito de sequência e lei de formação",
                subtopics=["Definição", "Lei de Formação", "Sequências Recursivas"],
                concepts=["sequência", "termo geral", "lei de formação", "sequência recursiva"]
            ),
            Topic(
                id="4.2",
                name="Progressão Aritmética",
                description="PA, termo geral, soma dos termos e propriedades",
                subtopics=["Definição", "Termo Geral", "Soma dos Termos", "Propriedades", "Interpolação"],
                concepts=["progressão aritmética", "razão", "termo geral", "soma de PA", "média aritmética"]
            ),
            Topic(
                id="4.3",
                name="Progressão Geométrica",
                description="PG, termo geral, soma dos termos e limite",
                subtopics=["Definição", "Termo Geral", "Soma Finita", "Soma Infinita", "Propriedades"],
                concepts=["progressão geométrica", "razão", "termo geral", "soma de PG", "PG infinita"]
            ),
            Topic(
                id="4.4",
                name="Matrizes",
                description="Definição, tipos, operações e aplicações",
                subtopics=["Definição", "Tipos de Matrizes", "Operações", "Matriz Transposta", "Matriz Inversa"],
                concepts=["matriz", "elemento", "linha", "coluna", "matriz quadrada", "matriz identidade", "transposta", "inversa"]
            ),
            Topic(
                id="4.5",
                name="Determinantes",
                description="Cálculo de determinantes e propriedades",
                subtopics=["Determinante 2x2", "Determinante 3x3", "Regra de Sarrus", "Propriedades", "Teorema de Laplace"],
                concepts=["determinante", "menor complementar", "cofator", "regra de Sarrus", "Laplace"]
            ),
            Topic(
                id="4.6",
                name="Sistemas Lineares",
                description="Resolução e classificação de sistemas lineares",
                subtopics=["Definição", "Regra de Cramer", "Escalonamento", "Discussão de Sistemas"],
                concepts=["sistema linear", "solução", "sistema possível", "sistema impossível", "sistema indeterminado", "Cramer"]
            ),
        ]
    ),
    5: Volume(
        id=5,
        name="Análise Combinatória e Probabilidade",
        description="Princípios de contagem, arranjos, combinações e cálculo de probabilidades",
        topics=[
            Topic(
                id="5.1",
                name="Princípio Fundamental da Contagem",
                description="Princípio multiplicativo e aplicações",
                subtopics=["Princípio Multiplicativo", "Princípio Aditivo", "Árvore de Possibilidades"],
                concepts=["princípio multiplicativo", "princípio aditivo", "contagem"]
            ),
            Topic(
                id="5.2",
                name="Fatorial e Permutações",
                description="Fatorial, permutações simples e com repetição",
                subtopics=["Fatorial", "Permutação Simples", "Permutação com Repetição", "Permutação Circular"],
                concepts=["fatorial", "permutação", "anagrama", "permutação circular"]
            ),
            Topic(
                id="5.3",
                name="Arranjos",
                description="Arranjos simples e com repetição",
                subtopics=["Arranjo Simples", "Arranjo com Repetição", "Fórmula"],
                concepts=["arranjo", "ordem", "seleção ordenada"]
            ),
            Topic(
                id="5.4",
                name="Combinações",
                description="Combinações simples, propriedades e aplicações",
                subtopics=["Combinação Simples", "Propriedades", "Combinação com Repetição"],
                concepts=["combinação", "seleção não ordenada", "número binomial", "propriedades"]
            ),
            Topic(
                id="5.5",
                name="Binômio de Newton",
                description="Desenvolvimento binomial e triângulo de Pascal",
                subtopics=["Teorema Binomial", "Triângulo de Pascal", "Termo Geral"],
                concepts=["binômio de Newton", "coeficiente binomial", "triângulo de Pascal", "termo geral"]
            ),
            Topic(
                id="5.6",
                name="Probabilidade",
                description="Conceitos básicos e cálculo de probabilidades",
                subtopics=["Espaço Amostral", "Eventos", "Probabilidade Clássica", "Eventos Complementares"],
                concepts=["experimento aleatório", "espaço amostral", "evento", "probabilidade", "evento complementar"]
            ),
            Topic(
                id="5.7",
                name="Probabilidade Condicional",
                description="Probabilidade condicional e independência",
                subtopics=["Probabilidade Condicional", "Eventos Independentes", "Teorema da Multiplicação"],
                concepts=["probabilidade condicional", "eventos independentes", "eventos dependentes"]
            ),
            Topic(
                id="5.8",
                name="Distribuição Binomial",
                description="Experimentos de Bernoulli e distribuição binomial",
                subtopics=["Experimento de Bernoulli", "Lei Binomial", "Aplicações"],
                concepts=["ensaio de Bernoulli", "distribuição binomial", "sucesso", "fracasso"]
            ),
        ]
    ),
    6: Volume(
        id=6,
        name="Números Complexos e Polinômios",
        description="Conjunto dos números complexos, operações, polinômios e equações algébricas",
        topics=[
            Topic(
                id="6.1",
                name="Números Complexos - Forma Algébrica",
                description="Definição, operações e representação algébrica",
                subtopics=["Unidade Imaginária", "Forma Algébrica", "Operações", "Conjugado", "Módulo"],
                concepts=["número complexo", "parte real", "parte imaginária", "conjugado", "módulo"]
            ),
            Topic(
                id="6.2",
                name="Números Complexos - Forma Trigonométrica",
                description="Representação trigonométrica e operações",
                subtopics=["Forma Trigonométrica", "Multiplicação", "Divisão", "Potenciação", "Radiciação"],
                concepts=["forma trigonométrica", "argumento", "módulo", "fórmula de Moivre"]
            ),
            Topic(
                id="6.3",
                name="Polinômios - Definições",
                description="Definição, grau e operações com polinômios",
                subtopics=["Definição", "Grau", "Igualdade", "Operações", "Valor Numérico"],
                concepts=["polinômio", "coeficiente", "grau", "polinômio nulo", "valor numérico"]
            ),
            Topic(
                id="6.4",
                name="Divisão de Polinômios",
                description="Divisão, teorema do resto e dispositivo de Briot-Ruffini",
                subtopics=["Divisão Euclidiana", "Teorema do Resto", "Teorema de D'Alembert", "Briot-Ruffini"],
                concepts=["dividendo", "divisor", "quociente", "resto", "teorema do resto", "Briot-Ruffini"]
            ),
            Topic(
                id="6.5",
                name="Equações Polinomiais",
                description="Raízes, teorema fundamental e relações de Girard",
                subtopics=["Raízes", "Teorema Fundamental", "Multiplicidade", "Relações de Girard"],
                concepts=["equação polinomial", "raiz", "multiplicidade", "relações de Girard", "teorema fundamental da álgebra"]
            ),
            Topic(
                id="6.6",
                name="Raízes Reais e Complexas",
                description="Teoremas sobre raízes reais, racionais e complexas",
                subtopics=["Raízes Racionais", "Raízes Complexas Conjugadas", "Teorema de Bolzano"],
                concepts=["raiz racional", "raízes conjugadas", "localização de raízes"]
            ),
        ]
    ),
    7: Volume(
        id=7,
        name="Geometria Analítica",
        description="Estudo analítico de pontos, retas, circunferências e cônicas",
        topics=[
            Topic(
                id="7.1",
                name="Ponto e Reta",
                description="Coordenadas, distância, ponto médio e equações da reta",
                subtopics=["Sistema Cartesiano", "Distância entre Pontos", "Ponto Médio", "Equação da Reta", "Coeficiente Angular"],
                concepts=["coordenadas", "distância", "ponto médio", "equação geral", "equação reduzida", "coeficiente angular"]
            ),
            Topic(
                id="7.2",
                name="Posições Relativas de Retas",
                description="Paralelismo, perpendicularismo e ângulo entre retas",
                subtopics=["Retas Paralelas", "Retas Perpendiculares", "Retas Concorrentes", "Ângulo entre Retas"],
                concepts=["retas paralelas", "retas perpendiculares", "retas concorrentes", "ângulo entre retas"]
            ),
            Topic(
                id="7.3",
                name="Distância Ponto-Reta",
                description="Distância de um ponto a uma reta e área de triângulo",
                subtopics=["Fórmula da Distância", "Área de Triângulo", "Bissetrizes"],
                concepts=["distância ponto-reta", "área por coordenadas", "bissetriz"]
            ),
            Topic(
                id="7.4",
                name="Circunferência",
                description="Equações da circunferência e posições relativas",
                subtopics=["Equação Reduzida", "Equação Geral", "Posições Relativas", "Tangentes"],
                concepts=["circunferência", "centro", "raio", "equação reduzida", "equação geral", "tangente"]
            ),
            Topic(
                id="7.5",
                name="Elipse",
                description="Definição, equação e propriedades da elipse",
                subtopics=["Definição", "Elementos", "Equação", "Excentricidade"],
                concepts=["elipse", "foco", "eixo maior", "eixo menor", "excentricidade"]
            ),
            Topic(
                id="7.6",
                name="Hipérbole",
                description="Definição, equação e propriedades da hipérbole",
                subtopics=["Definição", "Elementos", "Equação", "Assíntotas"],
                concepts=["hipérbole", "foco", "vértice", "assíntota", "excentricidade"]
            ),
            Topic(
                id="7.7",
                name="Parábola",
                description="Definição, equação e propriedades da parábola",
                subtopics=["Definição", "Elementos", "Equação", "Diretriz"],
                concepts=["parábola", "foco", "vértice", "diretriz", "parâmetro"]
            ),
        ]
    ),
    8: Volume(
        id=8,
        name="Limites, Derivadas e Integrais",
        description="Introdução ao Cálculo: limites, continuidade, derivadas e noções de integral",
        topics=[
            Topic(
                id="8.1",
                name="Limites - Noção Intuitiva",
                description="Conceito intuitivo e definição formal de limite",
                subtopics=["Noção Intuitiva", "Definição", "Limites Laterais", "Unicidade"],
                concepts=["limite", "aproximação", "limite lateral", "existência de limite"]
            ),
            Topic(
                id="8.2",
                name="Propriedades dos Limites",
                description="Teoremas e propriedades operacionais",
                subtopics=["Limite da Soma", "Limite do Produto", "Limite do Quociente", "Limites Fundamentais"],
                concepts=["propriedades de limites", "limite fundamental", "limite trigonométrico", "limite exponencial"]
            ),
            Topic(
                id="8.3",
                name="Limites Infinitos e no Infinito",
                description="Comportamento assintótico e limites infinitos",
                subtopics=["Limites Infinitos", "Limites no Infinito", "Assíntotas Horizontais e Verticais"],
                concepts=["limite infinito", "limite no infinito", "assíntota horizontal", "assíntota vertical"]
            ),
            Topic(
                id="8.4",
                name="Continuidade",
                description="Funções contínuas e propriedades",
                subtopics=["Definição", "Propriedades", "Teorema do Valor Intermediário"],
                concepts=["continuidade", "descontinuidade", "ponto de descontinuidade", "teorema do valor intermediário"]
            ),
            Topic(
                id="8.5",
                name="Derivada - Definição",
                description="Taxa de variação, derivada no ponto e função derivada",
                subtopics=["Taxa de Variação", "Derivada no Ponto", "Função Derivada", "Interpretação Geométrica"],
                concepts=["derivada", "taxa de variação", "reta tangente", "inclinação"]
            ),
            Topic(
                id="8.6",
                name="Regras de Derivação",
                description="Regras operacionais para calcular derivadas",
                subtopics=["Derivada da Soma", "Derivada do Produto", "Derivada do Quociente", "Regra da Cadeia"],
                concepts=["regra da soma", "regra do produto", "regra do quociente", "regra da cadeia"]
            ),
            Topic(
                id="8.7",
                name="Derivadas de Funções Elementares",
                description="Derivadas de potências, exponenciais, logaritmos e trigonométricas",
                subtopics=["Derivada de Potências", "Derivada Exponencial", "Derivada Logarítmica", "Derivadas Trigonométricas"],
                concepts=["derivada de x^n", "derivada de e^x", "derivada de ln x", "derivadas trigonométricas"]
            ),
            Topic(
                id="8.8",
                name="Aplicações da Derivada",
                description="Máximos, mínimos, crescimento e concavidade",
                subtopics=["Crescimento e Decrescimento", "Máximos e Mínimos", "Concavidade", "Pontos de Inflexão"],
                concepts=["ponto crítico", "máximo local", "mínimo local", "concavidade", "ponto de inflexão"]
            ),
            Topic(
                id="8.9",
                name="Noções de Integral",
                description="Integral definida e primitivas",
                subtopics=["Primitiva", "Integral Indefinida", "Integral Definida", "Teorema Fundamental"],
                concepts=["primitiva", "integral indefinida", "integral definida", "teorema fundamental do cálculo"]
            ),
        ]
    ),
    9: Volume(
        id=9,
        name="Geometria Plana",
        description="Estudo dos entes geométricos fundamentais, triângulos, quadriláteros e círculos",
        topics=[
            Topic(
                id="9.1",
                name="Conceitos Fundamentais",
                description="Ponto, reta, plano e ângulos",
                subtopics=["Ponto, Reta e Plano", "Semirreta e Segmento", "Ângulos", "Ângulos Complementares e Suplementares"],
                concepts=["ponto", "reta", "plano", "semirreta", "segmento", "ângulo", "ângulos complementares", "ângulos suplementares"]
            ),
            Topic(
                id="9.2",
                name="Triângulos",
                description="Classificação, propriedades e pontos notáveis",
                subtopics=["Classificação", "Soma dos Ângulos", "Desigualdade Triangular", "Pontos Notáveis"],
                concepts=["triângulo", "ângulo interno", "ângulo externo", "baricentro", "ortocentro", "incentro", "circuncentro"]
            ),
            Topic(
                id="9.3",
                name="Congruência de Triângulos",
                description="Casos de congruência e aplicações",
                subtopics=["Definição", "Casos LAL, ALA, LLL, LAA", "Aplicações"],
                concepts=["congruência", "caso LAL", "caso ALA", "caso LLL", "caso LAA"]
            ),
            Topic(
                id="9.4",
                name="Semelhança de Triângulos",
                description="Razão de semelhança e aplicações",
                subtopics=["Teorema de Tales", "Semelhança", "Casos AA, LAL, LLL", "Razão de Semelhança"],
                concepts=["semelhança", "razão de semelhança", "teorema de Tales", "teorema fundamental"]
            ),
            Topic(
                id="9.5",
                name="Relações Métricas no Triângulo Retângulo",
                description="Teorema de Pitágoras e relações métricas",
                subtopics=["Teorema de Pitágoras", "Projeções", "Relações Métricas", "Aplicações"],
                concepts=["teorema de Pitágoras", "projeção ortogonal", "altura relativa", "cateto", "hipotenusa"]
            ),
            Topic(
                id="9.6",
                name="Quadriláteros",
                description="Paralelogramos, trapézios e quadriláteros inscritíveis",
                subtopics=["Paralelogramo", "Retângulo", "Losango", "Quadrado", "Trapézio"],
                concepts=["quadrilátero", "paralelogramo", "retângulo", "losango", "quadrado", "trapézio"]
            ),
            Topic(
                id="9.7",
                name="Polígonos Regulares",
                description="Propriedades e cálculos em polígonos regulares",
                subtopics=["Definição", "Ângulos", "Apótema", "Inscritos e Circunscritos"],
                concepts=["polígono regular", "ângulo interno", "ângulo externo", "apótema", "polígono inscrito", "polígono circunscrito"]
            ),
            Topic(
                id="9.8",
                name="Circunferência e Círculo",
                description="Propriedades da circunferência e do círculo",
                subtopics=["Definições", "Posições Relativas", "Arcos e Ângulos", "Potência de Ponto"],
                concepts=["circunferência", "círculo", "raio", "diâmetro", "corda", "arco", "ângulo central", "ângulo inscrito"]
            ),
            Topic(
                id="9.9",
                name="Áreas de Figuras Planas",
                description="Cálculo de áreas de polígonos e círculos",
                subtopics=["Área do Triângulo", "Área do Quadrilátero", "Área do Círculo", "Setor Circular"],
                concepts=["área", "fórmula de Heron", "área do círculo", "setor circular", "segmento circular"]
            ),
        ]
    ),
    10: Volume(
        id=10,
        name="Geometria Espacial",
        description="Geometria de posição, poliedros e sólidos de revolução",
        topics=[
            Topic(
                id="10.1",
                name="Geometria de Posição",
                description="Posições relativas entre retas e planos no espaço",
                subtopics=["Postulados", "Posições de Retas", "Posições de Planos", "Retas e Planos"],
                concepts=["geometria espacial", "retas paralelas", "retas reversas", "planos paralelos", "planos secantes"]
            ),
            Topic(
                id="10.2",
                name="Perpendicularidade",
                description="Retas perpendiculares e planos perpendiculares",
                subtopics=["Reta Perpendicular a Plano", "Planos Perpendiculares", "Distâncias"],
                concepts=["perpendicular ao plano", "planos perpendiculares", "distância ponto-plano"]
            ),
            Topic(
                id="10.3",
                name="Poliedros Convexos",
                description="Definição, elementos e relação de Euler",
                subtopics=["Definição", "Elementos", "Relação de Euler", "Poliedros Regulares"],
                concepts=["poliedro", "face", "aresta", "vértice", "relação de Euler", "poliedros de Platão"]
            ),
            Topic(
                id="10.4",
                name="Prismas",
                description="Classificação, áreas e volumes de prismas",
                subtopics=["Definição", "Classificação", "Área Lateral e Total", "Volume"],
                concepts=["prisma", "prisma reto", "paralelepípedo", "cubo", "área do prisma", "volume do prisma"]
            ),
            Topic(
                id="10.5",
                name="Pirâmides",
                description="Classificação, áreas e volumes de pirâmides",
                subtopics=["Definição", "Classificação", "Área Lateral e Total", "Volume", "Tronco de Pirâmide"],
                concepts=["pirâmide", "apótema", "pirâmide regular", "tronco", "volume da pirâmide"]
            ),
            Topic(
                id="10.6",
                name="Cilindro",
                description="Cilindro de revolução, áreas e volume",
                subtopics=["Definição", "Seções", "Área Lateral e Total", "Volume"],
                concepts=["cilindro", "cilindro reto", "geratriz", "área do cilindro", "volume do cilindro"]
            ),
            Topic(
                id="10.7",
                name="Cone",
                description="Cone de revolução, áreas e volume",
                subtopics=["Definição", "Seções", "Área Lateral e Total", "Volume", "Tronco de Cone"],
                concepts=["cone", "geratriz", "apótema", "área do cone", "volume do cone", "tronco de cone"]
            ),
            Topic(
                id="10.8",
                name="Esfera",
                description="Esfera, seções, áreas e volume",
                subtopics=["Definição", "Seções", "Partes da Esfera", "Área", "Volume"],
                concepts=["esfera", "seção esférica", "fuso esférico", "cunha esférica", "área da esfera", "volume da esfera"]
            ),
            Topic(
                id="10.9",
                name="Inscrição e Circunscrição",
                description="Sólidos inscritos e circunscritos",
                subtopics=["Esfera e Cubo", "Esfera e Cilindro", "Esfera e Cone", "Poliedros e Esferas"],
                concepts=["inscrição", "circunscrição", "sólidos inscritos", "sólidos circunscritos"]
            ),
        ]
    ),
    11: Volume(
        id=11,
        name="Matemática Financeira e Estatística",
        description="Razões, proporções, juros, porcentagem e estatística descritiva",
        topics=[
            Topic(
                id="11.1",
                name="Razões e Proporções",
                description="Razão, proporção e propriedades",
                subtopics=["Razão", "Proporção", "Propriedades", "Grandezas Proporcionais"],
                concepts=["razão", "proporção", "extremos", "meios", "quarta proporcional"]
            ),
            Topic(
                id="11.2",
                name="Regra de Três",
                description="Regra de três simples e composta",
                subtopics=["Grandezas Diretamente Proporcionais", "Grandezas Inversamente Proporcionais", "Regra de Três Simples", "Regra de Três Composta"],
                concepts=["grandeza diretamente proporcional", "grandeza inversamente proporcional", "regra de três"]
            ),
            Topic(
                id="11.3",
                name="Porcentagem",
                description="Cálculos com porcentagem e variações",
                subtopics=["Definição", "Cálculos", "Aumentos e Descontos", "Variação Percentual"],
                concepts=["porcentagem", "taxa percentual", "aumento", "desconto", "variação percentual"]
            ),
            Topic(
                id="11.4",
                name="Juros Simples",
                description="Capitalização simples e descontos",
                subtopics=["Capital e Montante", "Taxa de Juros", "Fórmula dos Juros Simples", "Desconto Simples"],
                concepts=["capital", "juros", "montante", "taxa", "juros simples", "desconto comercial"]
            ),
            Topic(
                id="11.5",
                name="Juros Compostos",
                description="Capitalização composta e aplicações",
                subtopics=["Fórmula", "Taxas Equivalentes", "Período Fracionário", "Aplicações"],
                concepts=["juros compostos", "montante composto", "taxa equivalente", "capitalização"]
            ),
            Topic(
                id="11.6",
                name="Estatística Descritiva - Tabelas e Gráficos",
                description="Organização e representação de dados",
                subtopics=["Variáveis", "Frequências", "Tabelas", "Gráficos"],
                concepts=["variável", "frequência absoluta", "frequência relativa", "histograma", "polígono de frequências"]
            ),
            Topic(
                id="11.7",
                name="Medidas de Centralidade",
                description="Média, mediana e moda",
                subtopics=["Média Aritmética", "Média Ponderada", "Mediana", "Moda"],
                concepts=["média", "média ponderada", "mediana", "moda", "rol"]
            ),
            Topic(
                id="11.8",
                name="Medidas de Dispersão",
                description="Variância, desvio padrão e amplitude",
                subtopics=["Amplitude", "Variância", "Desvio Padrão", "Coeficiente de Variação"],
                concepts=["amplitude", "variância", "desvio padrão", "coeficiente de variação", "dispersão"]
            ),
        ]
    ),
}


def get_volume(volume_id: int) -> Optional[Volume]:
    return CURRICULUM.get(volume_id)


def get_all_volumes() -> Dict[int, Volume]:
    return CURRICULUM


def get_topic(volume_id: int, topic_id: str) -> Optional[Topic]:
    volume = get_volume(volume_id)
    if volume:
        for topic in volume.topics:
            if topic.id == topic_id:
                return topic
    return None


def get_all_topics_for_volume(volume_id: int) -> List[Topic]:
    volume = get_volume(volume_id)
    if volume:
        return volume.topics
    return []


def calculate_question_distribution(total: int) -> Dict[Difficulty, int]:
    easy = int(total * 0.4)
    medium = int(total * 0.4)
    hard = total - easy - medium
    return {
        Difficulty.FACIL: easy,
        Difficulty.MEDIO: medium,
        Difficulty.DIFICIL: hard
    }
