import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'D:/KPDL/envs/env_name/Library/plugins/platforms'


class YouTubeStatsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
    # Read the CSV file into a DataFrame
        df = pd.read_csv('DataYoutubeTrending.csv')

    # Group by 'channelTitle' and calculate the sum of views, likes, and comments for each channel
        channel_stats = df.groupby('channelTitle').agg({
            'viewCount': 'sum',
            'likeCount': 'sum',
            'commentCount': 'sum'
        }).reset_index()

        # Select the top 10 channels based on viewCount
        top_10_channels = channel_stats.nlargest(10, 'viewCount')

        # Print the aggregated statistics
        print(top_10_channels)

        # Plot bar chart
        plt.figure(figsize=(10, 6))
    
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Use a bar plot with a stacked layout
        top_10_channels.plot(kind='bar', x='channelTitle', y=['viewCount', 'likeCount', 'commentCount'], stacked=True, ax=plt.gca())

        plt.title('Top 10 Channels by Views')
        plt.xlabel('Channel Title')
        plt.ylabel('Count')

        # Embed the Matplotlib plot into the PyQt5 application
        canvas = FigureCanvas(plt.gcf())
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.addWidget(canvas)

        self.setLayout(layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Top 10 YouTube Channels by Views')
        self.show()


    def show_view_chart(self):
        self.plot_chart('viewCount', 'View Count')

    def show_like_chart(self):
        self.plot_chart('likeCount', 'Like Count')

    def show_comment_chart(self):
        self.plot_chart('commentCount', 'Comment Count')

    def plot_chart(self, column, title):
        # Plot bar chart
        plt.clf()  # Clear existing plot
        plt.xticks(rotation=45, ha='right')
        self.df.groupby('channelTitle')[column].sum().plot(kind='bar', ax=plt.gca())
        plt.title(title)
        plt.xlabel('Channel Title')
        plt.ylabel('Count')
        self.canvas.draw()

    def style_button(self, button):
        button.setStyleSheet(
            "QPushButton {"
            "background-color: #4CAF50;"
            "border: none;"
            "color: white;"
            "padding: 8px 16px;"
            "text-align: center;"
            "text-decoration: none;"
            "display: inline-block;"
            "font-size: 12px;"
            "margin: 4px 2px;"
            "transition-duration: 0.4s;"
            "cursor: pointer;"
            "border-radius: 4px;"
            "}"
            "QPushButton:hover {background-color: white; color: black;}"
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeStatsApp()
    sys.exit(app.exec_())
