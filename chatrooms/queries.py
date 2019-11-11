from chatrooms.models import Post, ChatSyn, Data


def get_all_validated_questions_texts():
    return Post.objects.filter(type=1).exclude(answer__isnull=True).values_list('body', flat=True)
    

def get_all_validated_questions_keys():
    return Post.objects.filter(type=1).exclude(answer__isnull=True).values_list('body_key', flat=True)


def get_answer_text_to_question(question):
    q = Post.objects.filter(body=question).exclude(answer__isnull=True)
    if q.count() > 0:
        return q[0].answer.body
    return None


def get_first_answer_text_to_question_keys(textkeys):
    q = Post.objects.filter(body_key=textkeys).exclude(answer__isnull=True)
    if q.count() > 0:
        return q[0].answer.body
    return None


def get_key_synonyms(textkeys):
    keys = ChatSyn.objects.filter(body_key_syn=textkeys).exclude(synonym=False)
    if keys.count() > 0:
        return keys[0].body_key
    return None
    
    
def get_key_false_synonyms(textkeys):
    keys = ChatSyn.objects.filter(body_key_syn=textkeys).exclude(synonym=True)
    if keys.count() > 0:
        return keys[0].body_key
    return None


def get_data_text_to_fit():
    return Data.objects.filter(raw_text__isnull=False)
