import asyncio
import random
import time
from typing import List

LINK_LENGTH = 60
PROPAGATION_DELAY = 0.1
JAM_SIGNAL_LENGTH = 4
MAX_RETRIES = 5

class Medium:
    def __init__(self, length):
        self.length = length
        self.state = ['_'] * length
        self.lock = asyncio.Lock()

    async def update(self, updates):
        async with self.lock:
            for pos, val in updates.items():
                if 0 <= pos < self.length:
                    if self.state[pos] in ['_', val]:
                        self.state[pos] = val
                    elif self.state[pos] != val and self.state[pos] not in ['X', 'A', 'B', 'C']:
                        self.state[pos] = 'X'  # Kolizja

    def snapshot(self) -> List[str]:
        return self.state.copy()

    async def reset_non_station(self):
        async with self.lock:
            for i in range(self.length):
                if self.state[i] not in ['A', 'B', 'C']:
                    self.state[i] = '_'

    def is_idle(self):
        return all(c in ['_', 'A', 'B', 'C'] for c in self.state)

class Station:
    def __init__(self, name: str, pos: int, medium: Medium):
        self.name = name
        self.pos = pos
        self.medium = medium
        self.retry = 0
        self.active = True

    async def run(self):
        await self.medium.update({self.pos: self.name})
        await asyncio.sleep(random.uniform(0.5, 1.5))

        while self.retry < MAX_RETRIES and self.active:
            if self.medium.is_idle():
                success = await self.transmit()
                if success:
                    print(f"[{self.name}] Transmission successful")
                    return
                else:
                    self.retry += 1
                    backoff = random.uniform(0.1, 0.5) * (2 ** self.retry)
                    print(f"[{self.name}] Collision detected, backing off for {backoff:.2f}s")
                    await asyncio.sleep(backoff)
                    await self.medium.reset_non_station()
            else:
                await asyncio.sleep(random.uniform(0.1, 0.3))

        print(f"[{self.name}] Gave up after {self.retry} retries")

    async def transmit(self):
        signal = self.name.lower()
        left = self.pos - 1
        right = self.pos + 1
        updates = {self.pos: self.name}

        for _ in range((LINK_LENGTH // 2)):
            if left >= 0:
                updates[left] = signal
                left -= 1
            if right < LINK_LENGTH:
                updates[right] = signal
                right += 1

            await self.medium.update(updates)
            snap = self.medium.snapshot()
            if 'X' in snap:
                await self.jam()
                return False
            await asyncio.sleep(PROPAGATION_DELAY)

        return True

    async def jam(self):
        jam_signal = 'X'
        for _ in range(JAM_SIGNAL_LENGTH):
            updates = {}
            for offset in range(-JAM_SIGNAL_LENGTH, JAM_SIGNAL_LENGTH + 1):
                pos = self.pos + offset
                if 0 <= pos < LINK_LENGTH:
                    updates[pos] = jam_signal
            await self.medium.update(updates)
            await asyncio.sleep(PROPAGATION_DELAY)

async def print_loop(medium: Medium, duration=100000):
    start = time.time()
    while time.time() - start < duration:
        print(''.join(medium.snapshot()))
        await asyncio.sleep(0.1)

async def main():
    medium = Medium(LINK_LENGTH)
    station_A = Station('A', 5, medium)
    station_B = Station('B', 30, medium)
    station_C = Station('C', 55, medium)

    await asyncio.gather(
        print_loop(medium),
        station_A.run(),
        station_B.run(),
        station_C.run(),
    )

asyncio.run(main())