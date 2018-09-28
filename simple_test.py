import asyncio
import bluealliance

b = bluealliance.Client(
    'LW1h5uuuM3SRywkU5sjYBw0uQdqdQ4fn6cgGfHI5HpTl6jTYtET7mHR9HrJMHQlE ')


async def test():
    print("Current TBA status:")
    print(await b.get_status())
    await b.get_team(254)
    team = await b.get_team(254)
    print(team.nickname)
    robots = await team.get_robots()
    print(robots)
    event = await b.get_event("2016nytr")
    print(event.name)
    alliances = await event.get_alliances()

asyncio.get_event_loop().run_until_complete(test())
