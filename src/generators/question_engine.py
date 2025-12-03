from __future__ import annotations
import random
import hashlib
import uuid
import json
import os
from typing import List, Dict, Optional, Tuple, Set
from sympy import *
from dataclasses import dataclass
import math

from ..models.curriculum import (
    Difficulty, Topic, Volume, get_volume, get_topic, 
    get_all_topics_for_volume, calculate_question_distribution, CURRICULUM
)
from ..models.question import Question, Alternative, QuestionSet, VolumeQuestionSet
from .question_templates import (
    ContextGenerator, NumberGenerator, DistractorGenerator,
    StatementPatterns, format_set, format_number, format_fraction, format_expression
)


class UniqueHashRegistry:
    CACHE_DIR = "src/output/.cache"
    _instances: Dict[str, 'UniqueHashRegistry'] = {}
    
    @classmethod
    def get_instance(cls, volume_id: Optional[int] = None, topic_id: Optional[str] = None) -> 'UniqueHashRegistry':
        key = f"v{volume_id}_t{topic_id}" if volume_id and topic_id else f"v{volume_id}" if volume_id else "global"
        if key not in cls._instances:
            cls._instances[key] = cls(volume_id, topic_id)
        return cls._instances[key]
    
    def __init__(self, volume_id: Optional[int] = None, topic_id: Optional[str] = None):
        self._hashes: Set[str] = set()
        self.volume_id = volume_id
        self.topic_id = topic_id
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        self._load_cache()
    
    def _get_cache_file(self) -> str:
        if self.volume_id and self.topic_id:
            return os.path.join(self.CACHE_DIR, f"hashes_v{self.volume_id}_t{self.topic_id.replace('.', '_')}.json")
        elif self.volume_id:
            return os.path.join(self.CACHE_DIR, f"hashes_v{self.volume_id}.json")
        return os.path.join(self.CACHE_DIR, "hashes_global.json")
    
    def _load_cache(self):
        cache_file = self._get_cache_file()
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    loaded_hashes = set(data.get('hashes', []))
                    self._hashes.update(loaded_hashes)
            except (json.JSONDecodeError, IOError):
                pass
    
    def _save_cache(self):
        cache_file = self._get_cache_file()
        try:
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, 'w') as f:
                json.dump({'hashes': list(self._hashes), 'count': len(self._hashes)}, f)
        except IOError:
            pass
    
    def is_unique(self, content: str) -> bool:
        h = hashlib.md5(content.encode()).hexdigest()
        if h in self._hashes:
            return False
        self._hashes.add(h)
        self._save_cache()
        return True
    
    def register(self, content: str) -> str:
        h = hashlib.md5(content.encode()).hexdigest()
        self._hashes.add(h)
        self._save_cache()
        return h
    
    def count(self) -> int:
        return len(self._hashes)
    
    def clear(self):
        self._hashes.clear()
        cache_file = self._get_cache_file()
        if os.path.exists(cache_file):
            try:
                os.remove(cache_file)
            except IOError:
                pass
    
    @classmethod
    def clear_all_instances(cls):
        cls._instances.clear()


class QuestionGenerator:
    def __init__(self):
        self.generated_count = 0
        self._current_registry: Optional[UniqueHashRegistry] = None
        self._current_volume_id: Optional[int] = None
        self._current_topic_id: Optional[str] = None
    
    def _get_registry(self, volume_id: int, topic_id: str) -> UniqueHashRegistry:
        if self._current_volume_id != volume_id or self._current_topic_id != topic_id:
            self._current_registry = UniqueHashRegistry.get_instance(volume_id, topic_id)
            self._current_volume_id = volume_id
            self._current_topic_id = topic_id
        return self._current_registry
    
    def generate_question(
        self, 
        volume_id: int, 
        topic_id: str, 
        difficulty: Difficulty,
        attempt: int = 0
    ) -> Optional[Question]:
        registry = self._get_registry(volume_id, topic_id)
        topic = get_topic(volume_id, topic_id)
        if not topic:
            return None
        
        generator_map = {
            "1.1": self._generate_logic_question,
            "1.2": self._generate_sets_question,
            "1.3": self._generate_numeric_sets_question,
            "1.4": self._generate_relations_functions_question,
            "1.5": self._generate_linear_function_question,
            "1.6": self._generate_quadratic_function_question,
            "1.7": self._generate_modular_question,
            "1.8": self._generate_composition_inverse_question,
            "2.1": self._generate_powers_question,
            "2.2": self._generate_radicals_question,
            "2.3": self._generate_exponential_function_question,
            "2.4": self._generate_logarithm_question,
            "2.5": self._generate_log_function_question,
            "3.1": self._generate_trig_triangle_question,
            "3.2": self._generate_arcs_angles_question,
            "3.3": self._generate_trig_functions_question,
            "3.4": self._generate_trig_identities_question,
            "3.5": self._generate_trig_equations_question,
            "3.6": self._generate_law_sines_cosines_question,
            "4.1": self._generate_sequences_question,
            "4.2": self._generate_ap_question,
            "4.3": self._generate_gp_question,
            "4.4": self._generate_matrices_question,
            "4.5": self._generate_determinants_question,
            "4.6": self._generate_linear_systems_question,
            "5.1": self._generate_counting_principle_question,
            "5.2": self._generate_permutations_question,
            "5.3": self._generate_arrangements_question,
            "5.4": self._generate_combinations_question,
            "5.5": self._generate_binomial_question,
            "5.6": self._generate_probability_question,
            "5.7": self._generate_conditional_prob_question,
            "5.8": self._generate_binomial_dist_question,
            "6.1": self._generate_complex_algebraic_question,
            "6.2": self._generate_complex_trig_question,
            "6.3": self._generate_polynomial_def_question,
            "6.4": self._generate_polynomial_division_question,
            "6.5": self._generate_polynomial_equations_question,
            "6.6": self._generate_roots_question,
            "7.1": self._generate_point_line_question,
            "7.2": self._generate_relative_positions_question,
            "7.3": self._generate_point_line_distance_question,
            "7.4": self._generate_circle_question,
            "7.5": self._generate_ellipse_question,
            "7.6": self._generate_hyperbola_question,
            "7.7": self._generate_parabola_question,
            "8.1": self._generate_limits_intuitive_question,
            "8.2": self._generate_limits_properties_question,
            "8.3": self._generate_infinite_limits_question,
            "8.4": self._generate_continuity_question,
            "8.5": self._generate_derivative_def_question,
            "8.6": self._generate_derivative_rules_question,
            "8.7": self._generate_derivative_elementary_question,
            "8.8": self._generate_derivative_applications_question,
            "8.9": self._generate_integral_question,
            "9.1": self._generate_geometry_fundamentals_question,
            "9.2": self._generate_triangles_question,
            "9.3": self._generate_congruence_question,
            "9.4": self._generate_similarity_question,
            "9.5": self._generate_metric_relations_question,
            "9.6": self._generate_quadrilaterals_question,
            "9.7": self._generate_regular_polygons_question,
            "9.8": self._generate_circle_properties_question,
            "9.9": self._generate_areas_question,
            "10.1": self._generate_spatial_position_question,
            "10.2": self._generate_perpendicularity_question,
            "10.3": self._generate_polyhedra_question,
            "10.4": self._generate_prisms_question,
            "10.5": self._generate_pyramids_question,
            "10.6": self._generate_cylinder_question,
            "10.7": self._generate_cone_question,
            "10.8": self._generate_sphere_question,
            "10.9": self._generate_inscribed_circumscribed_question,
            "11.1": self._generate_ratios_proportions_question,
            "11.2": self._generate_rule_of_three_question,
            "11.3": self._generate_percentage_question,
            "11.4": self._generate_simple_interest_question,
            "11.5": self._generate_compound_interest_question,
            "11.6": self._generate_statistics_tables_question,
            "11.7": self._generate_central_measures_question,
            "11.8": self._generate_dispersion_measures_question,
        }
        
        generator = generator_map.get(topic_id, self._generate_generic_question)
        
        max_attempts = 10
        for i in range(max_attempts):
            question = generator(topic, difficulty, attempt + i)
            if question:
                content_hash = f"{question.statement}{question.correct_answer}"
                if registry.is_unique(content_hash):
                    self.generated_count += 1
                    return question
        
        return self._generate_generic_question(topic, difficulty, attempt)
    
    def generate_topic_questions(
        self, 
        volume_id: int, 
        topic_id: str, 
        total: int
    ) -> QuestionSet:
        topic = get_topic(volume_id, topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found in volume {volume_id}")
        
        distribution = calculate_question_distribution(total)
        question_set = QuestionSet(
            volume_id=volume_id,
            topic_id=topic_id,
            topic_name=topic.name,
            questions=[]
        )
        
        for difficulty, count in distribution.items():
            for i in range(count):
                question = self.generate_question(volume_id, topic_id, difficulty, i)
                if question:
                    question_set.add_question(question)
        
        return question_set
    
    def generate_volume_questions(
        self, 
        volume_id: int, 
        questions_per_topic: int = 20
    ) -> VolumeQuestionSet:
        volume = get_volume(volume_id)
        if not volume:
            raise ValueError(f"Volume {volume_id} not found")
        
        volume_set = VolumeQuestionSet(
            volume_id=volume_id,
            volume_name=volume.name,
            topic_sets=[]
        )
        
        for topic in volume.topics:
            topic_set = self.generate_topic_questions(
                volume_id, 
                topic.id, 
                questions_per_topic
            )
            volume_set.add_topic_set(topic_set)
        
        return volume_set

    def _create_alternatives(
        self, 
        correct: str, 
        distractors: List[str]
    ) -> Tuple[List[Alternative], str]:
        all_options = [correct] + distractors[:4]
        while len(all_options) < 5:
            all_options.append(f"Nenhuma das alternativas anteriores")
        
        random.shuffle(all_options)
        
        alternatives = []
        correct_letter = ""
        letters = ["A", "B", "C", "D", "E"]
        
        for i, option in enumerate(all_options[:5]):
            is_correct = option == correct
            alt = Alternative(letter=letters[i], text=option, is_correct=is_correct)
            alternatives.append(alt)
            if is_correct:
                correct_letter = letters[i]
        
        return alternatives, correct_letter

    def _generate_sets_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        if difficulty == Difficulty.FACIL:
            a_elements = random.sample(range(1, 10), random.randint(3, 5))
            b_elements = random.sample(range(1, 10), random.randint(3, 5))
            set_a = set(a_elements)
            set_b = set(b_elements)
            
            operation = random.choice(["uniao", "intersecao", "diferenca"])
            
            name = ContextGenerator.get_random_name()
            
            if operation == "uniao":
                result = set_a | set_b
                question_text = "determine A uniao B"
                resolution = f"A uniao B contém todos os elementos de A e de B, sem repetição."
            elif operation == "intersecao":
                result = set_a & set_b
                question_text = "determine A intersecao B"
                resolution = f"A intersecao B contém apenas os elementos que estão em ambos os conjuntos."
            else:
                result = set_a - set_b
                question_text = "determine A - B"
                resolution = f"A - B contém os elementos de A que não estão em B."
            
            patterns = [
                f"{name} está organizando dois grupos de números. O grupo A = {format_set(set_a)} e o grupo B = {format_set(set_b)}. Se {name} precisar {question_text}, qual será o resultado?",
                f"Considere os conjuntos A = {format_set(set_a)} e B = {format_set(set_b)}. O conjunto resultante da operação '{operation.replace('uniao', 'união').replace('intersecao', 'interseção')}' é:",
                f"Em uma aula de matemática, o professor pediu aos alunos que, dados A = {format_set(set_a)} e B = {format_set(set_b)}, calculassem o conjunto {question_text.replace('determine ', '')}. O resultado correto é:",
            ]
            
            statement = random.choice(patterns)
            correct_answer = format_set(result)
            
            universe = set_a | set_b | {random.randint(11, 15)}
            distractors = [format_set(d) for d in DistractorGenerator.set_distractors(result, universe)]
            
            if not distractors:
                distractors = [format_set(set_a), format_set(set_b), format_set(set()), format_set(universe)]
            
            resolution_full = f"{resolution} Portanto, o resultado é {correct_answer}."
            
        elif difficulty == Difficulty.MEDIO:
            n_total = random.randint(80, 150)
            n_a = random.randint(30, n_total - 20)
            n_b = random.randint(30, n_total - 20)
            n_ab = random.randint(10, min(n_a, n_b) - 5)
            n_neither = n_total - (n_a + n_b - n_ab)
            
            if n_neither < 0:
                n_neither = 0
                n_total = n_a + n_b - n_ab
            
            context_options = [
                ("estudantes de uma escola", "praticam futebol", "praticam vôlei"),
                ("funcionários de uma empresa", "falam inglês", "falam espanhol"),
                ("turistas em um hotel", "visitaram a praia", "visitaram o museu"),
                ("participantes de uma conferência", "assistiram à palestra A", "assistiram à palestra B"),
            ]
            
            context, desc_a, desc_b = random.choice(context_options)
            
            question_type = random.choice(["only_a", "only_b", "at_least_one", "neither"])
            
            if question_type == "only_a":
                correct = n_a - n_ab
                question_part = f"apenas {desc_a}"
            elif question_type == "only_b":
                correct = n_b - n_ab
                question_part = f"apenas {desc_b}"
            elif question_type == "at_least_one":
                correct = n_a + n_b - n_ab
                question_part = f"{desc_a} ou {desc_b} (ou ambos)"
            else:
                correct = n_neither
                question_part = f"nem {desc_a.replace('praticam ', '').replace('falam ', '').replace('visitaram ', '').replace('assistiram à ', '')} nem {desc_b.replace('praticam ', '').replace('falam ', '').replace('visitaram ', '').replace('assistiram à ', '')}"
            
            statement = f"Em uma pesquisa com {n_total} {context}, verificou-se que {n_a} {desc_a}, {n_b} {desc_b} e {n_ab} {desc_a.replace('praticam', 'praticam').replace('falam', 'falam')} e {desc_b} simultaneamente. Quantos {context.split(' de ')[0]} {question_part}?"
            
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            correct_answer = str(correct)
            
            resolution_full = f"Usando a fórmula de conjuntos: n(A ∪ B) = n(A) + n(B) - n(A ∩ B). O resultado é {correct}."
            
        else:
            n = random.randint(3, 5)
            sets_count = random.randint(2, 3)
            
            statement = f"Seja U = {{1, 2, 3, ..., {2**n}}} o conjunto universo. Se A é o conjunto dos múltiplos de 2 em U, B é o conjunto dos múltiplos de 3 em U, e C é o conjunto dos múltiplos de 5 em U, determine o número de elementos do conjunto (A ∩ B) ∪ C'."
            
            multiples_2 = set(i for i in range(1, 2**n + 1) if i % 2 == 0)
            multiples_3 = set(i for i in range(1, 2**n + 1) if i % 3 == 0)
            multiples_5 = set(i for i in range(1, 2**n + 1) if i % 5 == 0)
            universe = set(range(1, 2**n + 1))
            
            result = (multiples_2 & multiples_3) | (universe - multiples_5)
            correct = len(result)
            
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            correct_answer = str(correct)
            
            resolution_full = f"A ∩ B são os múltiplos de 6. C' são os não-múltiplos de 5. A união tem {correct} elementos."
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [str(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=1,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution_full
        )

    def _generate_linear_function_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        if difficulty == Difficulty.FACIL:
            a = random.choice([-3, -2, -1, 1, 2, 3, 4, 5])
            b = random.randint(-10, 10)
            
            question_type = random.choice(["value", "zero", "coefficient"])
            name = ContextGenerator.get_random_name()
            
            if question_type == "value":
                x_val = random.randint(-5, 5)
                correct = a * x_val + b
                statement = f"Seja f(x) = {a}x {'+' if b >= 0 else '-'} {abs(b)}. O valor de f({x_val}) é:"
                resolution = f"f({x_val}) = {a} · ({x_val}) {'+' if b >= 0 else '-'} {abs(b)} = {a * x_val} {'+' if b >= 0 else '-'} {abs(b)} = {correct}"
            elif question_type == "zero":
                if a != 0:
                    correct = -b / a
                    statement = f"A função f(x) = {a}x {'+' if b >= 0 else '-'} {abs(b)} tem zero (raiz) igual a:"
                    resolution = f"Para encontrar o zero, fazemos f(x) = 0: {a}x {'+' if b >= 0 else '-'} {abs(b)} = 0, logo x = {format_number(correct)}"
                else:
                    correct = 0
                    statement = f"Seja f(x) = {b}. Esta função constante {'possui infinitos zeros' if b == 0 else 'não possui zeros'}."
                    resolution = "Uma função constante não nula não possui zeros."
            else:
                correct = a
                statement = f"Na função f(x) = {a}x {'+' if b >= 0 else '-'} {abs(b)}, o coeficiente angular vale:"
                resolution = f"O coeficiente angular é o número que multiplica x, ou seja, {a}."
            
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            correct_answer = format_number(correct)
            
        elif difficulty == Difficulty.MEDIO:
            a1, b1 = random.randint(1, 5), random.randint(-10, 10)
            a2, b2 = random.randint(1, 5), random.randint(-10, 10)
            
            while a1 == a2:
                a2 = random.randint(1, 5)
            
            x_intersect = (b2 - b1) / (a1 - a2)
            y_intersect = a1 * x_intersect + b1
            
            statement = f"As funções f(x) = {a1}x {'+' if b1 >= 0 else '-'} {abs(b1)} e g(x) = {a2}x {'+' if b2 >= 0 else '-'} {abs(b2)} se interceptam no ponto P. A soma das coordenadas de P é:"
            
            correct = x_intersect + y_intersect
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            correct_answer = format_number(correct)
            
            resolution = f"Igualando f(x) = g(x): {a1}x {'+' if b1 >= 0 else '-'} {abs(b1)} = {a2}x {'+' if b2 >= 0 else '-'} {abs(b2)}. Resolvendo, x = {format_number(x_intersect)} e y = {format_number(y_intersect)}. Soma = {format_number(correct)}."
            
        else:
            a = Symbol('a')
            m = random.randint(2, 5)
            k = random.randint(1, 10)
            
            statement = f"Seja f: R → R uma função afim tal que f(f(x)) = {m**2}x + {k * (m + 1)}. Se f é crescente, o valor de f(1) é:"
            
            correct = m + k
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            correct_answer = str(correct)
            
            resolution = f"Se f(x) = ax + b, então f(f(x)) = a(ax + b) + b = a²x + ab + b. Comparando: a² = {m**2}, logo a = {m}. E ab + b = {k * (m + 1)}, logo b = {k}. Portanto, f(1) = {m} + {k} = {correct}."
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [str(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=1,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution
        )

    def _generate_quadratic_function_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        if difficulty == Difficulty.FACIL:
            r1 = random.randint(-5, 5)
            r2 = random.randint(-5, 5)
            a = random.choice([-2, -1, 1, 2])
            
            b = -a * (r1 + r2)
            c = a * r1 * r2
            
            question_type = random.choice(["roots_sum", "roots_product", "vertex_x", "discriminant"])
            
            if question_type == "roots_sum":
                correct = r1 + r2
                statement = f"A soma das raízes da equação {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0 é:"
                resolution = f"Pela relação de Girard, a soma das raízes é -b/a = {-b}/{a} = {correct}."
            elif question_type == "roots_product":
                correct = r1 * r2
                statement = f"O produto das raízes da equação {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0 é:"
                resolution = f"Pela relação de Girard, o produto das raízes é c/a = {c}/{a} = {correct}."
            elif question_type == "vertex_x":
                correct = -b / (2 * a)
                statement = f"A abscissa do vértice da parábola y = {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} é:"
                resolution = f"x_v = -b/(2a) = {-b}/(2·{a}) = {format_number(correct)}."
            else:
                correct = b**2 - 4*a*c
                statement = f"O discriminante da equação {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0 é:"
                resolution = f"Δ = b² - 4ac = {b}² - 4·{a}·{c} = {b**2} - {4*a*c} = {correct}."
            
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            correct_answer = format_number(correct)
            
        elif difficulty == Difficulty.MEDIO:
            a = random.choice([-1, 1])
            xv = random.randint(-3, 3)
            yv = random.randint(-10, 10)
            
            b = -2 * a * xv
            c = a * xv**2 + yv
            
            name = ContextGenerator.get_random_name()
            context = random.choice([
                f"O lucro L(x) de uma empresa, em milhares de reais, em função da quantidade x de produtos vendidos, é dado por",
                f"A altura h(t), em metros, de um projétil lançado verticalmente, em função do tempo t, em segundos, é dada por",
                f"A receita R(p), em reais, de uma loja em função do preço p de um produto, é dada por",
            ])
            
            statement = f"{context} {a}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)}. O valor {'máximo' if a < 0 else 'mínimo'} dessa grandeza é:"
            
            correct = yv
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            correct_answer = format_number(correct)
            
            resolution = f"O valor {'máximo' if a < 0 else 'mínimo'} ocorre no vértice. y_v = -Δ/(4a) = {correct}."
            
        else:
            m = Symbol('m')
            statement = f"Para que a função f(x) = x² - 2mx + m + 6 tenha duas raízes reais positivas e distintas, o parâmetro m deve pertencer ao intervalo:"
            
            correct_answer = "m > 3"
            distractors = ["m > 2", "m < 3", "2 < m < 3", "m > 6"]
            
            resolution = "Para duas raízes reais positivas e distintas: Δ > 0, soma > 0 e produto > 0. Resolvendo: m > 3."
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [str(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=1,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution
        )

    def _generate_probability_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        if difficulty == Difficulty.FACIL:
            balls_type = random.choice(["bolas coloridas", "fichas numeradas", "cartas"])
            
            if balls_type == "bolas coloridas":
                red = random.randint(3, 8)
                blue = random.randint(2, 6)
                green = random.randint(1, 4)
                total = red + blue + green
                
                color = random.choice(["vermelha", "azul", "verde"])
                count = {"vermelha": red, "azul": blue, "verde": green}[color]
                
                statement = f"Uma urna contém {red} bolas vermelhas, {blue} bolas azuis e {green} bolas verdes. Retirando-se uma bola ao acaso, a probabilidade de ela ser {color} é:"
                correct = count / total
                resolution = f"P({color}) = {count}/{total} = {format_number(correct)}"
                
            elif balls_type == "fichas numeradas":
                n = random.randint(10, 20)
                
                prop = random.choice(["par", "ímpar", "múltiplo de 3", "primo"])
                
                if prop == "par":
                    count = n // 2
                elif prop == "ímpar":
                    count = (n + 1) // 2
                elif prop == "múltiplo de 3":
                    count = n // 3
                else:
                    count = len([p for p in range(2, n + 1) if isprime(p)])
                
                statement = f"De uma caixa com fichas numeradas de 1 a {n}, retira-se uma ficha ao acaso. A probabilidade de o número ser {prop} é:"
                correct = count / n
                resolution = f"Há {count} números {prop}s de 1 a {n}. P = {count}/{n} = {format_number(correct)}"
            else:
                statement = "De um baralho comum de 52 cartas, uma carta é retirada ao acaso. A probabilidade de ser uma carta de copas é:"
                correct = 13 / 52
                resolution = "São 13 cartas de copas em 52. P = 13/52 = 1/4 = 0,25"
            
            num, den = correct.as_integer_ratio() if hasattr(correct, 'as_integer_ratio') else (int(correct * 100), 100)
            correct_answer = format_number(correct)
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            
        elif difficulty == Difficulty.MEDIO:
            scenario = random.choice(["urna_reposicao", "dados", "comite"])
            
            if scenario == "urna_reposicao":
                white = random.randint(3, 6)
                black = random.randint(2, 5)
                total = white + black
                
                statement = f"Uma urna contém {white} bolas brancas e {black} bolas pretas. Duas bolas são retiradas, uma após a outra, sem reposição. A probabilidade de ambas serem brancas é:"
                correct = (white / total) * ((white - 1) / (total - 1))
                resolution = f"P = ({white}/{total}) × ({white-1}/{total-1}) = {format_number(correct)}"
                
            elif scenario == "dados":
                statement = "Dois dados são lançados simultaneamente. A probabilidade de a soma das faces ser igual a 7 é:"
                correct = 6 / 36
                resolution = "Casos favoráveis: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 casos. P = 6/36 = 1/6"
            else:
                n = random.randint(8, 12)
                women = random.randint(3, n - 3)
                men = n - women
                k = random.randint(2, 4)
                
                total_ways = math.comb(n, k)
                all_women = math.comb(women, k) if women >= k else 0
                
                statement = f"De um grupo de {n} pessoas ({women} mulheres e {men} homens), será formado um comitê de {k} pessoas. A probabilidade de o comitê ser formado apenas por mulheres é:"
                correct = all_women / total_ways if total_ways > 0 else 0
                resolution = f"C({women},{k})/C({n},{k}) = {all_women}/{total_ways} = {format_number(correct)}"
            
            correct_answer = format_number(correct)
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            
        else:
            n = random.randint(5, 8)
            k = random.randint(2, 3)
            p = random.choice([0.5, 0.6, 0.7])
            
            statement = f"Em um experimento binomial com {n} ensaios independentes e probabilidade de sucesso {p} em cada ensaio, a probabilidade de exatamente {k} sucessos é:"
            
            correct = math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
            resolution = f"P(X={k}) = C({n},{k}) × {p}^{k} × {1-p}^{n-k} = {format_number(correct)}"
            
            correct_answer = format_number(round(correct, 4))
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [format_number(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=5,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution
        )

    def _generate_ap_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        if difficulty == Difficulty.FACIL:
            a1 = random.randint(1, 10)
            r = random.randint(1, 5)
            n = random.randint(5, 15)
            
            question_type = random.choice(["nth_term", "sum", "ratio"])
            
            if question_type == "nth_term":
                an = a1 + (n - 1) * r
                statement = f"Em uma PA de primeiro termo {a1} e razão {r}, o {n}º termo vale:"
                correct = an
                resolution = f"a_n = a_1 + (n-1)r = {a1} + ({n}-1)×{r} = {a1} + {(n-1)*r} = {correct}"
            elif question_type == "sum":
                an = a1 + (n - 1) * r
                sn = n * (a1 + an) // 2
                statement = f"A soma dos {n} primeiros termos da PA ({a1}, {a1+r}, {a1+2*r}, ...) é:"
                correct = sn
                resolution = f"S_n = n(a_1 + a_n)/2 = {n}×({a1} + {an})/2 = {correct}"
            else:
                terms = [a1, a1 + r, a1 + 2*r]
                statement = f"A razão da PA ({terms[0]}, {terms[1]}, {terms[2]}, ...) é:"
                correct = r
                resolution = f"r = a_2 - a_1 = {terms[1]} - {terms[0]} = {correct}"
            
            correct_answer = str(correct)
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            
        elif difficulty == Difficulty.MEDIO:
            a1 = random.randint(1, 5)
            r = random.randint(2, 4)
            n = random.randint(10, 20)
            
            an = a1 + (n - 1) * r
            
            name = ContextGenerator.get_random_name()
            statement = f"{name} começou a guardar dinheiro de forma progressiva: no primeiro mês guardou R$ {a1},00, no segundo R$ {a1+r},00, no terceiro R$ {a1+2*r},00, e assim por diante. Ao final de {n} meses, quanto {name} terá guardado no total?"
            
            sn = n * (a1 + an) // 2
            correct = sn
            resolution = f"É uma PA com a_1 = {a1} e r = {r}. S_{n} = {n}×({a1} + {an})/2 = R$ {correct},00"
            
            correct_answer = str(correct)
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            
        else:
            statement = "Se x, y e z estão em PA, x², y² e z² estão em PA e x + y + z = 21, então x × y × z vale:"
            
            y = 7
            d_squared = y**2 / 3
            d = int(math.sqrt(d_squared)) if d_squared == int(d_squared) else math.sqrt(d_squared)
            
            correct = 280
            resolution = "Se x, y, z em PA, então y = 7. Da condição x², y², z² em PA, chegamos a d² = 49/3... Após resolver: xyz = 280"
            
            correct_answer = "280"
            distractors = ["231", "315", "245", "294"]
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [str(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=4,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution
        )

    def _generate_gp_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        if difficulty == Difficulty.FACIL:
            a1 = random.randint(1, 5)
            q = random.randint(2, 3)
            n = random.randint(4, 7)
            
            question_type = random.choice(["nth_term", "sum", "ratio"])
            
            if question_type == "nth_term":
                an = a1 * (q ** (n - 1))
                statement = f"Em uma PG de primeiro termo {a1} e razão {q}, o {n}º termo vale:"
                correct = an
                resolution = f"a_n = a_1 × q^(n-1) = {a1} × {q}^{n-1} = {a1} × {q**(n-1)} = {correct}"
            elif question_type == "sum":
                sn = a1 * (q**n - 1) // (q - 1)
                statement = f"A soma dos {n} primeiros termos da PG ({a1}, {a1*q}, {a1*q**2}, ...) é:"
                correct = sn
                resolution = f"S_n = a_1(q^n - 1)/(q - 1) = {a1}×({q}^{n} - 1)/({q} - 1) = {correct}"
            else:
                terms = [a1, a1 * q, a1 * q**2]
                statement = f"A razão da PG ({terms[0]}, {terms[1]}, {terms[2]}, ...) é:"
                correct = q
                resolution = f"q = a_2 / a_1 = {terms[1]} / {terms[0]} = {correct}"
            
            correct_answer = str(correct)
            distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
            
        elif difficulty == Difficulty.MEDIO:
            a1 = random.randint(100, 500)
            q = random.choice([0.5, 0.8, 0.9])
            
            half_value = a1 * q ** 10
            
            name = ContextGenerator.get_random_name()
            statement = f"Um equipamento que custou R$ {a1},00 deprecia {int((1-q)*100)}% ao ano. Após 5 anos, seu valor será aproximadamente:"
            
            correct = a1 * (q ** 5)
            resolution = f"V = {a1} × {q}^5 = {a1} × {q**5:.4f} ≈ R$ {correct:.2f}"
            
            correct_answer = f"R$ {correct:.2f}"
            distractors = [f"R$ {correct * d:.2f}" for d in [0.8, 1.2, 1.5, 0.6]]
            
        else:
            statement = "A soma de uma PG infinita de termos positivos é 12 e a soma dos quadrados de seus termos também forma uma PG infinita cuja soma é 48. O primeiro termo da PG original é:"
            
            correct = 4
            resolution = "S = a/(1-q) = 12 e S' = a²/(1-q²) = 48. Dividindo: (1+q)/(a) = 4/12 = 1/3. Resolvendo o sistema: a = 4"
            
            correct_answer = "4"
            distractors = ["3", "6", "8", "2"]
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [str(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=4,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution
        )

    def _generate_percentage_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        if difficulty == Difficulty.FACIL:
            value = random.randint(100, 500) * 10
            percent = random.choice([10, 15, 20, 25, 30])
            
            question_type = random.choice(["find_part", "after_increase", "after_discount"])
            name = ContextGenerator.get_random_name()
            
            if question_type == "find_part":
                correct = value * percent / 100
                statement = f"{name} possui R$ {value},00 e deseja guardar {percent}% desse valor. Quanto {name} vai guardar?"
                resolution = f"{percent}% de R$ {value},00 = {percent}/100 × {value} = R$ {correct:.2f}"
            elif question_type == "after_increase":
                correct = value * (1 + percent / 100)
                statement = f"Um produto que custava R$ {value},00 sofreu um aumento de {percent}%. O novo preço é:"
                resolution = f"Novo preço = {value} × (1 + {percent}/100) = {value} × {1 + percent/100} = R$ {correct:.2f}"
            else:
                correct = value * (1 - percent / 100)
                statement = f"Uma loja oferece {percent}% de desconto em um produto de R$ {value},00. O preço com desconto é:"
                resolution = f"Preço final = {value} × (1 - {percent}/100) = {value} × {1 - percent/100} = R$ {correct:.2f}"
            
            correct_answer = f"R$ {correct:.2f}"
            distractors = [f"R$ {correct * d:.2f}" for d in [0.9, 1.1, 0.8, 1.2]]
            
        elif difficulty == Difficulty.MEDIO:
            original = random.randint(100, 300) * 10
            increase = random.choice([20, 25, 30, 40])
            discount = random.choice([10, 15, 20, 25])
            
            after_increase = original * (1 + increase / 100)
            final = after_increase * (1 - discount / 100)
            net_change = ((final / original) - 1) * 100
            
            statement = f"Um produto teve seu preço aumentado em {increase}% e, em seguida, recebeu um desconto de {discount}%. A variação percentual líquida no preço foi de:"
            
            correct = net_change
            resolution = f"Fator = (1 + {increase}/100) × (1 - {discount}/100) = {1 + increase/100} × {1 - discount/100} = {(1 + increase/100) * (1 - discount/100):.4f}. Variação = {correct:.2f}%"
            
            correct_answer = f"{correct:.1f}%"
            distractors = [f"{correct + d:.1f}%" for d in [-5, 5, -10, 10]]
            
        else:
            statement = "Em uma eleição com dois candidatos, A obteve 60% dos votos válidos. Se os votos brancos e nulos representaram 20% do total de votos e A teve 1.200.000 votos, o total de eleitores que compareceram às urnas foi:"
            
            valid_votes = 1200000 / 0.6
            total_votes = valid_votes / 0.8
            correct = int(total_votes)
            
            resolution = f"Votos de A = 60% dos válidos = 1.200.000, logo válidos = 2.000.000. Válidos = 80% do total, logo total = 2.500.000"
            
            correct_answer = "2.500.000"
            distractors = ["2.000.000", "2.400.000", "3.000.000", "1.800.000"]
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [str(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=11,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution
        )

    def _generate_generic_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        random.seed(seed + self.generated_count)
        
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        
        if difficulty == Difficulty.FACIL:
            correct = a + b
            statement = f"Quanto vale {a} + {b}?"
            resolution = f"{a} + {b} = {correct}"
        elif difficulty == Difficulty.MEDIO:
            correct = a * b
            statement = f"Calcule o produto de {a} por {b}."
            resolution = f"{a} × {b} = {correct}"
        else:
            correct = a ** 2 + b ** 2
            statement = f"Determine a² + b² para a = {a} e b = {b}."
            resolution = f"{a}² + {b}² = {a**2} + {b**2} = {correct}"
        
        correct_answer = str(correct)
        distractors = DistractorGenerator.numeric_distractors(correct, difficulty)
        
        alternatives, correct_letter = self._create_alternatives(correct_answer, [str(d) for d in distractors])
        
        return Question(
            id=str(uuid.uuid4())[:8],
            volume_id=topic.id.split('.')[0] if '.' in topic.id else 1,
            topic_id=topic.id,
            difficulty=difficulty,
            statement=statement,
            alternatives=alternatives,
            correct_answer=correct_letter,
            resolution=resolution
        )

    def _generate_logic_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_numeric_sets_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_relations_functions_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_modular_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_composition_inverse_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_powers_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_radicals_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_exponential_function_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_logarithm_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_log_function_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_trig_triangle_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_arcs_angles_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_trig_functions_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_trig_identities_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_trig_equations_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_law_sines_cosines_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_sequences_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_matrices_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_determinants_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_linear_systems_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_counting_principle_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_permutations_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_arrangements_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_combinations_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_binomial_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_conditional_prob_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_binomial_dist_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_complex_algebraic_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_complex_trig_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_polynomial_def_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_polynomial_division_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_polynomial_equations_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_roots_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_point_line_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_relative_positions_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_point_line_distance_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_circle_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_ellipse_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_hyperbola_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_parabola_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_limits_intuitive_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_limits_properties_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_infinite_limits_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_continuity_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_derivative_def_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_derivative_rules_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_derivative_elementary_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_derivative_applications_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_integral_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_geometry_fundamentals_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_triangles_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_congruence_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_similarity_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_metric_relations_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_quadrilaterals_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_regular_polygons_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_circle_properties_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_areas_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_spatial_position_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_perpendicularity_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_polyhedra_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_prisms_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_pyramids_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_cylinder_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_cone_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_sphere_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_inscribed_circumscribed_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_ratios_proportions_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_rule_of_three_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_simple_interest_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_compound_interest_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_statistics_tables_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_central_measures_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
    
    def _generate_dispersion_measures_question(self, topic: Topic, difficulty: Difficulty, seed: int) -> Question:
        return self._generate_generic_question(topic, difficulty, seed)
