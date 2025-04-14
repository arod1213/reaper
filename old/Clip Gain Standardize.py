import reaper_python as rp




# --------------------------------------------------------------------------------------

import math
import statistics


# --------------------------------------------------------------------------------------

# ( retval, title, num_inputs, captions_csv, retvals_csv, retvals_csv_sz ) = rp.RPR_GetUserInputs(title, num_inputs, captions_csv, retvals_csv, retvals_csv_sz )

# --------------------------------------------------------------------------------------


def normal_cdf(x):
    "cdf for standard normal"
    q = math.erf(x / math.sqrt(2.0))
    return (1.0 + q) / 2.0


def amptoDB(amp):
    return 20 * math.log(amp, 10)


def dbtoAmp(db):
    return 10 ** (db / 20)


# finds difference from amp1 to amp2
# difference value is in DB then scaled
# scaled value is then added to amp1 value in DB
# scaled value + amp1db is converted back to amplitude
# var scale is a percentage 1 being 100%
def ampDiffLinear(amp1, amp2, scale):
    diffDB = (amptoDB(amp2) - amptoDB(amp1)) * scale
    return dbtoAmp(amptoDB(amp1) + diffDB)


# --------------------------------------------------------------------------------------


class MediaItem:

    def __init__(self, item):
        self.id = item
        self.start = rp.RPR_GetMediaItemInfo_Value(self.id, "D_POSITION")
        self.length = rp.RPR_GetMediaItemInfo_Value(self.id, "D_LENGTH")
        self.end = self.start + self.length
        self.take = rp.RPR_GetMediaItemTake(
            self.id, int(rp.RPR_GetMediaItemInfo_Value(self.id, "I_CURTAKE"))
        )
        self.playrate = rp.RPR_GetMediaItemTakeInfo_Value(self.take, "D_PLAYRATE")

        self.source = rp.RPR_GetMediaItemTake_Source(self.take)
        self.sourcelen = rp.RPR_GetMediaSourceLength(self.source, False)[0]
        self.startoffset = rp.RPR_GetMediaItemTakeInfo_Value(
            self.take, "D_STARTOFFS"
        )

        self.vol = rp.RPR_GetMediaItemInfo_Value(self.id, "D_VOL")

    def loop(self, bool):
        if bool:
            bool = 1
        else:
            bool = 0
        rp.RPR_SetMediaItemInfo_Value(self.id, "B_LOOPSRC", bool)

    def getToLoud(self, type, target):
        self.target = rp.RPR_CalculateNormalization(
            self.source,
            type,
            target,
            self.startoffset,
            self.startoffset + (self.length / self.playrate),
        )
        return self.target

    def changeVol(self, vol):
        rp.RPR_SetMediaItemInfo_Value(self.id, "D_VOL", vol)


# --------------------------------------------------------------------------------------


def loopOff(type, target, scale, tolerance):
    volChange = []
    newVol = []

    # collect +dB changes to items
    for x in range(0, rp.RPR_CountSelectedMediaItems(0)):
        item = MediaItem(rp.RPR_GetSelectedMediaItem(0, x))

        volChange.append(amptoDB(item.getToLoud(type, target)) - amptoDB(item.vol))
        newVol.append(ampDiffLinear(item.vol, item.getToLoud(type, target), scale))

    for x in range(0, rp.RPR_CountSelectedMediaItems(0)):

        if len(volChange) > 1:  # needs at least 2 to run statistics
            median = statistics.median(volChange)
            stDev = statistics.stdev(volChange)
            z = (volChange[x] - median) / stDev

            if abs(z) < tolerance:
                item = MediaItem(rp.RPR_GetSelectedMediaItem(0, x))
                # item.changeVol(item.getToLoud(type, target))
                item.changeVol(newVol[x])
            elif abs(z) < tolerance + 1:
                item = MediaItem(rp.RPR_GetSelectedMediaItem(0, x))
                # item.changeVol(dbtoAmp((abs(amptoDB(item.getToLoud(type, target)) * 0.5)))) # cut change in half
                item.changeVol(
                    ampDiffLinear(item.vol, item.getToLoud(type, target), scale * 0.5)
                )  # cut change in half

        else:  # if only two or less items are selected
            item = MediaItem(rp.RPR_GetSelectedMediaItem(0, x))
            item.changeVol(newVol[x])


userInput = rp.RPR_GetUserInputs(
    "Clip Gain", 3, "Type:,Peak:,Strength (0-1):", "RMS,-27, 1", 20
)[4]

if len(userInput) > 0:
    input = userInput.split(",")

    if "LUFS" in input[0].upper():
        input[0] = 0
    elif "RMS" in input[0].upper():
        input[0] = 1
    else:  # PEAK
        input[0] = 2
        target = dbtoAmp(int(input[1]))

loopOff(input[0], float(input[1]), float(input[2]), 2.5)  # RUN
rp.RPR_UpdateArrange()
