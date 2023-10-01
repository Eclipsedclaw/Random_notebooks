"""
Control smart plug at home
Aur: Jiancheng Zeng
Date: Oct 1, 2023
"""

import asyncio
import kasa

async def main():
    dev = kasa.SmartPlug("24.91.173.178", port = 14121)  # Only provide the IP address
    await dev.update()
    print(dev.alias)
    for n in range(100):
        print(f"{n+1} loop")
        await dev.turn_on()
        await asyncio.sleep(30)
        await dev.turn_off()
        await asyncio.sleep(1200)

if __name__ == "__main__":
    asyncio.run(main())
