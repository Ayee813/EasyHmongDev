import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--allow-file-access-from-files','--disable-gpu'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('ERR',e))
        await pg.goto('file://'+__import__('os').path.abspath(sys.argv[1]));await pg.evaluate('window.ready')
        await pg.screenshot(path=sys.argv[2]);await b.close()
asyncio.run(main())
