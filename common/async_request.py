import async_timeout
import json
import aiohttp


async def make_request(host: str, port: int, end: str, method: str, data: dict = None):
    try:
        with async_timeout.timeout(59):
            async with aiohttp.ClientSession() as session:
                request = getattr(session, method)
                async with request(url="http://{}:{}/{}".format(host, port, end), json=data) as response:
                    res = await response.read()
                    if res:
                        data = json.loads(res)
                    return (data, response.status)
    except TimeoutError:
        return None, 408
    except aiohttp.ClientConnectorError:
        return None, 503
