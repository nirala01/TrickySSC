#!/usr/bin/env python3
"""Uploads the signed app bundle to Google Play and puts it on the given testing tracks.

Run by .github/workflows/build-flutter.yml (never by hand):
    play_upload.py <package> <bundle.aab> <tracks, comma separated> <release name>
The service account key comes from the PLAY_JSON environment variable (GitHub secret
PLAY_SERVICE_ACCOUNT_JSON); release notes from NOTES (first line, 500 characters at most).
One Play "edit" does it all, so the bundle is uploaded once and every track gets the same build.
"""
import json
import os
import socket
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

pkg, aab, tracks, name = sys.argv[1], sys.argv[2], [t for t in sys.argv[3].split(',') if t], sys.argv[4]
notes = (os.environ.get('NOTES') or '').strip().splitlines()
notes = (notes[0] if notes else 'Improvements and fixes.')[:500]

socket.setdefaulttimeout(900)
creds = service_account.Credentials.from_service_account_info(
    json.loads(os.environ['PLAY_JSON']), scopes=['https://www.googleapis.com/auth/androidpublisher'])
edits = build('androidpublisher', 'v3', credentials=creds, cache_discovery=False).edits()

eid = edits.insert(packageName=pkg, body={}).execute()['id']
up = edits.bundles().upload(packageName=pkg, editId=eid,
                            media_body=MediaFileUpload(aab, mimetype='application/octet-stream', resumable=True)).execute()
code = up['versionCode']
print('Uploaded bundle, version code', code)
try:
    lang = edits.details().get(packageName=pkg, editId=eid).execute().get('defaultLanguage') or 'en-US'
except Exception:
    lang = 'en-US'
for t in tracks:
    edits.tracks().update(packageName=pkg, editId=eid, track=t, body={
        'track': t,
        'releases': [{'name': name, 'versionCodes': [str(code)], 'status': 'completed',
                      'releaseNotes': [{'language': lang, 'text': notes}]}],
    }).execute()
    print('Release', name, 'set on track', t)
edits.commit(packageName=pkg, editId=eid).execute()
print('Done: %s is on %s' % (name, ', '.join(tracks)))
