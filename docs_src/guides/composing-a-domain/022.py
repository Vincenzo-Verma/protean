import random
import time

from protean import Domain


def gen_ids(prefix="id"):
    timestamp = int(time.time() * 1000)  # Milliseconds since epoch
    return f"{prefix}-{timestamp}-{random.randint(0, 1000)}"


domain = Domain(identity_function=gen_ids)

# or you can pass parameters too
# domain = Domain(identity_function=lambda: gen_ids("foo"))
