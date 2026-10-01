"""Windo package database.

Line format:  package|Name|s/m/h|What it is|What happens if removed (optional)
s = safe, m = medium, h = high danger.  '@a,b' sets the device families for the lines below.
You can add your own lines in a file called custom_apps.txt next to Windo.exe.
"""
import os, sys

LEVELS = {"s": "safe", "m": "medium", "h": "high"}
DEFAULT_EFFECT = {
    "s": "Safe to remove. The app/feature disappears and nothing else depends on it. Can be restored.",
    "m": "May disable a feature you use. Read what it does before removing.",
    "h": "Can break calls, apps or even boot. Leave it unless you know exactly what you are doing.",
}
FAMILY_NAMES = {"xiaomi": "Xiaomi / Redmi / POCO (MIUI, HyperOS)", "samsung": "Samsung (One UI)",
                "oppo": "OPPO / realme / OnePlus (ColorOS)", "huawei": "Huawei / Honor (EMUI, HarmonyOS)",
                "infinix": "Infinix / Tecno / itel (XOS, HiOS)", "redmagic": "Red Magic / nubia / ZTE"}
FAMILIES = [("redmagic", ("redmagic", "red magic", "nubia", "zte")),
            ("xiaomi", ("xiaomi", "redmi", "poco", "blackshark")),
            ("samsung", ("samsung",)),
            ("oppo", ("oppo", "realme", "oneplus")),
            ("huawei", ("huawei", "honor")),
            ("infinix", ("infinix", "tecno", "itel", "transsion"))]

RAW = """
@*
# ---- social / preinstalled third party
com.facebook.appmanager|Facebook App Manager|s|Background installer/updater for Facebook apps.
com.facebook.services|Facebook Services|s|Background services for Facebook apps.
com.facebook.system|Facebook Installer|s|Facebook preinstall stub.
com.facebook.katana|Facebook|s|Facebook app.|App disappears; the website still works.
com.facebook.orca|Messenger|s|Facebook Messenger.|App disappears; chats stay on your account.
com.instagram.android|Instagram|s|Instagram app.
com.whatsapp|WhatsApp|m|Messaging app.|You lose WhatsApp until reinstalled. Back up chats first.
com.zhiliaoapp.musically|TikTok|s|TikTok app.
com.ss.android.ugc.trill|TikTok (Asia)|s|TikTok app.
com.snapchat.android|Snapchat|s|Snapchat app.
com.twitter.android|X (Twitter)|s|X/Twitter app.
com.pinterest|Pinterest|s|Pinterest app.
org.telegram.messenger|Telegram|m|Messaging app.|You lose Telegram until reinstalled.
com.linkedin.android|LinkedIn|s|LinkedIn app.
com.skype.raider|Skype|s|Skype calling app.
com.netflix.mediaclient|Netflix|s|Netflix streaming app.
com.netflix.partner.activation|Netflix Activation|s|Preinstall activation helper for Netflix.
com.spotify.music|Spotify|s|Spotify music app.
com.amazon.mShop.android.shopping|Amazon Shopping|s|Amazon shopping app.
in.amazon.mShop.android.shopping|Amazon Shopping (India)|s|Amazon shopping app.
com.amazon.avod.thirdpartyclient|Prime Video|s|Amazon Prime Video.
com.amazon.mp3|Amazon Music|s|Amazon Music.
com.audible.application|Audible|s|Audiobook app.
com.amazon.kindle|Kindle|s|Ebook reader.
com.booking|Booking.com|s|Hotel booking app.
com.alibaba.aliexpresshd|AliExpress|s|Shopping app.
com.king.candycrushsaga|Candy Crush Saga|s|Preinstalled game with ads.
com.microsoft.skydrive|OneDrive|s|Microsoft cloud storage.
com.microsoft.office.officehubrow|Microsoft 365|s|Office hub app.
com.microsoft.office.word|Word|s|Microsoft Word.
com.microsoft.office.excel|Excel|s|Microsoft Excel.
com.microsoft.office.powerpoint|PowerPoint|s|Microsoft PowerPoint.
com.microsoft.office.outlook|Outlook|s|Microsoft mail client.
com.microsoft.appmanager|Link to Windows|s|Phone-to-PC link service.
com.opera.browser|Opera|s|Opera browser.
com.opera.mini.native|Opera Mini|s|Opera Mini browser.
com.UCMobile.intl|UC Browser|s|UC browser with ads.
com.cleanmaster.mguard|Clean Master|s|Cleaner app with ads.
in.startv.hotstar|Hotstar|s|Streaming app.
com.eterno|Dailyhunt|s|News app.
# ---- Google apps
com.google.android.apps.tachyon|Google Meet|s|Video calling.|No Meet calls until reinstalled.
com.google.android.apps.magazines|Google News|s|News reader.
com.google.android.videos|Google TV|s|Movies and TV store/player.
com.google.android.apps.youtube.music|YouTube Music|s|Music streaming.
com.google.android.youtube|YouTube|s|YouTube app.|App disappears; the website still works.
com.google.android.apps.docs|Google Drive|s|Cloud storage app.|No Drive app; files stay in the cloud.
com.google.android.apps.docs.editors.docs|Google Docs|s|Document editor.
com.google.android.apps.docs.editors.sheets|Google Sheets|s|Spreadsheet editor.
com.google.android.apps.docs.editors.slides|Google Slides|s|Presentation editor.
com.google.android.apps.photos|Google Photos|m|Gallery and cloud photo backup.|Loses cloud photo backup unless another gallery is used.
com.google.android.apps.maps|Google Maps|m|Maps and navigation.|No Maps app. Some apps use it to pick locations.
com.google.android.gm|Gmail|m|Email client.|No Gmail app. Other mail apps still work.
com.google.android.calendar|Google Calendar|m|Calendar app.|No calendar unless another is installed.
com.google.android.keep|Google Keep|s|Notes app.|Notes stay in your account.
com.google.android.apps.googleassistant|Google Assistant|m|Voice assistant.|No 'Hey Google' voice assistant.
com.google.android.googlequicksearchbox|Google App|h|Search bar, Assistant and Discover. Some launchers depend on it.|Search widget and Assistant break.
com.google.android.feedback|Google Feedback|s|Sends feedback reports.
com.google.android.partnersetup|Google Partner Setup|s|Setup-time partner helper.
com.google.android.onetimeinitializer|One Time Initializer|s|First-boot helper.
com.google.android.projection.gearhead|Android Auto|s|Car connection app.
com.google.android.apps.wellbeing|Digital Wellbeing|s|Screen time and focus modes.|No usage stats or app timers.
com.google.android.apps.turbo|Device Health Services|m|Battery and adaptive charging insights.|Adaptive battery features may stop.
com.google.android.gms|Google Play Services|h|Core of Google services: push, login, location, Play Store.|Most apps break and notifications stop. Bootloop risk.
com.android.vending|Google Play Store|h|App store.|You cannot install or update apps.
com.google.android.gsf|Google Services Framework|h|Required by Google services.|Google login and sync break.
com.google.android.webview|Android System WebView|h|Shows web content inside apps.|Many apps crash or show blank pages.
com.android.chrome|Chrome|m|Web browser.|No browser unless another is installed.
com.google.android.apps.nbu.files|Files by Google|m|File manager and cleaner.
com.google.android.apps.messaging|Google Messages|m|SMS/RCS app.|No SMS unless another app is set as default.
com.google.android.dialer|Google Phone|m|Dialer app.|Dialer missing unless the brand dialer exists.
com.google.android.contacts|Google Contacts|m|Contacts app.
com.google.android.apps.subscriptions.red|Google One|s|Storage subscription app.
com.google.android.apps.walletnfcrel|Google Wallet|m|Tap-to-pay wallet.|No NFC payments.
com.google.android.apps.kids.familylinkhelper|Family Link Helper|s|Parental control helper.
com.google.android.printservice.recommendation|Print Recommendations|s|Suggests print plugins.
com.google.android.syncadapters.calendar|Calendar Sync|m|Syncs Google Calendar.|Calendar stops syncing.
com.google.android.syncadapters.contacts|Contacts Sync|m|Syncs Google Contacts.|Contacts stop syncing.
com.google.android.tts|Speech Services by Google|m|Text-to-speech engine.|No text-to-speech.
com.google.android.marvin.talkback|Accessibility Suite|m|TalkBack and Select to Speak.|Screen reader unavailable.
com.google.ar.core|Google Play Services for AR|s|AR support.
com.google.android.inputmethod.latin|Gboard|m|Google keyboard.|Keyboard missing unless another is installed.
com.google.android.deskclock|Google Clock|m|Alarm clock.
com.google.android.calculator|Google Calculator|m|Calculator.
com.google.android.safetycore|Android SafetyCore|m|On-device sensitive content scanning.
com.google.android.configupdater|Config Updater|h|Updates system config.
com.google.android.ext.services|Android Services Library|h|Framework extension services.
com.google.android.permissioncontroller|Permission Controller|h|Manages app permissions.
com.google.android.networkstack|Network Stack|h|Wi-Fi and mobile network checks.
com.google.android.carriersetup|Carrier Setup|m|Carrier configuration.
com.google.android.cellbroadcastreceiver|Emergency Alerts|m|Government alerts.|No emergency alerts.
# ---- Android / AOSP
com.android.egg|Android Easter Egg|s|Hidden game.
com.android.dreams.basic|Basic Daydreams|s|Screensaver.
com.android.bips|Default Print Service|s|Printing support.
com.android.printspooler|Print Spooler|s|Print job manager.
com.android.stk|SIM Toolkit|m|Carrier SIM menu.|Some carrier services may stop.
com.android.htmlviewer|HTML Viewer|s|Opens local .html files.
com.android.bookmarkprovider|Bookmark Provider|s|Stores browser bookmarks.
com.android.wallpaperbackup|Wallpaper Backup|s|Backs up wallpapers.
com.android.providers.partnerbookmarks|Partner Bookmarks|s|Carrier bookmarks.
com.android.traceur|System Tracing|s|Developer tracing tool.
com.android.email|Email|s|Old AOSP email app.
com.android.browser|Browser|s|Old AOSP browser.
com.android.calculator2|Calculator|s|AOSP calculator.
com.android.wallpaper.livepicker|Live Wallpaper Picker|s|Picks live wallpapers.
com.android.sharedstoragebackup|Shared Storage Backup|s|Backup helper.
com.android.backupconfirm|Backup Confirmation|s|Backup dialog.
com.android.dynsystem|Dynamic System Updates|s|DSU loader.
com.android.providers.telephony|Telephony Provider|h|Stores SMS/MMS and call data.|Calls and SMS break.
com.android.systemui|System UI|h|Status bar, notifications, navigation.|Phone becomes unusable.
com.android.phone|Phone Services|h|Core telephony.|No calls or mobile data.
com.android.settings|Settings|h|System settings.|You cannot change settings.
com.android.launcher3|Launcher3|h|Default home screen on many devices.|No home screen if no other launcher exists.
com.android.providers.contacts|Contacts Storage|h|Contacts database.
com.android.providers.media|Media Storage|h|Indexes photos, music, video.
com.android.providers.downloads|Download Manager|h|Handles downloads.
com.android.providers.settings|Settings Storage|h|Stores system settings.
com.android.bluetooth|Bluetooth|h|Bluetooth stack.
com.android.nfc|NFC Service|m|NFC stack.|No NFC or tap-to-pay.
com.android.server.telecom|Telecom|h|Call routing.
com.android.packageinstaller|Package Installer|h|Installs apps.
com.android.permissioncontroller|Permission Controller|h|Manages permissions.
com.android.mms.service|MMS Service|h|Sends and receives MMS.
com.android.carrierconfig|Carrier Config|m|Carrier settings.
com.android.cellbroadcastreceiver|Cell Broadcast|m|Emergency alerts.
com.android.emergency|Emergency Info|m|Lock screen emergency info.
com.android.keychain|Key Chain|h|Certificates and keys.
com.android.shell|Shell|h|ADB shell service.
com.android.location.fused|Fused Location|h|Location provider.
com.android.inputdevices|Input Devices|h|Keyboard/device input.
com.android.companiondevicemanager|Companion Device Manager|m|Pairs watches and accessories.
com.android.certinstaller|Certificate Installer|m|Installs certificates.
com.android.vpndialogs|VPN Dialogs|m|VPN permission dialogs.

@redmagic,xiaomi,oppo,samsung
com.qualcomm.qti.qmmi|QMMI Factory Test|s|Factory hardware test tool.
com.qualcomm.qti.workloadclassifier|Workload Classifier|s|Performance hints.
com.qualcomm.qti.confdialer|Conference Dialer|s|Conference call helper.
com.qualcomm.qti.xrcb|XR Callback|s|Qualcomm helper service.
com.qualcomm.qti.devicestatisticsservice|Device Statistics|s|Qualcomm usage stats.
com.qualcomm.qti.seccamservice|Secure Camera Service|s|Secure camera helper.
com.qualcomm.qti.dynamicddsservice|Dynamic DDS|s|Dual SIM data switching helper.|Automatic data SIM switching may stop.
com.qualcomm.embms|eMBMS|s|Mobile broadcast service.
com.qualcomm.uimremoteclient|UIM Remote Client|s|Remote SIM helper.
com.qualcomm.qti.poweroffalarm|Power Off Alarm|s|Alarm while phone is off.|Power-off alarms stop.
com.qti.qualcomm.datastatusnotification|Data Status Notification|s|Mobile data status popup.
com.qti.dpmserviceapp|DPM Service|s|Data path manager.
com.qualcomm.qti.cne|Connectivity Engine|m|Wi-Fi/mobile switching logic.
com.qualcomm.atfwd|AT Forward|m|Modem AT command service.
com.qualcomm.timeservice|Time Service|m|Network time sync.
com.qualcomm.qti.telephonyservice|Qualcomm Telephony|h|Telephony extensions.
com.qualcomm.location|Qualcomm Location|h|GPS/location service.
com.qualcomm.qti.services.systemhelper|System Helper|h|Qualcomm system helper.

@xiaomi,infinix,oppo
com.mediatek.mtklogger|MTK Logger|s|MediaTek debug logger.
com.mediatek.engineermode|Engineer Mode|s|Hardware test menu.
com.mediatek.ygps|MTK GPS Test|s|GPS test tool.
com.mediatek.batterywarning|Battery Warning|s|Battery alert helper.
com.mediatek.fmradio|FM Radio|s|FM radio.
com.mediatek.mdmlsample|MDM Sample|s|Modem log sample.
com.mediatek.atmwifimeta|Wi-Fi Meta Test|s|Factory Wi-Fi test.
com.mediatek.duraspeed|DuraSpeed|m|Background app limiter.|Less aggressive RAM management.
com.mediatek.miravision.ui|MiraVision|m|Display color tuning.
com.mediatek.thermalmanager|Thermal Manager|m|Heat control.
com.mediatek.camera|MTK Camera|h|Camera on some devices.
com.mediatek.ims|MTK IMS|h|VoLTE/VoWiFi.

@xiaomi
com.miui.analytics|MIUI Analytics|s|Xiaomi telemetry and usage collection.|Less data sent to Xiaomi. Nothing breaks.
com.miui.msa.global|MIUI System Ads (MSA)|s|Ad service used by system apps.|Fewer ads in system apps.
com.miui.systemAdSolution|Ad Solution|s|Ad service for system apps (China builds).|Fewer ads in system apps.
com.miui.bugreport|Bug Report|s|Sends bug reports to Xiaomi.
com.miui.klo.bugreport|Feedback Logger|s|Collects logs for Xiaomi feedback.
com.xiaomi.mipicks|GetApps|s|Xiaomi app store with ads.|No GetApps store; Play Store unaffected.
com.xiaomi.discover|System Apps Updater|m|Updates Xiaomi system apps.|Xiaomi apps stop auto-updating.
com.xiaomi.market|Xiaomi App Store|s|App store on China ROMs.
com.miui.videoplayer|Mi Video|s|Xiaomi video player with ads.
com.miui.player|Mi Music|s|Xiaomi music player.
com.miui.cloudservice|Mi Cloud|m|Xiaomi cloud sync and backup.|No Mi Cloud sync or backup.
com.miui.cloudbackup|Cloud Backup|m|Backs up to Mi Cloud.|No Mi Cloud backups.
com.miui.cloudservice.sysbase|Mi Cloud Base|m|Support service for Mi Cloud.
com.miui.yellowpage|Yellow Pages / Caller ID|s|Business lookup and caller ID.|No Xiaomi caller ID names.
com.miui.cleaner|Cleaner|m|Storage cleaner.
com.miui.securitycenter|Security|h|Permissions, battery, cleaner, app lock.|Permission and battery features break.
com.miui.securitycore|Security Core|h|Core of Security app.
com.miui.securityadd|Security Add-on|m|Extra Security features.
com.miui.guardprovider|Security Scan|s|Antivirus engine (Avast/AVL).|No built-in virus scan.
com.miui.antispam|Spam Filter|m|Blocks spam calls and SMS.|Spam filtering stops.
com.miui.miwallpaper.earth|Super Wallpaper Earth|s|Animated wallpaper.
com.miui.miwallpaper.mars|Super Wallpaper Mars|s|Animated wallpaper.
com.miui.miwallpaper.saturn|Super Wallpaper Saturn|s|Animated wallpaper.
com.miui.miwallpaper|Wallpaper|m|Wallpaper service.
com.miui.android.fashiongallery|Wallpaper Carousel|s|Lock screen wallpaper rotation with ads.|Lock screen stops rotating wallpapers.
com.mfashiongallery.emag|Wallpaper Carousel (old)|s|Old carousel app.
com.miui.hybrid|Quick Apps|s|Instant apps platform.
com.miui.hybrid.accessory|Quick Apps Accessory|s|Quick Apps helper.
com.miui.daemon|MIUI Daemon|m|Background performance and stats daemon.
com.miui.fm|FM Radio|s|FM radio app.
com.miui.compass|Compass|s|Compass app.
com.miui.calculator|Calculator|m|Calculator.
com.miui.notes|Notes|m|Notes app.|Notes app gone; data may be lost if not synced.
com.miui.weather2|Weather|m|Weather app and widget.|Weather widget stops.
com.miui.gallery|Gallery|m|Photo gallery.|No gallery unless another is installed.
com.miui.mediaeditor|Gallery Editor|m|Photo/video editor.
com.miui.screenrecorder|Screen Recorder|s|Screen recording.
com.miui.touchassistant|Quick Ball|s|Floating shortcut ball.
com.miui.mishare.connectivity|Mi Share|s|File sharing.
com.miui.personalassistant|App Vault|s|Swipe-right page with widgets and ads.
com.miui.contentcatcher|Content Catcher|s|Recommends content from screen.
com.miui.catcherpatch|Content Catcher Patch|s|Content Catcher helper.
com.miui.audiomonitor|Audio Monitor|s|Audio usage monitor.
com.miui.voiceassist|Mi AI Voice Assistant|s|Xiaomi assistant.
com.miui.translation.kingsoft|Translation (Kingsoft)|s|Translation engine.
com.miui.translationservice|Translation Service|s|Translation helper.
com.miui.miservice|Services & Feedback|s|Support and feedback app.
com.miui.backup|Backup|m|Local phone backup.
com.miui.cit|Hardware Test (CIT)|s|Factory test tool.
com.miui.tsmclient|Mi Pay NFC|s|NFC payment client.
com.miui.nextpay|Next Pay|s|Payment helper.
com.miui.greenguard|Family Guard|s|Child protection.
com.miui.qr|QR Scanner|s|QR scanning.
com.miui.huanji|Mi Mover|s|Phone transfer tool.
com.miui.carlink|Car with Mi|s|Car connection.
com.miui.thirdappassistant|Third App Assistant|s|Helper for third-party apps.
com.miui.accessibility|Accessibility|m|Accessibility features.
com.miui.phrase|Phrases|s|Quick phrases.
com.miui.misound|Sound Effects|m|Audio enhancement.
com.miui.powerkeeper|Battery & Performance|h|Battery and background management.|Battery saving and app standby break.
com.miui.home|System Launcher|h|Default MIUI/HyperOS home screen.|No home screen without another launcher.
com.miui.system|MIUI System|h|Core system package.
com.miui.core|MIUI Core|h|Core MIUI framework.
com.miui.rom|MIUI ROM|h|ROM resource package.
com.miui.packageinstaller|Package Installer|h|Installs apps.
com.miui.global.packageinstaller|Package Installer (Global)|h|Installs apps.
com.lbe.security.miui|Permission Manager|h|Manages app permissions.
com.android.updater|System Update|h|OTA updater.|No system updates.
com.android.thememanager|Themes|m|Theme store and manager.
com.android.quicksearchbox|Quick Search Box|s|Launcher search.
com.android.soundrecorder|Sound Recorder|m|Voice recorder.
com.android.fileexplorer|File Manager (China)|m|File manager.
com.mi.android.globalFileexplorer|Mi File Manager|m|File manager.
com.mi.android.globalminusscreen|App Vault (Global)|s|Swipe-right page.
com.mi.globalbrowser|Mi Browser|s|Xiaomi browser with ads.
com.mi.global.bbs|Mi Community|s|Xiaomi forum app.
com.mi.global.shop|Mi Store|s|Xiaomi shopping app.
com.mi.health|Mi Health|s|Health and fitness.
com.mi.globalTrendNews|Mi Feed|s|News feed.
com.mi.android.globallauncher|POCO Launcher|h|POCO home screen.|No home screen without another launcher.
com.xiaomi.joyose|Joyose|m|Performance and thermal cloud rules.|Thermal/game tuning changes.
com.xiaomi.payment|Mi Payment|s|Payment service.
com.mipay.wallet|Mi Pay|s|Xiaomi wallet.
com.mipay.wallet.in|Mi Pay (India)|s|Xiaomi wallet.
com.xiaomi.account|Mi Account|m|Xiaomi account service.|Mi Account login and sync break.
com.xiaomi.xmsf|Xiaomi Service Framework|m|Push notifications for Xiaomi apps.|Some push notifications stop.
com.xiaomi.finddevice|Find Device|m|Locate a lost phone.|Cannot locate the phone remotely.
com.xiaomi.mi_connect_service|Mi Connect Service|s|Cross-device link.
com.xiaomi.midrop|ShareMe|s|Offline file sharing.
com.xiaomi.misettings|Settings Extras|m|Extra settings pages.
com.xiaomi.simactivate.service|SIM Activate|s|SIM activation service.
com.xiaomi.scanner|Scanner|s|Document/QR scanner.
com.xiaomi.mirror|Mi Mirror|s|Screen mirroring.
com.xiaomi.aiasst.vision|AI Vision|s|AI image features.
com.xiaomi.aiasst.service|AI Engine|m|AI features backend.
com.xiaomi.glgm|Xiaomi Games|s|Games center.
com.xiaomi.gamecenter.sdk.service|Game Center SDK|s|Game login SDK.
com.xiaomi.bluetooth|Xiaomi Bluetooth|m|Bluetooth extras.
com.xiaomi.micloud.sdk|Mi Cloud SDK|m|Cloud SDK service.
com.milink.service|Mi Link|s|Device linking.
com.android.mms|Messages|m|SMS app.|No SMS unless another is installed.
com.android.contacts|Contacts|m|Contacts app.
com.android.camera|Camera|h|Camera app.|No camera.
com.android.incallui|In-Call UI|h|Call screen.|Calls become unusable.
com.android.calendar|Calendar|m|Calendar app.
com.android.deskclock|Clock|m|Clock and alarms.|Alarms stop.
com.android.providers.downloads.ui|Downloads UI|s|Downloads screen.

@samsung
com.samsung.android.bixby.agent|Bixby Voice|s|Samsung voice assistant.|No Bixby voice.
com.samsung.android.bixby.service|Bixby Service|s|Bixby background service.
com.samsung.android.bixbyvision.framework|Bixby Vision Framework|s|Camera visual search.
com.samsung.android.visionintelligence|Bixby Vision|s|Visual search.
com.samsung.android.bixby.wakeup|Bixby Wakeup|s|Voice wake word.
com.samsung.android.app.settings.bixby|Bixby Settings|s|Bixby settings pages.
com.samsung.android.app.routines|Modes and Routines|m|Automation rules.|Routines stop working.
com.samsung.android.app.spage|Samsung Free|s|Left home screen news feed.|Feed page disappears.
com.samsung.android.game.gamehome|Game Launcher|s|Games folder and booster.
com.samsung.android.game.gametools|Game Tools|s|Game overlay tools.
com.samsung.android.game.gos|Game Optimizing Service|m|Throttles games for heat/battery.|Games may run hotter and faster.
com.samsung.android.aremoji|AR Emoji|s|AR avatars.
com.samsung.android.arzone|AR Zone|s|AR features hub.
com.samsung.android.ardrawing|AR Doodle|s|Draw in AR.
com.samsung.android.livestickers|Live Stickers|s|Camera stickers.
com.samsung.android.emojiupdater|Emoji Updater|s|Emoji update helper.
com.samsung.android.stickercenter|Sticker Center|s|Sticker packs.
com.sec.android.mimage.avatarstickers|AR Emoji Stickers|s|Avatar stickers.
com.samsung.android.app.camera.sticker.facearavatar.preload|Camera AR Stickers|s|Preloaded stickers.
com.samsung.android.kidsinstaller|Samsung Kids Installer|s|Kids mode installer.
com.sec.android.app.kidshome|Kids Home|s|Kids mode.
com.samsung.android.app.parentalcare|Parental Controls|s|Parental controls.
com.samsung.android.app.sharelive|Quick Share|s|File sharing.
com.samsung.android.app.simplesharing|Simple Sharing|s|Sharing helper.
com.sec.android.app.samsungapps|Galaxy Store|s|Samsung app store.|No Galaxy Store; Play Store stays.
com.samsung.android.themestore|Galaxy Themes|s|Themes store.
com.samsung.android.app.galaxyfinder|Finder|s|Device search.
com.samsung.android.app.tips|Tips|s|Tips app.
com.samsung.android.app.watchmanagerstub|Galaxy Wearable Stub|s|Watch manager stub.
com.samsung.android.samsungpass|Samsung Pass|m|Password and biometric login.|Samsung Pass logins stop.
com.samsung.android.authfw|Samsung Pass Authentication|m|Pass authentication.
com.samsung.android.spay|Samsung Wallet|m|Wallet and pay.|No Samsung Pay/Wallet.
com.samsung.android.spayfw|Samsung Pay Framework|m|Pay framework.
com.samsung.android.mobileservice|Samsung Experience Service|m|Samsung account features.
com.samsung.android.scloud|Samsung Cloud|m|Cloud backup and sync.|No Samsung Cloud sync.
com.samsung.android.app.contacts|Samsung Contacts|m|Contacts app.
com.samsung.android.dialer|Samsung Phone|m|Dialer app.
com.samsung.android.incallui|Samsung Call UI|h|Call screen.|Calls become unusable.
com.samsung.android.messaging|Samsung Messages|m|SMS app.|No SMS unless another app is default.
com.samsung.android.email.provider|Samsung Email|s|Email client.
com.samsung.android.calendar|Samsung Calendar|m|Calendar.
com.samsung.android.app.notes|Samsung Notes|m|Notes app.|Notes app gone; sync first.
com.samsung.android.app.reminder|Reminder|s|Reminders.
com.samsung.android.voc|Samsung Members|s|Support and ads.
com.samsung.android.fmm|Find My Mobile|m|Locate a lost phone.|Cannot locate the phone remotely.
com.sec.android.easyMover|Smart Switch|s|Transfer from old phone.
com.sec.android.easyMover.Agent|Smart Switch Agent|s|Smart Switch helper.
com.samsung.android.smartswitchassistant|Smart Switch Assistant|s|Smart Switch helper.
com.samsung.android.dynamiclock|Dynamic Lock Screen|s|Lock screen wallpapers with ads.
com.samsung.android.app.ledcoverdream|LED Cover|s|LED cover app.
com.samsung.android.forest|Digital Wellbeing (Samsung)|s|Screen time.
com.samsung.android.da.daagent|Dual Messenger|s|Dual accounts.
com.samsung.android.lool|Device Care|m|Battery and storage care.
com.samsung.android.sm.devicesecurity|Device Security|s|McAfee security scan.
com.samsung.android.sm|Device Care Service|m|Device care backend.
com.sec.android.app.popupcalculator|Calculator|m|Calculator.
com.sec.android.app.clockpackage|Clock|m|Alarms and clock.|Alarms stop.
com.sec.android.app.sbrowser|Samsung Internet|m|Browser.
com.sec.android.app.myfiles|My Files|m|File manager.
com.sec.android.gallery3d|Gallery|m|Photo gallery.
com.sec.android.app.camera|Camera|h|Camera app.|No camera.
com.sec.android.app.voicenote|Voice Recorder|s|Voice recorder.
com.sec.android.app.shealth|Samsung Health|m|Health and steps.
com.sec.android.daemonapp|Weather|m|Weather app.
com.sec.android.app.launcher|One UI Home|h|Home screen.|No home screen.
com.sec.android.inputmethod|Samsung Keyboard|h|Default keyboard.
com.sec.android.app.dexonpc|DeX on PC|s|Desktop mode on PC.
com.sec.android.app.desktoplauncher|DeX Launcher|s|Desktop mode launcher.
com.samsung.android.mdx|Link to Windows|s|Windows link.
com.samsung.android.mdx.kit|Link to Windows Kit|s|Windows link helper.
com.samsung.android.app.aodservice|Always On Display|m|AOD service.|AOD stops.
com.samsung.android.rubin.app|Customization Service|s|Personalized suggestions.
com.samsung.android.privateshare|Private Share|m|Protected file sharing.
com.samsung.android.tvplus|Samsung TV Plus|s|Free TV channels.
com.samsung.android.hmt.vrsvc|Gear VR Service|s|Gear VR support.
com.samsung.android.hmt.vrshell|Gear VR Shell|s|Gear VR shell.
com.samsung.android.service.aircommand|Air Command|s|S Pen menu.|S Pen air menu stops.
com.samsung.android.smartmirroring|Smart View|m|Screen mirroring.
com.samsung.android.app.smartcapture|Smart Select|m|Screenshot tools.
com.samsung.android.app.taskedge|Edge Task Panel|m|Edge panel.
com.samsung.android.app.cocktailbarservice|Edge Panels|m|Edge panel service.
com.samsung.android.service.peoplestripe|People Edge|s|Contacts edge panel.
com.samsung.android.oneconnect|SmartThings|m|Smart home control.
com.samsung.android.knox.analytics.uploader|Knox Analytics|s|Knox telemetry.
com.samsung.android.knox.attestation|Knox Attestation|m|Device integrity.
com.samsung.android.knox.containeragent|Knox Container Agent|m|Secure Folder support.
com.sec.enterprise.knox.cloudmdm.smdms|Knox Cloud MDM|s|Enterprise management.
com.wssyncmldm|Software Update|m|OTA updater.|No system updates.
com.sec.android.soagent|Software Update Agent|m|OTA helper.
com.sec.spp.push|Samsung Push Service|m|Push for Samsung apps.|Samsung push stops.
com.sec.android.diagmonagent|Diagnostic Monitor|s|Sends diagnostics.
com.sec.android.app.billing|Samsung Checkout|s|In-app billing.
com.sec.android.preloadinstaller|Preload Installer|s|Installs bloat after setup.
com.samsung.klmsagent|KLMS Agent|s|Knox license agent.
com.samsung.android.app.appsedge|Apps Edge|s|Apps edge panel.
com.samsung.android.ims|IMS Service|h|VoLTE and Wi-Fi calling.
com.samsung.android.networkdiagnostic|Network Diagnostic|s|Diagnostics.
com.samsung.android.net.wifi.wifiguider|Wi-Fi Guider|s|Wi-Fi tips.
com.samsung.android.fast|Secure Wi-Fi|s|Wi-Fi security.
com.samsung.android.dialer|Samsung Dialer|m|Dialer.
com.samsung.android.ipsgeofence|IPS Geofence|s|Location helper.
com.samsung.android.service.livedrawing|Live Drawing|s|Live drawing.

@oppo
com.heytap.market|App Market|s|OPPO app store.|No OPPO store.
com.heytap.browser|HeyTap Browser|m|Default browser.
com.heytap.music|HeyTap Music|s|Music player.
com.heytap.cloud|HeyTap Cloud|m|Cloud sync and backup.|No cloud sync.
com.heytap.themestore|Theme Store|m|Theme store.
com.heytap.habit.analysis|Habit Analysis|s|Usage analytics.
com.heytap.mcs|HeyTap Push|m|Push service.|Some push notifications stop.
com.heytap.openid|OpenID Service|s|Ad ID service.
com.heytap.yoli|Yoli Video|s|Short videos.
com.heytap.quicksearchbox|Quick Search|s|Launcher search.
com.heytap.usercenter|HeyTap Account|m|OPPO account.
com.heytap.vip|HeyTap VIP|s|Membership app.
com.heytap.pictorial|Pictorial|s|Lock screen wallpapers with ads.
com.heytap.health|HeyTap Health|s|Health app.
com.heytap.wallet|HeyTap Wallet|s|Wallet app.
com.coloros.gamespace|Game Space|s|Games hub and booster.
com.coloros.gallery3d|Photos|m|Photo gallery.
com.coloros.calendar|Calendar|m|Calendar.
com.coloros.alarmclock|Clock|m|Alarms.|Alarms stop.
com.coloros.weather2|Weather|m|Weather app.
com.coloros.weather.service|Weather Service|s|Weather provider.
com.coloros.note|Notes|m|Notes app.
com.coloros.filemanager|File Manager|m|File manager.
com.coloros.soundrecorder|Recorder|s|Voice recorder.
com.coloros.compass2|Compass|s|Compass.
com.coloros.calculator|Calculator|s|Calculator.
com.coloros.smartsidebar|Smart Sidebar|m|Side panel.
com.coloros.phonemanager|Phone Manager|m|Cleaner and security.
com.coloros.safecenter|Security Center|h|Permissions and security.
com.coloros.securitypermission|Security Permission|h|Permission handling.
com.coloros.oppomultiapp|Clone Apps|m|Dual apps.
com.coloros.floatassistant|Float Assistant|s|Floating helper.
com.coloros.assistantscreen|Assistant Screen|s|Swipe-right page.
com.coloros.backuprestore|Clone Phone|s|Phone transfer.
com.coloros.oshare|O Share|s|File sharing.
com.coloros.screenrecorder|Screen Recorder|s|Screen recorder.
com.coloros.video|Video|s|Video player.
com.coloros.ocrscanner|Scanner|s|Document scanner.
com.coloros.translate.engine|Translate Engine|s|Translation.
com.coloros.mcs|MCS Push|m|Older push service.
com.coloros.focusmode|Focus Mode|s|Focus mode.
com.coloros.childrenspace|Children's Space|s|Kids mode.
com.coloros.sceneservice|Scene Service|m|Smart scene rules.
com.coloros.operationManual|User Manual|s|Manual app.
com.coloros.healthservice|Health Service|s|Health service.
com.coloros.athena|Athena|m|Smart recommendations.
com.coloros.simsettings|SIM Settings|m|SIM settings.
com.oppo.quicksearchbox|Quick Search Box|s|Launcher search.
com.oppo.market|Software Store|s|Older OPPO store.
com.oppo.music|Music|s|Older music app.
com.oppo.community|Community|s|OPPO community.
com.oppo.ctautoregist|CT Auto Registration|s|Carrier telemetry.
com.oppo.store|OPPO Store|s|Shopping app.
com.oplus.melody|HeyMelody|m|Earbuds companion.|No earbuds control.
com.oplus.games|Games|s|Games hub.
com.oplus.battery|Battery|m|Battery manager.
com.oplus.appdetail|App Detail|s|App info.
com.oplus.postmanservice|Postman Service|s|Telemetry.
com.oplus.statistics.rom|Statistics|s|Usage stats.
com.oplus.crashbox|Crash Box|s|Crash log collector.
com.oplus.logkit|Log Kit|s|Log collector.
com.oplus.dmp|DMP|s|Data management platform.
com.oplus.cosa|COSA|m|Game/CPU optimizer.
com.oplus.themestore|Theme Store|m|Theme store.
com.oplus.smartengine|Smart Engine|m|Smart features.
com.oplus.sau|System Update Service|m|Update helper.
com.oplus.onetrace|One Trace|s|Tracing.
com.oplus.exserviceui|Ex Service UI|s|Service prompts.
com.oplus.notes|Notes|m|Notes app.
com.oplus.location|Location|h|Location service.
com.oplus.phone|Phone|h|Telephony.
com.oplus.trafficmonitor|Traffic Monitor|s|Data usage.
com.oplus.metis|Metis|s|AI assistant.
com.oplus.wallpapers|Wallpapers|m|Wallpapers.
com.oplus.eyeprotect|Eye Protection|s|Eye comfort.
com.oplus.screenshot|Screenshot|m|Screenshot tool.
com.oplus.screenrecorder|Screen Recorder|s|Screen recorder.
com.oplus.wirelesssettings|Wireless Settings|h|Wi-Fi/Bluetooth settings.
com.nearme.gamecenter|Game Center|s|Games store.
com.nearme.instant.platform|Instant Games|s|Quick games.
com.nearme.statistics.rom|Nearme Statistics|s|Usage stats.
com.nearme.romupdate|ROM Update|m|OTA helper.
com.realme.link|realme Link|m|Device link.
com.finshell.wallet|Finshell Wallet|s|Wallet.
com.opos.ads|OPOS Ads|s|Ad service.
com.android.launcher|ColorOS Launcher|h|Home screen.|No home screen.
com.android.contacts|Contacts|m|Contacts.
com.android.incallui|In-Call UI|h|Call screen.
com.android.mms|Messages|m|SMS app.

@huawei
com.huawei.appmarket|AppGallery|s|Huawei app store.|No AppGallery.
com.hihonor.appmarket|Honor App Market|s|Honor app store.
com.huawei.hwid|HMS Core / Huawei ID|m|Huawei account and services.|Huawei account features break.
com.huawei.vassistant|Celia Assistant|s|Voice assistant.
com.huawei.hiai|HiAI|s|AI engine.
com.huawei.hiaction|HiAction|s|Smart suggestions.
com.huawei.intelligent|Smart Suggestions|s|HiBoard suggestions.
com.huawei.android.hwouc|System Update|m|OTA updater.|No system updates.
com.huawei.music|Huawei Music|s|Music player.
com.huawei.himovie|Huawei Video|s|Video app.
com.huawei.himovie.overseas|Huawei Video (Global)|s|Video app.
com.huawei.browser|Huawei Browser|m|Browser.
com.huawei.hidisk|Files|m|File manager.
com.huawei.android.thememanager|Themes|m|Theme store.
com.huawei.android.totemweather|Weather|m|Weather app.
com.huawei.notepad|Notepad|m|Notes app.
com.huawei.calendar|Calendar|m|Calendar.
com.huawei.calculator|Calculator|s|Calculator.
com.huawei.compass|Compass|s|Compass.
com.huawei.soundrecorder|Sound Recorder|s|Recorder.
com.huawei.screenrecorder|Screen Recorder|s|Screen recorder.
com.huawei.health|Huawei Health|m|Health and steps.
com.huawei.wallet|Huawei Wallet|s|Wallet.
com.huawei.hwdetectrepair|Smart Diagnosis|s|Diagnosis tool.
com.huawei.phoneservice|HiCare|s|Support app.
com.huawei.tips|Tips|s|Tips.
com.huawei.systemmanager|Phone Manager|h|Optimizer, permissions, app startup.|Permission and battery controls break.
com.huawei.android.FloatTasks|Floating Tasks|s|Floating shortcut.
com.huawei.android.hsf|HwServices Framework|m|Huawei services.
com.huawei.android.pushagent|Push Service|m|Push service.
com.huawei.android.launcher|Huawei Home|h|Home screen.|No home screen.
com.huawei.camera|Camera|h|Camera.|No camera.
com.huawei.photos|Gallery|m|Photo gallery.
com.huawei.android.instantshare|Huawei Share|m|File sharing.
com.huawei.fastapp|Quick Apps|s|Quick apps.
com.huawei.parentcontrol|Parent Control|s|Parental control.
com.huawei.hwireader|Huawei Books|s|Ebooks.
com.huawei.gamebox|Game Center|s|Games.
com.huawei.scanner|HiVision Scanner|s|Scanner.
com.huawei.lives|Huawei Lives|s|Local services.
com.huawei.ar.measure|AR Measure|s|AR ruler.
com.huawei.arengine.service|AR Engine|s|AR support.
com.huawei.skytone|Skytone|s|Roaming data.
com.huawei.mycenter|Club|s|Community.
com.huawei.mateservice|Mate Service|s|Feature hub.
com.huawei.iaware|iAware|m|App management.
com.huawei.powergenie|Power Genie|m|Battery management.
com.huawei.bd|Big Data|s|Telemetry.
com.huawei.fans|Huawei Club|s|Community.
com.hicloud.android.clone|Phone Clone|s|Phone transfer.
com.huawei.pcassistant|PC Assistant|s|PC link.

@infinix
com.transsion.phonemaster|Phone Master|m|Cleaner and security.
com.cyin.himgr|Phone Master (HiManager)|m|Cleaner and security.
com.transsion.smartpanel|Smart Panel|s|Side panel.
com.transsion.hilauncher|HiOS Launcher|h|Home screen.|No home screen.
com.transsion.XOSLauncher|XOS Launcher|h|Home screen.|No home screen.
com.transsion.theme|Theme|s|Theme store.
com.transsion.weather|Weather|m|Weather app.
com.transsion.notebook|Notebook|m|Notes.
com.transsion.carlcare|Carlcare|s|Support app.
com.transsion.gamemode|Game Mode|s|Game booster.
com.transsion.magicshow|Magic Show|s|Video effects.
com.transsion.aivoiceassistant|Ella Assistant|s|Voice assistant.
com.transsion.kolun.assistant|Kolun Assistant|s|Assistant.
com.transsion.batterylab|Battery Lab|s|Battery tips.
com.transsion.palmstore|Palm Store|s|App store with ads.
com.transsion.phoenix|Phoenix Browser|s|Browser.
com.transsion.letswitch|Let's Switch|s|Phone transfer.
com.transsion.ossettingsext|OS Settings Ext|h|Settings extension.
com.infinix.xshare|XShare|s|File sharing.
com.afmobi.boomplayer|Boomplay|s|Music streaming.
com.scene.zeroscreen|ZeroScreen|s|Left page feed.
com.rlk.weathers|Weather Widget|m|Weather widget.
com.talpa.hibrowser|Hi Browser|s|Browser.
com.sh.smart.caller|Smart Caller|s|Caller ID.
com.gallery20|Gallery|m|Photo gallery.
com.palmplay.carlcare|Carlcare (old)|s|Support app.
com.transsion.childmode|Kids Mode|s|Kids mode.
com.transsion.tpay|TPay|s|Payment helper.
com.transsion.tsplay|TS Play|s|Media app.

@redmagic
cn.nubia.neostore|nubia Store|s|App store.
cn.nubia.music|nubia Music|s|Music player.
cn.nubia.gallery|nubia Gallery|m|Photo gallery.
cn.nubia.weather|nubia Weather|s|Weather.
cn.nubia.bbs|nubia Community|s|Forum app.
cn.nubia.externdevice|External Device Service|m|Cooler/accessory support.|Fan cooler support stops.
cn.nubia.gamelauncher|Game Space|m|Game hub and performance.
cn.nubia.flashlight|Flashlight|s|Flashlight app.
cn.nubia.notepad|Notepad|m|Notes.
cn.nubia.calendar|Calendar|m|Calendar.
cn.nubia.themestore|Theme Store|s|Themes.
cn.nubia.systemupdate|System Update|m|OTA updater.
com.zte.feedback|Feedback|s|Feedback app.
"""

DB, BRANDS_OF = {}, {}


def parse(text):
    tags = ["*"]
    eff_default = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            tags = [t.strip() for t in line[1:].split(",") if t.strip()]
            eff_default = None
            continue
        if line.startswith("!"):
            eff_default = line[1:].strip()
            continue
        p = [x.strip() for x in line.split("|")] + ["", ""]
        pkg, name, lv, what, eff = p[:5]
        if lv not in LEVELS or "." not in pkg:
            continue
        DB[pkg] = (name, LEVELS[lv], what or name, eff or eff_default or DEFAULT_EFFECT[lv])
        BRANDS_OF.setdefault(pkg, set()).update(tags)


def detect_brand(*vals):
    s = " ".join(vals).lower()
    for fam, keys in FAMILIES:
        if any(k in s for k in keys):
            return fam
    return None


def relevant(pkg, fam):
    if pkg not in DB:
        return False
    return fam is None or "*" in BRANDS_OF[pkg] or fam in BRANDS_OF[pkg]


def counts():
    return {f: sum(1 for p in DB if relevant(p, f)) for f, _ in FAMILIES}


def load_custom():
    dirs = [os.path.dirname(os.path.abspath(sys.argv[0]))]
    if hasattr(sys, "_MEIPASS"):
        dirs.insert(0, sys._MEIPASS)
    for d in dirs:
        f = os.path.join(d, "custom_apps.txt")
        if os.path.isfile(f):
            with open(f, encoding="utf-8") as fh:
                parse("@*\n" + fh.read())


parse(RAW)
try:
    import windo_games, windo_apps
    parse(windo_games.RAW)
    parse(windo_apps.RAW)
except ImportError:
    pass
load_custom()
