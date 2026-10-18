import asyncio,sys,os
from playwright.async_api import async_playwright
async def main():
    s,e,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3];os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--allow-file-access-from-files','--disable-gpu'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda x:print('ERR',x))
        await pg.goto('file://'+os.path.abspath(sys.argv[4]));await pg.evaluate('window.ready')
        for i in range(s,e):
            await pg.evaluate(f'render({i}/15)');await pg.screenshot(path=f'{out}/f{i:05d}.jpg',type='jpeg',quality=94)
        await b.close()
asyncio.run(main())
