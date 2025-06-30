from model_utils import Choices

IMAGE_SCALE = Choices(
    ('RAW', 'RAW', '원본'),  # 원본
    ('DETAIL', 'DETAIL', '상세'),  # 상세보기
    ('NORMAL', 'NORMAL', '일반'),  # 일반
    ('THUMBNAIL', 'THUMBNAIL', '미리보기'),  # 미리보기
    ('AVATAR', 'AVATAR', '아바타'),  # 미리보기
)