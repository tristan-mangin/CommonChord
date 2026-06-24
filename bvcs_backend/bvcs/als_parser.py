import gzip
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ClipInfo:
    name: str
    start_time: float
    end_time: float

@dataclass 
class TrackInfo:
    name: str
    track_type: str
    clips: list[ClipInfo] = field(default_factory=list)

@dataclass 
class ALSInfo:
    tempo: Optional[float]
    time_signature_numerator: Optional[int]
    time_signature_denominator: Optional[int]
    tracks: list[TrackInfo] = field(default_factory=list)

def parse_als(file_bytes: bytes) -> ALSInfo:
    """
    Decompress and parse an Ableton .als file from raw bytes.
    Returns an ALSInfo dataclass with tempo, time signature, and track data.
    """
    try:
        xml_bytes = gzip.decompress(file_bytes)
    except OSError as e:
        raise ValueError(f"Failed to decompress .als file: {e}")

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse .als XML: {e}")
    
    tempo = _parse_tempo(root)
    numerator, denominator = _parse_time_signature(root)
    tracks = _parse_tracks(root)

    return ALSInfo(
        tempo=tempo,
        time_signature_numerator=numerator,
        time_signature_denominator=denominator,
        tracks=tracks
    )

def _parse_tempo(root: ET.Element) -> Optional[float]:
    """
    Parse the tempo from the ALS XML root element.
    """
    try:
        tempo_el = root.find('.//Tempo/Manual')
        if tempo_el is not None:
            return float(tempo_el.attrib.get('Value', 0))
    except (ValueError, KeyError):
        pass
    return None

def _parse_time_signature(root: ET.Element) -> tuple[Optional[int], Optional[int]]:
    """
    Parse the time signature from the ALS XML root element.
    """
    try:
        num_el = root.find('.//TimeSignature/TimeSignatures/RemoteableTimeSignature/Numerator')
        den_el = root.find('.//TimeSignature/TimeSignatures/RemoteableTimeSignature/Denominator')
        numerator = int(num_el.attrib.get('Value', 4)) if num_el is not None else None
        denominator = int(den_el.attrib.get('Value', 4)) if den_el is not None else None
        return numerator, denominator
    except (ValueError, KeyError):
        return None, None

def _parse_tracks(root: ET.Element) -> list[TrackInfo]:
    """
    Parse track information from the ALS XML root element.
    """
    tracks = []
    track_tags = [
        ('AudioTrack', 'audio'),
        ('MidiTrack', 'midi'),
        ('ReturnTrack', 'return'),
        ('MasterTrack', 'master'),
    ]

    for tag, track_type in track_tags:
        for track_el in root.iter(tag):
            name = _get_track_name(track_el)
            clips = _get_clips(track_el, track_type)
            tracks.append(TrackInfo(name=name, track_type=track_type, clips=clips))

    return tracks

def _get_track_name(track_el: ET.Element) -> str:
    """
    Extract the track name from a track XML element.
    """
    name_el = track_el.find('.//Name/EffectiveName')
    if name_el is not None:
        return name_el.attrib.get('Value', 'Unnamed')
    name_el = track_el.find('.//Name/UserName')
    if name_el is not None:
        val = name_el.attrib.get('Value', '')
        if val:
            return val
    return 'Unnamed'

def _get_clips(track_el: ET.Element, track_type: str) -> list[ClipInfo]:
    """
    Extract clip information from a track XML element.
    """
    clips = []
    clip_tag = 'AudioClip' if track_type == 'audio' else 'MidiClip'

    for clip_el in track_el.iter(clip_tag):
        name_el = clip_el.find('Name')
        name = name_el.attrib.get('Value', 'Unnamed') if name_el is not None else 'Unnamed'

        start_el = clip_el.find('CurrentStart')
        end_el = clip_el.find('CurrentEnd')

        try:
            start = float(start_el.attrib.get('Value', 0)) if start_el is not None else 0.0
            end = float(end_el.attrib.get('Value', 0)) if end_el is not None else 0.0
        except ValueError:
            start, end = 0.0, 0.0

        clips.append(ClipInfo(name=name, start_time=start, end_time=end))

    return clips