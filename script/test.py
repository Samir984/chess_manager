from core.models import User
import time


def run():
    print("start")
    s = time.time()
    d = User.objects.all()
    print(d)
    e = time.time()
    print(f"time: {e-s}")

