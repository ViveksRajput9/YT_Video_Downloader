from .size_formatter import SizeFormatter

class QualityParser:
    @staticmethod
    def parse(formats):
        qualities = []
        best_audio_quality = None
        best_audio_size = 0
        audio_720_size = 0
        highest_quality = None

        for f in formats:
            if f.get('vcodec') == 'none' and isinstance(f.get('acodec'), str) and f.get('filesize', 0):
                if best_audio_quality is None or (f['abr'] > best_audio_quality and f['abr'] < 130):
                    best_audio_quality = f['abr']
                best_audio_size = f['filesize']
                if audio_720_size is None or f['abr'] <= 70:
                    audio_720_size = f['filesize']
                desc = f"Audio-{int(f.get('abr', 'unknown'))}-({SizeFormatter.format(best_audio_size)})-{f['ext']}"
                if desc not in qualities:
                    qualities.append(desc)

        for f in formats:
            if isinstance(f.get('height'), int) and f.get('filesize', 0):
                size = f['filesize'] + (audio_720_size if f['height'] <= 720 else best_audio_size)
                size_str = SizeFormatter.format(size)
                qualities.append(f"{f['format_id']}-{f.get('format_note', 'unknown')} ({size_str})-{f['ext']}")
                if highest_quality is None or f['height'] > highest_quality:
                    highest_quality = f['height']

        return qualities, best_audio_quality, best_audio_size, audio_720_size, highest_quality