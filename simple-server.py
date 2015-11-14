import logging
import asyncio
import functools
import os
import signal
import aiohttp
from aiohttp import web


async def healthcheck(request):
    """
    Healthcheck end point which Kubernetes hits to check if the container is still running.
    """

    logger.info("HTTP Health Check")

    return web.Response(body=b"All good!")


async def a():
    await asyncio.sleep(3)

    raise Exception("My Exception from a()")


async def b():
    for i in range(0, 120):
        await asyncio.sleep(1)
        logger.info("Loop in b()")
    raise Exception("My Exception from b()")


async def process1():
    while True:
        await a()


async def process2():
    while True:
        await b()


async def main():
    """
    Function to serve as the main of the server. It first sets up a HTTP server endpoint to respond to
    Kubernetes HTTP health checks then creates and runs the user defined tasks.
    """

    app = web.Application()
    app.router.add_route('GET', '/healthcheck/', healthcheck)
    handler = app.make_handler()
    srv = loop.create_server(handler, '0.0.0.0', 8080)
    await srv

    # Our tasks.
    t1 = loop.create_task(process1())
    t2 = loop.create_task(process2())

    pending = [t1, t2]

    # This loop may seem over complicated but waiting on tasks is necessary to get any exceptions that are raised
    # within the task. This loop allows such exceptions to be logged immediately not when the process exits.
    while True:
        if len(pending) is 0:
            break

        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            try:
                task.result()
            except Exception as e:
                logger.exception("Got exception in main for task {}".format(task))


def exit(signame, loop, task):
    """
    Signal handler to gracefully shut down the process when getting a SIGTERM. Kubernetes sends Docker a SIGTERM
    when it wants to shut down a pod an Docker sends the process inside the container a SIGTERM.
    """

    logger.info("Received SIGTERM. Shutting down.")
    tasks = asyncio.Task.all_tasks()
    for task in tasks:
        task.cancel()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name="python-asyncio-kubernetes-template")

    loop = asyncio.get_event_loop()
    loop.set_debug(False)

    task = loop.create_task(main())

    for signame in ('SIGTERM',):
        loop.add_signal_handler(getattr(signal, signame), functools.partial(exit, signame, loop, task))

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt as e:
        tasks = asyncio.Task.all_tasks()
        for task in tasks:
            task.cancel()
        loop.run_forever()
    except asyncio.CancelledError as e:
        # From the SIGTERM handler.
        pass
    finally:
        loop.close()
