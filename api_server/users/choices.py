from model_utils import Choices

MBTI_TYPE = Choices(
    ('ENFJ', 'ENFJ', 'ENFJ'),
    ('ENFP', 'ENFP', 'ENFP'),
('ENTJ', 'ENTJ', 'ENTJ'),
('ENTP', 'ENTP', 'ENTP'),
('ESFJ', 'ESFJ', 'ESFJ'),
('ESFP', 'ESFP', 'ESFP'),
('ESTJ', 'ESTJ', 'ESTJ'),
('ESTP', 'ESTP', 'ESTP'),
('INFJ', 'INFJ', 'INFJ'),
('INFP', 'INFP', 'INFP'),
('INTJ', 'INTJ', 'INTJ'),
('INTP', 'INTP', 'INTP'),
('ISFJ', 'ISFJ', 'ISFJ'),
('ISFP', 'ISFP', 'ISFP'),
('ISTJ', 'ISTJ', 'ISTJ'),
('ISTP', 'ISTP', 'ISTP'),
)

GENDER_TYPE = Choices(
    ('M', 'MALE', '남자'),
    ('F', 'FEMALE', '여자'),
    ('U', 'OTHER', '미제공'),
)

IMAGE_SCALE = Choices(
    ('RAW', 'RAW', '원본'),  # 원본
    ('DETAIL', 'DETAIL', '상세'),  # 상세보기
    ('NORMAL', 'NORMAL', '일반'),  # 일반
    ('THUMBNAIL', 'THUMBNAIL', '미리보기'),  # 미리보기
    ('AVATAR', 'AVATAR', '아바타'),  # 미리보기
)