from __future__ import annotations
import random
import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from sympy import *
from ..models.curriculum import Difficulty


@dataclass
class QuestionTemplate:
    id: str
    topic_id: str
    difficulty: Difficulty
    template_type: str
    generate_func: callable
    contexts: List[str]
    statement_patterns: List[str]


class ContextGenerator:
    PEOPLE_NAMES = [
        "Ana", "Bruno", "Carlos", "Diana", "Eduardo", "Fernanda", "Gabriel", "Helena",
        "Igor", "Julia", "Lucas", "Marina", "Natan", "Olivia", "Pedro", "Rafaela",
        "Sofia", "Thiago", "Valentina", "William", "Amanda", "Bernardo", "Camila",
        "Daniel", "Elisa", "Felipe", "Giovana", "Henrique", "Isabela", "João",
        "Laura", "Matheus", "Natalia", "Otavio", "Patricia", "Ricardo", "Sara",
        "Tales", "Ursula", "Victor", "Wesley", "Ximena", "Yasmin", "Zoe"
    ]
    
    PROFESSIONS = [
        "engenheiro", "arquiteta", "professor", "médica", "advogado", "cientista",
        "programador", "economista", "veterinária", "empresário", "farmacêutica",
        "contador", "designer", "bióloga", "físico", "química", "geólogo",
        "agrônomo", "nutricionista", "psicólogo", "jornalista", "artista"
    ]
    
    COMPANIES = [
        "TechNova", "AgroVerde", "ConstrutoraBrasil", "EdificaPrime", "InovaTech",
        "BioSaude", "EcoEnergy", "MetalMaster", "QuimicaViva", "TransLogix",
        "DataSmart", "AeroBrasil", "NavegaSul", "SolarPower", "AquaPura"
    ]
    
    CITIES = [
        "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília",
        "Curitiba", "Fortaleza", "Manaus", "Recife", "Porto Alegre", "Goiânia",
        "Belém", "Campinas", "Florianópolis", "Vitória", "Natal", "Campo Grande"
    ]
    
    SPORTS = [
        "futebol", "basquete", "vôlei", "natação", "atletismo", "tênis", "ciclismo",
        "handebol", "judô", "ginástica", "xadrez", "surf", "skate"
    ]
    
    PRODUCTS = [
        "smartphones", "notebooks", "tablets", "livros", "camisetas", "sapatos",
        "relógios", "óculos", "mochilas", "bicicletas", "instrumentos musicais",
        "equipamentos esportivos", "eletrodomésticos", "móveis", "cosméticos"
    ]
    
    SCHOOL_SUBJECTS = [
        "Matemática", "Física", "Química", "Biologia", "História", "Geografia",
        "Português", "Inglês", "Filosofia", "Sociologia", "Artes", "Educação Física"
    ]
    
    GEOMETRIC_OBJECTS = [
        "terreno", "jardim", "piscina", "quadra", "sala", "escritório", "praça",
        "parque", "campo", "telhado", "parede", "janela", "porta", "mesa"
    ]
    
    INVESTMENT_TYPES = [
        "poupança", "CDB", "tesouro direto", "ações", "fundos imobiliários",
        "LCI", "LCA", "fundos de investimento"
    ]
    
    @classmethod
    def get_random_name(cls) -> str:
        return random.choice(cls.PEOPLE_NAMES)
    
    @classmethod
    def get_random_names(cls, n: int) -> List[str]:
        return random.sample(cls.PEOPLE_NAMES, min(n, len(cls.PEOPLE_NAMES)))
    
    @classmethod
    def get_random_profession(cls) -> str:
        return random.choice(cls.PROFESSIONS)
    
    @classmethod
    def get_random_company(cls) -> str:
        return random.choice(cls.COMPANIES)
    
    @classmethod
    def get_random_city(cls) -> str:
        return random.choice(cls.CITIES)
    
    @classmethod
    def get_random_cities(cls, n: int) -> List[str]:
        return random.sample(cls.CITIES, min(n, len(cls.CITIES)))
    
    @classmethod
    def get_random_product(cls) -> str:
        return random.choice(cls.PRODUCTS)
    
    @classmethod
    def get_random_geometric_object(cls) -> str:
        return random.choice(cls.GEOMETRIC_OBJECTS)


class NumberGenerator:
    @staticmethod
    def prime(min_val: int = 2, max_val: int = 50) -> int:
        primes = [p for p in range(min_val, max_val + 1) if isprime(p)]
        return random.choice(primes) if primes else 2
    
    @staticmethod
    def integer(min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)
    
    @staticmethod
    def positive_integer(max_val: int = 100) -> int:
        return random.randint(1, max_val)
    
    @staticmethod
    def even(min_val: int = 2, max_val: int = 100) -> int:
        nums = [n for n in range(min_val, max_val + 1) if n % 2 == 0]
        return random.choice(nums) if nums else 2
    
    @staticmethod
    def odd(min_val: int = 1, max_val: int = 99) -> int:
        nums = [n for n in range(min_val, max_val + 1) if n % 2 == 1]
        return random.choice(nums) if nums else 1
    
    @staticmethod
    def fraction_nice() -> Tuple[int, int]:
        denominators = [2, 3, 4, 5, 6, 8, 10, 12]
        d = random.choice(denominators)
        n = random.randint(1, d - 1)
        g = math.gcd(n, d)
        return n // g, d // g
    
    @staticmethod
    def percentage() -> int:
        return random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
    
    @staticmethod
    def angle_notable() -> int:
        return random.choice([30, 45, 60, 90, 120, 135, 150, 180])
    
    @staticmethod
    def pythagorean_triple() -> Tuple[int, int, int]:
        triples = [
            (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
            (6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25)
        ]
        return random.choice(triples)


class DistractorGenerator:
    @staticmethod
    def numeric_distractors(correct: float, difficulty: Difficulty, count: int = 4) -> List[float]:
        distractors = set()
        
        if isinstance(correct, int):
            errors = []
            if difficulty == Difficulty.FACIL:
                errors = [1, -1, 2, -2, correct // 2 if correct > 1 else 1, correct * 2]
            elif difficulty == Difficulty.MEDIO:
                errors = [1, -1, 2, -2, 3, -3, correct + 10, correct - 10, correct * 2, correct // 2]
            else:
                errors = [1, -1, 2, -2, 5, -5, correct % 10 if correct > 10 else 1, 
                         int(str(correct)[::-1]) if correct > 9 else correct + 1]
            
            for err in errors:
                if isinstance(err, (int, float)):
                    val = correct + err if random.random() > 0.5 else err
                    if val != correct and val > 0:
                        distractors.add(int(val))
        else:
            base_errors = [0.1, -0.1, 0.5, -0.5, 1, -1, 0.25, -0.25]
            mult_errors = [2, 0.5, 1.5, 0.75]
            
            for err in base_errors:
                val = round(correct + err, 2)
                if val != correct and val > 0:
                    distractors.add(val)
            
            for mult in mult_errors:
                val = round(correct * mult, 2)
                if val != correct and val > 0:
                    distractors.add(val)
        
        distractors_list = list(distractors)
        random.shuffle(distractors_list)
        return distractors_list[:count]
    
    @staticmethod
    def expression_distractors(correct_expr: str, var_symbol: str = 'x') -> List[str]:
        x = Symbol(var_symbol)
        try:
            expr = sympify(correct_expr)
            distractors = []
            
            distractors.append(str(-expr))
            distractors.append(str(expr + 1))
            distractors.append(str(expr - 1))
            distractors.append(str(2 * expr))
            distractors.append(str(expr / 2))
            
            filtered = [d for d in distractors if d != correct_expr and d != str(expr)]
            return filtered[:4]
        except:
            return [f"{var_symbol} + 1", f"{var_symbol} - 1", f"2{var_symbol}", f"-{var_symbol}"]
    
    @staticmethod
    def set_distractors(correct_set: set, universe: set) -> List[set]:
        distractors = []
        
        if len(correct_set) > 0:
            subset = set(list(correct_set)[:-1]) if len(correct_set) > 1 else set()
            if subset != correct_set:
                distractors.append(subset)
        
        extra_elements = universe - correct_set
        if extra_elements:
            superset = correct_set | {list(extra_elements)[0]}
            if superset != correct_set:
                distractors.append(superset)
        
        if universe - correct_set:
            complement = universe - correct_set
            if complement != correct_set:
                distractors.append(complement)
        
        return distractors[:4]


class StatementPatterns:
    CONJUNTOS_PATTERNS = [
        "Considere os conjuntos {A} = {set_a} e {B} = {set_b}. {question}",
        "Sejam {A} e {B} dois conjuntos tais que {A} = {set_a} e {B} = {set_b}. {question}",
        "Em uma pesquisa, identificou-se que {context}. Se representarmos por {A} o conjunto {desc_a} e por {B} o conjunto {desc_b}, {question}",
        "Uma escola oferece atividades extracurriculares. O conjunto {A} representa {desc_a}, e {B} representa {desc_b}. {question}",
        "{name}, organizando uma lista, definiu {A} = {set_a} e {B} = {set_b}. {question}",
    ]
    
    FUNCAO_PATTERNS = [
        "Seja f: R -> R definida por f(x) = {expression}. {question}",
        "Considere a função f(x) = {expression}, onde {domain}. {question}",
        "{name} modelou uma situação por meio da função f(x) = {expression}. {question}",
        "O lucro de uma empresa, em reais, é dado pela função L(x) = {expression}, onde x representa {variable_meaning}. {question}",
        "A altura de um objeto em queda livre é dada por h(t) = {expression}, onde t é o tempo em segundos. {question}",
    ]
    
    EQUACAO_PATTERNS = [
        "Determine o valor de x que satisfaz a equação {equation}.",
        "Resolva a equação {equation} e encontre a soma das raízes.",
        "{name} precisa encontrar o valor de x tal que {equation}. Qual é esse valor?",
        "Em uma aplicação prática, {context}, obtém-se a equação {equation}. Determine x.",
        "A solução da equação {equation} representa {meaning}. Qual é essa solução?",
    ]
    
    GEOMETRIA_PATTERNS = [
        "Um {shape} possui {properties}. {question}",
        "Calcule {what} de um {shape} cujas {dimensions}.",
        "{name} precisa {action} um {object} que tem formato de {shape}. {question}",
        "Em um projeto de arquitetura, {context}. {question}",
        "Uma região delimitada por {description} forma um {shape}. {question}",
    ]
    
    PROBABILIDADE_PATTERNS = [
        "Uma urna contém {balls}. {action}, qual a probabilidade de {event}?",
        "Em um experimento aleatório, {description}. Qual a probabilidade de {event}?",
        "De um grupo de {total} pessoas, {details}. Se uma pessoa for escolhida ao acaso, qual a probabilidade de {condition}?",
        "{name} participa de um sorteio em que {rules}. Qual a probabilidade de {result}?",
        "Em uma competição, {context}. A probabilidade de {event} é:",
    ]
    
    FINANCEIRA_PATTERNS = [
        "Um capital de R$ {capital} foi aplicado a uma taxa de {rate}% ao mês, no regime de juros {type}. {question}",
        "{name} investiu R$ {capital} em uma aplicação que rende {rate}% ao {period}. {question}",
        "Uma loja oferece {discount}% de desconto para pagamento à vista. Se o preço original é R$ {price}, {question}",
        "Um produto teve seu preço aumentado em {increase}% e, posteriormente, foi dado um desconto de {discount}%. {question}",
        "Em uma aplicação financeira, {context}. {question}",
    ]


def format_set(elements: list) -> str:
    if not elements:
        return "{}"
    return "{" + ", ".join(str(e) for e in sorted(elements)) + "}"


def format_number(num: float) -> str:
    if isinstance(num, int) or num == int(num):
        return str(int(num))
    return f"{num:.2f}".rstrip('0').rstrip('.')


def format_fraction(num: int, den: int) -> str:
    if den == 1:
        return str(num)
    return f"{num}/{den}"


def format_expression(expr: str) -> str:
    expr = expr.replace("**", "^")
    expr = expr.replace("*", " . ")
    expr = expr.replace("sqrt", "raiz quadrada de")
    return expr
