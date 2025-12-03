# MathQuest - Gerador Supremo de Questões Matemáticas

## Visão Geral

O MathQuest é um sistema avançado de geração de questões de matemática desenvolvido em Python com Flask. O sistema gera questões únicas e variadas, organizadas por Volumes, Tópicos e níveis de Dificuldade, com foco em preparação para vestibulares de alta dificuldade (ITA, IME, ENEM).

## Estrutura do Projeto

```
.
├── app.py                          # Aplicação Flask principal
├── src/
│   ├── models/
│   │   ├── curriculum.py           # Modelo de currículo (11 volumes, tópicos)
│   │   └── question.py             # Modelo de questões e alternativas
│   └── generators/
│       ├── question_engine.py      # Motor de geração de questões
│       ├── question_templates.py   # Templates e geradores de contexto
│       └── pdf_generator.py        # Gerador de PDF com WeasyPrint
├── templates/                      # Templates HTML Jinja2
│   ├── base.html
│   ├── index.html
│   ├── generate.html
│   ├── preview.html
│   ├── questions.html
│   ├── volume_questions.html
│   └── about.html
└── static/
    └── css/
        └── style.css               # Estilos CSS da interface
```

## Características Principais

### Questões Únicas
- Sistema de hash para garantir unicidade absoluta
- Variação de parâmetros numéricos
- Contextos e cenários aleatórios
- Nomes e situações diversificados

### Distribuição de Dificuldade
- **40% Fácil**: Nível Ensino Fundamental/Médio inicial
- **40% Médio**: Nível ENEM/Vestibulares
- **20% Difícil**: Nível ITA/IME/Olimpíadas

### Volumes Cobertos (11 volumes)
1. Conjuntos, Lógica e Funções Básicas
2. Potências, Raízes, Logaritmos e Exponenciais
3. Trigonometria
4. Sequências, Matrizes e Sistemas Lineares
5. Análise Combinatória e Probabilidade
6. Números Complexos e Polinômios
7. Geometria Analítica
8. Limites, Derivadas e Integrais
9. Geometria Plana
10. Geometria Espacial
11. Matemática Financeira e Estatística

## Tecnologias Utilizadas

- **Flask**: Framework web Python
- **WeasyPrint**: Geração de PDFs profissionais
- **SymPy**: Validação matemática e cálculos simbólicos
- **Jinja2**: Templates HTML
- **CSS3**: Estilização moderna da interface

## Como Executar

O projeto é executado automaticamente pelo workflow configurado:

```bash
python app.py
```

A aplicação estará disponível na porta 5000.

## API Endpoints

### Interface Web
- `GET /` - Página inicial com listagem de volumes
- `GET /generate` - Formulário de geração de questões
- `GET /preview/<volume_id>` - Visualização dos tópicos de um volume
- `GET /about` - Informações sobre o sistema

### API REST
- `GET /api/volumes` - Lista todos os volumes
- `GET /api/volume/<id>/topics` - Lista tópicos de um volume
- `POST /api/generate/topic` - Gera questões de um tópico
- `POST /api/generate/volume` - Gera questões de um volume completo
- `POST /api/generate/pdf/topic` - Gera PDF de um tópico
- `POST /api/generate/pdf/volume` - Gera PDF de um volume

## Arquivos de Saída

Os PDFs gerados são salvos em `src/output/` com nomes descritivos:
- `volume_X_Nome_do_Volume.pdf`
- `topico_X.X_Nome_do_Topico.pdf`

## Preferências do Usuário

- Interface em português brasileiro
- Foco em vestibulares ITA/IME
- PDFs visualmente elegantes
- Questões com contextos criativos e relevantes
- Gabarito e resolução detalhada inclusos

## Sistema de Unicidade

O sistema implementa um registro de hash persistente com padrão singleton:
- Cache armazenado em `src/output/.cache/` em arquivos JSON por tópico
- Classe `UniqueHashRegistry` com método `get_instance()` para singleton
- Hashes são salvos imediatamente após cada verificação
- Garante que questões não se repetem entre sessões

## Alterações Recentes

- **02/12/2025**: Sistema completo implementado
  - Motor de geração com 11 volumes e 80+ geradores específicos
  - Interface web Flask responsiva com seleção dinâmica de tópicos
  - Gerador de PDF profissional com WeasyPrint
  - Sistema de unicidade por hash com persistência singleton
