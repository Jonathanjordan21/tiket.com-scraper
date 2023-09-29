import pandas as pd
import json
import os


def load_data(dict_name):
    df_data = pd.DataFrame()
    questionTitles = []
    for file_name in os.listdir(dict_name):
        try :
            with open(os.path.join(dict_name, file_name), "r") as f:
                a = json.loads(json.loads(f.read()))['data']
    
                df = pd.DataFrame(a['userReviews']['content'])
                df.dropna(inplace=True)

                questionTitles += list(set([y['questionTitle'] for x in df['userReviewAnswers'].values for y in x ]))

                for index, row in df['userReviewAnswers'].items():
                    for k in row:
                        key = k['questionTitle']
                        col = k['answerInteger']
                        df.at[index, f"Rating_{key}"] = col
                        df.at[index, key] = k['answerString']

                df_data = pd.concat([df_data, df], ignore_index=True)

        except Exception as e: 
            print("error! file_name:", file_name+dict_name)
    
    return df_data.drop(columns=['userReviewAnswers','likedByMe','reviewSource', 'totalItems']), list(set(questionTitles))