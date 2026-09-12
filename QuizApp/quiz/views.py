from django.shortcuts import render, get_object_or_404
from .models import Topic, Question, Choice

def home(request):
    topics = Topic.objects.all()
    return render(request, 'quiz/home.html', {'topics': topics})

def take_exam(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        topic = get_object_or_404(Topic, id=topic_id)
        
        # Grab 60 random questions for this topic
        questions = Question.objects.filter(topic=topic).order_by('?')[:60]
        
        return render(request, 'quiz/exam.html', {
            'topic': topic,
            'questions': questions
        })

def submit_exam(request):
    if request.method == 'POST':
        score = 0
        total_questions = 0
        summary = []
        
        for key, value in request.POST.items():
            if key.startswith('question_'):
                total_questions += 1
                question_id = key.split('_')[1]
                
                try:
                    question = Question.objects.get(id=question_id)
                    selected_choice = Choice.objects.get(id=value)
                    correct_choice = question.choices.get(is_correct=True)
                    
                    is_correct = selected_choice.is_correct
                    if is_correct:
                        score += 1
                        
                    summary.append({
                        'question_text': question.text,
                        'selected': selected_choice.text,
                        'correct': correct_choice.text,
                        'is_correct': is_correct,
                        'explanation': question.explanation
                    })
                except (Question.DoesNotExist, Choice.DoesNotExist):
                    pass
        
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        return render(request, 'quiz/result.html', {
            'score': score,
            'total_questions': total_questions,
            'percentage': round(percentage, 2),
            'summary': summary
        })