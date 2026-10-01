"""Recovery / fastboot data for each brand category shown in Windo's Boot Modes tab."""

CATS = [
    {"key": "oppo", "label": "OPPO", "rom": "ColorOS / realme UI (also realme, OnePlus)",
     "rec_cmd": ["reboot", "recovery"], "fb_cmd": ["reboot", "bootloader"], "fb_label": "Fastboot",
     "rec_keys": "Power off, then hold Volume Down + Power until the logo appears and release.",
     "fb_keys": "Power off, then hold Volume Up + Power until the Fastboot screen appears.",
     "keys": ("oppo", "realme", "oneplus"),
     "notes": "ColorOS recovery is limited (install update, wipe data). On Android 10+ there is also userspace fastboot (fastbootd): run 'adb reboot fastboot'."},
    {"key": "xiaomi", "label": "Redmi / Xiaomi", "rom": "MIUI / HyperOS",
     "rec_cmd": ["reboot", "recovery"], "fb_cmd": ["reboot", "bootloader"], "fb_label": "Fastboot",
     "rec_keys": "Power off, then hold Volume Up + Power until the Mi logo appears and release.",
     "fb_keys": "Power off, then hold Volume Down + Power until the Fastboot bunny screen appears.",
     "keys": ("xiaomi", "redmi", "blackshark"),
     "notes": "Unlocking the bootloader needs a Mi account and a waiting period. Windo does not unlock or flash."},
    {"key": "samsung", "label": "Samsung", "rom": "One UI",
     "rec_cmd": ["reboot", "recovery"], "fb_cmd": ["reboot", "download"], "fb_label": "Download Mode",
     "rec_keys": "Power off, then hold Volume Up + Side (Power) key until the logo appears. Some models need the USB cable plugged in.",
     "fb_keys": "Power off, hold Volume Up + Volume Down, plug in the USB cable, then press Volume Up to confirm.",
     "keys": ("samsung",),
     "notes": "Samsung phones have no fastboot. Download Mode (used by Odin) is the equivalent, so the second button opens Download Mode."},
    {"key": "infinix", "label": "Infinix", "rom": "XOS / HiOS (also Tecno, itel)",
     "rec_cmd": ["reboot", "recovery"], "fb_cmd": ["reboot", "bootloader"], "fb_label": "Fastboot",
     "rec_keys": "Power off, then hold Volume Up + Power until the logo appears and release.",
     "fb_keys": "Varies by model (often Volume Up or Volume Down + Power). The button here is the reliable way.",
     "keys": ("infinix", "tecno", "itel", "transsion"),
     "notes": "Infinix phones use MediaTek chips. Some models only show fastboot after 'adb reboot bootloader'."},
    {"key": "redmagic", "label": "Red Magic", "rom": "Redmagic OS (nubia / ZTE)",
     "rec_cmd": ["reboot", "recovery"], "fb_cmd": ["reboot", "bootloader"], "fb_label": "Fastboot",
     "rec_keys": "Power off, then hold Volume Up + Power until the logo appears and release.",
     "fb_keys": "Power off, then hold Volume Down + Power until the Fastboot screen appears.",
     "keys": ("redmagic", "red magic", "nubia", "zte"),
     "notes": "Red Magic phones use Snapdragon chips, so fastboot works the standard way."},
    {"key": "huawei", "label": "Huawei", "rom": "EMUI / HarmonyOS (also Honor)",
     "rec_cmd": ["reboot", "recovery"], "fb_cmd": ["reboot", "bootloader"], "fb_label": "Fastboot",
     "rec_keys": "Power off, then hold Volume Up + Power to open eRecovery.",
     "fb_keys": "Power off, hold Volume Down, then plug in the USB cable (Fastboot & Rescue mode).",
     "keys": ("huawei", "honor"),
     "notes": "Huawei stopped giving bootloader unlock codes in 2018, so fastboot is mostly a rescue mode. Windo does not flash anything."},
    {"key": "poco", "label": "POCO", "rom": "MIUI / HyperOS (POCO)",
     "rec_cmd": ["reboot", "recovery"], "fb_cmd": ["reboot", "bootloader"], "fb_label": "Fastboot",
     "rec_keys": "Power off, then hold Volume Up + Power until the logo appears and release.",
     "fb_keys": "Power off, then hold Volume Down + Power until the Fastboot bunny screen appears.",
     "keys": ("poco",),
     "notes": "POCO is a Xiaomi sub-brand, so it uses the same modes as Redmi / Xiaomi. Windo does not unlock or flash."},
]

CAT_BY_KEY = {c["key"]: c for c in CATS}
# check order matters: Red Magic and POCO must be tested before the broader Xiaomi match
_ORDER = ["redmagic", "poco", "xiaomi", "samsung", "oppo", "huawei", "infinix"]


def detect_category(*vals):
    s = " ".join(vals).lower()
    for key in _ORDER:
        if any(k in s for k in CAT_BY_KEY[key]["keys"]):
            return key
    return None
