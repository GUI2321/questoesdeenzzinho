from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
from datetime import datetime

from src.models.curriculum import (
    get_all_volumes, get_volume, get_all_topics_for_volume, 
    get_topic, Difficulty, calculate_question_distribution
)
from src.generators.question_engine import QuestionGenerator
from src.generators.pdf_generator import PDFGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

generator = QuestionGenerator()
pdf_generator = PDFGenerator()


@app.route('/')
def index():
    volumes = get_all_volumes()
    return render_template('index.html', volumes=volumes)


@app.route('/api/volumes')
def api_volumes():
    volumes = get_all_volumes()
    result = []
    for vol_id, vol in volumes.items():
        result.append({
            'id': vol.id,
            'name': vol.name,
            'description': vol.description,
            'topics_count': len(vol.topics)
        })
    return jsonify(result)


@app.route('/api/volume/<int:volume_id>/topics')
def api_topics(volume_id):
    topics = get_all_topics_for_volume(volume_id)
    result = []
    for topic in topics:
        result.append({
            'id': topic.id,
            'name': topic.name,
            'description': topic.description,
            'subtopics': topic.subtopics
        })
    return jsonify(result)


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    volumes = get_all_volumes()
    
    if request.method == 'POST':
        volume_id = int(request.form.get('volume_id', 1))
        topic_id = request.form.get('topic_id')
        questions_count = int(request.form.get('questions_count', 20))
        generate_pdf = request.form.get('generate_pdf') == 'on'
        
        try:
            if topic_id and topic_id != 'all':
                question_set = generator.generate_topic_questions(
                    volume_id, topic_id, questions_count
                )
                
                if generate_pdf:
                    pdf_path = pdf_generator.generate_topic_pdf(question_set)
                    return send_file(
                        pdf_path,
                        as_attachment=True,
                        download_name=os.path.basename(pdf_path)
                    )
                else:
                    return render_template(
                        'questions.html',
                        question_set=question_set,
                        volume=get_volume(volume_id)
                    )
            else:
                volume_set = generator.generate_volume_questions(
                    volume_id, questions_count
                )
                
                if generate_pdf:
                    pdf_path = pdf_generator.generate_volume_pdf(volume_set)
                    return send_file(
                        pdf_path,
                        as_attachment=True,
                        download_name=os.path.basename(pdf_path)
                    )
                else:
                    return render_template(
                        'volume_questions.html',
                        volume_set=volume_set
                    )
        except Exception as e:
            return render_template(
                'generate.html',
                volumes=volumes,
                error=str(e)
            )
    
    return render_template('generate.html', volumes=volumes)


@app.route('/api/generate/topic', methods=['POST'])
def api_generate_topic():
    data = request.get_json()
    volume_id = data.get('volume_id', 1)
    topic_id = data.get('topic_id')
    questions_count = data.get('questions_count', 20)
    
    if not topic_id:
        return jsonify({'error': 'topic_id is required'}), 400
    
    try:
        question_set = generator.generate_topic_questions(
            volume_id, topic_id, questions_count
        )
        
        questions_data = []
        for q in question_set.questions:
            questions_data.append(q.to_dict())
        
        return jsonify({
            'success': True,
            'volume_id': volume_id,
            'topic_id': topic_id,
            'topic_name': question_set.topic_name,
            'total_questions': len(questions_data),
            'questions': questions_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/volume', methods=['POST'])
def api_generate_volume():
    data = request.get_json()
    volume_id = data.get('volume_id', 1)
    questions_per_topic = data.get('questions_per_topic', 20)
    
    try:
        volume_set = generator.generate_volume_questions(
            volume_id, questions_per_topic
        )
        
        topics_data = []
        for ts in volume_set.topic_sets:
            topic_questions = [q.to_dict() for q in ts.questions]
            topics_data.append({
                'topic_id': ts.topic_id,
                'topic_name': ts.topic_name,
                'questions': topic_questions
            })
        
        return jsonify({
            'success': True,
            'volume_id': volume_id,
            'volume_name': volume_set.volume_name,
            'total_questions': volume_set.total_count(),
            'topics': topics_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/pdf/topic', methods=['POST'])
def api_generate_pdf_topic():
    data = request.get_json()
    volume_id = data.get('volume_id', 1)
    topic_id = data.get('topic_id')
    questions_count = data.get('questions_count', 20)
    
    if not topic_id:
        return jsonify({'error': 'topic_id is required'}), 400
    
    try:
        question_set = generator.generate_topic_questions(
            volume_id, topic_id, questions_count
        )
        pdf_path = pdf_generator.generate_topic_pdf(question_set)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=os.path.basename(pdf_path)
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/pdf/volume', methods=['POST'])
def api_generate_pdf_volume():
    data = request.get_json()
    volume_id = data.get('volume_id', 1)
    questions_per_topic = data.get('questions_per_topic', 20)
    
    try:
        volume_set = generator.generate_volume_questions(
            volume_id, questions_per_topic
        )
        pdf_path = pdf_generator.generate_volume_pdf(volume_set)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=os.path.basename(pdf_path)
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/preview/<int:volume_id>')
def preview_volume(volume_id):
    volume = get_volume(volume_id)
    if not volume:
        return redirect(url_for('index'))
    
    topics = get_all_topics_for_volume(volume_id)
    return render_template('preview.html', volume=volume, topics=topics)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    os.makedirs('src/output', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
