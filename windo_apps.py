"""Popular Android apps (social, streaming, shopping, tools...) known to Windo (all devices)."""
RAW = """
@*
!Removes the app. Its local data may be lost; reinstall it from the store to use it again.
# ---- social and messaging
com.whatsapp.w4b|WhatsApp Business|m|Business messaging.|You lose WhatsApp Business until reinstalled. Back up chats first.
com.viber.voip|Viber|s|Messaging and calls.
com.facebook.lite|Facebook Lite|s|Light Facebook app.
com.facebook.mlite|Messenger Lite|s|Light Messenger app.
com.discord|Discord|s|Chat for gamers.
com.reddit.frontpage|Reddit|s|Forum app.
com.tumblr|Tumblr|s|Blogging app.
com.ss.android.ugc.aweme|Douyin|s|Short video app.
com.zhiliaoapp.musically.go|TikTok Lite|s|Light TikTok app.
com.tencent.mm|WeChat|m|Messaging and payments.|You lose WeChat until reinstalled. Back up chats first.
com.tencent.mobileqq|QQ|s|Chat app.
jp.naver.line.android|LINE|m|Messaging app.|You lose LINE until reinstalled. Back up chats first.
com.kakao.talk|KakaoTalk|m|Messaging app.|You lose KakaoTalk until reinstalled. Back up chats first.
org.thoughtcrime.securesms|Signal|m|Private messaging.|You lose Signal and its messages unless backed up.
com.imo.android.imoim|imo|s|Video calls and chat.
com.truecaller|Truecaller|s|Caller ID and spam blocking.
in.mohalla.sharechat|ShareChat|s|Social network.
in.mohalla.video|Moj|s|Short video app.
video.like|Likee|s|Short video app.
com.kwai.video|Kwai|s|Short video app.
com.badoo.mobile|Badoo|s|Dating app.
com.tinder|Tinder|s|Dating app.
com.bumble.app|Bumble|s|Dating app.
com.grindrapp.android|Grindr|s|Dating app.
co.hinge.app|Hinge|s|Dating app.
com.vkontakte.android|VK|s|Social network.
# ---- streaming and music
com.disney.disneyplus|Disney+|s|Video streaming.
com.wbd.stream|Max|s|Video streaming.
tv.twitch.android.app|Twitch|s|Live game streaming.
com.hulu.plus|Hulu|s|Video streaming.
com.google.android.apps.youtube.kids|YouTube Kids|s|Kids video app.
com.spotify.lite|Spotify Lite|s|Light Spotify app.
deezer.android.app|Deezer|s|Music streaming.
com.soundcloud.android|SoundCloud|s|Music streaming.
com.shazam.android|Shazam|s|Song recognition.
com.pandora.android|Pandora|s|Music streaming.
com.apple.android.music|Apple Music|s|Music streaming.
com.jio.media.ondemand|JioCinema|s|Video streaming.
com.graymatrix.did|ZEE5|s|Video streaming.
com.sonyliv|SonyLIV|s|Video streaming.
com.mxtech.videoplayer.ad|MX Player|s|Video player with ads.
org.videolan.vlc|VLC|m|Video and audio player.|No VLC; other players are unaffected.
com.crunchyroll.crunchyroid|Crunchyroll|s|Anime streaming.
com.vimeo.android.videoapp|Vimeo|s|Video platform.
com.dailymotion.dailymotion|Dailymotion|s|Video platform.
tv.pluto.android|Pluto TV|s|Free TV streaming.
com.tubitv|Tubi|s|Free video streaming.
com.amazon.dee.app|Amazon Alexa|s|Voice assistant companion.
com.amazon.clouddrive.photos|Amazon Photos|s|Photo backup.
com.amazon.venezia|Amazon Appstore|s|Amazon app store.
com.netease.cloudmusic|NetEase Cloud Music|s|Music streaming.
# ---- shopping
com.ebay.mobile|eBay|s|Online marketplace.
com.zzkko|SHEIN|s|Fashion shopping.
com.einnovation.temu|Temu|s|Shopping app.
com.lazada.android|Lazada|s|Shopping app.
com.flipkart.android|Flipkart|s|Shopping app.
com.myntra.android|Myntra|s|Fashion shopping.
com.walmart.android|Walmart|s|Shopping app.
com.target.ui|Target|s|Shopping app.
com.etsy.android|Etsy|s|Handmade marketplace.
com.contextlogic.wish|Wish|s|Shopping app.
com.jumia.android|Jumia|s|Shopping app.
com.mercadolibre|Mercado Libre|s|Marketplace.
com.taobao.taobao|Taobao|s|Shopping app.
com.jingdong.app.mall|JD.com|s|Shopping app.
# ---- payments and finance
com.paypal.android.p2pmobile|PayPal|m|Payments.|You lose the PayPal app; your account stays.
com.phonepe.app|PhonePe|m|Payments.|You lose the app; your account stays.
net.one97.paytm|Paytm|m|Payments.|You lose the app; your account stays.
com.google.android.apps.nbu.paisa.user|Google Pay (India)|m|Payments.|You lose the app; your account stays.
com.revolut.revolut|Revolut|m|Banking app.|You lose the app; your account stays.
com.venmo|Venmo|m|Payments.|You lose the app; your account stays.
com.squareup.cash|Cash App|m|Payments.|You lose the app; your account stays.
# ---- travel, rides, food
com.ubercab|Uber|s|Ride hailing.
com.ubercab.eats|Uber Eats|s|Food delivery.
me.lyft.android|Lyft|s|Ride hailing.
com.airbnb.android|Airbnb|s|Stays booking.
com.tripadvisor.tripadvisor|Tripadvisor|s|Travel reviews.
com.expedia.bookings|Expedia|s|Travel booking.
net.skyscanner.android.main|Skyscanner|s|Flight search.
com.agoda.mobile.consumer|Agoda|s|Hotel booking.
com.waze|Waze|s|Navigation.
com.here.app.maps|HERE WeGo|s|Maps and navigation.
com.grabtaxi.passenger|Grab|s|Rides and delivery.
ee.mtakso.client|Bolt|s|Ride hailing.
com.olacabs.customer|Ola|s|Ride hailing.
com.application.zomato|Zomato|s|Food delivery.
in.swiggy.android|Swiggy|s|Food delivery.
com.dd.doordash|DoorDash|s|Food delivery.
com.deliveroo.orderapp|Deliveroo|s|Food delivery.
# ---- browsers
org.mozilla.firefox|Firefox|m|Web browser.|No Firefox; other browsers are unaffected.
com.brave.browser|Brave|m|Web browser.|No Brave; other browsers are unaffected.
com.microsoft.emmx|Microsoft Edge|m|Web browser.|No Edge; other browsers are unaffected.
com.duckduckgo.mobile.android|DuckDuckGo|m|Private browser.|No DuckDuckGo; other browsers are unaffected.
com.opera.gx|Opera GX|s|Gaming browser.
com.kiwibrowser.browser|Kiwi Browser|m|Web browser.|No Kiwi; other browsers are unaffected.
com.vivaldi.browser|Vivaldi|m|Web browser.|No Vivaldi; other browsers are unaffected.
com.yandex.browser|Yandex Browser|s|Web browser.
ru.yandex.searchplugin|Yandex|s|Search and services.
ru.yandex.yandexmaps|Yandex Maps|s|Maps and navigation.
ru.yandex.taxi|Yandex Go|s|Ride hailing.
# ---- security and cleaners
com.avast.android.mobilesecurity|Avast Security|s|Antivirus with ads.
com.kms.free|Kaspersky|s|Antivirus.
com.antivirus|AVG AntiVirus|s|Antivirus with ads.
com.eset.ems2.gp|ESET Mobile Security|s|Antivirus.
com.wsandroid.suite|McAfee Security|s|Antivirus.
com.bitdefender.security|Bitdefender|s|Antivirus.
com.lookout|Lookout|s|Mobile security.
com.symantec.mobilesecurity|Norton|s|Antivirus.
com.trendmicro.tmmspersonal|Trend Micro|s|Antivirus.
com.nordvpn.android|NordVPN|s|VPN.
com.expressvpn.vpn|ExpressVPN|s|VPN.
com.protonvpn.android|Proton VPN|s|VPN.
com.surfshark.vpnclient.android|Surfshark|s|VPN.
com.cloudflare.onedotonedotonedotone|1.1.1.1|s|DNS and VPN app.
org.zwanoo.android.speedtest|Speedtest|s|Connection speed test.
# ---- productivity
com.dropbox.android|Dropbox|s|Cloud storage.
com.evernote|Evernote|s|Notes app.
com.microsoft.todos|Microsoft To Do|s|Task list.
com.todoist|Todoist|s|Task list.
notion.id|Notion|s|Notes and docs.
com.Slack|Slack|s|Team chat.
com.microsoft.teams|Microsoft Teams|s|Team chat and meetings.
us.zoom.videomeetings|Zoom|s|Video meetings.
com.adobe.reader|Adobe Acrobat Reader|s|PDF reader.
com.adobe.scan.android|Adobe Scan|s|Document scanner.
cn.wps.moffice_eng|WPS Office|s|Office suite.
com.google.android.apps.authenticator2|Google Authenticator|m|Two-factor codes.|You LOSE your 2FA codes unless transferred first. Do not remove without a backup.
com.azure.authenticator|Microsoft Authenticator|m|Two-factor codes.|You LOSE your 2FA codes unless transferred first. Do not remove without a backup.
com.lastpass.lpandroid|LastPass|m|Password manager.|You lose quick access to your passwords. Log in on the web to get them.
com.x8bit.bitwarden|Bitwarden|m|Password manager.|You lose quick access to your passwords. Log in on the web to get them.
com.intsig.camscanner|CamScanner|s|Document scanner.
com.canva.editor|Canva|s|Design app.
com.picsart.studio|Picsart|s|Photo editor.
com.niksoftware.snapseed|Snapseed|s|Photo editor.
com.vsco.cam|VSCO|s|Photo editor.
com.camerasideas.instashot|InShot|s|Video editor.
com.lemon.lvoverseas|CapCut|s|Video editor.
com.commsource.beautyplus|BeautyPlus|s|Selfie editor.
io.faceapp|FaceApp|s|Face editing app.
com.nexstreaming.app.kinemasterfree|KineMaster|s|Video editor.
# ---- health and learning
com.fitbit.FitbitMobile|Fitbit|s|Fitness tracker app.
com.strava|Strava|s|Running and cycling tracker.
com.myfitnesspal.android|MyFitnessPal|s|Calorie tracker.
com.runtastic.android|Runtastic|s|Running tracker.
com.garmin.android.apps.connectmobile|Garmin Connect|s|Garmin watch companion.
com.xiaomi.hm.health|Zepp (Mi Fit)|s|Xiaomi band companion.|You lose band syncing until reinstalled.
com.google.android.apps.fitness|Google Fit|s|Fitness tracker.
com.duolingo|Duolingo|s|Language learning.
com.memrise.android.memrisecompanion|Memrise|s|Language learning.
com.babbel.mobile.android.en|Babbel|s|Language learning.
com.khanacademy.android|Khan Academy|s|Free lessons.
org.coursera.android|Coursera|s|Online courses.
com.udemy.android|Udemy|s|Online courses.
org.wikipedia|Wikipedia|s|Encyclopedia.
com.quizlet.quizletandroid|Quizlet|s|Flashcards.
# ---- news
flipboard.app|Flipboard|s|News reader.
com.nytimes.android|New York Times|s|News app.
com.cnn.mobile.android.phone|CNN|s|News app.
bbc.mobile.news.ww|BBC News|s|News app.
com.microsoft.amp.apps.bingnews|Microsoft Start|s|News feed.
com.nis.app|Inshorts|s|Short news.
# ---- keyboards, launchers, file sharing
com.touchtype.swiftkey|SwiftKey|m|Keyboard.|Keyboard missing unless another is installed.
com.microsoft.swiftkey|SwiftKey (Microsoft)|m|Keyboard.|Keyboard missing unless another is installed.
com.cootek.smartinputv5|TouchPal|s|Keyboard with ads.
net.zedge.android|Zedge|s|Wallpapers and ringtones.
com.teslacoilsw.launcher|Nova Launcher|m|Home screen.|Home screen changes to another launcher.
com.microsoft.launcher|Microsoft Launcher|m|Home screen.|Home screen changes to another launcher.
com.google.android.apps.wallpaper|Wallpapers by Google|s|Wallpaper picker.
com.google.android.launcher|Google Now Launcher|m|Home screen.|Home screen changes to another launcher.
com.lenovo.anyshare.gps|SHAREit|s|File sharing with ads.
cn.xender|Xender|s|File sharing.
# ---- Microsoft extras and gaming platforms
com.microsoft.bing|Bing|s|Search app.
com.microsoft.translator|Microsoft Translator|s|Translation app.
com.microsoft.xboxone.smartglass|Xbox|s|Xbox companion.
com.microsoft.office.onenote|OneNote|s|Notes app.
com.microsoft.copilot|Copilot|s|AI assistant.
com.google.android.play.games|Google Play Games|m|Play Games sign-in and saves.|Games lose Play Games sign-in and cloud saves.
com.valvesoftware.steamlink|Steam Link|s|Game streaming.
com.valvesoftware.android.steam.community|Steam|s|Steam mobile app.
com.epicgames.portal|Epic Games|s|Epic store app.
# ---- more Google apps
com.google.android.apps.searchlite|Google Go|s|Light Google search.
com.google.android.apps.classroom|Google Classroom|s|Classroom app.
com.google.android.apps.translate|Google Translate|s|Translation app.
com.google.android.street|Street View|s|Street-level maps.
com.google.earth|Google Earth|s|Satellite globe.
com.google.android.apps.podcasts|Google Podcasts|s|Podcast player.
com.google.android.apps.chromecast.app|Google Home|m|Smart home and Chromecast control.|No Chromecast or smart home control.
com.google.android.apps.adm|Find My Device|m|Locate a lost phone.|Cannot locate the phone remotely.
com.google.android.apps.bard|Gemini|m|AI assistant.|No Gemini assistant.
com.google.android.apps.recorder|Recorder|s|Voice recorder.
com.google.android.apps.youtube.creator|YouTube Studio|s|Creator app.
com.google.android.apps.tasks|Google Tasks|s|Task list.
com.google.android.apps.genie.geniewidget|News & Weather|s|News and weather widget.
com.google.android.apps.dynamite|Google Chat|s|Team chat.
com.google.android.apps.photosgo|Gallery Go|m|Light gallery.|No gallery unless another is installed.
com.google.android.apps.books|Play Books|s|Ebook reader.
com.google.android.apps.youtube.unplugged|YouTube TV|s|Live TV streaming.
com.google.android.apps.paidtasks|Opinion Rewards|s|Survey app.
com.google.android.as|Android System Intelligence|h|On-device smart features: Now Playing, suggestions, Live Caption.|Smart replies and suggestions stop.
com.google.android.as.oss|Private Compute Services|h|Private processing for smart features.|Smart features may stop.
com.google.android.modulemetadata|Modules Metadata|h|Mainline module support.|System update modules can break.
com.google.android.setupwizard|Setup Wizard|h|Initial phone setup.|Phone setup and factory reset flow can break.
"""
