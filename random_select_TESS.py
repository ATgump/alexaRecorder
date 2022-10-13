import random
import os
import shutil
fixed_tess_path = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess"

emotion_groups = []
import itertools
for folder in os.listdir(fixed_tess_path):
    key_func = lambda c: c[10]
    for key,group in itertools.groupby(os.listdir(os.path.join(fixed_tess_path,folder)),key=key_func):
        #print(key)
        emotion_groups.append((list(group),folder,str(key)))
#print(len(emotion_groups))
#print(emotion_groups)
#picked_files = []
rand_ints_chosen = []
emotion_split = {}
for i in [1,3,4,5,6]:
    emotion_split[str(i)]=[]

for eg in emotion_groups:
    #print(eg[1])
    picked_files = []
    # for i in range(0,10):
    #     # rand = random.randint(0,(len(eg[0])-1))
    #     # while rand in rand_ints_chosen:
    #     #     rand = random.randint(0,(len(eg[0])-1))
    #     #     #print(rand)
    #     # rand_ints_chosen.append(rand)
    #rint(rand)
    print(len(eg[0]))
    picked_files = [(random.sample(eg[0],10),eg[1])]
    #print(picked_files)
    emotion_split[eg[2]] = emotion_split[eg[2]] + picked_files

print(len(emotion_split["1"]))
#print(len(emotion_groups))

# DEST = r"C:\Users\avery\OneDrive\Documents\tess_sample_diff_DB_test2"
# for emotion_key in emotion_split.keys():
#     print(emotion_split[key])
#     os.mkdir(os.path.join(DEST,emotion_key))
#     for actor_tuple in emotion_split[emotion_key]:
#         #print(actor_tuple)
#         #os.mkdir(os.path.join(DEST,emotion_key,actor_tuple[1]))
#         for file in actor_tuple[0]:
#             shutil.copy(os.path.join(fixed_tess_path,actor_tuple[1],file),os.path.join(DEST,emotion_key))





