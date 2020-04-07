# NoFrills Tablo Exporter
<br/>
A containerized python script to export recordings from Tablo and save it to a mass storage device such as a NAS.  The process runs every 15 minutes exporting all available recordings from Tablo to mp4 files.  The resulting files are the same quality as they are on Tablo and follow the Plex naming format.
<br/><br/>

## Parameters
```-e TABLO_IP=127.0.0.1```<br/>
The IP address of the Tablo DVR.

```-e EXEC_INTERVAL_MINUTES=15```<br/>
The number of minutes between each job run.

```-e DELETE_AFTER_EXPORT=true```<br/>
Delete the recording from Tablo after it has been exported.
<br/><br/>

## Volumes
```-v /local/path/to/movies:/nofrills_tablo_export/export/movies```<br/>
The path you want to export movie recordings to.

```-v /local/path/to/sports:/nofrills_tablo_export/export/sports```<br/>
The path you want to export sport recordings to.

```-v /local/path/to/tv:/nofrills_tablo_export/export/tv```<br/>
The path you want to export tv recordings to.

```-v /local/path/to/incomplete:/nofrills_tablo_export/export/incomplete```<br/>
The path you want to export incomplete recordings to.
<br/><br/>

## Run Command
```
docker run -d \
--restart=unless-stopped \
--name=nofrills_tablo_export \
-e TABLO_IP=127.0.0.1 \
-e DELETE_AFTER_EXPORT=true \
-e EXEC_INTERVAL_MINUTES=15 \
-v /mnt/plex/media/movies:/nofrills_tablo_export/export/movies \
-v /mnt/plex/media/sports:/nofrills_tablo_export/export/sports \
-v /mnt/plex/media/tv:/nofrills_tablo_export/export/tv \
-v /mnt/plex/media/incomplete:/nofrills_tablo_export/export/tv \
bbrigadier/nofrills_tablo_export:latest
```
