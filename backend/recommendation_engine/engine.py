import gc
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack, csr_matrix
import pandas as pd
import numpy as np

from dao.media_dao import MediaDAO
from utils.media_util import MediaUtil

"""
Dictionary of Terms: 
    df = data frame
    sim_df = df de similaridade
    ctt_sim_df = content sim_df
    cll_sim_df = collaborative sim_df 
    id2meta = dict[movie id | movie meta data]
"""

class Engine:
    def __init__(self):
        self.id2idx = {}
        self.idx2id = {}
        self.sim_matrix = self._create_sparse_similarity_matrix()
        self.cll_sim_df = "TO-DO..."

    def _create_sparse_similarity_matrix(self):
        vec = TfidfVectorizer()
        dao = MediaDAO()

        data = dao.load_media_to_df_content()
        MediaUtil.normalize_media_genres(data)
        MediaUtil.normalize_media_credits(data)

        df = pd.DataFrame(data)
        media_ids = df['id'].tolist()
        self.id2idx = {id_: idx for idx, id_ in enumerate(media_ids)}
        self.idx2id = {idx: id_ for id_, idx in self.id2idx.items()}

        # Store metadata
        self.id2meta = (df.set_index('id')[
            ['title', 'description', 'release_date', 'poster_path', 'backdrop_path']]
            .to_dict(orient='index'))

        tfidf_genres = vec.fit_transform(df['media_genres_normalized']) * 3
        tfidf_credits = vec.fit_transform(df['media_credits_normalized']) * 5
        tfidf_desc = vec.fit_transform(df['description']) * 0.5
        tfidf_dates = vec.fit_transform(df['release_date']) * 2

        combined = hstack([tfidf_genres, tfidf_credits, tfidf_desc, tfidf_dates]).tocsr()

        del tfidf_genres, tfidf_credits, tfidf_desc, tfidf_dates
        gc.collect()

        # Use sparse dot product directly to get cosine similarity matrix
        sim_sparse = cosine_similarity(combined, dense_output=False)

        return sim_sparse  # scipy.sparse.csr_matrix

    def recommend_media(self, user_history_scores: dict[str, int]) -> pd.Series:
        score_vector = np.zeros(self.sim_matrix.shape[0], dtype=np.float32)

        for media_id, user_score in user_history_scores.items():
            if media_id in self.id2idx:
                idx = self.id2idx[media_id]
                score_vector += self.sim_matrix[idx].toarray().flatten() * user_score

        # Zero out scores of already seen media
        for media_id in user_history_scores:
            if media_id in self.id2idx:
                idx = self.id2idx[media_id]
                score_vector[idx] = 0.0

        # Convert back to media IDs and return as Series
        result = pd.Series(score_vector, index=[self.idx2id[i] for i in range(len(score_vector))])
        return result.sort_values(ascending=False)

if __name__ == '__main__':
    engine = Engine()
    user_rec = {
        552524: 4,
        1396: 1,
        1022789: 5
    }
    recomendation = engine.recommend_media(user_rec)
    print(recomendation)