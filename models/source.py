import reaper_python as rp


class Source:
    def __init__(self, source):
        self.source = source
        self.type = rp.RPR_GetMediaSourceType(source, "", 15)
        # self.sample_rate = rp.RPR_GetMediaSourceSampleRate(source)
        # self.length = rp.RPR_GetMediaSourceLength(source, False)[2]
