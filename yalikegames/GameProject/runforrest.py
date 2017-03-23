from gamelib3 import *
game=Game(800,600,"Habitual Runner")
bk=Image("GameProject\\city.png",game)
bk.resizeTo(game.width,game.height)
game.setBackground(bk)
game.setMusic("GameProject\\Wheatley2.wav")
platforms=[]
jumping=False
landed=False
factor=1
currentrocklanded=-1
for num in range(8):
    platforms.append(Image("GameProject\\sverige.png",game))
platforms[0].moveTo(game.width,randint(100,500))
platforms[0].setSpeed(2,90)
platforms[0].resizeBy(-70)
for pos in range(1,len(platforms)):
    x=platforms[pos-1].right + randint(0,1)
    y=randint(100,500)
    platforms[pos].setSpeed(2,90)
    platforms[pos].moveTo(x,y)
    platforms[pos].resizeBy(-70)
hero=Animation("GameProject\\run.png",8,game,108,140,-5)
hero.resizeBy(-15)
hero.setSpeed(2,90)
hero.moveTo(platforms[0].x,platforms[0].y-60)
crusty=Animation("GameProject\\crab.png",12,game,400,297,-2)
crusty.moveTo(100,430)
crusty.resizeBy(50)
jump=Animation("GameProject\\jump.gif",10,game,43.9,76,-3)
jump.resizeTo(hero.width-20,hero.height)
rocket=Image("GameProject\\rocket.png",game)
rocket.resizeBy(-50)
rocket.setSpeed(2,90)
y=platforms[pos-1].top-75
x=randint(5000,7000)
#rocket.moveTo(x,y)
bkspeed=7
blood=Animation("GameProject\\blood.png",9,game,500,500)
blood.resizeBy(-70)
blood.visible=False
ground=Image("GameProject\\ground.png",game)
ground.resizeBy(-50)
ground.moveTo(ground.x+10000,600)
ground.setSpeed(2,90)
finish=Image("GameProject\\finishflags.png",game)
finish.resizeBy(-50)
finish.moveTo(ground.x+200,ground.y-100)
finish.setSpeed(2,90)
roar=Sound("GameProject\\crustyroar.wav",1)
blastoff=Sound("GameProject\\thruster.wav",2)
powerup= False
while not game.over:
    game.processInput()
    game.scrollBackground("left",3)
    game.drawText("Habitual Runner",game.width/4,game.height/4,Font(blue,90,white))
    game.drawText("Press [SPACE] to Start",game.width/2+80,game.height-50,Font(blue,40,white))
    if keys.Pressed[K_SPACE]:
        game.over=True
        game.playMusic()
    game.update(60)
game.over=False
while not game.over:    
    game.processInput()
    game.scrollBackground("left",bkspeed)
    hero.move()
    hero.y+=5
    rocket.draw()
    ground.move()
    finish.move()
    onrock=False
    if hero.collidedWith(finish):
        game.over=True
    if keys.Pressed[K_RIGHT]:
        hero.x+=5  
    if keys.Pressed[K_LEFT]:
        hero.x-=5
    if keys.Pressed[K_UP]:
        jumping=True
        hero.y-=9
        hero.x+=6
    for p in platforms:
        p.move()
        if p.isOffScreen("left"):
            x=game.width+randint(100,500)
            y=randint(100,500)
            p.moveTo(x,y)
            if hero.collidedWith(p,"rectangle")and hero.bottom<p.top+15 and hero.x>p.left and hero.x<p.right:
                onrock=True
                landed=True
                jumping=False
                hero.y-=5
                if hero.collidedWith(p,"rectangle")and hero.bottom<p.top+200:  
                    onrock=True
                    landed=True
                    jumping=False
                    hero.y-=5
                else:
                    landed=True
            if jumping:
                landed=False
                hero.y -= 18 * factor
                factor *= .95
                landed = False
                if factor < .18:
                    jumping = False
                    factor = 1
                if not onrock:
                    hero.y+=5
        if hero.collidedWith(rocket):
            game.time=5
            hero.visible=False
            rocket.rotateBy(90,"right")
            bkspeed+=14
            powerup=True
            roar.play()
            blastoff.play()
        if bkspeed>7 and game.time>0:
            crusty.x-=7
            p.x-=19
            hero.y-=5
    crusty.draw()
    if rocket.isOffScreen("left"):
        y=platforms[pos-1].top+200
        x=randint(5000,7000)
        rocket.moveTo(x,y)
    if hero.isOffScreen("bottom"):
        game.over=True
    if hero.collidedWith(crusty,"circle"):
        blood.visible=True
        blood.moveTo(hero.x,hero.y)
        hero.visible=False
        game.over=True
    if game.time < 1 and powerup:
        rocket.visible = False
        powerup= False
        hero.visible=True
        bkspeed=7
        hero.moveTo(rocket.x,rocket.y)
        crusty.moveTo(100,430)
        y=platforms[pos-1].top-75
        x=randint(5000,7000)
        rocket.moveTo(x,y)
    game.update(60)
game.drawText("GAME OVER",game.width/4,game.height/4,Font(red,90,white))
game.drawText("Press [ESC] to Exit",game.width/2+80,game.height-50,Font(red,40,white))
game.stopMusic()
game.update(60)
game.wait(K_ESCAPE)
game.quit()
