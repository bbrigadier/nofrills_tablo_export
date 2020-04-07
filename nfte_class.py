#!/usr/bin/python3


class recording_info:
    airing_datetime = ''
    airing_duration = 0
    episode_number = ''
    episode_title = ''
    movie_release_year = ''
    recording_id = ''
    recording_duration = 0
    recording_type = ''
    season_number = ''
    show_title = ''
    sport_event_title = ''
    playlist_url = ''
    recording_delete_url = ''
    isincomplete = False
    mp4_path = ''
    mp4_file = ''


class recording_types:
    movies = 'movies'
    sports = 'sports'
    series = 'series'


class ffmpeg:
    __exe_path = ''
    __movies_export_path = ''
    __series_export_path = ''
    __sports_export_path = ''
    __incomplete_export_path = ''

    def __init__(self, ffmpeg_exe_path = '', movies_export_path = '', series_export_path = '', sports_export_path = '', incomplete_export_path = ''):
        self.__exe_path = ffmpeg_exe_path
        self.__movies_export_path = movies_export_path
        self.__series_export_path = series_export_path
        self.__sports_export_path = sports_export_path
        self.__incomplete_export_path = incomplete_export_path

    def cmd(self, playlist_url = '', outfile = ''):
        # ffmpeg params only copy the stream and convert audio to mp4 compatible.
        # this gives 1:1 quality to what was recorded in tablo
        outcmd = [self.__exe_path, '-y', '-i', playlist_url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', '-f', 'mp4', outfile]
        return outcmd

    def mp4(self, recording = recording_info):
        outval = ''
        
        if recording.recording_type == recording_types.movies:
            outval = '{}/{} ({}).mp4'.format(
                self.__incomplete_export_path if recording.isincomplete else self.__movies_export_path,
                recording.show_title,
                recording.movie_release_year)

        if recording.recording_type == recording_types.series:
            outval = '{}/{}/{} - s{}e{} - {}.mp4'.format(
                self.__incomplete_export_path if recording.isincomplete else self.__series_export_path,
                recording.show_title,
                recording.show_title,
                str(recording.season_number).zfill(2),
                str(recording.episode_number).zfill(2),
                recording.episode_title)

        if recording.recording_type == recording_types.sports:
            outval = '{}/{} - {} - {}.mp4'.format(
                self.__incomplete_export_path if recording.isincomplete else self.__sports_export_path,
                recording.show_title,
                recording.airing_datetime[0:10],
                recording.sport_event_title)

        return outval


class tablo:
    __ip = ''
    __url = 'http://{}:{}{}'
    __info_port = '8885'
    __pvr_port = '18080'
    __server_info_path = '/server/info'
    __recording_list_path = '/recordings/airings'
    __playlist_path = '/pvr/{}/pl/playlist.m3u8'

    def __init__(self, ip_address):
        self.__ip = ip_address

    def playlist_url(self, recording_id = ''):
        return self.__url.format(
            self.__ip,
            self.__pvr_port,
            self.__playlist_path.format(recording_id))

    def recording_info_url(self, recording_path = ''):
        return self.__url.format(
            self.__ip,
            self.__info_port,
            recording_path)

    def recording_list_url(self):
        return self.__url.format(
            self.__ip,
            self.__info_port,
            self.__recording_list_path)

    def server_info_url(self):
        return self.__url.format(
            self.__ip,
            self.__info_port,
            self.__server_info_path)
