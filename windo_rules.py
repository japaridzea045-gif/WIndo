"""Pattern rules: give every package that is not in the database a best-guess name, level and description.

classify() returns (name, level, what, effect, kind) where kind is 'guess' or 'unknown'.
"""
import re

GENERIC = {"android", "app", "apps", "client", "mobile", "main", "release", "gp", "full", "free", "lite",
           "prod", "google", "play", "global", "intl", "overseas", "ww", "row", "sdk", "service",
           "services", "game", "games", "com", "org", "net"}

PUBLISHERS = {
    "com.supercell.": "Supercell", "com.king.": "King", "com.gameloft.": "Gameloft", "com.ea.": "Electronic Arts",
    "com.miniclip.": "Miniclip", "com.rovio.": "Rovio", "com.zynga.": "Zynga", "com.playrix.": "Playrix",
    "com.activision.": "Activision", "com.mojang.": "Mojang", "com.netease.": "NetEase", "com.garena.": "Garena",
    "com.dts.": "Garena", "com.mihoyo.": "miHoYo", "com.hoyoverse.": "HoYoverse", "com.ubisoft.": "Ubisoft",
    "com.outfit7.": "Outfit7", "com.kiloo.": "Kiloo", "com.sybogames.": "SYBO", "com.voodoo.": "Voodoo",
    "com.ketchapp.": "Ketchapp", "com.nianticlabs.": "Niantic", "com.halfbrick.": "Halfbrick",
    "com.imangi.": "Imangi", "com.ludia.": "Ludia", "com.glu.": "Glu", "com.nexon.": "Nexon",
    "com.netmarble.": "Netmarble", "com.com2us.": "Com2uS", "com.square_enix.": "Square Enix",
    "com.bandainamcogames.": "Bandai Namco", "com.bandainamcoent.": "Bandai Namco", "jp.konami.": "Konami",
    "com.sega.": "SEGA", "com.kabam.": "Kabam", "com.machinezone.": "Machine Zone", "com.lilithgame.": "Lilith",
    "com.igg.": "IGG", "com.moonton.": "Moonton", "com.proximabeta.": "Proxima Beta", "com.levelinfinite.": "Level Infinite",
    "com.krafton.": "Krafton", "com.pubg.": "Krafton", "com.tap4fun.": "Tap4Fun", "com.fingersoft.": "Fingersoft",
    "com.ninjakiwi.": "Ninja Kiwi", "com.chillingo.": "Chillingo", "com.popcap.": "PopCap",
    "com.tencent.tmgp.": "Tencent", "com.playtika.": "Playtika", "air.com.playtika.": "Playtika",
    "com.scopely.": "Scopely", "com.tripledot.": "Tripledot", "com.easybrain.": "Easybrain",
    "com.nintendo.": "Nintendo", "com.riotgames.": "Riot Games", "com.epicgames.": "Epic Games",
    "com.firsttouchgames.": "First Touch Games", "com.nekki.": "Nekki", "com.dreamgames.": "Dream Games",
}

VENDORS = {
    "com.samsung.": "Samsung", "com.sec.": "Samsung", "com.miui.": "Xiaomi (MIUI/HyperOS)", "com.xiaomi.": "Xiaomi",
    "com.mi.": "Xiaomi", "com.lbe.": "Xiaomi", "com.coloros.": "OPPO (ColorOS)", "com.oplus.": "OPPO",
    "com.heytap.": "OPPO (HeyTap)", "com.oppo.": "OPPO", "com.nearme.": "OPPO", "com.realme.": "realme",
    "com.oneplus.": "OnePlus", "com.huawei.": "Huawei", "com.hihonor.": "Honor", "com.transsion.": "Transsion (Infinix/Tecno)",
    "cn.nubia.": "nubia (Red Magic)", "com.zte.": "ZTE", "com.qualcomm.": "Qualcomm", "com.qti.": "Qualcomm",
    "com.mediatek.": "MediaTek", "com.unisoc.": "Unisoc", "com.spreadtrum.": "Unisoc", "com.android.": "Android",
    "com.google.android.": "Google", "com.vivo.": "vivo", "com.bbk.": "vivo", "com.motorola.": "Motorola",
    "com.lenovo.": "Lenovo", "com.asus.": "ASUS", "com.sonymobile.": "Sony", "com.sonyericsson.": "Sony",
    "com.lge.": "LG", "com.htc.": "HTC", "com.hmdglobal.": "HMD", "com.tcl.": "TCL",
}

TELEMETRY = ("analytics", "statistic", "bugreport", "feedback", "logkit", "crashbox", "telemetry", "diagnos")
GAME_WORDS = ("game", "casino", "slots", "solitaire", "puzzle", "racing", "bubble", "candy", "quest", "saga",
              "legend", "warrior", "battle", "royale", "runner", "simulator", "tycoon")
GAME_EFFECT = "Deletes the game. Progress is lost unless it is linked to an account or cloud save."
USER_EFFECT = "Removes the app. Windo may not be able to restore it, so reinstall from the store if needed. Back up its data first."


def pretty(pkg):
    parts = pkg.split(".")
    seg = next((x for x in reversed(parts[1:]) if x.lower() not in GENERIC), parts[-1])
    seg = re.sub(r"([a-z])([A-Z])", r"\1 \2", seg).replace("_", " ").replace("-", " ")
    return seg[:1].upper() + seg[1:]


def classify(pkg, third=False):
    low, name = pkg.lower(), pretty(pkg)
    for pre, pub in PUBLISHERS.items():
        if low.startswith(pre):
            return name, "safe", "Game by %s (not in Windo's database)." % pub, GAME_EFFECT, "guess"
    if not third and any(k in low for k in TELEMETRY) and not low.startswith("com.android."):
        return (name, "medium", "Looks like a telemetry, log or feedback component (guessed from its name).",
                "Usually removable, but confirm what it is before removing it.", "guess")
    if not third:
        for pre, vendor in VENDORS.items():
            if low.startswith(pre):
                return (name, "high", "System component from %s. Not in Windo's database, so its purpose is unknown." % vendor,
                        "Unknown effects. Search the package name online before removing it.", "guess")
    else:
        if any(w in low for w in GAME_WORDS):
            return name, "safe", "Looks like a game (guessed from its name).", GAME_EFFECT, "guess"
        return name, "safe", "App installed from a store (not in Windo's database).", USER_EFFECT, "guess"
    return name, "high", "Unknown app, not in Windo's database.", "Unknown effects. Only remove it if you know what it is.", "unknown"
