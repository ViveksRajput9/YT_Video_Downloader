class SizeFormatter:
    @staticmethod
    def format(size_bytes):
        if size_bytes >= 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
        return f"{int(size_bytes / (1024 * 1024))} MB"