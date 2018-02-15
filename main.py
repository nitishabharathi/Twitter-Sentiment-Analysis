
from tkinter import *
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
matplotlib.use("TkAgg")

print("sentimental analysis of INDIA vs NEW ZEALAND ODI match")

def pie():
    tweets=pd.read_csv("maimdb.csv",encoding='iso-8859-1')
        
    sid = SentimentIntensityAnalyzer()
    
    tweets['sentiment_compound_polarity']=tweets.processedTweet.apply(lambda x:sid.polarity_scores(x)['compound'])
    tweets['sentiment_neutral']=tweets.processedTweet.apply(lambda x:sid.polarity_scores(x)['neu'])
    tweets['sentiment_negative']=tweets.processedTweet.apply(lambda x:sid.polarity_scores(x)['neg'])
    tweets['sentiment_pos']=tweets.processedTweet.apply(lambda x:sid.polarity_scores(x)['pos'])
    tweets['sentiment_type']=''
    tweets.loc[tweets.sentiment_compound_polarity>0,'sentiment_type']='POSITIVE'
    tweets.loc[tweets.sentiment_compound_polarity==0,'sentiment_type']='NEUTRAL'
    tweets.loc[tweets.sentiment_compound_polarity<0,'sentiment_type']='NEGATIVE'
    tweets.sentiment_type.value_counts().plot(kind='pie',title="sentiment analysis")
    tweets.to_csv('finalee.csv')

def graph():
    tweets=pd.read_csv("finalee.csv",encoding='iso-8859-1')

    arr=tweets['sentiment_compound_polarity'].tolist()
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    def animate(i):
        xar = []
        yar = []
    
        x = 0
        y = 0
    
        for i in range(len(tweets['text'])):
        
            x += 1
            if (arr[i]>0):
                y += 1
            elif (arr[i]<0):
                y-=1
        
            xar.append(x)
            yar.append(y)
            
        ax1.clear()
        ax1.plot(xar,yar)
        fig.text(0.5, 0.04,'tweets', ha='center')
        fig.text(0.04, 0.5, 'sentiment', va='center', rotation='vertical')

    class mclass:
        def __init__(self,widow):
            self.window=window
            self.button1=Button(window,text="Growth of sentiment",command=self.plot)
            self.button1.pack()
            
        def plot(self):
            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()
            canvas=FigureCanvasTkAgg(fig,master=self.window)
            canvas.get_tk_widget().pack()
            canvas.draw()
    
            
    window=Tk()
    start=mclass(window)
    window.mainloop()



root=Tk()


button1=Button(root,text="Sentiment graph",command=pie)
button2=Button(root,text="Growth of sentiments",command=graph)
button1.pack(side="left")
button2.pack(side="left")


root.mainloop()