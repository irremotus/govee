import asyncio

from govee.temp.scanner import GoveeScanner


async def main():
    def found_device(data):
        print(data)

    scanner = GoveeScanner()
    scanner.register(found_device)
    await scanner.start()
    await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
