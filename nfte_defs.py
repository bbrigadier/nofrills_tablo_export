#!/usr/bin/python3

import requests
import json
import subprocess
import sys
import time
import os
import nfte_class
import nfte_globals


def GetServerInfo(url = ''):
    outval = ''
    try:
        req = requests.get(url)
    except:
        nfte_globals.logging.exception(url)
        sys.exit(1)
    
    dct = json.loads(req.text)
    for ikey, ival in dct.items():
        if ikey == 'warnings': continue
        if ikey == 'model':
            for subikey, subival in ival.items():
                outval += '{:<20}{:<1}\n'.format(subikey, subival)
            continue
        outval += '{:<20}{:<1}\n'.format(ikey, ival) 
    
    return outval


def GetRecordingList(url = ''):
    try:
        req = requests.get(url)
    except:
        nfte_globals.logging.exception(url)
        sys.exit(1)

    return json.loads(req.text)


def GetRecordingInfo(url = '', tab = nfte_class.tablo, mpeg = nfte_class.ffmpeg):
    url = tab.recording_info_url(url)

    try:
        req = requests.get(url)
    except:
        nfte_globals.logging.exception(url)
        sys.exit(1)

    outval = nfte_class.recording_info()
    rectype = url.split('/')[4]
    dct = json.loads(req.text)

    if dct['video_details']['state'] == 'finished':
        # clean up unwanted characters for the file name
        outval.show_title = dct['airing_details']['show_title'].replace('`', '\'')
        outval.show_title = ''.join(i for i in outval.show_title if i not in '\"/:*?<>|')
        outval.airing_datetime = dct['airing_details']['datetime']
        outval.recording_id = dct['object_id']
        outval.recording_type = rectype
        outval.playlist_url = tab.playlist_url(dct['object_id'])
        outval.recording_delete_url = url
        outval.airing_duration = dct['airing_details']['duration']
        outval.recording_duration = dct['video_details']['duration']

        if outval.recording_duration < (outval.airing_duration - nfte_globals.INCOMPLETE_PAD_SECONDS):
            outval.isincomplete = True
            
        if rectype == nfte_class.recording_types.movies:
            outval.movie_release_year = dct['movie_airing']['release_year']

        if rectype == nfte_class.recording_types.series:
            outval.episode_title = dct['episode']['title'] if dct['episode']['title'] is not None else 'Special {}'.format(outval.airing_datetime)
            # clean up unwanted characters for the file name
            outval.episode_title = outval.episode_title.replace('`', '\'')
            outval.episode_title = ''.join(i for i in outval.episode_title if i not in '\"/:*?<>|')
            outval.season_number = dct['episode']['season_number']
            outval.episode_number = dct['episode']['number']

        if rectype == nfte_class.recording_types.sports:
            # clean up unwanted characters for the file name
            outval.sport_event_title = dct['event']['title'].replace('`', '\'')
            outval.sport_event_title = ''.join(i for i in outval.sport_event_title if i not in '\"/:*?<>|')

        outval.mp4_file = mpeg.mp4(outval)
        outval.mp4_path = os.path.dirname(outval.mp4_file)

    return outval


def ExportRecording(rec = nfte_class.recording_info, mpeg = nfte_class.ffmpeg):
    cmd = mpeg.cmd(rec.playlist_url, rec.mp4_file)
    outval = True
    log = ''
    
    for ikey, ival in rec.__dict__.items():
        if not ikey.startswith('__'):
            log += '{:<25}{:<1}\n'.format(ikey, ival)
    
    if not os.path.exists(rec.mp4_path):
        try:
            os.mkdir(rec.mp4_path)
        except:
            nfte_globals.logging.error('Error creating directory {}'.format(rec.mp4_path))

    log += 'ffmpeg parameters\n{}\n'.format(cmd)
    nfte_globals.logging.info(log)
    start_time = time.time()
    proc = subprocess.Popen(cmd, stderr = subprocess.PIPE)
    _, stderr = proc.communicate()
    end_time = time.time()
    elapsed_time = end_time - start_time

    if proc.returncode != 0:
        # ffmpeg failed somehow and the export isnt complete.
        # delete it so it can be exported again
        outval = False
        log = 'Error exporting to {}\n{}\n'.format(rec.mp4_file, stderr.decode())
        nfte_globals.logging.error(log)
        if os.path.exists(rec.mp4_file):
            os.remove(rec.mp4_file)
    if proc.returncode == 0:
        file_size = os.path.getsize(rec.mp4_file)
        conv_rate = file_size / elapsed_time
        log = 'Exported {}\nElapsed time {:.2f} min, file size {:.2f} MB, conversion rate {:.2f} MB/s\n'.format(
            rec.mp4_file,
            (elapsed_time / 60),
            (file_size / 1024) / 1024,
            (conv_rate / 1024) / 1024)
        nfte_globals.logging.info(log)

    return outval


def DeleteTabloRecording(url = ''):
    try:
        requests.delete(url)
    except:
        nfte_globals.logging.exception(url)
        sys.exit(1)

    return
