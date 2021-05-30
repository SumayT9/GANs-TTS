# Updates JSON file from AssemblyAI to combine sentences which have less than a 20 second gap between them 


import json

def should_combine(sentence1, sentence2):
    first_end = sentence1['end']
    second_start = sentence2['start']

    difference = second_start - first_end

    if difference <= 20:
        return True
    else:
        return False


def combine(sentence1, sentence2):

    text_1 = sentence1['text']
    text_2 = sentence2['text']
    all_text = text_1 + " " + text_2

    start = sentence1['start']
    end = sentence2['end']

    confidence_1 = sentence1['confidence']
    confidence_2 = sentence2['confidence']
    new_confidence = (confidence_1+confidence_2)/2

    speaker = sentence1['speaker']

    words_1 = sentence1['words']
    words_2 = sentence2['words']   
    all_words = words_1+words_2 

    new_sentence = {
        'text': all_text,
        'start': start,
        'end': end,
        'confidence': new_confidence,
        'words': all_words  
    }
     
    return new_sentence


def save_file(filename, data):
    with open(filename + '.json', 'w') as json_file:
        text = json.dumps(data)
        json_file.write(text)

# For debugging
updated_indices = []

def combine_file(path):

    json_file = open(path)
    json_data = json.load(json_file)

    data_id = json_data['id']
    confidence = json_data['confidence']
    audio_duration = json_data['audio_duration']

    data = {
        "sentences": [],
        "audio_duration": audio_duration

    }
    
    i = 0
    length = len(json_data["sentences"])
    while i < length:
        print(i)

        if i+1 < length:

            sentence = json_data["sentences"][i]
            next_sentence = json_data["sentences"][i+1]

            should_combine_sents = should_combine(sentence, next_sentence)
        
            if should_combine_sents:
                combined = combine(sentence, next_sentence)
                data['sentences'].append(combined)
                # print("updating with first end: ", sentence['end'])
                # print("second start: ", next_sentence['start'])
                # print("difference: ", next_sentence['start'] - sentence['end'])
                updated_indices.append([i, i+1])
                i += 2

            else:
                data['sentences'].append(sentence)
                # print("not updating updating with first end: ", sentence['end'])
                # print("second start: ", next_sentence['start'])
                # print("difference: ", next_sentence['start'] - sentence['end'])

                i +=1
        else:
            sentence = json_data["sentences"][i]

            data['sentences'].append(sentence)
            print(i)
            i += 1
        
    return data
    

# if __name__ == "__main__":  
#     data = combine_file("test_j_2.json")
#     save_file("updated", data) 

# print(updated_indices)