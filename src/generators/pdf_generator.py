import os
from datetime import datetime
from typing import List, Optional
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from ..models.question import Question, QuestionSet, VolumeQuestionSet
from ..models.curriculum import Difficulty, get_volume


class PDFGenerator:
    def __init__(self, output_dir: str = "src/output"):
        self.output_dir = output_dir
        self.font_config = FontConfiguration()
        os.makedirs(output_dir, exist_ok=True)
    
    def get_css(self) -> str:
        return """
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&family=Open+Sans:wght@400;600;700&display=swap');
        
        @page {
            size: A4;
            margin: 2cm 2.5cm;
            
            @top-center {
                content: "Banco de Questões Matemáticas";
                font-family: 'Open Sans', sans-serif;
                font-size: 9pt;
                color: #666;
            }
            
            @bottom-center {
                content: counter(page);
                font-family: 'Open Sans', sans-serif;
                font-size: 10pt;
                color: #333;
            }
            
            @bottom-right {
                content: "Gerado em " attr(data-date);
                font-family: 'Open Sans', sans-serif;
                font-size: 8pt;
                color: #999;
            }
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Merriweather', Georgia, serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
            background: #fff;
        }
        
        .cover {
            page-break-after: always;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
            text-align: center;
            padding: 3cm;
        }
        
        .cover-title {
            font-family: 'Open Sans', sans-serif;
            font-size: 32pt;
            font-weight: 700;
            color: #1a365d;
            margin-bottom: 0.5em;
            letter-spacing: -0.02em;
        }
        
        .cover-subtitle {
            font-family: 'Open Sans', sans-serif;
            font-size: 18pt;
            font-weight: 400;
            color: #4a5568;
            margin-bottom: 2em;
        }
        
        .cover-volume {
            font-family: 'Open Sans', sans-serif;
            font-size: 24pt;
            font-weight: 600;
            color: #2b6cb0;
            margin-bottom: 0.3em;
            padding: 0.5em 1.5em;
            border: 3px solid #2b6cb0;
            border-radius: 8px;
        }
        
        .cover-description {
            font-size: 12pt;
            color: #718096;
            max-width: 80%;
            margin: 1.5em auto;
        }
        
        .cover-info {
            margin-top: 3em;
            font-size: 10pt;
            color: #a0aec0;
        }
        
        .cover-stats {
            margin-top: 2em;
            padding: 1em;
            background: #f7fafc;
            border-radius: 8px;
        }
        
        .cover-stats-item {
            display: inline-block;
            margin: 0 1.5em;
            font-family: 'Open Sans', sans-serif;
        }
        
        .cover-stats-number {
            font-size: 24pt;
            font-weight: 700;
            color: #2b6cb0;
        }
        
        .cover-stats-label {
            font-size: 9pt;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .decorative-line {
            width: 120px;
            height: 4px;
            background: linear-gradient(90deg, #2b6cb0, #4299e1);
            margin: 1.5em auto;
            border-radius: 2px;
        }
        
        .toc {
            page-break-after: always;
            padding: 1cm 0;
        }
        
        .toc-title {
            font-family: 'Open Sans', sans-serif;
            font-size: 20pt;
            font-weight: 700;
            color: #1a365d;
            margin-bottom: 1em;
            text-align: center;
        }
        
        .toc-section {
            margin-bottom: 1.5em;
        }
        
        .toc-section-title {
            font-family: 'Open Sans', sans-serif;
            font-size: 12pt;
            font-weight: 600;
            color: #2b6cb0;
            margin-bottom: 0.5em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .toc-item {
            display: flex;
            justify-content: space-between;
            padding: 0.3em 0;
            font-size: 10pt;
        }
        
        .toc-item-title {
            flex: 1;
        }
        
        .toc-item-dots {
            flex: 1;
            border-bottom: 1px dotted #cbd5e0;
            margin: 0 0.5em;
            margin-bottom: 0.4em;
        }
        
        .toc-item-page {
            color: #4a5568;
        }
        
        .section {
            page-break-before: always;
        }
        
        .section-header {
            background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
            color: white;
            padding: 1.5em 2em;
            margin: -2cm -2.5cm 2em -2.5cm;
            text-align: center;
        }
        
        .section-title {
            font-family: 'Open Sans', sans-serif;
            font-size: 18pt;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.01em;
        }
        
        .section-subtitle {
            font-family: 'Open Sans', sans-serif;
            font-size: 11pt;
            font-weight: 400;
            margin-top: 0.5em;
            opacity: 0.9;
        }
        
        .topic-header {
            margin: 2em 0 1.5em 0;
            padding-bottom: 0.5em;
            border-bottom: 2px solid #2b6cb0;
        }
        
        .topic-title {
            font-family: 'Open Sans', sans-serif;
            font-size: 14pt;
            font-weight: 600;
            color: #1a365d;
            margin: 0;
        }
        
        .topic-description {
            font-size: 10pt;
            color: #718096;
            margin-top: 0.3em;
        }
        
        .difficulty-section {
            margin: 2em 0;
        }
        
        .difficulty-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5em;
            padding: 0.8em 1em;
            border-radius: 6px;
        }
        
        .difficulty-easy {
            background: linear-gradient(90deg, #c6f6d5, #9ae6b4);
            border-left: 4px solid #38a169;
        }
        
        .difficulty-medium {
            background: linear-gradient(90deg, #fefcbf, #faf089);
            border-left: 4px solid #d69e2e;
        }
        
        .difficulty-hard {
            background: linear-gradient(90deg, #fed7d7, #feb2b2);
            border-left: 4px solid #c53030;
        }
        
        .difficulty-label {
            font-family: 'Open Sans', sans-serif;
            font-size: 12pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .difficulty-easy .difficulty-label { color: #276749; }
        .difficulty-medium .difficulty-label { color: #975a16; }
        .difficulty-hard .difficulty-label { color: #9b2c2c; }
        
        .difficulty-count {
            margin-left: auto;
            font-family: 'Open Sans', sans-serif;
            font-size: 10pt;
            padding: 0.3em 0.8em;
            background: rgba(255,255,255,0.7);
            border-radius: 20px;
        }
        
        .question {
            margin-bottom: 2.5em;
            padding: 1.5em;
            background: #fafafa;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            page-break-inside: avoid;
        }
        
        .question-header {
            display: flex;
            align-items: center;
            margin-bottom: 1em;
        }
        
        .question-number {
            font-family: 'Open Sans', sans-serif;
            font-size: 11pt;
            font-weight: 700;
            color: white;
            background: #2b6cb0;
            padding: 0.3em 0.8em;
            border-radius: 4px;
            margin-right: 1em;
        }
        
        .question-difficulty-badge {
            font-family: 'Open Sans', sans-serif;
            font-size: 8pt;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.2em 0.6em;
            border-radius: 3px;
        }
        
        .badge-easy {
            background: #c6f6d5;
            color: #276749;
        }
        
        .badge-medium {
            background: #fefcbf;
            color: #975a16;
        }
        
        .badge-hard {
            background: #fed7d7;
            color: #9b2c2c;
        }
        
        .question-statement {
            font-size: 11pt;
            line-height: 1.7;
            margin-bottom: 1.2em;
            text-align: justify;
            color: #2d3748;
        }
        
        .alternatives {
            margin: 1em 0;
            padding-left: 0;
            list-style: none;
        }
        
        .alternative {
            display: flex;
            align-items: flex-start;
            margin-bottom: 0.6em;
            font-size: 10.5pt;
        }
        
        .alternative-letter {
            font-family: 'Open Sans', sans-serif;
            font-weight: 700;
            color: #2b6cb0;
            min-width: 2em;
            margin-right: 0.5em;
        }
        
        .alternative-text {
            flex: 1;
        }
        
        .answer-section {
            margin-top: 1.5em;
            padding-top: 1em;
            border-top: 1px dashed #cbd5e0;
        }
        
        .answer-row {
            display: flex;
            margin-bottom: 0.8em;
        }
        
        .answer-label {
            font-family: 'Open Sans', sans-serif;
            font-size: 9pt;
            font-weight: 700;
            text-transform: uppercase;
            color: #4a5568;
            min-width: 80px;
            letter-spacing: 0.03em;
        }
        
        .answer-value {
            font-size: 10pt;
            color: #2d3748;
        }
        
        .answer-correct {
            font-weight: 700;
            color: #276749;
            background: #c6f6d5;
            padding: 0.1em 0.5em;
            border-radius: 3px;
        }
        
        .resolution {
            font-size: 10pt;
            color: #4a5568;
            line-height: 1.6;
            text-align: justify;
            background: #fff;
            padding: 0.8em;
            border-radius: 4px;
            border-left: 3px solid #4299e1;
        }
        
        .footer-note {
            margin-top: 3em;
            padding-top: 1em;
            border-top: 1px solid #e2e8f0;
            font-size: 9pt;
            color: #a0aec0;
            text-align: center;
        }
        
        sup, sub {
            font-size: 75%;
            line-height: 0;
            position: relative;
            vertical-align: baseline;
        }
        
        sup { top: -0.5em; }
        sub { bottom: -0.25em; }
        
        .math {
            font-family: 'Times New Roman', Times, serif;
            font-style: italic;
        }
        
        .fraction {
            display: inline-block;
            text-align: center;
            vertical-align: middle;
        }
        
        .fraction-num {
            display: block;
            border-bottom: 1px solid currentColor;
            padding: 0 0.2em;
        }
        
        .fraction-den {
            display: block;
            padding: 0 0.2em;
        }
        """
    
    def generate_cover_html(self, volume_set: VolumeQuestionSet) -> str:
        total_questions = volume_set.total_count()
        total_topics = len(volume_set.topic_sets)
        
        easy_count = sum(len(ts.get_easy_questions()) for ts in volume_set.topic_sets)
        medium_count = sum(len(ts.get_medium_questions()) for ts in volume_set.topic_sets)
        hard_count = sum(len(ts.get_hard_questions()) for ts in volume_set.topic_sets)
        
        date_str = datetime.now().strftime("%d/%m/%Y")
        
        return f"""
        <div class="cover">
            <div class="cover-title">Banco de Questões</div>
            <div class="cover-subtitle">Matemática Elementar</div>
            
            <div class="decorative-line"></div>
            
            <div class="cover-volume">Volume {volume_set.volume_id}</div>
            <div class="cover-subtitle" style="font-size: 14pt;">{volume_set.volume_name}</div>
            
            <div class="cover-description">
                Material de estudo completo com questões organizadas por nível de dificuldade,
                desenvolvido para preparação para os principais vestibulares do país.
            </div>
            
            <div class="cover-stats">
                <div class="cover-stats-item">
                    <div class="cover-stats-number">{total_questions}</div>
                    <div class="cover-stats-label">Questões</div>
                </div>
                <div class="cover-stats-item">
                    <div class="cover-stats-number">{total_topics}</div>
                    <div class="cover-stats-label">Tópicos</div>
                </div>
                <div class="cover-stats-item">
                    <div class="cover-stats-number">{easy_count}</div>
                    <div class="cover-stats-label">Fáceis</div>
                </div>
                <div class="cover-stats-item">
                    <div class="cover-stats-number">{medium_count}</div>
                    <div class="cover-stats-label">Médias</div>
                </div>
                <div class="cover-stats-item">
                    <div class="cover-stats-number">{hard_count}</div>
                    <div class="cover-stats-label">Difíceis</div>
                </div>
            </div>
            
            <div class="cover-info">
                Gerado em {date_str}
            </div>
        </div>
        """
    
    def generate_toc_html(self, volume_set: VolumeQuestionSet) -> str:
        toc_items = []
        for ts in volume_set.topic_sets:
            toc_items.append(f"""
            <div class="toc-item">
                <span class="toc-item-title">{ts.topic_id} - {ts.topic_name}</span>
                <span class="toc-item-dots"></span>
                <span class="toc-item-page">{ts.total_count()} questões</span>
            </div>
            """)
        
        return f"""
        <div class="toc">
            <div class="toc-title">Sumário</div>
            
            <div class="toc-section">
                <div class="toc-section-title">Tópicos</div>
                {''.join(toc_items)}
            </div>
        </div>
        """
    
    def generate_question_html(self, question: Question, index: int) -> str:
        difficulty_class = {
            Difficulty.FACIL: "easy",
            Difficulty.MEDIO: "medium",
            Difficulty.DIFICIL: "hard"
        }.get(question.difficulty, "medium")
        
        difficulty_label = {
            Difficulty.FACIL: "Fácil",
            Difficulty.MEDIO: "Médio",
            Difficulty.DIFICIL: "Difícil"
        }.get(question.difficulty, "Médio")
        
        alternatives_html = ""
        for alt in question.alternatives:
            alternatives_html += f"""
            <li class="alternative">
                <span class="alternative-letter">{alt.letter})</span>
                <span class="alternative-text">{alt.text}</span>
            </li>
            """
        
        return f"""
        <div class="question">
            <div class="question-header">
                <span class="question-number">Questão {index}</span>
                <span class="question-difficulty-badge badge-{difficulty_class}">{difficulty_label}</span>
            </div>
            
            <div class="question-statement">
                {question.statement}
            </div>
            
            <ul class="alternatives">
                {alternatives_html}
            </ul>
            
            <div class="answer-section">
                <div class="answer-row">
                    <span class="answer-label">Gabarito:</span>
                    <span class="answer-value answer-correct">{question.correct_answer}</span>
                </div>
                <div class="answer-row">
                    <span class="answer-label">Resolução:</span>
                    <div class="resolution">{question.resolution}</div>
                </div>
            </div>
        </div>
        """
    
    def generate_topic_section_html(self, topic_set: QuestionSet) -> str:
        sections_html = ""
        
        difficulty_configs = [
            (Difficulty.FACIL, "Questões Fáceis", "easy", topic_set.get_easy_questions()),
            (Difficulty.MEDIO, "Questões Médias", "medium", topic_set.get_medium_questions()),
            (Difficulty.DIFICIL, "Questões Difíceis", "hard", topic_set.get_hard_questions()),
        ]
        
        question_counter = 1
        
        for diff, label, css_class, questions in difficulty_configs:
            if not questions:
                continue
            
            questions_html = ""
            for q in questions:
                questions_html += self.generate_question_html(q, question_counter)
                question_counter += 1
            
            sections_html += f"""
            <div class="difficulty-section">
                <div class="difficulty-header difficulty-{css_class}">
                    <span class="difficulty-label">{label}</span>
                    <span class="difficulty-count">{len(questions)} questões</span>
                </div>
                {questions_html}
            </div>
            """
        
        return f"""
        <div class="section">
            <div class="topic-header">
                <h2 class="topic-title">{topic_set.topic_id} - {topic_set.topic_name}</h2>
                <p class="topic-description">Total de {topic_set.total_count()} questões</p>
            </div>
            {sections_html}
        </div>
        """
    
    def generate_volume_html(self, volume_set: VolumeQuestionSet) -> str:
        cover = self.generate_cover_html(volume_set)
        toc = self.generate_toc_html(volume_set)
        
        sections = ""
        for topic_set in volume_set.topic_sets:
            sections += self.generate_topic_section_html(topic_set)
        
        date_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Volume {volume_set.volume_id} - {volume_set.volume_name}</title>
        </head>
        <body data-date="{date_str}">
            {cover}
            {toc}
            
            <div class="section-header">
                <h1 class="section-title">Volume {volume_set.volume_id}</h1>
                <p class="section-subtitle">{volume_set.volume_name}</p>
            </div>
            
            {sections}
            
            <div class="footer-note">
                Banco de Questões Matemáticas - Material de Estudo<br>
                Gerado automaticamente em {date_str}
            </div>
        </body>
        </html>
        """
    
    def generate_topic_html(self, topic_set: QuestionSet) -> str:
        volume = get_volume(topic_set.volume_id)
        volume_name = volume.name if volume else f"Volume {topic_set.volume_id}"
        
        date_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        section_html = self.generate_topic_section_html(topic_set)
        
        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>{topic_set.topic_id} - {topic_set.topic_name}</title>
        </head>
        <body data-date="{date_str}">
            <div class="section-header">
                <h1 class="section-title">{topic_set.topic_name}</h1>
                <p class="section-subtitle">{volume_name}</p>
            </div>
            
            {section_html}
            
            <div class="footer-note">
                Banco de Questões Matemáticas - Material de Estudo<br>
                Gerado automaticamente em {date_str}
            </div>
        </body>
        </html>
        """
    
    def generate_volume_pdf(self, volume_set: VolumeQuestionSet) -> str:
        html_content = self.generate_volume_html(volume_set)
        css = CSS(string=self.get_css(), font_config=self.font_config)
        
        filename = f"volume_{volume_set.volume_id}_{volume_set.volume_name.replace(' ', '_').replace(',', '')[:30]}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        HTML(string=html_content).write_pdf(filepath, stylesheets=[css], font_config=self.font_config)
        
        return filepath
    
    def generate_topic_pdf(self, topic_set: QuestionSet) -> str:
        html_content = self.generate_topic_html(topic_set)
        css = CSS(string=self.get_css(), font_config=self.font_config)
        
        filename = f"topico_{topic_set.topic_id}_{topic_set.topic_name.replace(' ', '_')[:30]}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        HTML(string=html_content).write_pdf(filepath, stylesheets=[css], font_config=self.font_config)
        
        return filepath
