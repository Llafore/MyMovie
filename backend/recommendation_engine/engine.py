import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        self.ctt_sim_df = self._create_df_content()
        self.cll_sim_df = "TO-DO..."

    def  _create_df_content(self):
        vec = TfidfVectorizer()
        dao = MediaDAO()

        data = dao.load_media_to_df_content()
        MediaUtil.normalize_media_genres(data)
        df = pd.DataFrame(data)
        self.id2meta = (df.set_index('id')[
            ['title','description','release_date','poster_path','backdrop_path']]
                        .to_dict(orient='index'))

        tfidf_genres = vec.fit_transform(df['media_genres_normalized']) * 3
        tfidf_desc = vec.fit_transform(df['description']) * 0.5
        tfdf_release_date = vec.fit_transform(df['release_date']) * 2

        combined = hstack([tfidf_genres, tfidf_desc, tfdf_release_date])

        sim = cosine_similarity(combined)

        sim_df = pd.DataFrame(sim, index=df['id'], columns=df['id'])

        return sim_df
    def recommend_media(
        self,
        user_history_scores: dict[int, int]
    ) -> pd.Series:
        media_similarity_scores = pd.Series(0.0, index=self.ctt_sim_df.index, dtype=float)

        for media_id, user_score in user_history_scores.items():
            if media_id in self.ctt_sim_df.columns:
                media_similarity_scores += user_score * self.ctt_sim_df[media_id]

        for media_id in user_history_scores:
            media_similarity_scores.pop(media_id)

        sorted_scores = media_similarity_scores.sort_values(ascending=False)
        print(sorted_scores)

        return sorted_scores

    # def recommend_media(self, past_recommendations: dict[int, int], top_n=10):
    #     score_ctt = pd.Series(0.0, index=self.ctt_sim_df.index, dtype=float)

    #     for media, score in past_recommendations.items():
    #         if media in self.ctt_sim_df.columns:
    #             score_ctt += score * self.ctt_sim_df[media]

    #     for past_recommendation in past_recommendations:
    #         if past_recommendation in score_ctt.index:
    #             score_ctt.drop(past_recommendation, inplace=True)

    #     recommendations = score_ctt.sort_values(ascending=False).head(top_n)
    #     return recommendations


if __name__ == '__main__':
    engine = Engine()
    user_rec = {
        552524: 4,
        1396: 1,
        1022789: 5
    }
    recomendation = engine.recommend_media(user_rec)
    print(recomendation)