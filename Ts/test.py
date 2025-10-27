import asyncio
import random

LINK_LENGTH = 70
SIGNAL_LENGTH = 3
PROPAGATION_DELAY = 0.05  # sekundy
DECAY_TIME = 6  # liczba kroków zanim sygnał znika

class Medium:
    def __init__(self, length):
        self.link = ['_'] * length
        self.lock = asyncio.Lock()
        self.decay = [0] * length

    async def propagate(self, position, symbol):
        async with self.lock:
            if 0 <= position < len(self.link):
                current = self.link[position]
                if current == '_' or current == symbol:
                    self.link[position] = symbol
                    self.decay[position] = DECAY_TIME
                elif current.islower() and current != symbol:
                    self.link[position] = 'X'
                    self.decay[position] = DECAY_TIME

    async def decay_signals(self):
        async with self.lock:
            for i in range(len(self.link)):
                if self.link[i] != '_' and self.link[i].isalpha():
                    self.decay[i] -= 1
                    if self.decay[i] <= 0:
                        self.link[i] = '_'

    async def is_idle(self, position):
        async with self.lock:
            return self.link[position] == '_'

    def __str__(self):
        return ''.join(self.link)

class Station:
    def __init__(self, name, position, medium, start_delay=0.0):
        self.name = name
        self.pos = position
        self.medium = medium
        self.symbol = name.lower()
        self.start_delay = start_delay

    async def run(self):
        await asyncio.sleep(self.start_delay)
        while True:
            await asyncio.sleep(random.uniform(0.1, 0.2))
            if await self.medium.is_idle(self.pos):
                print(f"🚀 Stacja {self.name} nadaje z pozycji {self.pos}")
                collision = False

                for i in range(SIGNAL_LENGTH):
                    left = self.pos - i
                    right = self.pos + i
                    await self.medium.propagate(left, self.symbol)
                    await self.medium.propagate(right, self.symbol)
                    await asyncio.sleep(PROPAGATION_DELAY)

                async with self.medium.lock:
                    for i in range(self.pos - SIGNAL_LENGTH, self.pos + SIGNAL_LENGTH + 1):
                        if 0 <= i < LINK_LENGTH and self.medium.link[i] == 'X':
                            collision = True
                            break

                if collision:
                    backoff = random.uniform(0.5, 1.0)
                    print(f"⚠️  Stacja {self.name}: kolizja, backoff ({SIGNAL_LENGTH}) {backoff:.2f}s")
                    await asyncio.sleep(backoff)
                else:
                    print(f"✅ Stacja {self.name}: transmisja zakończona pomyślnie\n")
                    break

async def print_loop(medium):
    while True:
        print(medium)
        await asyncio.sleep(0.1)
        await medium.decay_signals()

async def main():
    medium = Medium(LINK_LENGTH)
    station_A = Station('A', 5, medium, start_delay=0.2)
    station_B = Station('B', 30, medium, start_delay=0.2)
    station_C = Station('C', 55, medium, start_delay=0.2)

    # wstawienie stacji do kabla
    medium.link[station_A.pos] = 'A'
    medium.link[station_B.pos] = 'B'
    medium.link[station_C.pos] = 'C'

    await asyncio.gather(
        station_A.run(),
        station_B.run(),
        station_C.run(),
        print_loop(medium)
    )

asyncio.run(main())
