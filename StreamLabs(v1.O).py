from os import truncate
from tkinter.ttk import Style
import progressbar
import time
import pyfiglet
from rich.console import Console
from rich.table import Column, Table
from rich.markdown import Markdown
from os import walk 
import requests
import subprocess
import sys 
import webbrowser
from bs4 import BeautifulSoup as soup


def animated_marker():  
    widgets = ['Loading: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
      
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)


def wanna_dload(lnk):
    choice = input("Wanna download(y) or only stream(y/n):")
    print(lnk)
    if(choice == 'y'):
        run_file(lnk, True)
    else:
        run_file(lnk, False)


def tst_condition(se):
    l1 = se.find_all("a", {"class":"magnet-download download-torrent magnet"})
    if len(l1) == 0:
        print("Sorry! No results found :(")
    elif len(l1) == 1:
        lnk = l1[0].get("href")
        wanna_dload(lnk)
    elif len(l1) >= 2:
        quality = input("Enter the quality(720p/1080p):")
        if(quality == '720p'):
            lnk = l1[0].get("href")
            wanna_dload(lnk)
            
        elif(quality == '1080p'):
            lnk = l1[1].get("href")
            wanna_dload(lnk)


def search_(titles, rating, links, con):
    animated_marker()
    if(len(rating)==0):
        print("Sorry, this one is currently unavailable :(")
    else:
        li = []
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Sr.no.", style="dim", width=12)
        table.add_column("Title")
        table.add_column ("Torrent Link")
        table.add_column("Rating")
        for i in range(len(links)):
            table.add_row(
                str(i+1), str(links[i].figure.img["alt"]), str(titles[i]['href']), str(rating[i].text)
            )
            li.append(titles[i]['href'])
        con.print(table)
        n = int(input("Enter movie number : "))
        req = requests.get(li[n-1]) #i
        se=soup(req.text, 'html.parser')#lxml
        tst_condition(se)


def main():
    con = Console()
    title = """StreamLabs v1.O""" 
    con.print(pyfiglet.figlet_format(title), style="cyan")
    # _title_disp = Markdown(title)
    # con.print(_title_disp, style='bold red')
    nm = input('Enter Movie name:')
    res = requests.get('https://yts.proxyninja.org/browse-movies/'+''.join(nm))
    s = soup(res.text, 'lxml')
    titles = s.select('.browse-movie-title')
    rating = s.select('.rating')
    links = s.select('.browse-movie-link')
    search_(titles, rating, links, con)

def run_file(magnet_link: str, download: bool): #, download: bool
    # webbrowser.open('https://webtor.io/#/'+magnet_link) <-- For internet stream(include Ads)
    # download = False
    if sys.platform.startswith('linux'):
        cmd = []
        cmd.append("webtorrent")
        cmd.append(magnet_link)
        if not download:
            print('streamming...')
            cmd.append('--vlc')
        subprocess.call(cmd)

    elif sys.platform.startswith('win32'):
        cmd = ""
        cmd= cmd + "webtorrent"
        cmd=cmd+" download "
        cmd=cmd+'"{}"'.format(magnet_link)
        if not download:
            print('streamming...')
            cmd=cmd+' --vlc'
            subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    main()
