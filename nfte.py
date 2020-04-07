#!/usr/bin/python3

import nfte_globals
import nfte_class
import nfte_defs


mytablo = nfte_class.tablo(nfte_globals.TABLO_IP)
myffmpeg = nfte_class.ffmpeg(nfte_globals.FFMPEG_EXE_PATH,
    nfte_globals.MOVIES_EXPORT_PATH,
    nfte_globals.SERIES_EXPORT_PATH,
    nfte_globals.SPORTS_EXPORT_PATH,
    nfte_globals.INCOMPLETE_EXPORT_PATH)

reclist = nfte_defs.GetRecordingList(mytablo.recording_list_url())

if len(reclist) > 0:
    recordings = []

    for recording_path in reclist:
        rec = nfte_defs.GetRecordingInfo(recording_path, mytablo, myffmpeg)
        if rec.recording_id != '':
            recordings.append(rec)

    if len(recordings) > 0:
        nfte_globals.logging.info('Tablo system info\n{}'.format(nfte_defs.GetServerInfo(mytablo.server_info_url())))
        recordings = sorted(recordings, key = lambda i: (i.show_title, i.recording_duration))
        for rec in recordings:
            if nfte_defs.ExportRecording(rec, myffmpeg):
                if nfte_globals.DELETE_AFTER_EXPORT:
                    nfte_defs.DeleteTabloRecording(rec.recording_delete_url)
