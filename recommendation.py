import pandas as pd

def get_recommendations(user_id, user_item_matrix, user_similarity_df):
    if user_id not in user_similarity_df.index:
        raise ValueError(f"User ID {user_id} not found in user_similarity_df")

    # Retrieve similar users, ignoring the user itself
    similar_users = user_similarity_df.loc[user_id].sort_values(ascending=False).index[1:]

    # Calculate average ratings of similar users
    similar_users_ratings = user_item_matrix.loc[similar_users].mean()
    
    # Sort recommendations by rating
    recommendations = similar_users_ratings.sort_values(ascending=False)
    
    return recommendations
