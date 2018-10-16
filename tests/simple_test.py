import asyncio
import bluealliance
import logging
import random
import sys

b = bluealliance.Client(
    "LW1h5uuuM3SRywkU5sjYBw0uQdqdQ4fn6cgGfHI5HpTl6jTYtET7mHR9HrJMHQlE "
)


async def test():
    # set up logging
    logger = logging.getLogger("bluealliance")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    logger.info("Current TBA status:")
    logger.info(await b.get_status())
    # teams
    logger.info("Testing intial team fetching...")
    await b.get_team(254)
    logger.info("Testing team retrieval from cache...")
    team = await b.get_team(254)
    print("Hello,", team.nickname)
    # robots
    logger.info("Testing inital robot fetching...")
    await team.get_robots()
    logger.info("Testing robot retrieval from cache...")
    robots = await team.get_robots()
    # all that matters is that we actually get the list, so this print being random doesn't compromise the test
    rob = random.choice(robots)
    print(
        "In {}, team {} named thier robot {}".format(
            rob.year, team.nickname, rob.robot_name
        )
    )
    # events
    logger.info("Testing initial event fetching...")
    await b.get_event("2016nytr")
    logger.info("Testing event retrieval from cache...")
    event = await b.get_event("2016nytr")
    print("Downloaded data for", event.name)
    # alliances
    logger.info("Testing initial event fetching...")
    await event.get_alliances()
    logger.info("Testing alliance retrieval from cache...")
    alliances = await event.get_alliances()
    print(alliances)
    logger.info("Testing team retrieval given an event...")
    d = await alliances[0].get_teams()
    print([t.nickname for t in d])
    await b.close()


asyncio.get_event_loop().run_until_complete(test())
exit(0)
