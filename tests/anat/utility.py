""" ANAT Utility """
import os

WORK_DIR = os.path.normpath(os.path.dirname(__file__))
BIN_DIR = os.path.normpath(os.path.join(WORK_DIR, 'binary'))
LOG_DIR = os.path.normpath(os.path.join(WORK_DIR, 'log'))
TMP_DIR = os.path.normpath(os.path.join(WORK_DIR, 'tmp'))
SCRIPT_DIR = os.path.normpath(os.path.join(WORK_DIR, 'script'))

PROFILE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, 'profile'))
TMP_REFERENCE_DIR = os.path.join(os.path.join(TMP_DIR, 'reference'))
TMP_EVIDENCE_DIR = os.path.normpath(os.path.join(TMP_DIR, 'evidence'))
TMP_VIDEO_DIR = os.path.normpath(os.path.join(TMP_DIR, 'video'))

FFMPEG_BIN = os.path.normpath(os.path.join(BIN_DIR, 'ffmpeg', 'bin', 'ffmpeg.exe'))
