exec(open("betterkara.py", "r").read())


kara.pickupleaf(2)
kara.move_num(5)
kara.turn_180()
kara.pickupleaf(1)
kara.move_num(10)


tools.sleep(300)


kara.lookdown()
kara.lookup()
kara.lookleft()
kara.lookright()

tools.sleep(300)

if kara.islookingup():
    tools.showMessage("Kara schaut nach Oben")
elif kara.islookingdown():
    tools.showMessage("Kara schaut nach Unten")
elif kara.islookingright():
    tools.showMessage("Kara schaut nach Rechts")
elif kara.islookingleft():
    tools.showMessage("Kara schaut nach Links")

tools.sleep(300)

kara.put()

tools.sleep(300)

kara.clear()
  
tools.sleep(300)

text = tools.stringInput("Text zum schreiben eingeben")

kara.writestring(text)
