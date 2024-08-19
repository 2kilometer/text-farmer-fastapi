import os
import pickle
import time

from sklearn.metrics.pairwise import cosine_similarity

from tf_idf_bow.repository.tf_idf_bow_repository import TfIdfBowRepository


class TfIdfBowRepositoryImpl(TfIdfBowRepository):
    VECTORIZATION_FILE_PATH = os.path.join(
        os.getcwd(), "assets", "totalAnswerVectorization.pickle"
    )
    RAW_ANSWERS_FILE_PATH = os.path.join(
        os.getcwd(), "assets", "answers_8cols.pickle"
    )
    TOP_RANK_LIMIT = 3
    SIMILARITY_THRESHOLD = 0.1

    def findSimilarText(self, userQuestion):
        stime = time.time()
        with open(self.VECTORIZATION_FILE_PATH, "rb") as pickleFile:
            countVectorizer = pickle.load(pickleFile)
            countMatrix = pickle.load(pickleFile)
            # answerList = pickle.load(pickleFile)

        with open(self.RAW_ANSWERS_FILE_PATH, "rb") as pickleFile:
            allAnswerData = pickle.load(pickleFile)

        userQuestionVector = countVectorizer.transform([userQuestion])
        cosineSimilarityList = cosine_similarity(userQuestionVector, countMatrix).flatten()
        similarIndexList = cosineSimilarityList.argsort()[-self.TOP_RANK_LIMIT:][::-1]
        similarAnswerList = [allAnswerData.iloc[index, :]
                             for index in similarIndexList
                             if cosineSimilarityList[index] >= self.SIMILARITY_THRESHOLD]
        etime = time.time()

        similarityValueList = [cosineSimilarityList[index]
                             for index in similarIndexList
                             if cosineSimilarityList[index] >= self.SIMILARITY_THRESHOLD]

        print(similarAnswerList)
        print(similarityValueList)
        print(f"{etime-stime} 초")

        return similarAnswerList