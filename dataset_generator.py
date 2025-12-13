import random
import string

def generate_room_names(n):
    dataset = []
    for _ in range(n):
        pattern = random.choice([1, 2, 3, 4])

        if pattern == 1:
            # R.{angka}
            name = f"R.{random.randint(1, 500)}"

        elif pattern == 2:
            # Lab{huruf}.{angka}
            letter = random.choice(string.ascii_uppercase)
            name = f"Lab{letter}.{random.randint(1, 500)}"

        elif pattern == 3:
            # A{angka}.{angka}
            name = f"A{random.randint(1, 50)}.{random.randint(1, 50)}"

        elif pattern == 4:
            # {huruf}{angka}.{angka}
            letter = random.choice(string.ascii_uppercase)
            name = f"{letter}{random.randint(1, 50)}.{random.randint(1, 50)}"

        dataset.append(name)

    return dataset
