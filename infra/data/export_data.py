import pandas as pd
import numpy as np

"""
ml-1M 데이터셋을 사용하여 사용자, 아이템, 인터랙션 데이터를 생성합니다.

RATINGS FILE DESCRIPTION
================================================================================

All ratings are contained in the file "ratings.dat" and are in the
following format:

UserID::MovieID::Rating::Timestamp

- UserIDs range between 1 and 6040 
- MovieIDs range between 1 and 3952
- Ratings are made on a 5-star scale (whole-star ratings only)
- Timestamp is represented in seconds since the epoch as returned by time(2)
- Each user has at least 20 ratings

USERS FILE DESCRIPTION
================================================================================

User information is in the file "users.dat" and is in the following
format:

UserID::Gender::Age::Occupation::Zip-code

All demographic information is provided voluntarily by the users and is
not checked for accuracy.  Only users who have provided some demographic
information are included in this data set.

- Gender is denoted by a "M" for male and "F" for female
- Age is chosen from the following ranges:

	*  1:  "Under 18"
	* 18:  "18-24"
	* 25:  "25-34"
	* 35:  "35-44"
	* 45:  "45-49"
	* 50:  "50-55"
	* 56:  "56+"

- Occupation is chosen from the following choices:

	*  0:  "other" or not specified
	*  1:  "academic/educator"
	*  2:  "artist"
	*  3:  "clerical/admin"
	*  4:  "college/grad student"
	*  5:  "customer service"
	*  6:  "doctor/health care"
	*  7:  "executive/managerial"
	*  8:  "farmer"
	*  9:  "homemaker"
	* 10:  "K-12 student"
	* 11:  "lawyer"
	* 12:  "programmer"
	* 13:  "retired"
	* 14:  "sales/marketing"
	* 15:  "scientist"
	* 16:  "self-employed"
	* 17:  "technician/engineer"
	* 18:  "tradesman/craftsman"
	* 19:  "unemployed"
	* 20:  "writer"

MOVIES FILE DESCRIPTION
================================================================================

Movie information is in the file "movies.dat" and is in the following
format:

MovieID::Title::Genres

- Titles are identical to titles provided by the IMDB (including
year of release)
- Genres are pipe-separated and are selected from the following genres:

	* Action
	* Adventure
	* Animation
	* Children's
	* Comedy
	* Crime
	* Documentary
	* Drama
	* Fantasy
	* Film-Noir
	* Horror
	* Musical
	* Mystery
	* Romance
	* Sci-Fi
	* Thriller
	* War
	* Western

- Some MovieIDs do not correspond to a movie due to accidental duplicate
entries and/or test entries
- Movies are mostly entered by hand, so errors and inconsistencies may exist

"""
USER_OCCUPATION_MAP = {
    0: "other",
    1: "academic/educator",
    2: "artist",
    3: "clerical/admin",
    4: "college/grad student",
    5: "customer service",
    6: "doctor/health care",
    7: "executive/managerial",
    8: "farmer",
    9: "homemaker",
    10: "K-12 student",
    11: "lawyer",
    12: "programmer",
    13: "retired",
    14: "sales/marketing",
    15: "scientist",
    16: "self-employed",
    17: "technician/engineer",
    18: "tradesman/craftsman",
    19: "unemployed",
    20: "writer"
}


def load_movielens_data():
    """MovieLens 데이터를 로드합니다."""
    print("MovieLens 데이터 로딩 중...")
    
    # 유저 정보 로딩
    u_cols = ['user_id', 'gender', 'age', 'occupation', 'zip-code']
    users = pd.read_csv('ml-1m/users.dat', names=u_cols, sep='::', encoding='latin-1', engine='python')
    
    # 영화 정보 로딩
    m_cols = ['movie_id', 'title', 'genre']
    movies = pd.read_csv('ml-1m/movies.dat', names=m_cols, sep='::', encoding='latin-1', engine='python')
    movies['genre'] = movies.genre.apply(lambda x: x.split('|'))
    
    # 평점 데이터 로딩
    r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_csv('ml-1m/ratings.dat', names=r_cols, sep='::', engine='python')
    
    # 사용자 수를 1000명으로 제한 (메모리 절약)
    valid_user_ids = sorted(ratings.user_id.unique())[:1000]
    ratings = ratings[ratings["user_id"].isin(valid_user_ids)]
    users = users[users["user_id"].isin(valid_user_ids)]
    valid_movie_ids = sorted(ratings.movie_id.unique())[:1000]
    movies = movies[movies["movie_id"].isin(valid_movie_ids)]
    
    print(f"로딩 완료: {len(ratings)}개의 평점, {len(ratings.user_id.unique())}명의 사용자, {len(ratings.movie_id.unique())}개의 영화")
    
    return users, movies, ratings

def create_user_data(users):
    """사용자 데이터를 생성합니다."""
    print("사용자 데이터 생성 중...")

    users_data = users[['user_id', 'gender', 'age', 'occupation']].drop_duplicates().copy()
    
    # 컬럼명을 스키마에 맞게 변경
    users_data = users_data.rename(columns={
        'user_id': 'USER_ID',
        'gender': 'GENDER',
        'age': 'AGE',
        'occupation': 'OCCUPATION'
    })
    
    users_data = users_data[['USER_ID', 'GENDER', 'AGE', 'OCCUPATION']]
    
    return users_data

def create_item_data(movies):
    """아이템 데이터를 생성합니다."""
    print("아이템 데이터 생성 중...")
    
    items_data = movies[['movie_id', 'title', 'genre']].copy()
    
    # genre, tag를 문자열로 변환 (리스트 -> 파이프(|)로 join, 최대 1000자)
    def limit_string_length(val, max_length=1000):
        if isinstance(val, list):
            clean_list = [str(x) for x in val if pd.notnull(x)]
            
            # 전체 길이가 max_length를 넘으면 요소를 하나씩 제거
            while len('|'.join(clean_list)) > max_length and len(clean_list) > 1:
                clean_list.pop()
            
            return '|'.join(clean_list)
        elif pd.isnull(val):
            return ''
        else:
            str_val = str(val)
            return str_val[:max_length] if len(str_val) > max_length else str_val
    
    items_data['genre'] = items_data['genre'].apply(lambda x: limit_string_length(x))
    
    items_data = items_data.drop_duplicates().copy()
    
    # 컬럼명을 스키마에 맞게 변경
    items_data = items_data.rename(columns={
        'movie_id': 'ITEM_ID',
        'title': 'TITLE',
        'genre': 'GENRE'
    })
    
    # 필요한 컬럼만 선택
    items_data = items_data[['ITEM_ID', 'TITLE', 'GENRE']]
    
    return items_data

def create_interaction_data(ratings):
    """인터랙션 데이터를 생성합니다."""
    print("인터랙션 데이터 생성 중...")
    
    interactions_data = ratings[['user_id', 'movie_id', 'rating', 'timestamp']].copy()
    
    # 컬럼명을 스키마에 맞게 변경
    interactions_data = interactions_data.rename(columns={
        'user_id': 'USER_ID',
        'movie_id': 'ITEM_ID',
        'rating': 'RATING',
        'timestamp': 'TIMESTAMP'
    })
    
    # 필요한 컬럼만 선택
    interactions_data = interactions_data[['USER_ID', 'ITEM_ID', 'RATING', 'TIMESTAMP']]
    
    return interactions_data

def save_to_csv(users_data, items_data, interactions_data):
    """데이터를 CSV 파일로 저장합니다."""
    print("CSV 파일로 저장 중...")
    
    # CSV 파일로 저장
    users_data.to_csv('csv/users.csv', index=False)
    items_data.to_csv('csv/items.csv', index=False)
    interactions_data.to_csv('csv/interactions.csv', index=False)
    
    print("저장 완료!")
    print(f"사용자 수: {len(users_data)}")
    print(f"아이템 수: {len(items_data)}")
    print(f"인터랙션 수: {len(interactions_data)}")
    print("\n저장된 파일:")
    print("- csv/users.csv")
    print("- csv/items.csv")
    print("- csv/interactions.csv")

def main():
    """메인 함수"""
    try:
        # 데이터 로딩
        users, movies, ratings = load_movielens_data()
        
        # 각 데이터 생성
        users_data = create_user_data(users)
        items_data = create_item_data(movies)
        interactions_data = create_interaction_data(ratings)
        
        # CSV 파일로 저장
        save_to_csv(users_data, items_data, interactions_data)
        
        print("\n=== 데이터 추출 완료 ===")
        
    except FileNotFoundError as e:
        print(f"오류: {e}")
        print("MovieLens 데이터 파일이 없습니다. 먼저 data_download.ipynb를 실행하여 데이터를 다운로드하세요.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main() 