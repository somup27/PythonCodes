import turicreate
import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

ratings_train = pd.read_csv('datas/ua.base',sep='\t',names=r_cols,encoding='latin-1')
ratings_test = pd.read_csv('datas/ua.test',sep='\t',names=r_cols,encoding='latin-1')

#Creating SFrames of the training and testing data
train_data = turicreate.SFrame(ratings_train)
test_data = turicreate.Sframe(ratings_test)

#Construct engine based on popularity of items
popularity_model = turicreate.popularity_recommender.create(train_data, user_id='user_id', item_id='movie_id', target='rating')

#Recommend items based on popularity
popularity_recomm = popularity_model.recommend(users=[1,2,3,4,5],k=5)
popularity_recomm.print_rows(num_rows=25)

#Training the item-item collaborative filtering model
item_sim_model = turicreate.item_similarity_recommender.create(train_data, user_id='user_id', item_id='movie_id', target='rating', similarity_type='cosine')

#Making recommendations
item_sim_recomm = item_sim_model.recommend(users=[1,2,3,4,5],k=5)
item_sim_recomm.print_rows(num_rows=25)