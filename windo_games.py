"""Popular Android games known to Windo (all devices)."""
RAW = """
@*
!Deletes the game. Progress is lost unless it is linked to an account or cloud save.
com.supercell.clashofclans|Clash of Clans|s|Base-building strategy game.
com.supercell.clashroyale|Clash Royale|s|Card battle game.
com.supercell.brawlstars|Brawl Stars|s|Multiplayer brawler.
com.supercell.hayday|Hay Day|s|Farming game.
com.supercell.boombeach|Boom Beach|s|Strategy game.
com.supercell.squad|Squad Busters|s|Multiplayer battle game.
com.supercell.clashmini|Clash Mini|s|Auto-battler game.
com.tencent.ig|PUBG Mobile|s|Battle royale shooter.
com.pubg.imobile|BGMI|s|Battle royale shooter (India).
com.tencent.iglite|PUBG Mobile Lite|s|Lightweight battle royale.
com.pubg.newstate|PUBG: New State|s|Battle royale shooter.
com.activision.callofduty.shooter|Call of Duty Mobile|s|Shooter game.
com.activision.callofduty.warzone|Call of Duty: Warzone Mobile|s|Battle royale shooter.
com.garena.game.codm|Call of Duty Mobile (Garena)|s|Shooter game.
com.riotgames.league.wildrift|LoL: Wild Rift|s|MOBA game.
com.riotgames.league.teamfighttactics|Teamfight Tactics|s|Auto-battler game.
com.dts.freefireth|Free Fire|s|Battle royale shooter.
com.dts.freefiremax|Free Fire MAX|s|Battle royale shooter.
com.mobile.legends|Mobile Legends|s|MOBA game.
com.mojang.minecraftpe|Minecraft|s|Sandbox building game.
com.roblox.client|Roblox|s|Online game platform.
com.epicgames.fortnite|Fortnite|s|Battle royale shooter.
com.miHoYo.GenshinImpact|Genshin Impact|s|Open-world RPG.
com.HoYoverse.hkrpgoversea|Honkai: Star Rail|s|Turn-based RPG.
com.HoYoverse.Nap|Zenless Zone Zero|s|Action RPG.
com.miHoYo.bh3oversea|Honkai Impact 3rd|s|Action RPG.
com.kurogame.wutheringwaves.global|Wuthering Waves|s|Action RPG.
com.levelinfinite.sgameGlobal|Honor of Kings|s|MOBA game.
com.king.candycrushsodasaga|Candy Crush Soda Saga|s|Puzzle game.
com.king.candycrushjellysaga|Candy Crush Jelly Saga|s|Puzzle game.
com.king.bubblewitch3saga|Bubble Witch 3 Saga|s|Puzzle game.
com.king.farmheroessaga|Farm Heroes Saga|s|Puzzle game.
com.king.petrescuesaga|Pet Rescue Saga|s|Puzzle game.
com.gameloft.android.ANMP.GloftA8HM|Asphalt 8|s|Racing game.
com.gameloft.android.ANMP.GloftA9HM|Asphalt 9|s|Racing game.
com.gameloft.android.ANMP.GloftM5HM|Modern Combat 5|s|Shooter game.
com.gameloft.android.ANMP.GloftDMHM|Disney Magic Kingdoms|s|Park building game.
com.ea.game.pvzfree_row|Plants vs. Zombies|s|Tower defense game.
com.ea.game.pvz2_row|Plants vs. Zombies 2|s|Tower defense game.
com.ea.gp.fifamobile|FIFA Mobile|s|Football game.
com.ea.gp.apexlegendsmobilefps|Apex Legends Mobile|s|Battle royale shooter.
com.ea.gp.nbamobile|NBA Live Mobile|s|Basketball game.
com.ea.game.simcitymobile_row|SimCity BuildIt|s|City builder.
com.ea.game.sims3_row|The Sims FreePlay|s|Life simulation game.
com.ea.games.r3_row|Real Racing 3|s|Racing game.
com.ea.game.nfs14_row|Need for Speed No Limits|s|Racing game.
com.miniclip.eightballpool|8 Ball Pool|s|Pool game.
com.miniclip.carrom|Carrom Pool|s|Board game.
com.miniclip.agar.io|Agar.io|s|Arcade game.
com.miniclip.plagueinc|Plague Inc.|s|Strategy game.
com.kiloo.subwaysurf|Subway Surfers|s|Endless runner.
com.imangi.templerun|Temple Run|s|Endless runner.
com.imangi.templerun2|Temple Run 2|s|Endless runner.
com.rovio.angrybirds|Angry Birds|s|Puzzle game.
com.rovio.baba|Angry Birds 2|s|Puzzle game.
com.zynga.words3|Words With Friends 2|s|Word game.
com.zynga.livepoker|Zynga Poker|s|Card game.
com.zynga.FarmVille2CountryEscape|FarmVille 2|s|Farming game.
com.playrix.gardenscapes|Gardenscapes|s|Puzzle and decoration game.
com.playrix.homescapes|Homescapes|s|Puzzle and decoration game.
com.playrix.township|Township|s|Farm and city game.
com.playrix.fishdomdd|Fishdom|s|Puzzle game.
com.playrix.manormatters|Manor Matters|s|Puzzle and decoration game.
com.nianticlabs.pokemongo|Pokemon GO|s|Augmented reality game.
com.nianticproject.ingress|Ingress|s|Augmented reality game.
com.outfit7.talkingtom|Talking Tom|s|Virtual pet game.
com.outfit7.mytalkingtom2|My Talking Tom 2|s|Virtual pet game.
com.halfbrick.fruitninjafree|Fruit Ninja|s|Arcade game.
com.halfbrick.jetpackjoyride|Jetpack Joyride|s|Arcade game.
com.fingersoft.hillclimb|Hill Climb Racing|s|Racing game.
com.fingersoft.hcr2|Hill Climb Racing 2|s|Racing game.
com.innersloth.spacemafia|Among Us|s|Social deduction game.
com.ludo.king|Ludo King|s|Board game.
com.firsttouchgames.dls3|Dream League Soccer|s|Football game.
com.firsttouchgames.dls7|Dream League Soccer (new)|s|Football game.
jp.konami.pesam|eFootball|s|Football game.
com.nekki.shadowfight|Shadow Fight 2|s|Fighting game.
com.nekki.shadowfight3|Shadow Fight 3|s|Fighting game.
com.netease.dwrg|Identity V|s|Asymmetric horror game.
com.netease.chiji|Rules of Survival|s|Battle royale shooter.
com.bandainamcogames.dblegends_ww|Dragon Ball Legends|s|Fighting game.
com.bandainamcogames.dbzdokfanww|Dragon Ball Z Dokkan Battle|s|Puzzle RPG.
com.pokemon.unite|Pokemon UNITE|s|MOBA game.
jp.pokemon.pokemonhome|Pokemon HOME|s|Storage app for your Pokemon.
com.robtopx.geometryjump|Geometry Dash|s|Rhythm platformer.
com.kitkagames.fallbuddies|Stumble Guys|s|Party game.
com.fgol.HungrySharkEvolution|Hungry Shark Evolution|s|Arcade game.
com.yodo1.crossyroad|Crossy Road|s|Arcade game.
com.ustwo.monumentvalley|Monument Valley|s|Puzzle game.
com.mobigame.zombietsunami|Zombie Tsunami|s|Runner game.
com.mobilityware.solitaire|Solitaire|s|Card game.
com.axlebolt.standoff2|Standoff 2|s|Shooter game.
com.criticalforceentertainment.criticalops|Critical Ops|s|Shooter game.
com.madfingergames.deadtrigger2|Dead Trigger 2|s|Zombie shooter.
com.ubisoft.brawlhalla|Brawlhalla|s|Fighting game.
com.tocaboca.tocalifeworld|Toca Life World|s|Sandbox play game.
com.playgendary.bowmasters|Bowmasters|s|Archery game.
com.appsomniacs.da2|Mini Militia|s|Shooter game.
com.olzhas.carparking.multyplayer|Car Parking Multiplayer|s|Driving game.
com.nintendo.zaka|Mario Kart Tour|s|Racing game.
com.nintendo.zara|Super Mario Run|s|Platformer game.
com.nintendo.zaba|Fire Emblem Heroes|s|Strategy RPG.
com.nintendo.zaca|Animal Crossing: Pocket Camp|s|Life simulation game.
com.igg.android.lordsmobile|Lords Mobile|s|Strategy game.
com.lilithgame.roc.gp|Rise of Kingdoms|s|Strategy game.
com.plarium.raidlegends|Raid: Shadow Legends|s|RPG.
com.topgamesinc.evony|Evony|s|Strategy game.
com.kingsgroup.sos|State of Survival|s|Zombie strategy game.
es.socialpoint.DragonCity|Dragon City|s|Monster game.
es.socialpoint.MonsterLegends|Monster Legends|s|Monster game.
com.moonactive.coinmaster|Coin Master|s|Casual game with ads.
com.buffalo_studios.newslots|Bingo Blitz|s|Bingo game.
air.com.playtika.slotomania|Slotomania|s|Casino slots game.
com.huuuge.casino.slots|Huuuge Casino|s|Casino slots game.
com.ddi|DoubleDown Casino|s|Casino slots game.
com.pacificinteractive.HouseOfFun|House of Fun|s|Casino slots game.
com.peoplefun.wordcross|Wordscapes|s|Word puzzle game.
com.lotum.photoguess|4 Pics 1 Word|s|Puzzle game.
com.etermax.preguntados.lite|Trivia Crack|s|Quiz game.
com.amanotes.magictiles3|Magic Tiles 3|s|Rhythm game.
com.naturalmotion.customstreetracer2|CSR Racing 2|s|Racing game.
com.ninjakiwi.bloonstd6|Bloons TD 6|s|Tower defense game.
com.kabam.marvelbattle|Marvel Contest of Champions|s|Fighting game.
com.nexon.bluearchive|Blue Archive|s|RPG.
com.YoStarEN.Arknights|Arknights|s|Tower defense game.
com.aniplex.fategrandorder.en|Fate/Grand Order|s|RPG.
com.peakgames.toonblast|Toon Blast|s|Puzzle game.
com.dreamgames.royalmatch|Royal Match|s|Puzzle game.
com.tgc.sky.android|Sky: Children of the Light|s|Adventure game.
com.scopely.monopolygo|Monopoly GO|s|Board game.
com.pixel.gun3d|Pixel Gun 3D|s|Shooter game.
com.tripledot.woodoku|Woodoku|s|Block puzzle game.
com.easybrain.sudoku.android|Sudoku.com|s|Number puzzle game.
"""
