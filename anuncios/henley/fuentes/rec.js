const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
 const card=await b.newPage({viewport:{width:1080,height:1920}});await card.goto('file://'+process.argv[2]+'/card.html',{waitUntil:'networkidle'});await card.evaluate(()=>document.fonts.ready);await card.screenshot({path:process.argv[2]+'/card.png'});await card.close();
 const ctx=await b.newContext({viewport:{width:540,height:960},deviceScaleFactor:2,recordVideo:{dir:process.argv[2]+'/rec',size:{width:540,height:960}}});
 const p=await ctx.newPage();await p.goto('file://'+process.argv[3],{waitUntil:'networkidle'});await p.waitForTimeout(800);
 for(let y=0;y<=900;y+=12){await p.evaluate(v=>window.scrollTo(0,v),y);await p.waitForTimeout(16);}
 await p.waitForTimeout(500);await ctx.close();await b.close();})();
