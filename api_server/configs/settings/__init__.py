import os
from pathlib import Path
import environ

# .env 로드 (기존 환경변수도 덮어쓰기)
ENV_ROOT = Path(__file__).resolve().parent.parent.parent.parent
environ.Env.read_env(os.path.join(ENV_ROOT, '.env'), overwrite=True)
env = os.environ
ENV_TYPE = os.getenv('RUNNING_ENV', 'base')

try:
    exec('from .{} import *'.format(ENV_TYPE))
except ImportError:
    from .base import *
