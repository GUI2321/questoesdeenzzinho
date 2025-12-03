from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import hashlib
import uuid
from .curriculum import Difficulty


@dataclass
class Alternative:
    letter: str
    text: str
    is_correct: bool = False


@dataclass
class Question:
    id: str
    volume_id: int
    topic_id: str
    difficulty: Difficulty
    statement: str
    alternatives: List[Alternative]
    correct_answer: str
    resolution: str
    context: Optional[str] = None
    source_inspiration: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    hash_signature: str = field(default="")
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        if not self.hash_signature:
            self.hash_signature = self._generate_hash()
    
    def _generate_hash(self) -> str:
        content = f"{self.statement}{self.correct_answer}{self.resolution}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_formatted_alternatives(self) -> str:
        lines = []
        for alt in self.alternatives:
            lines.append(f"{alt.letter}) {alt.text}")
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "volume_id": self.volume_id,
            "topic_id": self.topic_id,
            "difficulty": self.difficulty.value,
            "statement": self.statement,
            "alternatives": [
                {"letter": a.letter, "text": a.text, "is_correct": a.is_correct}
                for a in self.alternatives
            ],
            "correct_answer": self.correct_answer,
            "resolution": self.resolution,
            "context": self.context,
            "source_inspiration": self.source_inspiration,
            "hash_signature": self.hash_signature
        }


@dataclass
class QuestionSet:
    volume_id: int
    topic_id: str
    topic_name: str
    questions: List[Question] = field(default_factory=list)
    
    def get_questions_by_difficulty(self, difficulty: Difficulty) -> List[Question]:
        return [q for q in self.questions if q.difficulty == difficulty]
    
    def get_easy_questions(self) -> List[Question]:
        return self.get_questions_by_difficulty(Difficulty.FACIL)
    
    def get_medium_questions(self) -> List[Question]:
        return self.get_questions_by_difficulty(Difficulty.MEDIO)
    
    def get_hard_questions(self) -> List[Question]:
        return self.get_questions_by_difficulty(Difficulty.DIFICIL)
    
    def total_count(self) -> int:
        return len(self.questions)
    
    def add_question(self, question: Question):
        self.questions.append(question)


@dataclass
class VolumeQuestionSet:
    volume_id: int
    volume_name: str
    topic_sets: List[QuestionSet] = field(default_factory=list)
    
    def add_topic_set(self, topic_set: QuestionSet):
        self.topic_sets.append(topic_set)
    
    def get_all_questions(self) -> List[Question]:
        all_questions = []
        for ts in self.topic_sets:
            all_questions.extend(ts.questions)
        return all_questions
    
    def total_count(self) -> int:
        return sum(ts.total_count() for ts in self.topic_sets)
