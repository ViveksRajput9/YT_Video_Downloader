
import threading
from Gui.ContentArea import ContentArea
class FilterManager:


    def __init__(self):
         pass
    
    def filter_videos(self, text: str,obj:ContentArea):
        """Filter videos based on search text and active filters."""
        text = text.lower()
        visible_widgets = []
        widgets = obj.get_widgets()
        for widget in widgets:
            title = widget.video_data.get('title', '').lower()
            channel = widget.video_data.get('uploader', '').lower()
            # Check text match
            matches_text = text in title or text in channel
            # Combine all conditions
            is_visible = matches_text
            widget.setVisible(is_visible)
            if is_visible:
                visible_widgets.append(widget)
        return visible_widgets
     
    def sort_videos(self, sort_by: str,obj:ContentArea):
        """Sort videos based on selected criteria"""

        widgets = obj.get_widgets()
        if sort_by == "Newest":
            widgets.sort(key=lambda w: w.video_data.get('upload_date', ''), reverse=True)
        elif sort_by == "Oldest":
            widgets.sort(key=lambda w: w.video_data.get('upload_date', ''))
        elif sort_by == "Title":
            widgets.sort(key=lambda w: w.video_data['title'].lower())
        elif sort_by == "Duration":
            widgets.sort(key=lambda w: int(w.video_data.get('duration', 0)))
        elif sort_by == "Duration (Descending)":
            widgets.sort(key=lambda w: int(w.video_data.get('duration', 0)), reverse=True)
        elif sort_by == "Title (Descending)":
            widgets.sort(key=lambda w: w.video_data['title'].lower(), reverse=True)
        elif sort_by == "Highest Quality":
            widgets.sort(key=lambda w: int(str(w.video_data['highest_quality']).rstrip('p')), reverse=True)
        elif sort_by == "Lowest Quality":
            widgets.sort(key=lambda w: int(str(w.video_data['highest_quality']).rstrip('p')))
        return widgets
