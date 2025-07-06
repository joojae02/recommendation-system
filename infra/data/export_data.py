import pandas as pd
import numpy as np

def load_movielens_data():
    """MovieLens 데이터를 로드합니다."""
    print("MovieLens 데이터 로딩 중...")
    
    # 영화 정보 로딩
    m_cols = ['movie_id', 'title', 'genre']
    movies = pd.read_csv('ml-10M100K/movies.dat', names=m_cols, sep='::', encoding='latin-1', engine='python')
    movies['genre'] = movies.genre.apply(lambda x: x.split('|'))
    
    # 사용자 부여한 영화의 태그 정보 로딩
    t_cols = ['user_id', 'movie_id', 'tag', 'timestamp']
    user_tagged_movies = pd.read_csv('ml-10M100K/tags.dat', names=t_cols, sep='::', engine='python')

    # tag를 소문자로 한다
    user_tagged_movies['tag'] = user_tagged_movies['tag'].str.lower()
    
    # tag를 영화별로 list 형식으로 저장한다
    movie_tags = user_tagged_movies.groupby('movie_id').agg({'tag':list})
    
    # 태그 정보를 결합한다
    movies = movies.merge(movie_tags, on='movie_id', how='left')
    
    # 태그가 없는 경우 빈 리스트로
    movies['tag'] = movies['tag'].apply(lambda x: x if isinstance(x, list) else [])
    
    # 평점 데이터 로딩
    r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_csv('ml-10M100K/ratings.dat', names=r_cols, sep='::', engine='python')
    
    # 사용자 수를 1000명으로 제한 (메모리 절약)
    valid_user_ids = sorted(ratings.user_id.unique())[:1000]
    ratings = ratings[ratings["user_id"].isin(valid_user_ids)]
    
    # 데이터 결합
    movielens = ratings.merge(movies, on='movie_id')
    
    print(f"로딩 완료: {len(movielens)}개의 평점, {len(movielens.user_id.unique())}명의 사용자, {len(movielens.movie_id.unique())}개의 영화")
    print(movielens.head())
    return movielens

def create_user_data(movielens):
    """사용자 데이터를 생성합니다."""
    print("사용자 데이터 생성 중...")
    
    users_data = movielens[['user_id']].drop_duplicates().copy()
    
    # 컬럼명을 스키마에 맞게 변경
    users_data = users_data.rename(columns={'user_id': 'USER_ID'})
    
    return users_data

def create_item_data(movielens):
    """아이템 데이터를 생성합니다."""
    print("아이템 데이터 생성 중...")
    
    items_data = movielens[['movie_id', 'title', 'genre', 'tag']].copy()
    
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
    items_data['tag'] = items_data['tag'].apply(lambda x: limit_string_length(x))
    
    items_data = items_data.drop_duplicates().copy()
    
    # 컬럼명을 스키마에 맞게 변경
    items_data = items_data.rename(columns={
        'movie_id': 'ITEM_ID',
        'title': 'TITLE',
        'genre': 'GENRE',
        'tag': 'TAG'
    })
    
    # 필요한 컬럼만 선택
    items_data = items_data[['ITEM_ID', 'TITLE', 'GENRE', 'TAG']]
    
    return items_data

def create_interaction_data(movielens):
    """인터랙션 데이터를 생성합니다."""
    print("인터랙션 데이터 생성 중...")
    
    interactions_data = movielens[['user_id', 'movie_id', 'rating', 'timestamp']].copy()
    
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
    print("- users.csv")
    print("- items.csv")
    print("- interactions.csv")

def main():
    """메인 함수"""
    try:
        # 데이터 로딩
        movielens = load_movielens_data()
        
        # 각 데이터 생성
        users_data = create_user_data(movielens)
        items_data = create_item_data(movielens)
        interactions_data = create_interaction_data(movielens)
        
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